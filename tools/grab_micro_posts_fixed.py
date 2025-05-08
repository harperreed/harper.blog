import requests
import os
import re
import hashlib
import json
from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache
import html2text
import frontmatter
from slugify import slugify
from urllib.parse import urlparse
from dotenv import load_dotenv
import logging

# Load environment variables from .env file if it exists
load_dotenv()

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# URL registry file will be stored in the data directory
URL_REGISTRY_FILENAME = "processed_urls.json"


def normalize_url(url):
    """
    Normalize URLs to prevent duplicates from minor variations.
    
    Args:
        url (str): The URL to normalize
        
    Returns:
        str: Normalized URL
    """
    if not url:
        return ""
        
    parsed = urlparse(url)
    # Remove trailing slashes, normalize to lowercase
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/').lower()
    # Add parameters if present, sorted to ensure consistent order
    if parsed.query:
        params = sorted(parsed.query.split('&'))
        normalized += f"?{'&'.join(params)}"
    return normalized


def strip_html(html_string):
    """
    Convert HTML to plain text.
    
    Args:
        html_string (str): HTML content
        
    Returns:
        str: Plain text without HTML tags
    """
    return BeautifulSoup(html_string, "html.parser").get_text()


def download_json_feed(url):
    """
    Download and parse JSON feed from URL.
    
    Args:
        url (str): Feed URL
        
    Returns:
        dict: Parsed JSON feed
        
    Raises:
        requests.RequestException: If download fails
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to download JSON feed: {e}")
        raise


def html_to_markdown(html_content):
    """
    Convert HTML to Markdown.
    
    Args:
        html_content (str): HTML content
        
    Returns:
        str: Markdown content
    """
    h = html2text.HTML2Text()
    h.wrap_links = False
    h.body_width = 0  # Disable line wrapping
    return h.handle(html_content)


def download_image(url, output_path):
    """
    Download an image from URL to local file.
    
    Args:
        url (str): Image URL
        output_path (str): Local path to save image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to download image from {url}: {e}")
        return False


def process_images(content, post_dir):
    """
    Process images in markdown content.
    
    Args:
        content (str): Markdown content
        post_dir (str): Directory to save images
        
    Returns:
        str: Updated content with local image references
    """
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    img_matches = img_pattern.findall(content)

    for i, (alt_text, img_url) in enumerate(img_matches):
        parsed_url = urlparse(img_url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        if not file_extension:
            file_extension = '.jpg'  # Default to .jpg if no extension is found
        local_img_path = f'image_{i + 1}{file_extension}'
        full_img_path = os.path.join(post_dir, local_img_path)
        if download_image(img_url, full_img_path):
            # Remove the image from the content
            content = content.replace(f'![{alt_text}]({img_url})', '')

    # Remove any empty lines left after removing images
    content = re.sub(r'\n\s*\n', '\n\n', content)
    return content.strip()


def generate_hash(content):
    """
    Generate a 12-character SHA-1 hash of the content.
    
    Args:
        content (str): Content to hash
        
    Returns:
        str: 12-character hash
    """
    sha1 = hashlib.sha1()
    sha1.update(content.encode('utf-8'))
    return sha1.hexdigest()[:12]


def load_url_registry(data_dir):
    """
    Load the URL registry from data directory.
    
    Args:
        data_dir (str): Data directory path
        
    Returns:
        dict: Dictionary with processed URLs and their timestamps
    """
    registry_path = os.path.join(data_dir, URL_REGISTRY_FILENAME)
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading URL registry: {e}")
            return {}
    return {}


def save_url_registry(registry, data_dir):
    """
    Save URL registry to data directory.
    
    Args:
        registry (dict): URL registry
        data_dir (str): Data directory path
    """
    registry_path = os.path.join(data_dir, URL_REGISTRY_FILENAME)
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2)
    except IOError as e:
        logging.error(f"Error saving URL registry: {e}")


def is_duplicate_content(content, hugo_content_dir):
    """
    Check if identical content already exists.
    
    Args:
        content (str): Content to check
        hugo_content_dir (str): Directory to check against
        
    Returns:
        bool: True if duplicate content found, False otherwise
    """
    content_hash = generate_hash(content[:500])  # Use first 500 chars for efficiency
    for root, dirs, files in os.walk(hugo_content_dir):
        for file in files:
            if file == "index.md":
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        if generate_hash(post.content[:500]) == content_hash:
                            return True
                except Exception as e:
                    logging.warning(f"Error checking duplicate content in {os.path.join(root, file)}: {e}")
                    continue
    return False


