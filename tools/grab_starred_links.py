import os
import feedparser
from datetime import datetime
import slugify
import frontmatter
import hashlib
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime

# Load environment variables
load_dotenv()

# Configuration
RSS_URL = os.getenv('LINKS_RSS_URL')
HUGO_CONTENT_DIR = os.getenv('LINKS_HUGO_CONTENT_DIR')

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
        
        slug = generate_unique_slug(title, date, url)
        file_path = os.path.join(HUGO_CONTENT_DIR, f"{slug}.md")
        
        if os.path.exists(file_path):
            print(f"Skipping existing entry: {title}")
            return False
        
        # Create a new Post object with the title as the content
        post = frontmatter.Post(title)
        
        # Add metadata to the front matter
        post.metadata['title'] = title
        post.metadata['date'] = date
        post.metadata['draft'] = False
        post.metadata['original_url'] = url
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        print(f"Created post: {file_path}")
        return True
    except Exception as e:
        print(f"Error creating post for '{title}': {e}")
        return False

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
