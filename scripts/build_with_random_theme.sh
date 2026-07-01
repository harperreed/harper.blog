#!/bin/bash

# ABOUTME: Build wrapper that selects a random theme before running Hugo
# ABOUTME: Used by Netlify to give the site a different theme on each deploy

set -euo pipefail

# Available themes (must match themes.css)
THEMES=(
    "nature"
    "sunset"
    "nordic"
    "terminal"
)

# Select random theme
RANDOM_INDEX=$((RANDOM % ${#THEMES[@]}))
SELECTED_THEME="${THEMES[$RANDOM_INDEX]}"

echo "============================================"
echo "  Random Theme Builder"
echo "============================================"
echo "  Selected theme: $SELECTED_THEME"
echo "============================================"

# Export for Hugo to pick up
export HUGO_RANDOM_THEME="$SELECTED_THEME"

# Run Hugo with all passed arguments
exec hugo "$@"
