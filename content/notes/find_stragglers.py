#!/usr/bin/env python3
# ABOUTME: Find bundles after June 10, 2024
# ABOUTME: Quick check for remaining stragglers

from pathlib import Path

TARGET_DIR = Path(".")
cutoff_date = "2024-06-10"

stragglers = []
for target in TARGET_DIR.glob("20*"):
    if not target.is_dir():
        continue

    parts = target.name.split('_', 1)
    if len(parts) < 1:
        continue

    bundle_date = parts[0]

    if bundle_date > cutoff_date:
        stragglers.append(target.name)

if stragglers:
    print(f"Found {len(stragglers)} bundles after {cutoff_date}:\n")
    for name in sorted(stragglers):
        print(f"  {name}")
else:
    print(f"✓ No stragglers found after {cutoff_date}")
