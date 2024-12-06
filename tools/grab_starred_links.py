import os
import feedparser
from datetime import datetime
import slugify
import frontmatter
import hashlib
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime
from firecrawl import FirecrawlApp
from openai import OpenAI, RateLimitError, APIError
from pydantic import BaseModel
from typing import Optional, List
import logging
from readabilipy import simple_json_from_html_string
from diskcache import Cache

# Load environment variables
load_dotenv()

# Configuration
CACHE_DIRECTORY = "./script_cache"
CACHE_TIMEOUT = 86400  # 24 hours
RSS_URL = os.getenv('LINKS_RSS_URL')
HUGO_CONTENT_DIR = os.getenv('LINKS_HUGO_CONTENT_DIR')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

class Tags(BaseModel):
    tags: List[str]
    summary: Optional[str]

firecrawler = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Initialize disk cache
cache = Cache(CACHE_DIRECTORY)

try:
    client = OpenAI()
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    raise

def fetch_rss_feed(url):
    try:
        return feedparser.parse(url)
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return None

def generate_unique_slug(title, date_str, url):
    base_slug = slugify.slugify(title)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    
    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        try:
            date = parsedate_to_datetime(date_str)
        except Exception:
            date = datetime.now()
    
    date_str = date.strftime("%Y%m%d")
    return f"{date_str}-{base_slug}-{url_hash}"

def create_hugo_post(entry):
    try:

        title = entry.title
        date = entry.get('published', entry.get('updated', datetime.now().isoformat()))
        url = entry.link
        if not title or not date or not url:
            print(f"Skipping invalid entry: {title}, {url}")
            return False
        
        slug = generate_unique_slug(title, date, url)
        file_path = os.path.join(HUGO_CONTENT_DIR, f"{slug}.md")
        
        if os.path.exists(file_path):
            print(f"Skipping existing entry: {title}")
            return False
        else:
            print(f"Creating post for: {title}, {url}")

        scraped_content = scrape_url(url)
     
        if scraped_content:
            tags = get_tags_summary(title, scraped_content)
        else:
            tags = Tags(tags=[], summary=None)
    
        
        # Create a new Post object with the title as the content
        post = frontmatter.Post(title)
        
        # Add metadata to the front matter
        post.metadata['title'] = title
        post.metadata['date'] = date
        if tags: 
            if tags.tags:
                post.metadata['tags'] = tags.tags
            if tags.summary:
                post.metadata['summary'] = tags.summary
        post.metadata['draft'] = False
        post.metadata['original_url'] = url
        
        with open(file_path, 'w', encoding='utf-8') as f:
           f.write(frontmatter.dumps(post))
        
        print(f"Created post: {file_path}")
        return True
 
    except Exception as e:
        print(f"Error creating post for '{title}': {e}")
        return False

def get_tags_summary(title, content):
    logging.debug(f"Getting tags for title: {title[:100]}...")

    if not title or not content:
        logging.warning("Empty title or content provided")
        return Tags(tags=[], summary=None)

    # Truncate content to avoid token limits while preserving meaning
    max_content_len = 1000


    prompt = f"""
    Analyze this webpage and suggest up to 3 relevant tags.

    Title: {title}
    Content: {content[:max_content_len]}

    Requirements:
    - Use lowercase tags only
    - Use hyphens for multi-word tags (e.g., 'machine-learning')
    - Avoid similar tags ('ai-assistant', 'ai-tools' should be 'ai')
    - Consider existing tags for continuity
    - only related to the direct content of the url
    - also return a calm, but quirky summary

    Respond with a JSON object in this format:
    {{"tags": ["tag1", "tag2", "tag3"]}}
    """

    try:
        

        # Create cache key from prompt
        cache_key = hashlib.md5(prompt.encode()).hexdigest()

        # Try to get cached response
        result = cache.get(cache_key)
        if result is None:
            logging.debug("Cache miss - sending request to OpenAI API") 
            response = client.beta.chat.completions.parse(
                model=OPENAI_MODEL,  # Fixed model name
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                response_format=Tags
            )
            # Cache the response
            logging.debug(f"Raw API response: {response}")
            result = response.choices[0].message.parsed
            cache.set(cache_key, result, expire=CACHE_TIMEOUT) # Cache for 24 hours
        else:
            logging.debug("Using cached OpenAI response")

        

        # Parse response and validate
        

        

        logging.info(f"Generated tags: {result.tags}")
        return result

    except RateLimitError as e:
        logging.error(f"OpenAI rate limit exceeded: {e}")
        return Tags(tags=[])
    except APIError as e:
        logging.error(f"OpenAI API error: {e}")
        return Tags(tags=[])
    except Exception as e:
        logging.error(f"Unexpected error in tag generation: {e}")
        return Tags(tags=[])

def scrape_url(url):
    logging.info(f"Attempting to scrape URL: {url}")
    try:
        # Initialize disk cache for URL scraping

        # Create cache key from URL
        cache_key = hashlib.md5(url.encode()).hexdigest()

        # Try to get cached response
        scrape = cache.get(cache_key)
        if scrape is None:
            scrape = firecrawler.scrape_url(url, params={'formats': ['html']})
            # Cache the response for 24 hours
            cache.set(cache_key, scrape, expire=CACHE_TIMEOUT)
        
        if not scrape:
            logging.warning(f"Empty scrape result for {url}")
            return ""

        logging.debug(f"Successfully scraped {url} - Content length: {len(str(scrape))}")        
        article = simple_json_from_html_string(scrape['html'], use_readability=True)
        raw = ""
        for p in article['plain_text']:
            raw = raw + p['text'] + "\n"
        
        return raw

    except Exception as e:
        logging.error(f"Failed to scrape {url}: {str(e)}")
        # Return empty string rather than None for safer handling
        return ""

def main():
    if not RSS_URL or not HUGO_CONTENT_DIR:
        print("Error: RSS_URL or HUGO_CONTENT_DIR not set in .env file")
        return

    feed = fetch_rss_feed(RSS_URL)
    if not feed:
        print("Failed to fetch RSS feed. Exiting.")
        return

    new_entries_count = 0
    for entry in feed.entries:
        
        if create_hugo_post(entry):
            new_entries_count += 1
    
    print(f"Processed {new_entries_count} new entries")

if __name__ == "__main__":
    main()
