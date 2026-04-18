---
name: read-rss
description: Subscribe to harper.blog via RSS for recent posts
---

# Read RSS Feed

Consume the blog's RSS feeds for structured access to recent content.

## Usage

- **Main feed:** `GET https://harper.blog/index.xml` — latest 20 items across all content types (posts, notes, links)
- **Posts only:** `GET https://harper.blog/posts/index.xml` — blog posts only
- **Notes only:** `GET https://harper.blog/notes/index.xml` — micro-posts only
- **Content-Type:** `application/rss+xml`

## Feed Contents

Each item includes: title, link, publication date, full HTML content, and author. The main feed mixes all content types; use section-specific feeds for filtered access.
