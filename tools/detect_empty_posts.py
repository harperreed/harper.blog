#!/usr/bin/env python
import os
import re
import json
import argparse
import logging
from pathlib import Path
import frontmatter

# ABOUTME: This script detects posts with valid frontmatter but empty or nearly empty body content.
# ABOUTME: It scans content directories to find posts that may need content added.
#
# Basic usage:
#   uv run --with python-frontmatter tools/detect_empty_posts.py --verbose
# 
# Advanced usage with CLI options:
#   uv run --with python-frontmatter tools/detect_empty_posts.py --directory content/links --min-chars 20 --min-words 10 --summary
#
# Find only posts where content is exactly the title:
#   uv run --with python-frontmatter tools/detect_empty_posts.py --title-only
#
# Find only completely empty posts (no content at all):
#   uv run --with python-frontmatter tools/detect_empty_posts.py --only-completely-empty
#
# Don't flag posts where content matches title as empty:
#   uv run --with python-frontmatter tools/detect_empty_posts.py --no-check-title
#
# Available options:
#   --content-dirs, -d    Directories to scan (default: content and all language variants)
#   --directory           Single directory to scan (shortcut for --content-dirs)
#   --extensions, -e      File extensions to check (default: .md)
#   --output, -o          Output JSON file path (default: data/empty_posts.json)
#   --verbose, -v         Enable verbose logging
#   --min-chars, -m       Minimum number of characters to consider content non-empty (default: 10)
#   --min-words, -w       Minimum number of words to consider content non-empty (default: 5)
#   --summary, -s         Show only summary count, not individual files
#   --json-only, -j       Output only JSON file, no console output
#   --limit, -l           Limit output to specified number of results
#   --no-check-title      Do not consider posts empty if content matches title
#   --no-check-length     Do not consider posts empty based on content length
#   --only-completely-empty  Only detect posts with absolutely no content
#   --title-only          Only detect posts where content is exactly the title

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def is_content_empty(content, title=None):
    """
    Check if post content is empty or nearly empty.
    
    Args:
        content (str): The content of the post
        title (str, optional): The title of the post, to check if content is just the title
        
    Returns:
        bool: True if content is considered empty, False otherwise
    """
    # Remove whitespace
    stripped = content.strip()
    
    # If completely empty
    if not stripped:
        return True
    
    # If content is exactly the same as the title, consider it empty
    # but only if check_title_match is enabled
    if check_title_match and title and stripped == title.strip():
        return True
    
    # For link posts that just have the title and nothing else
    # but only if check_title_match is enabled
    if check_title_match and title and stripped.startswith(title.strip()) and len(stripped) <= len(title.strip()) + 10:
        return True
    
    # If title is null but there's content, don't consider it empty
    # regardless of length - it has some content
    if not check_min_length:
        return False
        
    # If very short (fewer characters than min_chars)
    if len(re.sub(r'\s+', '', stripped)) < min_chars:
        # But if there's multiple lines, it's probably intentional content
        if len(stripped.split('\n')) > 1:
            return False
        return True
        
    # If very few words (fewer words than min_words)
    if len(stripped.split()) < min_words:
        # But if there's multiple lines, it's probably intentional content
        if len(stripped.split('\n')) > 1:
            return False
        return True
        
    return False

def scan_directory(directory, extensions=['.md']):
    """
    Scan a directory for empty posts.
    
    Args:
        directory (str): Path to the content directory to scan
        extensions (list): File extensions to consider
        
    Returns:
        list: Information about empty posts found
    """
    empty_posts = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        logging.warning(f"Directory does not exist: {directory}")
        return empty_posts
        
    for file_path in dir_path.glob('**/*'):
        # Skip directories and non-matching extensions
        if file_path.is_dir() or not any(file_path.name.endswith(ext) for ext in extensions):
            continue
            
        try:
            # Load the frontmatter and content
            post = frontmatter.load(file_path)
            
            # Get the title for comparison
            title = post.get('title', 'Untitled')
            
            # Check if content is empty
            if is_content_empty(post.content, title):
                empty_posts.append({
                    'path': str(file_path),
                    'title': title,
                    'date': str(post.get('date', 'Unknown')),
                    'content_length': len(post.content.strip()),
                    'status': 'empty' if not post.content.strip() else 'nearly_empty',
                    'is_title_only': post.content.strip() == title.strip()
                })
                
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            
    return empty_posts

