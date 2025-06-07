#!/usr/bin/env python3
# ABOUTME: This script audits blog posts that are 10+ years old and replaces external links with archive.org links
# ABOUTME: It helps preserve content accessibility by preventing link rot in older posts

import os
import re
from datetime import datetime, timedelta
import argparse
from pathlib import Path
import frontmatter
from urllib.parse import urlparse
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def is_external_link(url):
    """Check if a URL is an external link that needs archiving"""
    if not url:
        return False
    
    # Parse the URL
    parsed = urlparse(url)
    
    # If no scheme or netloc, it's likely a relative link
    if not parsed.scheme or not parsed.netloc:
        return False
    
    # Check if it's already an archive.org link
    if 'archive.org' in parsed.netloc or 'web.archive.org' in parsed.netloc:
        return False
    
    # Check if it's an archive.is or archive.today link
    if any(domain in parsed.netloc for domain in ['archive.is', 'archive.today', 'archive.ph', 'archive.vn']):
        return False
    
    # List of local/internal domains (customize as needed)
    internal_domains = ['localhost', '127.0.0.1', 'harper.blog', 'nata2.org', 'nata3.org']
    
    # Check if the domain is internal
    for domain in internal_domains:
        if domain in parsed.netloc:
            return False
    
    return True

def extract_links_from_content(content):
    """Extract all links from markdown content"""
    # Match markdown links: [text](url)
    markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # Match HTML links: <a href="url">
    html_link_pattern = r'<a\s+(?:[^>]*?\s+)?href=["\'](.*?)["\']'
    
    links = []
    
    # Find markdown links
    for match in re.finditer(markdown_link_pattern, content):
        link_text = match.group(1)
        link_url = match.group(2)
        links.append({
            'type': 'markdown',
            'text': link_text,
            'url': link_url,
            'full_match': match.group(0),
            'start': match.start(),
            'end': match.end()
        })
    
    # Find HTML links
    for match in re.finditer(html_link_pattern, content, re.IGNORECASE):
        link_url = match.group(1)
        links.append({
            'type': 'html',
            'url': link_url,
            'full_match': match.group(0),
            'start': match.start(),
            'end': match.end()
        })
    
    return links

def create_archive_url(original_url, post_date=None):
    """Create an archive.org URL for the given URL"""
    # Clean up the URL
    original_url = original_url.strip()
    
    # If we have a post date, try to find an archive close to that date
    if post_date:
        # Format: YYYYMMDDhhmmss
        timestamp = post_date.strftime('%Y%m%d000000')
        archive_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
    else:
        # Use a generic archive URL that will redirect to the closest capture
        archive_url = f"https://web.archive.org/web/*/{original_url}"
    
    return archive_url

