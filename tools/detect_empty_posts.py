#!/usr/bin/env python
import os
import argparse
import logging
import json
from pathlib import Path
import frontmatter
import re

# ABOUTME: This script detects posts with valid frontmatter but empty or nearly empty body content.
# ABOUTME: It can scan multiple content directories for multilingual support.

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def is_empty_content(content):
    """
    Check if content is empty or nearly empty (just whitespace or minimal characters).
    
    Args:
        content (str): Content to check
        
    Returns:
        bool: True if content is considered empty, False otherwise
    """
    # Remove whitespace
    stripped = content.strip()
    
    # If completely empty
    if not stripped:
        return True
    
    # If very short (less than 10 non-whitespace characters)
    if len(re.sub(r'\s+', '', stripped)) < 10:
        return True
        
    return False

def find_empty_posts(content_dirs, extensions=['.md']):
    """
    Find all posts with valid frontmatter but empty body content.
    
    Args:
        content_dirs (list): List of directories to search
        extensions (list): File extensions to consider
        
    Returns:
        list: Information about empty posts found
    """
    empty_posts = []
    
    for content_dir in content_dirs:
        content_path = Path(content_dir)
        if not content_path.exists():
            logging.warning(f"Directory not found: {content_dir}")
            continue
            
        logging.info(f"Scanning directory: {content_dir}")
        
        # Walk through all files in the directory
        for root, _, files in os.walk(content_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check file extension
                if not any(file.endswith(ext) for ext in extensions):
                    continue
                
                try:
                    # Parse frontmatter and content
                    post = frontmatter.load(file_path)
                    
                    # Check if content is empty
                    if is_empty_content(post.content):
                        # Extract key information
                        empty_posts.append({
                            'path': file_path,
                            'title': post.get('title', 'Untitled'),
                            'date': str(post.get('date', 'Unknown')),
                            'content': post.content.strip(),
                            'status': 'empty' if not post.content.strip() else 'nearly_empty'
                        })
                        
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")
    
    return empty_posts

def get_log_path(base_dir):
    """Get path for the empty posts log file."""
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'empty_posts_log.json')

def main():
    """Main function to find empty posts."""
    parser = argparse.ArgumentParser(description='Find posts with empty content')
    parser.add_argument('--content-dirs', '-d', nargs='+', default=['content'], 
                        help='Directories to scan (default: content)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file path')
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    content_dirs = args.content_dirs
    logging.info(f"Scanning directories: {', '.join(content_dirs)}")
    
    # Find empty posts
    empty_posts = find_empty_posts(content_dirs)
    
    # Display results
    if empty_posts:
        for post in empty_posts:
            status = "[EMPTY]" if post['status'] == 'empty' else "[NEARLY EMPTY]"
            logging.info(f"{status} {post['path']} - {post['title']} ({post['date']})")
        
        logging.info(f"Found {len(empty_posts)} empty or nearly empty posts")
    else:
        logging.info("No empty posts found!")
    
    # Save log to file
    output_path = args.output if args.output else get_log_path(os.getcwd())
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'count': len(empty_posts),
            'empty_posts': empty_posts
        }, f, indent=2)
    
    logging.info(f"Results saved to {output_path}")
    return len(empty_posts)

if __name__ == "__main__":
    main()