---
name: read-rss
description: Subscribe to harper.blog via RSS for recent posts
---

# Read RSS Feed

Consume the blog's RSS feed for structured access to recent content.

## Usage

- **Main feed:** `GET https://harper.blog/index.xml` — latest 20 posts (full content)
- **Content-Type:** `application/rss+xml`

## Feed Contents

Each item includes: title, link, publication date, full HTML content, and author. The feed is limited to the 20 most recent posts.
