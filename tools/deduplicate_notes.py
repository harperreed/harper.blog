#!/usr/bin/env python
import os
import re
import json
import logging
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import frontmatter

# ABOUTME: This script finds and removes duplicate notes, keeping the most recent version.
# ABOUTME: It detects duplicates based on content similarity and handles Note ID preservation.

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def generate_content_hash(content):
    """
    Generate a SHA-1 hash of content for comparison.
    
    Args:
        content (str): Content to hash
        
    Returns:
        str: SHA-1 hash
    """
    sha1 = hashlib.sha1()
    sha1.update(content.encode('utf-8'))
    return sha1.hexdigest()

def clean_content_for_comparison(content):
    """
    Clean and normalize content for consistent comparison.
    
    Args:
        content (str): Content to clean
        
    Returns:
        str: Cleaned content
    """
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', content.strip())
    # Remove any URLs or common variations that might differ but point to the same resource
    normalized = re.sub(r'https?://\S+', '', normalized)
    return normalized

def get_note_id_from_title(title):
    """
    Extract note ID from title.
    
    Args:
        title (str): Title string like "Note #123"
        
    Returns:
        int or None: Extracted note ID or None if not found
    """
    if not title:
        return None
        
    match = re.search(r'Note\s*#(\d+)', title)
    if match:
        return int(match.group(1))
    return None

def find_and_analyze_notes(notes_dir):
    """
    Find all notes and analyze for duplicates.
    
    Args:
        notes_dir (str): Directory containing notes
        
    Returns:
        tuple: (duplicate_sets, all_notes)
            - duplicate_sets is a dict mapping content hash to list of duplicate note paths
            - all_notes is a dict mapping file path to metadata
    """
    notes_path = Path(notes_dir)
    all_notes = {}
    content_hash_map = {}
    
    # Track by note ID to preserve IDs
    note_id_map = {}
    
    for post_dir in notes_path.glob("**/"):
        index_file = post_dir / "index.md"
        if not index_file.is_file():
            continue
            
        try:
            post = frontmatter.load(index_file)
            
            # Extract key information
            creation_date = None
            date_str = post.get('date')
            if date_str:
                try:
                    if isinstance(date_str, str):
                        creation_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        creation_date = date_str
                except (ValueError, TypeError):
                    logging.warning(f"Could not parse date {date_str} in {index_file}")
            
            # Get file stats as fallback date
            if not creation_date:
                file_stat = index_file.stat()
                creation_date = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Clean content for comparison
            clean_content = clean_content_for_comparison(post.content)
            content_hash = generate_content_hash(clean_content)
            
            # Extract note ID
            note_id = get_note_id_from_title(post.get('title'))
            
            # Store metadata
            metadata = {
                'path': str(index_file),
                'dir_path': str(post_dir),
                'content': post.content,
                'clean_content': clean_content,
                'content_hash': content_hash,
                'date': creation_date,
                'note_id': note_id,
                'frontmatter': dict(post.metadata)
            }
            
            all_notes[str(index_file)] = metadata
            
            # Map content hash to file paths
            if content_hash not in content_hash_map:
                content_hash_map[content_hash] = []
            content_hash_map[content_hash].append(str(index_file))
            
            # Map note ID to file paths if available
            if note_id:
                if note_id not in note_id_map:
                    note_id_map[note_id] = []
                note_id_map[note_id].append(str(index_file))
                
        except Exception as e:
            logging.error(f"Error processing {index_file}: {e}")
    
    # Find duplicates
    duplicate_sets = {h: paths for h, paths in content_hash_map.items() if len(paths) > 1}
    duplicate_ids = {id: paths for id, paths in note_id_map.items() if len(paths) > 1}
    
    logging.info(f"Found {len(all_notes)} total notes")
    logging.info(f"Found {len(duplicate_sets)} sets of content duplicates")
    logging.info(f"Found {len(duplicate_ids)} sets of note ID duplicates")
    
    return duplicate_sets, all_notes

def get_log_path(notes_dir):
    """Get path for the deduplication log file."""
    base_dir = os.path.dirname(notes_dir)
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'deduplication_log.json')

def delete_duplicates(duplicate_sets, all_notes, dry_run=True):
    """
    Delete duplicate notes, keeping the most recent version of each.
    
    Args:
        duplicate_sets (dict): Maps content hash to list of duplicate note paths
        all_notes (dict): Maps file path to metadata
        dry_run (bool): If True, only log actions without performing them
        
    Returns:
        list: Information about deleted duplicates
    """
    action_log = []
    
    for content_hash, duplicate_paths in duplicate_sets.items():
        if len(duplicate_paths) <= 1:
            continue
            
        # Sort duplicates by date, newest first
        sorted_duplicates = sorted(
            duplicate_paths,
            key=lambda path: all_notes[path]['date'],
            reverse=True
        )
        
        # Keep the newest one
        keeper = sorted_duplicates[0]
        keeper_metadata = all_notes[keeper]
        
        for duplicate in sorted_duplicates[1:]:
            duplicate_metadata = all_notes[duplicate]
            duplicate_dir = Path(duplicate_metadata['dir_path'])
            
            # Log the action
            action = {
                'action': 'delete',
                'content_hash': content_hash,
                'keeper': {
                    'path': keeper,
                    'date': keeper_metadata['date'].isoformat(),
                    'note_id': keeper_metadata['note_id']
                },
                'duplicate': {
                    'path': duplicate,
                    'date': duplicate_metadata['date'].isoformat(),
                    'note_id': duplicate_metadata['note_id']
                }
            }
            action_log.append(action)
            
            # Perform the deletion if not a dry run
            if not dry_run:
                try:
                    if duplicate_dir.exists():
                        shutil.rmtree(duplicate_dir)
                        logging.info(f"Deleted duplicate: {duplicate_dir}")
                except Exception as e:
                    logging.error(f"Failed to delete {duplicate_dir}: {e}")
            else:
                logging.info(f"[DRY RUN] Would delete: {duplicate_dir}")
    
    return action_log

def main():
    """Main function to find and remove duplicate notes."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Find and remove duplicate notes')
    parser.add_argument('--notes-dir', '-d', type=str, required=True, help='Directory containing notes')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Dry run (do not delete any files)')
    args = parser.parse_args()
    
    notes_dir = args.notes_dir
    dry_run = args.dry_run
    
    if dry_run:
        logging.info("Running in DRY RUN mode. No files will be modified.")
    
    # Find and analyze duplicates
    duplicate_sets, all_notes = find_and_analyze_notes(notes_dir)
    
    if not duplicate_sets:
        logging.info("No duplicates found!")
        return
    
    # Delete duplicates and log actions
    action_log = delete_duplicates(duplicate_sets, all_notes, dry_run)
    
    # Save log
    log_path = get_log_path(notes_dir)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'dry_run': dry_run,
            'total_notes': len(all_notes),
            'duplicate_sets': len(duplicate_sets),
            'actions': action_log
        }, f, indent=2)
    
    logging.info(f"Deduplication complete. Log saved to {log_path}")
    if not dry_run:
        logging.info(f"Deleted {len(action_log)} duplicate notes.")
    else:
        logging.info(f"Would have deleted {len(action_log)} duplicate notes.")

if __name__ == "__main__":
    main()
