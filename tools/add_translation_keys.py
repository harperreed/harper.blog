#!/usr/bin/env python

"""
ABOUTME: A tool to add translationKey to the frontmatter of Hugo content files.
ABOUTME: This helps with multilingual content by linking translations across languages.
"""

import os
import sys
import argparse
import uuid
import logging
from pathlib import Path
import frontmatter
from slugify import slugify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set up a color formatter for terminal output
try:
    import colorama
    colorama.init()
    
    # Define colors
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    RED = colorama.Fore.RED
    RESET = colorama.Style.RESET_ALL
except ImportError:
    # If colorama is not available, use empty strings
    GREEN = YELLOW = RED = RESET = ""

def generate_translation_key(post, use_title=True, use_uuid=False):
    """
    Generate a translationKey for a post.
    
    Args:
        post: The frontmatter post object
        use_title: Whether to use the title as the base for the key
        use_uuid: Whether to generate a UUID instead of using the title
        
    Returns:
        The generated translationKey
    """
    # If the post already has a translationKey, return it
    if 'translationKey' in post:
        return post['translationKey']
        
    # If use_uuid is True, generate a UUID
    if use_uuid:
        return str(uuid.uuid4())
        
    # If use_title is True, use the title or date-based key
    if use_title and 'title' in post:
        title = post['title']
        # If title exists, use it for the key
        return title
    
    # Fallback: use date + slug if available
    if 'date' in post:
        date_obj = post['date']
        date_str = date_obj.strftime('%Y-%m-%d') if hasattr(date_obj, 'strftime') else str(date_obj)
        
        if 'slug' in post:
            return f"{date_str}-{post['slug']}"
        elif post.content:
            # Create a slug from the first 30 chars of content
            content_slug = slugify(post.content[:100])[:30]
            return f"{date_str}-{content_slug}"
    
    # Last resort: UUID
    return str(uuid.uuid4())

def process_file(file_path, use_title=True, use_uuid=False, dry_run=False):
    """
    Process a single Markdown file to add or update translationKey.
    
    Args:
        file_path: Path to the Markdown file
        use_title: Whether to use the title as the translationKey
        use_uuid: Whether to generate a UUID instead
        dry_run: If True, don't write changes back to file
        
    Returns:
        A tuple of (success, message)
    """
    try:
        # Read the post
        post = frontmatter.load(file_path)
        
        # Get the old key if it exists
        old_key = post.get('translationKey', None)
        
        # Generate the new key
        new_key = generate_translation_key(post, use_title, use_uuid)
        
        # Update the post with the new key
        post['translationKey'] = new_key
        
        if not dry_run:
            # Write the updated post back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
        # Build response message
        if old_key is None:
            return True, f"{GREEN}Added translationKey: {new_key}{RESET}"
        elif old_key == new_key:
            return True, f"{YELLOW}Key unchanged: {new_key}{RESET}"
        else:
            return True, f"{GREEN}Updated key: {YELLOW}{old_key}{RESET} -> {GREEN}{new_key}{RESET}"
            
    except Exception as e:
        return False, f"Error processing {file_path}: {e}"

def process_directory(directory, recursive=False, use_title=True, use_uuid=False, dry_run=False):
    """
    Process all Markdown files in a directory.
    
    Args:
        directory: Path to the directory
        recursive: Whether to process subdirectories
        use_title: Whether to use the title as the translationKey
        use_uuid: Whether to generate a UUID instead
        dry_run: If True, don't write changes back to files
    """
    directory = Path(directory)
    
    # Ensure the directory exists
    if not directory.exists() or not directory.is_dir():
        logging.error(f"Directory not found: {directory}")
        return
    
    # Get all markdown files
    pattern = '**/*.md' if recursive else '*.md'
    files = list(directory.glob(pattern))
    
    if not files:
        logging.warning(f"No Markdown files found in {directory}")
        return
        
    logging.info(f"Found {len(files)} Markdown files in {directory}")
    
    # Process each file
    success_count = 0
    added_count = 0
    unchanged_count = 0
    updated_count = 0
    
    for file_path in files:
        success, message = process_file(file_path, use_title, use_uuid, dry_run)
        if success:
            if dry_run:
                message = f"[DRY RUN] {message}"
            logging.info(f"{file_path.relative_to(directory)}: {message}")
            success_count += 1
            
            # Count the different types of updates
            if "Added translationKey" in message:
                added_count += 1
            elif "Key unchanged" in message:
                unchanged_count += 1
            elif "Updated key" in message:
                updated_count += 1
        else:
            logging.error(f"{file_path.relative_to(directory)}: {message}")
    
    # Print summary
    if dry_run:
        logging.info(f"[DRY RUN] Would have updated {success_count} of {len(files)} files")
        if success_count > 0:
            logging.info(f"[DRY RUN] {GREEN}Added: {added_count}{RESET}, {YELLOW}Unchanged: {unchanged_count}{RESET}, {GREEN}Updated: {updated_count}{RESET}")
    else:
        logging.info(f"Updated {success_count} of {len(files)} files")
        if success_count > 0:
            logging.info(f"{GREEN}Added: {added_count}{RESET}, {YELLOW}Unchanged: {unchanged_count}{RESET}, {GREEN}Updated: {updated_count}{RESET}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Add translationKey to Hugo content frontmatter'
    )
    
    parser.add_argument(
        'directory',
        help='Directory containing Hugo content files'
    )
    
    parser.add_argument(
        '-nr', '--no-recursive',
        action='store_true',
        help='Do not process directories recursively (recursive is the default)'
    )
    
    parser.add_argument(
        '-u', '--uuid',
        action='store_true',
        help='Use UUID for translationKey instead of title'
    )
    
    parser.add_argument(
        '-n', '--no-title',
        action='store_true',
        help='Don\'t use title for translationKey (use date-slug or UUID)'
    )
    
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Process the directory (recursive by default)
    process_directory(
        directory=args.directory,
        recursive=not args.no_recursive,  # Recursive by default
        use_title=not args.no_title,
        use_uuid=args.uuid,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()