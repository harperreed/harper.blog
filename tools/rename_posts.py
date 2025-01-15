import os
import re
import hashlib
import frontmatter
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)

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
            content = frontmatter.dumps(post)
            
        # Get the date from frontmatter
        date = post.get('date')
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
