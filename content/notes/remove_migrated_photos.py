#!/usr/bin/env python3
# ABOUTME: Remove ONLY migrated photo bundles after June 10, 2024
# ABOUTME: Preserves original notes by checking for harper.photos URL

from pathlib import Path
import shutil
import re

TARGET_DIR = Path(".")
cutoff_date = "2024-06-10"

to_remove = []
for target in TARGET_DIR.glob("20*"):
    if not target.is_dir():
        continue

    # Extract date from bundle name
    parts = target.name.split('_', 1)
    if len(parts) < 1:
        continue

    bundle_date = parts[0]

    # Skip if not after cutoff
    if bundle_date <= cutoff_date:
        continue

    # Check if this is a migrated photo (has harper.photos URL)
    index_md = target / "index.md"
    if not index_md.exists():
        continue

    content = index_md.read_text()

    # Only remove if it's a migrated photo from harper.photos
    if 'harper.photos' in content and 'original_url:' in content:
        to_remove.append(target)

print(f"Removing {len(to_remove)} MIGRATED PHOTO bundles after {cutoff_date}\n")

for target in sorted(to_remove):
    print(f"Removing: {target.name}")
    shutil.rmtree(target)

print(f"\n✓ Removed {len(to_remove)} migrated photo bundles")
print("✓ Original notes preserved")
