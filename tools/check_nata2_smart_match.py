#!/usr/bin/env python3
# ABOUTME: This script smartly matches nata2.info URLs from blog posts with archived URLs
# ABOUTME: It handles different URL formats and finds the best available archive matches

import os
import json
import requests
import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse, quote, unquote, parse_qs
import time
from collections import defaultdict
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def normalize_url(url):
    """Normalize a URL to help with matching"""
    parsed = urlparse(url)
    
    # Extract path and query components
    if parsed.query:
        query_params = parse_qs(parsed.query)
        
        # Handle nata2.info query-based URLs
        if 'path' in query_params and 'img' in query_params:
            path = unquote(query_params['path'][0])
            img = query_params['img'][0]
            # Create a normalized representation
            return f"nata2.info/{path}/{img}"
        elif 'path' in query_params:
            path = unquote(query_params['path'][0])
            return f"nata2.info/{path}"
    
    # For direct URLs, normalize the domain and path
    domain = parsed.netloc.replace('www.', '').replace(':80', '')
    path = parsed.path.strip('/')
    
    if path:
        return f"{domain}/{path}"
    else:
        return domain

def extract_path_and_image(url):
    """Extract path and image components from a URL"""
    parsed = urlparse(url)
    
    if parsed.query:
        query_params = parse_qs(parsed.query)
        if 'path' in query_params:
            path = unquote(query_params['path'][0])
            img = query_params.get('img', [None])[0]
            return path, img
    
    # For direct URLs
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) > 1:
        # Assume last part is filename
        path = '/'.join(path_parts[:-1])
        img = path_parts[-1]
        return path, img
    
    return None, None

def find_matches(requested_urls, cdx_data):
    """Find matches between requested URLs and archived URLs"""
    # Create normalized lookup for archived URLs
    archived_lookup = defaultdict(list)
    
    for entry in cdx_data:
        url = entry.get('original', '')
        normalized = normalize_url(url)
        archived_lookup[normalized].append(entry)
    
    logger.debug(f"Created lookup with {len(archived_lookup)} normalized URLs")
    
    # Try to match requested URLs
    matches = []
    no_matches = []
    
    for requested_url in requested_urls:
        normalized_requested = normalize_url(requested_url)
        path, img = extract_path_and_image(requested_url)
        
        # Try direct normalized match
        if normalized_requested in archived_lookup:
            match_entry = archived_lookup[normalized_requested][0]
            matches.append({
                'requested': requested_url,
                'matched': match_entry['original'],
                'timestamp': match_entry['timestamp'],
                'match_type': 'exact_normalized'
            })
            continue
        
        # Try variations if we have path/img components
        if path and img:
            # Try different path variations
            variations = [
                f"nata2.info/{path}/{img}",
                f"nata2.info/pictures/{path}/{img}",
                f"nata2.info/{path.replace(':', '%3A')}/{img}",
                f"nata2.info/.thumbnails/{path}/{img}",
                f"nata2.info/%2Ethumbnails/{path}/{img}"
            ]
            
            found = False
            for variation in variations:
                if variation in archived_lookup:
                    match_entry = archived_lookup[variation][0]
                    matches.append({
                        'requested': requested_url,
                        'matched': match_entry['original'],
                        'timestamp': match_entry['timestamp'],
                        'match_type': 'variation'
                    })
                    found = True
                    break
            
            if not found:
                # Try partial path match
                for normalized, entries in archived_lookup.items():
                    if img in normalized and any(p in normalized for p in path.split('/')):
                        match_entry = entries[0]
                        matches.append({
                            'requested': requested_url,
                            'matched': match_entry['original'],
                            'timestamp': match_entry['timestamp'],
                            'match_type': 'partial'
                        })
                        found = True
                        break
            
            if not found:
                no_matches.append(requested_url)
        else:
            # For URLs without clear path/img structure
            no_matches.append(requested_url)
    
    return matches, no_matches

