import os
import re
import hashlib
import frontmatter
import logging
import requests
from datetime import datetime
from pathlib import Path
from functools import lru_cache

ARCHIVAL_FEED_URL = "https://raw.githubusercontent.com/harperreed/harper.micro.blog/refs/heads/main/feed.json"

logging.basicConfig(level=logging.INFO)

@lru_cache(maxsize=1)
def get_archival_feed():
    """Fetch and cache the archival feed."""
    try:
        response = requests.get(ARCHIVAL_FEED_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch archival feed: {e}")
        return None

def find_post_id(content, url=None):
    """Find the original post ID from the archival feed."""
    feed = get_archival_feed()
    if not feed:
        return None
    
    for item in feed.get('items', []):
        if (url and item.get('url') == url) or item.get('content_text') == content:
            post_id = item.get('id', '').split('/')[-1]
            if post_id.isdigit():
                return int(post_id)
    return None

def generate_hash(content):
    """Generate a 12-character SHA-1 hash of the content."""
    sha1 = hashlib.sha1()
    sha1.update(content.encode('utf-8'))
    return sha1.hexdigest()[:12]

def process_post(post_path):
    """Process a single post and return its new filename."""
    try:
        # Read the post
        with open(post_path / "index.md", 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            content = post.content
            
        # Get the date and URL from frontmatter
        date = post.get('date')
        url = post.get('original_url')
        
        # Try to find the original post ID
        post_id = find_post_id(content, url)
        if post_id:
            post['title'] = f"Note #{post_id}"
            # Write back the updated frontmatter
            with open(post_path / "index.md", 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
        if not date:
            logging.warning(f"No date found in {post_path}")
            return None
            
        # Generate hash from content and date
        hash_input = f"{content}{date}"
        content_hash = generate_hash(hash_input)
        
        # Create new filename
        new_name = f"{date.strftime('%Y-%m-%d-%H-%M')}_{content_hash}"
        
        return new_name
        
    except Exception as e:
        logging.error(f"Error processing {post_path}: {e}")
        return None

def main():
    notes_dir = Path("content/notes")
    
    # Process all post directories
    for post_path in notes_dir.iterdir():
        if not post_path.is_dir() or not (post_path / "index.md").exists():
            continue
            
        new_name = process_post(post_path)
        if not new_name:
            continue
            
        # Create new path
        new_path = notes_dir / new_name
        
        # Rename if new path doesn't exist
        if not new_path.exists():
            try:
                post_path.rename(new_path)
                logging.info(f"Renamed: {post_path.name} -> {new_name}")
            except Exception as e:
                logging.error(f"Error renaming {post_path}: {e}")
        else:
            logging.warning(f"Destination already exists: {new_path}")

if __name__ == "__main__":
    main()
