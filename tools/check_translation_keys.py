#!/usr/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
# ]
# ///

# ABOUTME: Checks Hugo posts for translationKey collisions, especially when dates differ.
# ABOUTME: Helps ensure consistent translation linking across multilingual content.
#
# Required dependencies: pyyaml
# uv add --script check_translation_keys.py pyyaml

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re

try:
    import yaml
except ImportError:
    print("Error: This script requires the PyYAML package.")
    print("Install it with: cd tools && uv add --script check_translation_keys.py pyyaml")
    sys.exit(1)


def parse_frontmatter(content):
    """Extract YAML frontmatter from content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]), parts[2]
            except yaml.YAMLError:
                return None, content
    return None, content


def extract_date(frontmatter):
    """Extract and parse date from frontmatter."""
    if not frontmatter or "date" not in frontmatter:
        return None
    
    date_str = frontmatter["date"]
    if isinstance(date_str, datetime):
        return date_str.date()
        
    # Handle different date formats
    date_formats = [
        "%Y-%m-%d",            # 2025-02-16
        "%Y-%m-%d %H:%M:%S",   # 2025-02-16 18:00:00
        "%Y-%m-%d %H:%M:%S%z", # 2025-02-16 18:00:00-05:00
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(str(date_str).split('.')[0], fmt)
            return parsed_date.date()
        except ValueError:
            continue
    
    return None


def find_hugo_content_files(directory):
    """Find all Hugo content files in the given directory."""
    content_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".md", ".html")):
                content_files.append(os.path.join(root, file))
    
    return content_files


def check_translation_keys(content_dir, verbose=False):
    """Check for translationKey collisions with date awareness."""
    files = find_hugo_content_files(content_dir)
    
    # Group files by translationKey
    translation_groups = defaultdict(list)
    skipped_files = []
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                if verbose:
                    print(f"Warning: Could not read {file_path} due to encoding issues. Skipping.")
                skipped_files.append(file_path)
                continue
        
        frontmatter, _ = parse_frontmatter(content)
        
        if not frontmatter:
            if verbose:
                print(f"Warning: No valid frontmatter found in {file_path}. Skipping.")
            skipped_files.append(file_path)
            continue
        
        translation_key = frontmatter.get("translationKey")
        
        if not translation_key:
            if verbose:
                print(f"Warning: No translationKey found in {file_path}. Skipping.")
            skipped_files.append(file_path)
            continue
        
        date = extract_date(frontmatter)
        
        translation_groups[translation_key].append({
            "file_path": file_path,
            "date": date,
            "frontmatter": frontmatter
        })
    
    # Check for collisions
    collisions = []
    
    for key, files in translation_groups.items():
        if len(files) <= 1:
            continue
        
        # Group by date
        date_groups = defaultdict(list)
        for file_info in files:
            date_str = str(file_info["date"]) if file_info["date"] else "unknown"
            date_groups[date_str].append(file_info)
        
        # If multiple dates for same translationKey, it's a collision
        if len(date_groups) > 1:
            collision_details = {
                "translation_key": key,
                "date_groups": date_groups
            }
            collisions.append(collision_details)
    
    return collisions, skipped_files


def get_suggested_key(key, file_info):
    """Generate a suggested translation key for a file"""
    if file_info["date"]:
        date_str = str(file_info["date"]).replace("-", "")
        return f"{key}-{date_str}"
    else:
        # Fallback to extracting date from file path if present
        file_path = file_info["file_path"]
        filename = os.path.basename(file_path)
        date_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{8})', filename)
        if date_match:
            date_str = date_match.group(1).replace("-", "")
            return f"{key}-{date_str}"
    
    # Last resort if no date is found
    return f"{key}-unique"


def fix_translation_key(file_path, old_key, new_key):
    """Fix a translation key in a given file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple string replacement for the translationKey line
        # This approach is safer than modifying the entire YAML frontmatter
        pattern = r'(translationKey\s*:\s*)(["\']?)' + re.escape(old_key) + r'\2'
        new_content = re.sub(pattern, f'\\1"{new_key}"', content)
        
        if content == new_content:
            # Try another pattern in case the key was not in quotes
            pattern = r'(translationKey\s*:\s*)' + re.escape(old_key)
            new_content = re.sub(pattern, f'\\1"{new_key}"', content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            print(f"      Warning: Could not find translationKey pattern in {file_path}")
            return False
    
    except Exception as e:
        print(f"      Error fixing file {file_path}: {str(e)}")
        return False


def print_collisions(collisions, verbose=False, suggest=False, fix=False):
    """Print collision information and optionally fix issues."""
    if not collisions:
        print("No translationKey collisions found! 🎉")
        return
    
    print(f"Found {len(collisions)} translationKey collision(s) with differing dates:")
    print("-" * 80)
    
    fixed_files = 0
    total_files = 0
    
    for idx, collision in enumerate(collisions, 1):
        key = collision["translation_key"]
        date_groups = collision["date_groups"]
        
        print(f"{idx}. Key: '{key}'")
        
        for date, files in date_groups.items():
            print(f"   Date: {date}")
            
            for file_info in files:
                total_files += 1
                file_path = file_info["file_path"]
                rel_path = os.path.relpath(file_path)
                print(f"      - {rel_path}")
                
                suggested_key = get_suggested_key(key, file_info)
                
                if suggest or fix:
                    print(f"        Suggested key: '{suggested_key}'")
                
                if fix:
                    success = fix_translation_key(file_path, key, suggested_key)
                    if success:
                        fixed_files += 1
                        print(f"        ✅ Fixed: translationKey updated to '{suggested_key}'")
                    else:
                        print(f"        ❌ Failed to update translationKey")
        
        if verbose and not suggest and not fix:
            print("   Suggestion: Make keys unique by adding date, e.g.:")
            print(f"      '{key}' → '{key}-2025-02-16'")
            print("   Use --suggest for specific suggestions")
            print("   Use --fix to automatically apply changes")
        
        print("-" * 80)
    
    if fix:
        print(f"\nFixed {fixed_files} out of {total_files} files with collisions")


def check_specific_files(files, verbose=False):
    """Check specific files for translationKey collisions."""
    # Group files by translationKey
    translation_groups = defaultdict(list)
    skipped_files = []
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError) as e:
            if verbose:
                print(f"Warning: Could not read {file_path}: {str(e)}. Skipping.")
            skipped_files.append(file_path)
            continue
        
        frontmatter, _ = parse_frontmatter(content)
        
        if not frontmatter:
            if verbose:
                print(f"Warning: No valid frontmatter found in {file_path}. Skipping.")
            skipped_files.append(file_path)
            continue
        
        translation_key = frontmatter.get("translationKey")
        
        if not translation_key:
            if verbose:
                print(f"Warning: No translationKey found in {file_path}. Skipping.")
            skipped_files.append(file_path)
            continue
        
        date = extract_date(frontmatter)
        
        translation_groups[translation_key].append({
            "file_path": file_path,
            "date": date,
            "frontmatter": frontmatter
        })
    
    # Check for collisions
    collisions = []
    
    for key, files in translation_groups.items():
        if len(files) <= 1:
            continue
        
        # Group by date
        date_groups = defaultdict(list)
        for file_info in files:
            date_str = str(file_info["date"]) if file_info["date"] else "unknown"
            date_groups[date_str].append(file_info)
        
        # If multiple dates for same translationKey, it's a collision
        if len(date_groups) > 1:
            collision_details = {
                "translation_key": key,
                "date_groups": date_groups
            }
            collisions.append(collision_details)
    
    return collisions, skipped_files