def get_archive_urls(matches):
    """Generate archive.org URLs for matched content"""
    archive_urls = []
    
    for match in matches:
        timestamp = match['timestamp']
        original_url = match['matched']
        
        # Create archive.org URL
        archive_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
        
        # For images, use if_ modifier
        if any(ext in original_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.3gp']):
            archive_url = f"https://web.archive.org/web/{timestamp}if_/{original_url}"
        
        archive_urls.append({
            **match,
            'archive_url': archive_url
        })
    
    return archive_urls

def main():
    parser = argparse.ArgumentParser(
        description='Smart matching of nata2.info URLs with archive.org data'
    )
    parser.add_argument(
        '--urls-file',
        default='nata2_urls.txt',
        help='File containing URLs to check (default: nata2_urls.txt)'
    )
    parser.add_argument(
        '--cdx-report',
        default='nata2_cdx_report.json',
        help='CDX report file (default: nata2_cdx_report.json)'
    )
    parser.add_argument(
        '--output',
        default='nata2_matches.json',
        help='Output file for matches (default: nata2_matches.json)'
    )
    parser.add_argument(
        '--fetch-cdx',
        action='store_true',
        help='Fetch fresh CDX data instead of using existing report'
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
    
    # Get CDX data
    if args.fetch_cdx:
        logger.info("Fetching fresh CDX data...")
        # Fetch CDX data
        cdx_url = "http://web.archive.org/cdx/search/cdx"
        params = {
            "url": "nata2.info/*",
            "output": "json",
            "fl": "timestamp,original",
            "filter": "statuscode:200"
        }
        
        try:
            response = requests.get(cdx_url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if len(data) <= 1:
                logger.error("No CDX data retrieved")
                return
            
            headers = data[0]
            rows = data[1:]
            
            cdx_data = []
            for row in rows:
                cdx_data.append(dict(zip(headers, row)))
            
            logger.info(f"Retrieved {len(cdx_data)} archived URLs")
            
        except Exception as e:
            logger.error(f"Error fetching CDX data: {e}")
            return
    else:
        # Load existing CDX report
        if not os.path.exists(args.cdx_report):
            logger.error(f"CDX report not found: {args.cdx_report}")
            logger.info("Run check_nata2_cdx.py first or use --fetch-cdx")
            return
        
        logger.info(f"Loading CDX data from {args.cdx_report}")
        with open(args.cdx_report, 'r') as f:
            report = json.load(f)
            
        # Extract CDX data if available
        if 'cdx_data' in report:
            cdx_data = report['cdx_data']
        else:
            logger.error("No cdx_data in report. Run check_nata2_cdx.py with -v flag")
            return
    
    # Load requested URLs
    if not os.path.exists(args.urls_file):
        logger.error(f"URLs file not found: {args.urls_file}")
        return
    
    with open(args.urls_file, 'r') as f:
        requested_urls = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Loaded {len(requested_urls)} URLs to check")
    
    # Find matches
    logger.info("Finding matches...")
    matches, no_matches = find_matches(requested_urls, cdx_data)
    
    logger.info(f"\nResults:")
    logger.info(f"  Matched: {len(matches)} URLs")
    logger.info(f"  Not matched: {len(no_matches)} URLs")
    logger.info(f"  Coverage: {round((len(matches) / len(requested_urls)) * 100, 2)}%")
    
    # Generate archive URLs
    archive_urls = get_archive_urls(matches)
    
    # Create report
    report = {
        'match_date': datetime.now().isoformat(),
        'total_requested': len(requested_urls),
        'total_matched': len(matches),
        'total_unmatched': len(no_matches),
        'coverage_percentage': round((len(matches) / len(requested_urls)) * 100, 2),
        'matches': archive_urls,
        'unmatched_urls': no_matches
    }
    
    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\nWrote match report to: {args.output}")
    
    # Show sample matches
    if matches:
        logger.info("\nSample matches:")
        for match in matches[:5]:
            logger.info(f"  {match['requested']}")
            logger.info(f"    → {match['matched']}")
            logger.info(f"    Type: {match['match_type']}")

if __name__ == '__main__':
    main()