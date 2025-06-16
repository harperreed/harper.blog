#!/usr/bin/env python3
# ABOUTME: This script generates a comprehensive summary of nata2.info archive availability
# ABOUTME: It combines data from multiple sources to create a final report

import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_json_file(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None

def generate_summary(urls_file, archive_report, cdx_report, matches_report):
    """Generate comprehensive summary report"""
    
    # Load all data
    logger.info("Loading data files...")
    
    # Load original URLs
    try:
        with open(urls_file, 'r') as f:
            original_urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error loading URLs file: {e}")
        return None
    
    archive_data = load_json_file(archive_report) if archive_report else None
    cdx_data = load_json_file(cdx_report) if cdx_report else None
    matches_data = load_json_file(matches_report) if matches_report else None
    
    # Create summary
    summary = {
        'report_date': datetime.now().isoformat(),
        'overview': {
            'total_urls_in_posts': len(original_urls),
            'unique_hosts': len(set(url.split('/')[2] for url in original_urls if '/' in url))
        }
    }
    
    # Add data from archive report
    if archive_data:
        summary['posts_analysis'] = {
            'total_posts_with_nata2_urls': archive_data.get('total_posts_with_urls', 0),
            'posts_breakdown': []
        }
        
        # Get top posts
        for post in sorted(archive_data.get('posts', []), key=lambda x: len(x['urls']), reverse=True)[:10]:
            summary['posts_analysis']['posts_breakdown'].append({
                'title': post['title'],
                'date': post['date'],
                'url_count': len(post['urls'])
            })
    
    # Add CDX analysis
    if cdx_data:
        summary['archive_coverage'] = {
            'total_archived_urls': cdx_data.get('total_archived_urls', 0),
            'archive_by_year': cdx_data.get('statistics', {}).get('by_year', {}),
            'archive_by_type': cdx_data.get('statistics', {}).get('by_type', {})
        }
    
    # Add matching results
    if matches_data:
        summary['matching_results'] = {
            'total_matched': matches_data.get('total_matched', 0),
            'total_unmatched': matches_data.get('total_unmatched', 0),
            'coverage_percentage': matches_data.get('coverage_percentage', 0),
            'match_types': defaultdict(int)
        }
        
        # Count match types
        for match in matches_data.get('matches', []):
            summary['matching_results']['match_types'][match.get('match_type', 'unknown')] += 1
        
        summary['matching_results']['match_types'] = dict(summary['matching_results']['match_types'])
        
        # Sample unmatched URLs
        summary['unmatched_samples'] = matches_data.get('unmatched_urls', [])[:20]
    
    # Generate recommendations
    summary['recommendations'] = []
    
    if matches_data and matches_data.get('coverage_percentage', 0) < 100:
        summary['recommendations'].append({
            'priority': 'high',
            'action': 'Archive missing content',
            'detail': f"{matches_data.get('total_unmatched', 0)} URLs are not archived and may be lost forever"
        })
    
    if cdx_data:
        recent_years = ['2023', '2024', '2025']
        recent_archives = sum(cdx_data.get('statistics', {}).get('by_year', {}).get(year, 0) for year in recent_years)
        if recent_archives < 100:
            summary['recommendations'].append({
                'priority': 'medium',
                'action': 'Update archive snapshots',
                'detail': 'Very few recent snapshots exist, consider triggering new archive captures'
            })
    
    summary['recommendations'].append({
        'priority': 'medium',
        'action': 'Run content migration',
        'detail': 'Use migrate_nata2_content.py to download and localize available archived content'
    })
    
    return summary

def print_summary(summary):
    """Print human-readable summary"""
    print("\n" + "="*60)
    print("NATA2.INFO ARCHIVE AVAILABILITY SUMMARY")
    print("="*60)
    
    print(f"\nReport Date: {summary['report_date']}")
    
    print(f"\n📊 OVERVIEW")
    print(f"  Total URLs in blog posts: {summary['overview']['total_urls_in_posts']}")
    print(f"  Unique hosts: {summary['overview']['unique_hosts']}")
    
    if 'posts_analysis' in summary:
        print(f"\n📝 POSTS WITH MOST NATA2 URLS")
        for post in summary['posts_analysis']['posts_breakdown'][:5]:
            print(f"  • {post['title'][:50]:<50} ({post['url_count']} URLs)")
    
    if 'archive_coverage' in summary:
        print(f"\n🗄️  ARCHIVE.ORG COVERAGE")
        print(f"  Total archived URLs: {summary['archive_coverage']['total_archived_urls']:,}")
        print(f"  By type:")
        for typ, count in summary['archive_coverage']['archive_by_type'].items():
            print(f"    - {typ}: {count:,}")
    
    if 'matching_results' in summary:
        print(f"\n🔍 MATCHING RESULTS")
        print(f"  Matched: {summary['matching_results']['total_matched']} URLs")
        print(f"  Unmatched: {summary['matching_results']['total_unmatched']} URLs")
        print(f"  Coverage: {summary['matching_results']['coverage_percentage']}%")
        
        if summary['matching_results']['match_types']:
            print(f"  Match types:")
            for typ, count in summary['matching_results']['match_types'].items():
                print(f"    - {typ}: {count}")
    
    if summary.get('unmatched_samples'):
        print(f"\n❌ SAMPLE UNMATCHED URLS (first 5)")
        for url in summary['unmatched_samples'][:5]:
            print(f"  • {url}")
    
    if summary.get('recommendations'):
        print(f"\n💡 RECOMMENDATIONS")
        for rec in summary['recommendations']:
            print(f"  [{rec['priority'].upper()}] {rec['action']}")
            print(f"         {rec['detail']}")
    
    print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description='Generate comprehensive nata2.info archive summary'
    )
    parser.add_argument(
        '--urls-file',
        default='../nata2_urls.txt',
        help='Original URLs file'
    )
    parser.add_argument(
        '--archive-report',
        default='../nata2_archive_report.json',
        help='Archive check report'
    )
    parser.add_argument(
        '--cdx-report',
        default='nata2_cdx_verbose.json',
        help='CDX report file'
    )
    parser.add_argument(
        '--matches-report',
        default='nata2_matches.json',
        help='Matches report file'
    )
    parser.add_argument(
        '--output',
        default='nata2_final_summary.json',
        help='Output summary file'
    )
    
    args = parser.parse_args()
    
    # Generate summary
    summary = generate_summary(
        args.urls_file,
        args.archive_report,
        args.cdx_report,
        args.matches_report
    )
    
    if not summary:
        logger.error("Failed to generate summary")
        return
    
    # Save summary
    with open(args.output, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved summary to: {args.output}")
    
    # Print human-readable summary
    print_summary(summary)

if __name__ == '__main__':
    main()