def main():
    parser = argparse.ArgumentParser(
        description="Check Hugo posts for translationKey collisions, especially when dates differ.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run check_translation_keys.py content/
  uv run check_translation_keys.py --verbose content/ content.ja/ content.ko/
  uv run check_translation_keys.py --suggest content/
  uv run check_translation_keys.py --fix content/
  uv run check_translation_keys.py --files content/music/file1.md content/music/file2.md
""")
    
    parser.add_argument("paths", nargs="+", help="Hugo content directories or files to check")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--suggest", "-s", action="store_true", help="Suggest fixes for collisions")
    parser.add_argument("--fix", action="store_true", help="Automatically fix collisions by adding date-based suffixes")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Only report issues without making changes (default behavior)")
    parser.add_argument("--files", "-f", action="store_true", help="Treat all paths as files instead of directories")
    
    args = parser.parse_args()
    
    all_collisions = []
    all_skipped = []
    all_files = []
    
    # First, collect all files to check
    if args.files:
        all_files = args.paths
    else:
        for path in args.paths:
            if os.path.isdir(path):
                print(f"Checking directory: {path}")
                all_files.extend(find_hugo_content_files(path))
            elif os.path.isfile(path):
                all_files.append(path)
            else:
                print(f"Error: '{path}' is not a valid directory or file", file=sys.stderr)
    
    # Then check for collisions
    if args.files or any(os.path.isfile(p) for p in args.paths):
        collisions, skipped = check_specific_files(all_files, args.verbose)
    else:
        collisions, skipped = [], []
        for directory in [p for p in args.paths if os.path.isdir(p)]:
            dir_collisions, dir_skipped = check_translation_keys(directory, args.verbose)
            collisions.extend(dir_collisions)
            skipped.extend(dir_skipped)
    
    all_collisions.extend(collisions)
    all_skipped.extend(skipped)
    
    print("\n" + "=" * 80)
    print_collisions(all_collisions, args.verbose, args.suggest, args.fix)
    
    if args.verbose and all_skipped:
        print(f"\nSkipped {len(all_skipped)} files (no frontmatter, missing translationKey, or encoding issues)")
    
    # Provide a summary with next steps if collisions were found
    if all_collisions and not args.fix:
        print("\nSummary:")
        print("  • Found translation key collisions that need to be resolved")
        print("  • Run with --suggest for specific suggestions for each file")
        print("  • Run with --fix to automatically apply suggested changes")
    
    # Return non-zero exit code if collisions were found and not fixed
    return 1 if all_collisions and not args.fix else 0


if __name__ == "__main__":
    sys.exit(main())