def process_post(file_path, dry_run=False, summary_only=False):
    """Process a single post file"""
    stats = {
        'has_links': False,
        'external_links': 0,
        'archived_links': 0,
        'updated': False,
        'old_enough': False
    }
    
    try:
        # Read the post
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Get the post date
        post_date = post.get('date')
        if not post_date:
            if not summary_only:
                logger.warning(f"No date found in {file_path}")
            return stats
        
        # Check if the post is 10+ years old
        if isinstance(post_date, str):
            # Try to parse the date string
            try:
                # Remove timezone info for consistent comparison
                post_date = datetime.fromisoformat(post_date.replace('+00:00', '').replace('Z', ''))
            except:
                if not summary_only:
                    logger.warning(f"Could not parse date in {file_path}: {post_date}")
                return stats
        elif hasattr(post_date, 'date'):
            # If it's a datetime object, ensure we're working with a naive datetime
            post_date = post_date.replace(tzinfo=None)
        elif hasattr(post_date, 'year'):
            # If it's a date object, convert to datetime
            post_date = datetime(post_date.year, post_date.month, post_date.day)
        
        ten_years_ago = datetime.now() - timedelta(days=365 * 10)
        
        if post_date > ten_years_ago:
            if not summary_only:
                logger.debug(f"Post {file_path} is not old enough (date: {post_date})")
            return stats
        
        stats['old_enough'] = True
        
        if not summary_only:
            logger.info(f"Processing post from {post_date.strftime('%Y-%m-%d')}: {file_path}")
        
        # Extract links from content
        content = post.content
        links = extract_links_from_content(content)
        
        # Filter for external links
        external_links = []
        archived_count = 0
        for link in links:
            parsed = urlparse(link['url'])
            if parsed.scheme and parsed.netloc:
                if 'archive.org' in parsed.netloc or 'web.archive.org' in parsed.netloc:
                    archived_count += 1
                elif any(domain in parsed.netloc for domain in ['archive.is', 'archive.today', 'archive.ph', 'archive.vn']):
                    archived_count += 1
                elif is_external_link(link['url']):
                    external_links.append(link)
        
        stats['archived_links'] = archived_count
        stats['external_links'] = len(external_links)
        stats['has_links'] = archived_count > 0 or len(external_links) > 0
        
        if not summary_only:
            if archived_count > 0:
                logger.info(f"  Found {archived_count} already archived links (skipping them)")
            
            if not external_links:
                if archived_count > 0:
                    logger.info(f"  No new external links to archive")
                else:
                    logger.info(f"  No external links found")
                return stats
            
            logger.info(f"  Found {len(external_links)} external links to archive")
        
        if not external_links:
            return stats
        
        # Replace links with archive.org versions
        if not dry_run and not summary_only:
            # Sort links by position in reverse order to avoid offset issues
            external_links.sort(key=lambda x: x['start'], reverse=True)
            
            for link in external_links:
                archive_url = create_archive_url(link['url'], post_date)
                logger.info(f"  Replacing: {link['url']}")
                logger.info(f"       with: {archive_url}")
                
                if link['type'] == 'markdown':
                    # Replace markdown link
                    new_link = f"[{link['text']}]({archive_url})"
                    content = content[:link['start']] + new_link + content[link['end']:]
                elif link['type'] == 'html':
                    # Replace just the URL in the HTML
                    new_match = link['full_match'].replace(link['url'], archive_url)
                    content = content[:link['start']] + new_match + content[link['end']:]
            
            # Update the post content
            post.content = content
            
            # Write the updated post back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            logger.info(f"  Updated {len(external_links)} links")
            stats['updated'] = True
        else:
            if not summary_only and external_links:
                logger.info(f"  DRY RUN: Would update {len(external_links)} links:")
                for link in external_links:
                    archive_url = create_archive_url(link['url'], post_date)
                    logger.info(f"    {link['url']} -> {archive_url}")
            if external_links:
                stats['updated'] = True
        
        return stats
        
    except Exception as e:
        if not summary_only:
            logger.error(f"Error processing {file_path}: {e}")
        return stats

def main():
    parser = argparse.ArgumentParser(
        description='Replace external links in old blog posts with archive.org links'
    )
    parser.add_argument(
        '--content-dir',
        default='content',
        help='Path to the content directory (default: content)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making actual changes'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--post-types',
        nargs='+',
        default=['post', 'notes'],
        help='Types of content to process (default: post notes)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show only summary statistics without processing details'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / args.content_dir
    
    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        return
    
    if not args.summary:
        logger.info(f"Scanning content in: {content_dir}")
        if args.dry_run:
            logger.info("DRY RUN MODE - No files will be modified")
    
    processed_count = 0
    old_posts_count = 0
    updated_count = 0
    posts_with_links = 0
    posts_with_archived_links = 0
    total_external_links = 0
    total_archived_links = 0
    
    # Process each content type
    for post_type in args.post_types:
        type_dir = content_dir / post_type
        if not type_dir.exists():
            logger.warning(f"Content type directory not found: {type_dir}")
            continue
        
        if not args.summary:
            logger.info(f"\nProcessing {post_type} content...")
        
        # Find all markdown files
        for md_file in type_dir.rglob('*.md'):
            # Skip _index.md files
            if md_file.name == '_index.md':
                continue
            
            processed_count += 1
            stats = process_post(md_file, args.dry_run, args.summary)
            
            if stats['old_enough']:
                old_posts_count += 1
            if stats['has_links']:
                posts_with_links += 1
            if stats['archived_links'] > 0:
                posts_with_archived_links += 1
            if stats['updated']:
                updated_count += 1
            total_external_links += stats['external_links']
            total_archived_links += stats['archived_links']
            
            # Be nice to archive.org - add a small delay between posts
            if not args.dry_run and not args.summary and stats['updated']:
                time.sleep(0.5)
    
    logger.info(f"\nSummary:")
    logger.info(f"  Total posts processed: {processed_count}")
    logger.info(f"  Posts 10+ years old: {old_posts_count}")
    logger.info(f"  Old posts with any links: {posts_with_links}")
    logger.info(f"  Old posts already with archive links: {posts_with_archived_links}")
    logger.info(f"  Old posts needing updates: {updated_count}")
    logger.info(f"  Total external links to archive: {total_external_links}")
    logger.info(f"  Total links already archived: {total_archived_links}")
    
    if args.dry_run and updated_count > 0:
        logger.info(f"\nRun without --dry-run to update {updated_count} posts")

if __name__ == '__main__':
    main()
