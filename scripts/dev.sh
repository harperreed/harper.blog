#!/bin/bash

# Run Tailwind in watch mode in background
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css --watch &
TAILWIND_PID=$!

# Run Hugo server
hugo serve --buildDrafts --buildFuture --navigateToChanged

# Cleanup on exit
trap "kill $TAILWIND_PID 2>/dev/null" EXIT
