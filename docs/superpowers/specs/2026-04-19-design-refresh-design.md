# Design Refresh: Unified Visual Language

**Date**: 2026-04-19
**Branch**: `design-refresh`
**Status**: Draft

## Problem

The blog has grown from a simple bearblog clone into a multi-section site (posts, notes, books, links, music, photos) but the design hasn't kept pace. Specific issues:

- **Typography**: Too plain, no clear hierarchy between headings, body, and metadata
- **Layout**: Content area feels cramped, needs breathing room
- **Section pages**: Each section uses different layout patterns and CSS classes — no consistency
- **Nav/sections**: Cluttered, too many items presented without structure
- **Visual identity**: Doesn't feel intentional anymore; the site has outgrown the stock bearblog look
- **Themes**: 25+ themes is excessive — most untested with the actual layout, creating maintenance burden

## Design Direction

**Modern minimal, bearblog-inspired.** Keep the philosophy (fast, clean, content-first) but give it a cohesive design language that works across all sections. One unified system, not a patchwork.

## Typography

**Font stack**: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

Zero web font downloads. San Francisco on Mac, Segoe UI on Windows. Neutral, invisible, modern. The most "bearblog" choice — lets the writing speak.

**Hierarchy** (approximate — refine during implementation):
- Page titles: 22–28px, weight 600–700, tight letter-spacing (-0.02em)
- Section headings: 14px, uppercase, letter-spacing 0.05em, muted color, weight 600
- Body text: 15–16px, line-height 1.55–1.65
- Metadata (dates, authors): 13px, muted color
- Nav items: 14px, weight 500–600 for active

## Header

**Compact header with section navigation tabs.**

Structure:
- Top row: small avatar (36px circle) + "Harper Reed" (18px, weight 600)
- Below: horizontal tab bar with section links — Posts, Notes, Books, Links, Music, RSS
- Active tab: bold weight + 2px bottom border
- Inactive tabs: muted color
- Header has a bottom border separating it from content
- Header stays compact — it recedes, content leads

On mobile: tabs should wrap or scroll horizontally if needed.

## Homepage

**Posts-first with photo strip and compact widgets.**

Layout (top to bottom):
1. **Posts feed** — Latest 3–5 posts in feed format (title, date, summary excerpt). Each post is an article block, not a list row. "More posts →" link at bottom.
2. **Photo strip** — Horizontal row of square thumbnails (120px) pulled from notes with image resources. Overflow hidden, no scrollbar. "More →" link. These are snapshots, not hero images.
3. **Compact widgets** — Three-column grid of small boxes:
   - **Reading**: 2–3 recent books (title + author)
   - **Notes**: 2 recent note excerpts (truncated)
   - **Links**: 2 recent links (title + domain)
   - Each widget has its section label and a "More →" link
4. Remove the current intro paragraph from `_index.md` content (the header already identifies the site)

On mobile: widgets stack to single column. Photo strip stays horizontal (natural swipe gesture).

## Section Pages

**Two rendering modes based on content type:**

### Feed Mode (Posts, Notes)
- Each item is an `<article>` block with title, date, and content preview/excerpt
- Posts: title (20px, weight 600) + date + summary (15px, muted)
- Notes: full text content inline (current behavior, refined styling), with date and tags
- Paginated
- Consistent class names across both

### Dense Row Mode (Books, Links, Music)
- Each item is a single row: date (80px fixed width, muted) + title (weight 500) + metadata (author/domain/artist, muted)
- Rows separated by subtle borders
- Paginated (20 per page, current behavior)
- Consistent class names and structure across all three
- **Grid toggle**: Books and music sections include a toggle to switch to the existing grid view (cover art cards). The grid view is the alternate, not the default.

### Unified patterns
- All sections use the same date format (from site config, not hardcoded)
- All sections use the same pagination partial
- Filter headings use a single shared class
- Posts section gets pagination (currently missing)

## Theme System

**Trim from 25 to ~5 curated themes.**

Keep:
1. **Default** (light/dark) — refined for the new layout. Better contrast, clearer hierarchy.
2. **Nature** — earthy greens
3. **Sunset** — warm pinks/oranges
4. **Nordic** — cool blues
5. **Terminal** — green-on-dark, hacker energy (fits the engineer identity)

Remove: dark, ocean, desert, autumn, cyber, academia, myspace, halloween, neon, electric, cyberpunk, volcano, midnight, lavender, coffee, mint, coral, synthwave, solarized, dracula, bubblegum (21 themes removed)

Each kept theme must:
- Have working light AND dark variants (via `prefers-color-scheme`)
- Look good with the new header, feed layout, photo strip, and widgets
- Be tested against all section page types before shipping

Remove all other themes. The 9-token color system stays — it works well. Just fewer theme definitions.

## Spacing & Breathing Room

- Increase max content width slightly if currently too narrow (test with real content)
- More vertical padding between sections on homepage (32px between major blocks)
- Post feed articles: 24–28px gap between items
- Dense rows: 10px vertical padding per row
- Widgets: 16px internal padding, 20px gap between widget boxes
- Header: 20px vertical padding, 14px gap between avatar row and nav tabs

## What This Does NOT Change

- Content structure (directories, frontmatter, markdown files)
- Hugo module system or theme inheritance model
- Build/deploy pipeline
- Content automation tools
- RSS feeds or sitemap structure
- Agent readiness files (.well-known/*)
- Existing grid view templates (kept as alternate views)
- The 9 semantic color token architecture

## Implementation Scope

Files likely touched:
- `layouts/index.html` — new homepage layout
- `layouts/post/list.html` — add pagination, feed-style rendering
- `layouts/notes/list.html` — standardize styling to match posts feed mode
- `layouts/books/list.html` — standardize to dense row pattern
- `layouts/links/list.html` — standardize to dense row pattern
- `layouts/music/list.html` — standardize to dense row pattern
- `layouts/partials/header.html` or equivalent — new compact header with tabs
- `assets/css/themes.css` — trim to 5 themes
- Various CSS files — typography hierarchy, spacing, widget styles, photo strip
- `content/_index.md` — simplify or remove intro text

Files NOT touched:
- Single page templates (post detail, book detail, etc.) — out of scope for this refresh
- Content files — no frontmatter changes needed
- Python tools — no changes
- Config files — minimal changes if any
