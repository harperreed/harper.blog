---
name: browse-posts
description: Browse and read blog posts on harper.blog
---

# Browse Posts

Navigate the blog's post archive at https://harper.blog/.

## Usage

- **Homepage:** `GET https://harper.blog/` — latest posts
- **Post archive:** `GET https://harper.blog/posts/` — all posts
- **Individual post:** `GET https://harper.blog/{YYYY}/{MM}/{DD}/{slug}/` — full post content (e.g., `/2025/04/17/my-post-title/`)

## Content Format

All pages return HTML with semantic heading hierarchy, structured meta tags, and Open Graph metadata.
