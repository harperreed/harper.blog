import requests
import os
import re
import hashlib
from datetime import datetime
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

def download_json_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to download JSON feed: {e}")
        raise

def html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.wrap_links = False
    h.body_width = 0  # Disable line wrapping
    return h.handle(html_content)

def download_image(url, output_path):
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


def create_hugo_content(entry, output_dir):
    sub_title = entry.get('title', "Untitled")
    content = entry.get('content_text') or entry.get('content_html', '')
    date_str = entry.get('date_published', datetime.now().isoformat())
    post_url = entry.get('url', '')

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()

    # Generate hash from content and date to ensure uniqueness
    hash_input = f"{content}{date_str}{post_url}"
    content_hash = generate_hash(hash_input)
    
    base_filename = f"{date.strftime('%Y-%m-%d-%H-%M')}_{content_hash}"
    post_dir = os.path.join(output_dir, base_filename)
    
    if os.path.exists(post_dir):
        logging.info(f"Post already exists: {post_dir}")
        return False

    os.makedirs(post_dir)

    content = html_to_markdown(content)
    content = process_images(content, post_dir)

    file_path = os.path.join(post_dir, "index.md")

    post = frontmatter.loads(content)
    post['title'] = f"Note #{content_hash[:6]}"  # Use first 6 chars of hash as ID
    post['sub_title'] = sub_title
    post['description'] = create_description(content)
    post['date'] = date
    post['draft'] = False
    post['original_url'] = post_url

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        logging.info(f"Created new post: {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error creating post: {e}")
        return False

def generate_hash(content):
    """Generate a 12-character SHA-1 hash of the content."""
    sha1 = hashlib.sha1()
    sha1.update(content.encode('utf-8'))
    return sha1.hexdigest()[:12]

def create_description(content, max_length=160):
    # Strip markdown syntax
    clean_content = re.sub(r'[#*`_~\[\]\(\)!]', '', content)
    # Normalize whitespace
    clean_content = ' '.join(clean_content.split())
    # Truncate and add ellipsis if needed
    if len(clean_content) > max_length:
        return clean_content[:max_length-3] + '...'
    return clean_content

def main():
    json_feed_url = os.getenv('NOTES_JSON_FEED_URL')
    hugo_content_dir = os.getenv('NOTES_HUGO_CONTENT_DIR')

    if not json_feed_url or not hugo_content_dir:
        logging.error("NOTES_JSON_FEED_URL and NOTES_HUGO_CONTENT_DIR must be set in the .env file")
        return

    os.makedirs(hugo_content_dir, exist_ok=True)

    try:
        feed_data = download_json_feed(json_feed_url)
    except Exception as e:
        logging.error(f"Failed to download JSON feed: {e}")
        return

    sorted_entries = sorted(
        feed_data.get('items', []),
        key=lambda x: datetime.fromisoformat(x.get('date_published', datetime.now().isoformat())),
        reverse=False
    )

    new_posts_created = 0
    for entry in sorted_entries:
        if create_hugo_content(entry, hugo_content_dir):
            new_posts_created += 1

    logging.info(f"Processed {len(sorted_entries)} entries.")
    logging.info(f"Created {new_posts_created} new posts.")

if __name__ == "__main__":
    main()
