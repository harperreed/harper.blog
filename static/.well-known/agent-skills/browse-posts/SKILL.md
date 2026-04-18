---
name: browse-posts
description: Browse and read blog posts on harper.blog
---

# Browse Posts

Navigate the blog's post archive at https://harper.blog/.

## Usage

- **Homepage:** `GET https://harper.blog/` — latest posts
- **Post archive:** `GET https://harper.blog/post/` — all posts
- **Individual post:** `GET https://harper.blog/post/{slug}/` — full post content

## Content Format

All pages return HTML. Posts include YAML frontmatter metadata (title, date, tags, summary) rendered into semantic HTML with proper heading hierarchy.
