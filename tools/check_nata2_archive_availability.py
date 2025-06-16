#!/usr/bin/env python3
# ABOUTME: This script extracts all nata2.info URLs from blog posts and checks their availability on archive.org
# ABOUTME: It outputs URLs to a text file and creates a report showing which URLs are archived

import os
import re
from pathlib import Path
import frontmatter
from urllib.parse import urlparse, quote
import requests
import time
import json
from datetime import datetime
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def is_nata2_url(url):
    """Check if a URL is from nata2.info"""
    if not url:
        return False
    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in ['nata2.info', 'www.nata2.info'])

def extract_urls_from_content(content):
    """Extract all nata2.info URLs from markdown/HTML content"""
    urls = set()
    
    # Patterns to match different URL formats
    patterns = [
        # Markdown images: ![alt](url)
        r'!\[([^\]]*)\]\(([^)]+)\)',
        # Markdown links: [text](url)
        r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',
        # HTML images: <img src="url">
        r'<img\s+[^>]*src=["\'](.*?)["\'][^>]*>',
        # HTML links: <a href="url">
        r'<a\s+[^>]*href=["\'](.*?)["\'][^>]*>',
        # Embedded objects/iframes
        r'<(?:embed|iframe|object)\s+[^>]*(?:src|data)=["\'](.*?)["\'][^>]*>',
        # Plain URLs
        r'(https?://[^\s<>"{}|\\^`\[\]]+)'
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            if len(match.groups()) >= 2:
                # For patterns with groups (markdown)
                url = match.group(2)
            else:
                # For single group patterns
                url = match.group(1)
            
            if is_nata2_url(url):
                urls.add(url.strip())
    
    return urls

def rewrite_nata2_url(url):
    """Rewrite nata2.info query-based URLs to direct file paths"""
    parsed = urlparse(url)
    
    if not parsed.query or 'nata2.info' not in parsed.netloc:
        return url
    
    import urllib.parse
    query_params = urllib.parse.parse_qs(parsed.query)
    
    if 'path' in query_params and 'img' in query_params:
        path = urllib.parse.unquote(query_params['path'][0])
        img = query_params['img'][0]
        return f"{parsed.scheme}://{parsed.netloc}/{path}/{img}"
    
    return url

def check_archive_availability(url):
    """Check if a URL is available on archive.org"""
    # First try to rewrite the URL
    original_url = url
    rewritten_url = rewrite_nata2_url(url)
    
    results = {
        'original_url': original_url,
        'rewritten_url': rewritten_url if rewritten_url != original_url else None,
        'archived': False,
        'archive_url': None,
        'timestamp': None,
        'checked_variations': []
    }
    
    # URLs to check (original and rewritten if different)
    urls_to_check = [original_url]
    if rewritten_url != original_url:
        urls_to_check.append(rewritten_url)
    
    # Also try HTTP version if HTTPS
    for url in list(urls_to_check):
        if url.startswith('https://'):
            urls_to_check.append(url.replace('https://', 'http://'))
    
    # Check each URL variation
    for check_url in urls_to_check:
        try:
            api_url = "http://archive.org/wayback/available"
            params = {"url": check_url}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            resp = requests.get(api_url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            results['checked_variations'].append({
                'url': check_url,
                'status': 'checked'
            })
            
            if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
                snapshot = data["archived_snapshots"]["closest"]
                if snapshot.get("available"):
                    results['archived'] = True
                    results['archive_url'] = snapshot["url"]
                    results['timestamp'] = snapshot.get("timestamp", "unknown")
                    logger.debug(f"  Found archive for {check_url}")
                    break
            
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            results['checked_variations'].append({
                'url': check_url,
                'status': f'error: {e}'
            })
            logger.error(f"  Error checking {check_url}: {e}")
    
    return results

def scan_content_directory(content_dir, post_types=['post']):
    """Scan content directory for nata2.info URLs"""
    all_urls = set()
    posts_with_urls = []
    
    for post_type in post_types:
        type_dir = content_dir / post_type
        if not type_dir.exists():
            logger.warning(f"Content type directory not found: {type_dir}")
            continue
        
        # Find all markdown files
        for md_file in type_dir.rglob('*.md'):
            # Skip _index.md files
            if md_file.name == '_index.md':
                continue
            
            logger.debug(f"Checking: {md_file}")
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                urls = extract_urls_from_content(post.content)
                
                if urls:
                    all_urls.update(urls)
                    # Convert date to string if it's a datetime object
                    post_date = post.get('date', 'Unknown')
                    if hasattr(post_date, 'isoformat'):
                        post_date = post_date.isoformat()
                    elif hasattr(post_date, 'strftime'):
                        post_date = post_date.strftime('%Y-%m-%d')
                    else:
                        post_date = str(post_date)
                    
                    posts_with_urls.append({
                        'path': str(md_file.relative_to(content_dir.parent)),
                        'title': post.get('title', 'Untitled'),
                        'date': post_date,
                        'urls': list(urls)
                    })
                    logger.info(f"  Found {len(urls)} nata2.info URLs in {md_file.name}")
                    
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")
    
    return all_urls, posts_with_urls

def main():
    parser = argparse.ArgumentParser(
        description='Check availability of nata2.info URLs on archive.org'
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
        '--output',
        default='nata2_urls.txt',
        help='Output file for URL list (default: nata2_urls.txt)'
    )
    parser.add_argument(
        '--report',
        default='nata2_archive_report.json',
        help='Output file for detailed report (default: nata2_archive_report.json)'
    )
    parser.add_argument(
        '--check-archives',
        action='store_true',
        help='Check archive.org availability for each URL (slower)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Handle both relative and absolute paths
    if Path(args.content_dir).is_absolute():
        content_dir = Path(args.content_dir)
    else:
        content_dir = project_root / args.content_dir
    
    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        return
    
    logger.info(f"Scanning content in: {content_dir}")
    logger.info(f"Looking for post types: {', '.join(args.post_types)}")
    
    # Scan for URLs
    all_urls, posts_with_urls = scan_content_directory(content_dir, args.post_types)
    
    logger.info(f"\nFound {len(all_urls)} unique nata2.info URLs across {len(posts_with_urls)} posts")
    
    # Write URLs to text file
    output_path = project_root / args.output
    with open(output_path, 'w', encoding='utf-8') as f:
        for url in sorted(all_urls):
            f.write(url + '\n')
    logger.info(f"Wrote URL list to: {output_path}")
    
    # Create report structure
    report = {
        'scan_date': datetime.now().isoformat(),
        'total_unique_urls': len(all_urls),
        'total_posts_with_urls': len(posts_with_urls),
        'posts': posts_with_urls,
        'urls': {}
    }
    
    # Check archive availability if requested
    if args.check_archives:
        logger.info("\nChecking archive.org availability...")
        archived_count = 0
        
        for i, url in enumerate(sorted(all_urls), 1):
            logger.info(f"\n[{i}/{len(all_urls)}] Checking: {url}")
            
            result = check_archive_availability(url)
            report['urls'][url] = result
            
            if result['archived']:
                archived_count += 1
                logger.info(f"  ✓ Archived: {result['archive_url']}")
            else:
                logger.info(f"  ✗ Not archived")
            
            # Show progress
            if i % 10 == 0:
                logger.info(f"\nProgress: {i}/{len(all_urls)} checked, {archived_count} archived")
        
        report['archived_count'] = archived_count
        report['missing_count'] = len(all_urls) - archived_count
        report['archive_percentage'] = round((archived_count / len(all_urls)) * 100, 2) if all_urls else 0
        
        logger.info(f"\n\nArchive Summary:")
        logger.info(f"  Total URLs: {len(all_urls)}")
        logger.info(f"  Archived: {archived_count} ({report['archive_percentage']}%)")
        logger.info(f"  Missing: {report['missing_count']}")
    
    # Write detailed report
    report_path = project_root / args.report
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    logger.info(f"\nWrote detailed report to: {report_path}")
    
    # Print summary of posts with the most URLs
    if posts_with_urls:
        logger.info("\n\nPosts with the most nata2.info URLs:")
        sorted_posts = sorted(posts_with_urls, key=lambda x: len(x['urls']), reverse=True)[:10]
        for post in sorted_posts:
            logger.info(f"  {post['title'][:50]:<50} - {len(post['urls'])} URLs")

if __name__ == '__main__':
    main()