ARCHIVAL_FEED_URL = "https://raw.githubusercontent.com/harperreed/harper.micro.blog/refs/heads/main/feed.json"


@lru_cache(maxsize=1)
def get_archival_feed():
    """
    Fetch and cache the archival feed.
    
    Returns:
        dict: Parsed JSON feed or None if fetch fails
    """
    try:
        response = requests.get(ARCHIVAL_FEED_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch archival feed: {e}")
        return None


def find_post_info(url, content):
    """
    Find the original post ID and title from the archival feed.
    
    Args:
        url (str): Post URL
        content (str): Post content
        
    Returns:
        tuple: (post_id, title) or (None, None) if not found
    """
    feed = get_archival_feed()
    if not feed:
        return None, None
    
    normalized_url = normalize_url(url)
    
    for item in feed.get('items', []):
        item_url = normalize_url(item.get('url', ''))
        if item_url == normalized_url or item.get('content_text') == content:
            # Extract ID from the id field which might be in format "post/123456"
            post_id = item.get('id', '').split('/')[-1]
            if post_id.isdigit():
                logging.debug(f"Found match in archive - URL: {url}")
                logging.debug(f"Archive title: {item.get('title')}")
                logging.debug(f"Archive content: {item.get('content_text')[:100]}...")
                return int(post_id), item.get('title')
    return None, None


def get_highest_note_id(hugo_content_dir):
    """
    Find the highest note ID from existing posts.
    
    Args:
        hugo_content_dir (str): Content directory
        
    Returns:
        int: Highest note ID
    """
    highest_note_id = 0
    for root, dirs, files in os.walk(hugo_content_dir):
        for file in files:
            if file == "index.md":
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        title = post.get('title', '')
                        if title.startswith('Note #'):
                            try:
                                current_id = int(title.split('#')[1])
                                highest_note_id = max(highest_note_id, current_id)
                            except (IndexError, ValueError):
                                continue
                except Exception as e:
                    logging.error(f"Error reading file {os.path.join(root, file)}: {str(e)}")
    
    return highest_note_id


def create_description(content, max_length=160):
    """
    Create a short description from content.
    
    Args:
        content (str): Source content
        max_length (int): Maximum description length
        
    Returns:
        str: Truncated description
    """
    # Strip markdown syntax
    clean_content = re.sub(r'[#*`_~\[\]\(\)!]', '', content)
    # Normalize whitespace
    clean_content = ' '.join(clean_content.split())
    # Truncate and add ellipsis if needed
    if len(clean_content) > max_length:
        return clean_content[:max_length-3] + '...'
    return clean_content


def create_hugo_content(entry, output_dir, url_registry, data_dir):
    """
    Create a Hugo content post from a feed entry.
    
    Args:
        entry (dict): Feed entry
        output_dir (str): Output directory
        url_registry (dict): Registry of processed URLs
        data_dir (str): Data directory path
        
    Returns:
        bool: True if post was created, False otherwise
    """
    sub_title = entry.get('title', "Untitled")
    content = entry.get('content_text') or entry.get('content_html', '')
    date_str = entry.get('date_published', datetime.now().isoformat())
    post_url = entry.get('url', '')
    
    if not post_url:
        logging.warning("Entry has no URL, skipping")
        return False
    
    # Normalize URL
    normalized_url = normalize_url(post_url)
    
    # Check URL registry
    if normalized_url in url_registry:
        logging.info(f"URL already processed, skipping: {post_url}")
        return False
    
    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()
        logging.warning(f"Failed to parse date '{date_str}', using current date")

    # Generate a more robust hash that includes URL, date, and content preview
    hash_input = f"{normalized_url}|{date.isoformat()}|{content[:100]}"
    content_hash = generate_hash(hash_input)
    
    content_text = strip_html(content)
    slug = slugify(content_text[:50])  # Limit slug length
    
    base_filename = f"{date.strftime('%Y-%m-%d')}_{content_hash}_{slug[:30]}"
    post_dir = os.path.join(output_dir, base_filename)
    
    # Check if directory already exists
    if os.path.exists(post_dir):
        logging.info(f"Post directory already exists: {post_dir}")
        # Add to registry if not already there
        if normalized_url not in url_registry:
            url_registry[normalized_url] = datetime.now().isoformat()
            save_url_registry(url_registry, data_dir)
        return False
    
    # Check for duplicate content
    if is_duplicate_content(content, output_dir):
        logging.info(f"Duplicate content detected for {post_url}, skipping")
        # Add to registry to avoid processing again
        url_registry[normalized_url] = datetime.now().isoformat()
        save_url_registry(url_registry, data_dir)
        return False

    # Create the directory
    try:
        os.makedirs(post_dir)
    except OSError as e:
        logging.error(f"Failed to create directory {post_dir}: {e}")
        return False

    # Process content
    if '<' in content and '>' in content:  # Simple check for HTML
        content = html_to_markdown(content)
    content = process_images(content, post_dir)

    file_path = os.path.join(post_dir, "index.md")

    # Parse or create frontmatter
    if frontmatter.checks(content):
        post = frontmatter.loads(content)
    else:
        post = frontmatter.Post(content)
    
    # Find post info from archive
    post_id, archive_title = find_post_info(post_url, content)
    if post_id is None:
        post_id = get_highest_note_id(os.path.dirname(post_dir)) + 1
        post['title'] = f"Note #{post_id}"
    else:
        post['title'] = archive_title if archive_title else f"Note #{post_id}"
    
    # Add metadata
    post['sub_title'] = sub_title
    post['description'] = create_description(content)
    post['date'] = date
    post['draft'] = False
    post['original_url'] = post_url
    post['translationKey'] = f"note-{post_id}"  # Use a consistent format for translation keys

    # Write the post
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        logging.info(f"Created new post: {file_path} with Note ID: {post_id}")
        
        # Add to registry after successful creation
        url_registry[normalized_url] = datetime.now().isoformat()
        save_url_registry(url_registry, data_dir)
        
        return True
    except Exception as e:
        logging.error(f"Error creating post: {e}")
        # Clean up directory if post creation fails
        try:
            import shutil
            shutil.rmtree(post_dir)
            logging.info(f"Cleaned up directory after failed post creation: {post_dir}")
        except Exception as cleanup_error:
            logging.error(f"Failed to clean up directory: {cleanup_error}")
        return False


def main():
    """Main function to process microblog entries."""
    json_feed_url = os.getenv('NOTES_JSON_FEED_URL')
    hugo_content_dir = os.getenv('NOTES_HUGO_CONTENT_DIR')
    hugo_data_dir = os.getenv('NOTES_HUGO_DATA_DIR', os.path.join(os.path.dirname(hugo_content_dir), 'data', 'notes'))

    if not json_feed_url or not hugo_content_dir:
        logging.error("NOTES_JSON_FEED_URL and NOTES_HUGO_CONTENT_DIR must be set in the .env file")
        return

    # Create directories if they don't exist
    os.makedirs(hugo_content_dir, exist_ok=True)
    os.makedirs(hugo_data_dir, exist_ok=True)

    # Load URL registry
    url_registry = load_url_registry(hugo_data_dir)
    logging.info(f"Loaded {len(url_registry)} entries from URL registry")

    try:
        # Download feed
        feed_data = download_json_feed(json_feed_url)
        if not feed_data or not feed_data.get('items'):
            logging.error("Feed contains no items or invalid format")
            return
            
        # Deduplicate feed entries by URL
        unique_entries = {}
        for entry in feed_data.get('items', []):
            url = entry.get('url')
            if url:
                normalized_url = normalize_url(url)
                # Keep the latest version of each entry
                if normalized_url not in unique_entries:
                    unique_entries[normalized_url] = entry
                
        # Sort entries chronologically
        sorted_entries = sorted(
            unique_entries.values(),
            key=lambda x: datetime.fromisoformat(x.get('date_published', datetime.now().isoformat())),
            reverse=False  # Oldest first
        )

        logging.info(f"Found {len(feed_data.get('items', []))} entries, {len(sorted_entries)} unique")

        # Process entries
        new_posts_created = 0
        for entry in sorted_entries:
            if create_hugo_content(entry, hugo_content_dir, url_registry, hugo_data_dir):
                new_posts_created += 1

        logging.info(f"Processed {len(sorted_entries)} entries.")
        logging.info(f"Created {new_posts_created} new posts.")
        logging.info(f"URL registry now contains {len(url_registry)} entries.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        import traceback
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()