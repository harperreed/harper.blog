#!/usr/bin/env python3
# ABOUTME: This script checks nata2.info URLs availability using archive.org CDX API
# ABOUTME: It's faster than individual checks and provides comprehensive archive data

import os
import json
import requests
import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse, quote
import time
from collections import defaultdict
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_cdx_data(domain="nata2.info"):
    """Fetch CDX data for a domain from archive.org"""
    cdx_url = f"http://web.archive.org/cdx/search/cdx"
    
    # Parameters for the CDX API
    params = {
        "url": f"{domain}/*",
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype,digest",
        "filter": "statuscode:200",
        "collapse": "original"  # Get unique URLs
    }
    
    logger.info(f"Fetching CDX data for {domain}...")
    logger.debug(f"CDX URL: {cdx_url}")
    logger.debug(f"Params: {params}")
    
    try:
        response = requests.get(cdx_url, params=params, timeout=60)
        response.raise_for_status()
        
        # CDX returns JSON array, first row is headers
        data = response.json()
        if len(data) <= 1:
            logger.warning("No archived URLs found")
            return []
        
        headers = data[0]
        rows = data[1:]
        
        # Convert to list of dicts
        results = []
        for row in rows:
            result = dict(zip(headers, row))
            results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error fetching CDX data: {e}")
        return []

def analyze_cdx_data(cdx_data):
    """Analyze CDX data to get statistics"""
    stats = {
        'total_unique_urls': len(cdx_data),
        'by_year': defaultdict(int),
        'by_path': defaultdict(int),
        'by_type': defaultdict(int),
        'image_urls': [],
        'page_urls': [],
        'other_urls': []
    }
    
    for entry in cdx_data:
        url = entry.get('original', '')
        timestamp = entry.get('timestamp', '')
        mimetype = entry.get('mimetype', '')
        
        # Extract year from timestamp
        if timestamp and len(timestamp) >= 4:
            year = timestamp[:4]
            stats['by_year'][year] += 1
        
        # Analyze URL path
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if path_parts and path_parts[0]:
            stats['by_path'][path_parts[0]] += 1
        
        # Categorize by type
        if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
            stats['by_type']['images'] += 1
            stats['image_urls'].append(url)
        elif any(ext in url.lower() for ext in ['.mp3', '.mp4', '.avi', '.mov', '.3gp']):
            stats['by_type']['media'] += 1
            stats['other_urls'].append(url)
        elif parsed.query:
            stats['by_type']['dynamic'] += 1
            stats['page_urls'].append(url)
        else:
            stats['by_type']['other'] += 1
            stats['other_urls'].append(url)
    
    return stats

def check_specific_urls(urls_file, cdx_data):
    """Check which specific URLs from a file are archived"""
    if not os.path.exists(urls_file):
        logger.error(f"URLs file not found: {urls_file}")
        return None
    
    # Create a set of archived URLs for fast lookup
    archived_urls = {entry['original'] for entry in cdx_data}
    
    # Also create variations (with/without www, http/https)
    archived_variations = set()
    for url in archived_urls:
        parsed = urlparse(url)
        # Add variations
        if parsed.scheme == 'http':
            archived_variations.add(url.replace('http://', 'https://'))
        elif parsed.scheme == 'https':
            archived_variations.add(url.replace('https://', 'http://'))
        
        if 'www.' in parsed.netloc:
            archived_variations.add(url.replace('www.', ''))
        else:
            domain_parts = parsed.netloc.split('.')
            if len(domain_parts) == 2:  # e.g., nata2.info
                archived_variations.add(url.replace(parsed.netloc, f'www.{parsed.netloc}'))
    
    archived_urls.update(archived_variations)
    
    # Read URLs from file
    with open(urls_file, 'r', encoding='utf-8') as f:
        requested_urls = [line.strip() for line in f if line.strip()]
    
    results = {
        'total_requested': len(requested_urls),
        'found': [],
        'not_found': []
    }
    
    for url in requested_urls:
        if url in archived_urls:
            results['found'].append(url)
        else:
            results['not_found'].append(url)
    
    results['found_count'] = len(results['found'])
    results['not_found_count'] = len(results['not_found'])
    results['coverage_percentage'] = round((results['found_count'] / results['total_requested']) * 100, 2) if results['total_requested'] > 0 else 0
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='Check nata2.info archive availability using CDX API'
    )
    parser.add_argument(
        '--domain',
        default='nata2.info',
        help='Domain to check (default: nata2.info)'
    )
    parser.add_argument(
        '--urls-file',
        help='File containing specific URLs to check against CDX data'
    )
    parser.add_argument(
        '--output',
        default='nata2_cdx_report.json',
        help='Output file for report (default: nata2_cdx_report.json)'
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
    
    # Fetch CDX data
    cdx_data = get_cdx_data(args.domain)
    
    if not cdx_data:
        logger.error("No CDX data retrieved")
        return
    
    logger.info(f"Retrieved {len(cdx_data)} archived URLs")
    
    # Analyze the data
    stats = analyze_cdx_data(cdx_data)
    
    # Print summary
    logger.info("\nArchive Summary:")
    logger.info(f"  Total unique URLs: {stats['total_unique_urls']}")
    
    logger.info("\nBy year:")
    for year in sorted(stats['by_year'].keys()):
        logger.info(f"  {year}: {stats['by_year'][year]} URLs")
    
    logger.info("\nBy type:")
    for type_name, count in stats['by_type'].items():
        logger.info(f"  {type_name}: {count} URLs")
    
    logger.info("\nBy path:")
    for path, count in sorted(stats['by_path'].items(), key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"  /{path}/: {count} URLs")
    
    # Create report
    report = {
        'query_date': datetime.now().isoformat(),
        'domain': args.domain,
        'total_archived_urls': len(cdx_data),
        'statistics': {
            'by_year': dict(stats['by_year']),
            'by_type': dict(stats['by_type']),
            'by_path': dict(stats['by_path'])
        },
        'sample_urls': {
            'images': stats['image_urls'][:10],
            'pages': stats['page_urls'][:10],
            'other': stats['other_urls'][:10]
        }
    }
    
    # Check specific URLs if provided
    if args.urls_file:
        logger.info(f"\nChecking specific URLs from: {args.urls_file}")
        check_results = check_specific_urls(args.urls_file, cdx_data)
        
        if check_results:
            report['specific_urls_check'] = check_results
            
            logger.info(f"\nSpecific URLs Check:")
            logger.info(f"  Total requested: {check_results['total_requested']}")
            logger.info(f"  Found in archive: {check_results['found_count']} ({check_results['coverage_percentage']}%)")
            logger.info(f"  Not found: {check_results['not_found_count']}")
            
            if check_results['not_found'] and len(check_results['not_found']) <= 20:
                logger.info("\nURLs not found in archive:")
                for url in check_results['not_found']:
                    logger.info(f"  - {url}")
    
    # Save full CDX data if verbose
    if args.verbose:
        report['cdx_data'] = cdx_data
    
    # Write report
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\nWrote report to: {output_path}")

if __name__ == '__main__':
    main()