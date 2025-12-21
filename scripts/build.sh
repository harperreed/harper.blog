#!/bin/bash
set -e

echo "Building Tailwind CSS..."
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css --minify

echo "Building Hugo..."
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info

echo "Building search index with Pagefind..."
npx pagefind --site public --glob "**/*.html"

echo "Build complete!"
