#!/usr/bin/env python3
# ABOUTME: This script migrates old nata2.info content to page bundles with local resources
# ABOUTME: It finds nata2.info links/images, downloads them from archive.org, and creates page bundles

import os
import re
import shutil
from datetime import datetime
import argparse
from pathlib import Path
import frontmatter
from urllib.parse import urlparse, urljoin, quote
import logging
import time
import requests
from bs4 import BeautifulSoup
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def is_nata2_resource(url):
    """Check if a URL is a nata2.info resource"""
    if not url:
        return False
    
    parsed = urlparse(url)
    
    # Check only nata2.info domains
    nata2_domains = ['nata2.info', 'www.nata2.info']
    
    for domain in nata2_domains:
        if domain in parsed.netloc:
            return True
    
    return False

def extract_resources_from_content(content):
    """Extract all nata2.info resources from markdown/HTML content"""
    resources = []
    
    # Match markdown images: ![alt](url)
    markdown_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    # Match markdown links: [text](url)
    markdown_link_pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    
    # Match HTML images: <img src="url">
    html_image_pattern = r'<img\s+[^>]*src=["\'](.*?)["\'][^>]*>'
    
    # Match HTML links: <a href="url">
    html_link_pattern = r'<a\s+[^>]*href=["\'](.*?)["\'][^>]*>'
    
    # Match embedded objects/iframes
    embed_pattern = r'<(?:embed|iframe|object)\s+[^>]*(?:src|data)=["\'](.*?)["\'][^>]*>'
    
    # Find markdown images
    for match in re.finditer(markdown_image_pattern, content):
        alt_text = match.group(1)
        url = match.group(2)
        if is_nata2_resource(url):
            resources.append({
                'type': 'markdown_image',
                'alt': alt_text,
                'url': url,
                'full_match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    
    # Find markdown links
    for match in re.finditer(markdown_link_pattern, content):
        link_text = match.group(1)
        url = match.group(2)
        if is_nata2_resource(url):
            resources.append({
                'type': 'markdown_link',
                'text': link_text,
                'url': url,
                'full_match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    
    # Find HTML images
    for match in re.finditer(html_image_pattern, content, re.IGNORECASE):
        url = match.group(1)
        if is_nata2_resource(url):
            resources.append({
                'type': 'html_image',
                'url': url,
                'full_match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    
    # Find HTML links
    for match in re.finditer(html_link_pattern, content, re.IGNORECASE):
        url = match.group(1)
        if is_nata2_resource(url):
            resources.append({
                'type': 'html_link',
                'url': url,
                'full_match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    
    # Find embeds
    for match in re.finditer(embed_pattern, content, re.IGNORECASE):
        url = match.group(1)
        if is_nata2_resource(url):
            resources.append({
                'type': 'embed',
                'url': url,
                'full_match': match.group(0),
                'start': match.start(),
                'end': match.end()
            })
    
    return resources

def rewrite_nata2_url(url):
    """Rewrite nata2.info query-based URLs to direct file paths"""
    parsed = urlparse(url)
    
    # Only process nata2.info URLs with query parameters
    if not parsed.query or 'nata2.info' not in parsed.netloc:
        return url
    
    # Parse query parameters
    import urllib.parse
    query_params = urllib.parse.parse_qs(parsed.query)
    
    logger.debug(f"    Query params: {query_params}")
    
    # Check if it has the expected path and img parameters
    if 'path' in query_params and 'img' in query_params:
        path = query_params['path'][0]
        img = query_params['img'][0]
        
        # Decode the path (convert %2F to /)
        path = urllib.parse.unquote(path)
        
        # Construct the direct URL
        direct_url = f"{parsed.scheme}://{parsed.netloc}/{path}/{img}"
        logger.info(f"    Rewrote URL from: {url}")
        logger.info(f"                  to: {direct_url}")
        return direct_url
    
    # Return original URL if it doesn't match the pattern
    logger.debug(f"    No rewrite needed for: {url}")
    return url

def get_archive_url(original_url, post_date=None):
    """Get the best archive.org URL for a resource using the Wayback Machine API"""
    # First try to rewrite nata2.info URLs to direct paths
    original_url = rewrite_nata2_url(original_url.strip())
    
    try:
        # Use the Wayback Machine Availability API
        api_url = "http://archive.org/wayback/available"
        params = {"url": original_url}
        
        # If we have a post date, add timestamp parameter
        if post_date:
            # Format: YYYYMMDDhhmmss
            params["timestamp"] = post_date.strftime('%Y%m%d000000')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logger.debug(f"    Checking availability for: {original_url}")
        resp = requests.get(api_url, params=params, headers=headers, timeout=10)
        data = resp.json()
        
        if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            snapshot = data["archived_snapshots"]["closest"]
            if snapshot.get("available"):
                archive_url = snapshot["url"]
                timestamp = snapshot.get("timestamp", "unknown")
                logger.info(f"    Found snapshot from {timestamp}")
                
                # For images/media, we need to modify the URL to get raw content
                if any(ext in original_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4', '.mp3', '.3gp']):
                    # Extract timestamp and construct raw URL
                    if '/web/' in archive_url:
                        parts = archive_url.split('/web/', 1)
                        if len(parts) > 1:
                            ts_and_url = parts[1].split('/', 1)
                            if len(ts_and_url) > 1:
                                ts = ts_and_url[0]
                                # Use if_ modifier for raw access
                                archive_url = f"https://web.archive.org/web/{ts}if_/{original_url}"
                                logger.debug(f"    Modified to raw URL: {archive_url}")
                
                return archive_url
        
        # If no snapshot found, try the query-based URL format for nata2.info
        if 'nata2.info' in original_url and '/pictures/' in original_url:
            # Extract filename from direct URL and try query format
            parsed = urlparse(original_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) > 1 and path_parts[0] == 'pictures':
                # Construct query-based URL
                filename = path_parts[-1]
                folder_path = '/'.join(path_parts[:-1])
                query_url = f"http://www.nata2.info/?path={quote(folder_path)}&img={filename}"
                
                logger.info(f"    Trying query-based format: {query_url}")
                
                # Check availability for query URL
                params["url"] = query_url
                resp = requests.get(api_url, params=params, headers=headers, timeout=10)
                data = resp.json()
                
                if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
                    snapshot = data["archived_snapshots"]["closest"]
                    if snapshot.get("available"):
                        logger.info(f"    Found snapshot using query format from {snapshot.get('timestamp')}")
                        return snapshot["url"]
        
        logger.warning(f"    No archive found for: {original_url}")
        
    except Exception as e:
        logger.error(f"    Archive API error: {e}")
    
    # Return None if no archive found
    return None

def download_resource(archive_url, local_path):
    """Download a resource from archive.org"""
    try:
        # Create directory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # For archive.org URLs, ensure we have the if_ modifier
        if 'web.archive.org' in archive_url and 'if_' not in archive_url:
            # Extract the original URL from the archive URL
            # Format is usually: https://web.archive.org/web/TIMESTAMP/ORIGINAL_URL
            parts = archive_url.split('/web/', 1)
            if len(parts) > 1:
                timestamp_and_url = parts[1]
                # Split by first slash after timestamp
                parts = timestamp_and_url.split('/', 1)
                if len(parts) > 1:
                    timestamp = parts[0].replace('if_', '')
                    original_url = parts[1]
                    # Add if_ to get the raw archived file
                    # This bypasses the Wayback Machine toolbar/wrapper
                    raw_archive_url = f"https://web.archive.org/web/{timestamp}if_/{original_url}"
                    archive_url = raw_archive_url
        
        logger.debug(f"    Downloading from: {archive_url}")
        
        # Download the file
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(archive_url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check if we got an image/media file
        content_type = response.headers.get('content-type', '').lower()
        logger.debug(f"    Content-Type: {content_type}")
        
        # For nata2.info, we might get application/octet-stream for images
        valid_types = ['image/', 'video/', 'audio/', 'application/octet-stream']
        if not any(valid_type in content_type for valid_type in valid_types):
            # Check if it's HTML (might be a wayback machine page)
            if 'text/html' in content_type:
                logger.warning(f"    Got HTML instead of media file, might be a wayback wrapper")
                # Try to extract the actual image URL from the HTML
                html_content = response.text
                if 'pictures/misc/phone_camera' in archive_url:
                    # This looks like a phone camera image, let's try a different approach
                    logger.info(f"    Attempting alternative download method for phone camera image")
                return False
        
        # Save to local file
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify the file was saved and has content
        if local_path.exists() and local_path.stat().st_size > 0:
            # Additional check: make sure it's not HTML
            with open(local_path, 'rb') as f:
                first_bytes = f.read(100)
                if b'<!DOCTYPE' in first_bytes or b'<html' in first_bytes:
                    logger.error(f"    Downloaded file appears to be HTML, not media")
                    local_path.unlink()
                    return False
            
            logger.info(f"    Downloaded: {local_path.name} ({local_path.stat().st_size} bytes)")
            return True
        else:
            logger.error(f"    Downloaded file is empty or missing")
            if local_path.exists():
                local_path.unlink()
            return False
        
    except Exception as e:
        logger.error(f"    Failed to download {archive_url}: {e}")
        return False

def sanitize_filename(filename):
    """Sanitize a filename for local storage"""
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        # Use a hash for very long names
        name = name[:50] + '_' + hashlib.md5(name.encode()).hexdigest()[:8]
    
    return name + ext

def convert_to_page_bundle(post_path, resources, dry_run=False):
    """Convert a post to a page bundle and download resources"""
    # Determine the bundle directory
    post_dir = post_path.parent
    post_name = post_path.stem
    
    # For posts already in bundles, use the existing directory
    if post_path.name == 'index.md':
        bundle_dir = post_dir
    else:
        # Create bundle directory
        bundle_dir = post_dir / post_name
        if not dry_run:
            bundle_dir.mkdir(exist_ok=True)
    
    # Read the post
    with open(post_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    # Get post date for archive lookups
    post_date = post.get('date')
    if isinstance(post_date, str):
        try:
            post_date = datetime.fromisoformat(post_date.replace('+00:00', '').replace('Z', ''))
        except:
            post_date = None
    elif hasattr(post_date, 'date'):
        post_date = post_date.replace(tzinfo=None)
    elif not hasattr(post_date, 'year'):
        post_date = None
    
    content = post.content
    downloaded_resources = []
    
    # Sort resources by position in reverse order to avoid offset issues
    resources.sort(key=lambda x: x['start'], reverse=True)
    
    for resource in resources:
        logger.info(f"  Processing: {resource['url']}")
        
        # Get archive URL (will rewrite URL internally if needed)
        archive_url = get_archive_url(resource['url'], post_date)
        if not archive_url:
            logger.warning(f"    No archive found, skipping resource")
            continue
        logger.info(f"    Archive URL: {archive_url}")
        
        # Determine local filename
        parsed = urlparse(resource['url'])
        filename = None
        
        # For nata2.info URLs with query params like ?path=...&img=...
        if parsed.query and 'img=' in parsed.query:
            # Extract the image filename from the query
            import urllib.parse
            query_params = urllib.parse.parse_qs(parsed.query)
            if 'img' in query_params:
                filename = query_params['img'][0]
                # Clean up the filename (remove Nokia6600 prefix, etc)
                filename = os.path.basename(filename)
        
        if not filename:
            filename = os.path.basename(parsed.path)
            
        if not filename or filename == '/' or filename == '':
            # Generate a filename based on the URL
            filename = f"resource_{hashlib.md5(resource['url'].encode()).hexdigest()[:8]}"
            
            # Try to guess extension for images
            if resource['type'] in ['markdown_image', 'html_image'] or 'image' in resource['url'].lower():
                if '.jpg' in resource['url'].lower() or '.jpeg' in resource['url'].lower():
                    filename += '.jpg'
                elif '.png' in resource['url'].lower():
                    filename += '.png'
                elif '.gif' in resource['url'].lower():
                    filename += '.gif'
                elif '.3gp' in resource['url'].lower():
                    filename += '.3gp'
                else:
                    filename += '.jpg'  # Default to jpg
        
        filename = sanitize_filename(filename)
        local_path = bundle_dir / filename
        
        # Download the resource
        if not dry_run:
            if download_resource(archive_url, local_path):
                downloaded_resources.append({
                    'original_url': resource['url'],
                    'archive_url': archive_url,
                    'local_path': filename,
                    'resource': resource
                })
            else:
                # Fall back to archive.org link if download fails
                logger.warning(f"    Falling back to archive.org link")
                downloaded_resources.append({
                    'original_url': resource['url'],
                    'archive_url': archive_url,
                    'local_path': None,
                    'resource': resource
                })
        else:
            logger.info(f"    DRY RUN: Would download to {filename}")
            downloaded_resources.append({
                'original_url': resource['url'],
                'archive_url': archive_url,
                'local_path': filename,
                'resource': resource
            })
    
    # Update content with new paths
    for res in downloaded_resources:
        resource = res['resource']
        
        if res['local_path']:
            # Use local path
            new_url = res['local_path']
        else:
            # Use archive URL
            new_url = res['archive_url']
        
        # Replace in content based on type
        if resource['type'] == 'markdown_image':
            new_match = f"![{resource['alt']}]({new_url})"
        elif resource['type'] == 'markdown_link':
            # Check if this is actually an image link
            if any(ext in resource['url'].lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
                if res['local_path']:
                    # Convert to markdown image
                    new_match = f"![{resource['text']}]({new_url})"
                else:
                    new_match = f"[{resource['text']}]({new_url})"
            else:
                # Keep as link
                new_match = f"[{resource['text']}]({new_url})"
        elif resource['type'] == 'html_image':
            new_match = resource['full_match'].replace(resource['url'], new_url)
        elif resource['type'] == 'html_link':
            # Check if this is actually an image link
            if any(ext in resource['url'].lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
                if res['local_path']:
                    # Keep as link but update URL
                    new_match = resource['full_match'].replace(resource['url'], new_url)
                else:
                    new_match = resource['full_match'].replace(resource['url'], new_url)
            else:
                # Keep as link
                new_match = resource['full_match'].replace(resource['url'], new_url)
        else:
            new_match = resource['full_match'].replace(resource['url'], new_url)
        
        content = content[:resource['start']] + new_match + content[resource['end']:]
    
    # Update post content and mark as migrated
    post.content = content
    post['nata2_migrated'] = True
    post['nata2_migration_date'] = datetime.now().isoformat()
    
    # Write the updated post
    if not dry_run:
        new_post_path = bundle_dir / 'index.md'
        with open(new_post_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        # If we moved the post to a bundle, delete the original
        if post_path != new_post_path and post_path.exists():
            post_path.unlink()
            logger.info(f"  Moved post to page bundle: {bundle_dir}")
    
    return len(downloaded_resources)

def process_post(post_path, auto_confirm=False, dry_run=False):
    """Process a single post"""
    logger.info(f"\nChecking: {post_path}")
    
    # Read the post
    with open(post_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    # Skip if already migrated
    if post.get('nata2_migrated'):
        logger.info("  Already migrated, skipping")
        return False
    
    # Extract nata2.info resources
    resources = extract_resources_from_content(post.content)
    
    if not resources:
        logger.info("  No nata2.info resources found")
        return False
    
    logger.info(f"  Found {len(resources)} nata2.info resources:")
    for res in resources:
        logger.info(f"    - {res['type']}: {res['url']}")
    
    # Ask for confirmation
    if not auto_confirm:
        response = input("\nMigrate this post? [y/N]: ").strip().lower()
        if response != 'y':
            logger.info("  Skipped")
            return False
    
    # Convert to page bundle and download resources
    logger.info("\nMigrating post...")
    num_migrated = convert_to_page_bundle(post_path, resources, dry_run)
    
    if not dry_run:
        logger.info(f"\n✓ Migration complete! Processed {num_migrated} resources.")
    else:
        logger.info(f"\n✓ DRY RUN complete! Would process {num_migrated} resources.")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Migrate nata2.info content to page bundles with local resources'
    )
    parser.add_argument(
        '--content-dir',
        default='content',
        help='Path to the content directory (default: content)'
    )
    parser.add_argument(
        '--post-types',
        nargs='+',
        default=['post'],
        help='Types of content to process (default: post)'
    )
    parser.add_argument(
        '--auto-confirm',
        '-y',
        action='store_true',
        help='Automatically confirm all migrations without prompting'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit the number of posts to process'
    )
    
    args = parser.parse_args()
    
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / args.content_dir
    
    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        return
    
    logger.info(f"Scanning content in: {content_dir}")
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be modified")
    
    processed_count = 0
    migrated_count = 0
    
    # Process each content type
    for post_type in args.post_types:
        type_dir = content_dir / post_type
        if not type_dir.exists():
            logger.warning(f"Content type directory not found: {type_dir}")
            continue
        
        # Find all markdown files
        for md_file in type_dir.rglob('*.md'):
            # Skip _index.md files
            if md_file.name == '_index.md':
                continue
            
            if args.limit and processed_count >= args.limit:
                break
            
            processed_count += 1
            if process_post(md_file, args.auto_confirm, args.dry_run):
                migrated_count += 1
                
                # Ask if user wants to continue
                if not args.auto_confirm:
                    response = input("\nContinue searching? [Y/n]: ").strip().lower()
                    if response == 'n':
                        break
    
    logger.info(f"\n\nSummary:")
    logger.info(f"  Total posts checked: {processed_count}")
    logger.info(f"  Posts migrated: {migrated_count}")

if __name__ == '__main__':
    main()
