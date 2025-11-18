#!/usr/bin/env python3
# ABOUTME: Remove "Photo: " prefix from migrated photo titles
# ABOUTME: Clean up title formatting for harper.photos bundles

from pathlib import Path
import re

TARGET_DIR = Path(".")

updated = 0
for target in TARGET_DIR.glob("20*"):
    if not target.is_dir():
        continue

    index_md = target / "index.md"
    if not index_md.exists():
        continue

    content = index_md.read_text()

    # Only process harper.photos bundles
    if 'harper.photos' not in content:
        continue

    # Check if title has "Photo: " prefix
    if "title: 'Photo: " not in content:
        continue

    # Remove "Photo: " prefix from title
    new_content = re.sub(
        r"title: 'Photo: (.*?)'",
        r"title: '\1'",
        content
    )

    if new_content != content:
        index_md.write_text(new_content)
        updated += 1
        print(f"Updated: {target.name}")

print(f"\n✓ Updated {updated} photo titles")