def get_output_path(output_file=None):
    """
    Get the path for the output JSON file.
    
    Args:
        output_file (str, optional): User-specified output file path
        
    Returns:
        str: Path to save the output file
    """
    if output_file:
        return output_file
        
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    return str(data_dir / 'empty_posts.json')

def main():
    """Main function to find empty posts."""
    parser = argparse.ArgumentParser(description='Find posts with empty content')
    parser.add_argument('--content-dirs', '-d', nargs='+', 
                        default=['content', 'content.ja', 'content.es', 'content.ko'],
                        help='Directories to scan (default: content and all language variants)')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.md'],
                        help='File extensions to check (default: .md)')
    parser.add_argument('--output', '-o', type=str, 
                        help='Output JSON file path (default: data/empty_posts.json)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Enable verbose logging')
    parser.add_argument('--min-chars', '-m', type=int, default=10,
                        help='Minimum number of characters to consider content non-empty (default: 10)')
    parser.add_argument('--min-words', '-w', type=int, default=5,
                        help='Minimum number of words to consider content non-empty (default: 5)')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Show only summary count, not individual files')
    parser.add_argument('--json-only', '-j', action='store_true',
                        help='Output only JSON file, no console output')
    parser.add_argument('--limit', '-l', type=int, 
                        help='Limit output to specified number of results')
    parser.add_argument('--directory', type=str,
                        help='Single directory to scan (shortcut for --content-dirs with one value)')
    parser.add_argument('--no-check-title', action='store_true',
                        help='Do not consider posts empty if content matches title')
    parser.add_argument('--no-check-length', action='store_true',
                        help='Do not consider posts empty based on content length')
    parser.add_argument('--only-completely-empty', action='store_true',
                        help='Only detect posts with absolutely no content')
    parser.add_argument('--title-only', action='store_true',
                        help='Only detect posts where content is exactly the title')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check for single directory shortcut
    if args.directory:
        content_dirs = [args.directory]
    else:
        content_dirs = args.content_dirs
    
    # Update global variables for content detection
    global min_chars, min_words, check_title_match, check_min_length
    min_chars = args.min_chars
    min_words = args.min_words
    check_title_match = not args.no_check_title
    check_min_length = not args.no_check_length
    
    # If only-completely-empty is specified, ignore other checks
    if args.only_completely_empty:
        check_title_match = False
        check_min_length = False
    
    # Log scan start if not json-only mode
    if not args.json_only:
        logging.info(f"Scanning directories: {', '.join(content_dirs)}")
    
    # Collect results from all directories
    all_empty_posts = []
    for directory in content_dirs:
        if not args.json_only:
            logging.info(f"Scanning directory: {directory}")
        empty_posts = scan_directory(directory, args.extensions)
        all_empty_posts.extend(empty_posts)
        if not args.json_only:
            logging.info(f"Found {len(empty_posts)} empty posts in {directory}")
    
    # Filter by title-only if specified
    if args.title_only:
        all_empty_posts = [post for post in all_empty_posts if post.get('is_title_only', False)]
    
    # Filter by only-completely-empty if specified
    if args.only_completely_empty:
        all_empty_posts = [post for post in all_empty_posts if post['status'] == 'empty']
    
    # Sort results by path for consistent output
    all_empty_posts.sort(key=lambda x: x['path'])
    
    # Apply limit if specified
    if args.limit and len(all_empty_posts) > args.limit:
        all_empty_posts = all_empty_posts[:args.limit]
    
    # Display results
    if all_empty_posts and not args.json_only:
        if args.summary:
            logging.info(f"Found {len(all_empty_posts)} total empty posts.")
        else:
            logging.info(f"Found {len(all_empty_posts)} total empty posts:")
            for post in all_empty_posts:
                status = "[EMPTY]" if post['status'] == 'empty' else "[NEARLY EMPTY]"
                logging.info(f"{status} {post['path']} - {post['title']}")
    elif not args.json_only:
        logging.info("No empty posts found!")
    
    # Save results to JSON file
    output_path = get_output_path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'count': len(all_empty_posts),
            'empty_posts': all_empty_posts
        }, f, indent=2)
    
    if not args.json_only:
        logging.info(f"Results saved to {output_path}")
    
    return len(all_empty_posts)

# Global variables for content emptiness detection
min_chars = 10
min_words = 5
check_title_match = True
check_min_length = True

if __name__ == "__main__":
    main()