#!/usr/bin/env python3
# ABOUTME: Check date range of migrated harper.photos bundles
# ABOUTME: Verify cutoff enforcement

from pathlib import Path

TARGET_DIR = Path(".")

migrated_dates = []
for target in TARGET_DIR.glob("20*"):
    if not target.is_dir():
        continue

    index_md = target / "index.md"
    if not index_md.exists():
        continue

    content = index_md.read_text()

    if 'harper.photos' in content:
        parts = target.name.split('_', 1)
        if parts:
            migrated_dates.append(parts[0])

if migrated_dates:
    migrated_dates.sort()
    print(f"Found {len(migrated_dates)} harper.photos bundles")
    print(f"Date range: {migrated_dates[0]} to {migrated_dates[-1]}")
    print(f"\nLast 10 dates:")
    for date in migrated_dates[-10:]:
        print(f"  {date}")
else:
    print("No harper.photos bundles found")
