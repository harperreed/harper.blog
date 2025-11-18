#!/usr/bin/env python3
# ABOUTME: Remove bundles newer than June 10, 2024
# ABOUTME: Clean up remaining stragglers

from pathlib import Path
import shutil

TARGET_DIR = Path(".")
cutoff_date = "2024-06-10"

to_remove = []
for target in TARGET_DIR.glob("20*"):
    if not target.is_dir():
        continue

    parts = target.name.split('_', 1)
    if len(parts) < 1:
        continue

    bundle_date = parts[0]

    if bundle_date > cutoff_date:
        to_remove.append(target)

print(f"Removing {len(to_remove)} bundles newer than {cutoff_date}\n")

for target in sorted(to_remove):
    print(f"Removing: {target.name}")
    shutil.rmtree(target)

print(f"\n✓ Removed {len(to_remove)} bundles")
