---
name: search-sitemap
description: Discover all URLs on harper.blog via XML sitemap
---

# Search via Sitemap

Use the XML sitemap to discover all available pages and content.

## Usage

- **Sitemap index:** `GET https://harper.blog/sitemap.xml`
- **Content-Type:** `application/xml`

## Sitemap Structure

The root `sitemap.xml` is a **sitemap index** containing links to per-language sub-sitemaps:

- `https://harper.blog/en/sitemap.xml` — English content
- `https://harper.blog/ja/sitemap.xml` — Japanese content
- `https://harper.blog/es/sitemap.xml` — Spanish content
- `https://harper.blog/ko/sitemap.xml` — Korean content

Each sub-sitemap lists all public URLs for that language including posts, notes, links, books, and music pages with last-modification dates. Follow the sub-sitemap links to get actual page URLs.
