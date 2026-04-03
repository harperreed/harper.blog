# Book Re-Read Tracking

**Date:** 2026-04-02
**Status:** Design approved, pending implementation

## Problem

The book tracking system creates separate entries for books read multiple times (via date-prefixed directories), but there is no linking between re-reads. A reader visiting a book page has no way to know the book was read before or after another instance.

## Goals

- Detect re-reads during ingestion by matching Goodreads book IDs
- Link re-read entries to each other via frontmatter
- Display a subtle note on each book page pointing to other reads of the same book
- Preserve existing behavior: re-reads count normally in stats, appear independently in timeline/grid

## Non-Goals

- Consolidating re-reads into a single canonical page
- Changing stats shortcodes (book-count, page-count)
- Changing list/grid views
- Adding re-read badges or prominent UI elements

## Approach: Frontmatter Linking

Chosen over data-file registry (unnecessary complexity) and Hugo taxonomy (overkill for a subtle display feature).

## Data Model

Two new frontmatter fields on book entries:

```yaml
goodreads_work_id: '50700'
related_reads:
  - 2006-11-26-old-man-s-war-old-man-s-war-1
```

- `goodreads_work_id`: The Goodreads "work" ID that groups editions of the same book. The regular book `id` differs between editions (51964 vs 640474 for Old Man's War), but `work.id` (50700 for both) is the canonical identifier. Already present in cached `data/books/*.yaml` files as `work.id`; needs to be surfaced to frontmatter.
- `related_reads`: List of directory slugs for other reads of the same book. Bidirectional — when a re-read is created, both old and new entries list each other.

## Ingestion Changes (grab_read_books.py)

Three modifications to the existing script:

1. **Surface `goodreads_id` to frontmatter** — When building post metadata via `create_post_metadata()`, include the Goodreads book ID from the cached data YAML.

2. **Detect re-reads** — Before creating a new book entry, scan existing `content/books/*/index.md` files for a matching `goodreads_id`. If a match is found, this is a re-read.

3. **Cross-link on detection** — When a re-read is detected:
   - Create the new entry normally (different date prefix = different directory, existing behavior).
   - Add `related_reads` to the new entry's frontmatter, listing the existing entry's slug.
   - Update the existing entry's frontmatter to append the new entry's slug to its `related_reads`.

The script never skips re-reads. The only new behavior is the cross-linking.

## Hugo Template Changes

### Single Book Page (layouts/books/single.html)

Add a block that checks for `related_reads` in frontmatter. If present:

- Loop through slugs, resolve each via `.GetPage (printf "/books/%s" $slug)`
- Compare dates to determine relationship direction:
  - If the related page is **older**: render *"Previously read in [Month Year]"* with a link
  - If the related page is **newer**: render *"Re-read in [Month Year]"* with a link
- Placement: subtle, below the existing book metadata

### No Changes

- **List view** (`layouts/books/list.html`) — entries appear independently in timeline
- **Grid view** (`layouts/books/books-grid.html`) — entries appear independently in grid
- **Stats shortcodes** (`book-count.html`, `page-count.html`) — re-reads count normally
- **RSS feed** (`layouts/books/rss.xml`) — no re-read annotation needed

## Backfill

One-time standalone script to:

1. Add `goodreads_id` to all existing book entries by reading from their corresponding `data/books/*.yaml` cache files
2. Detect the existing Old Man's War duplicate and add `related_reads` to both entries:
   - `2006-11-26-old-man-s-war-old-man-s-war-1/index.md`
   - `2025-02-25-old-man-s-war-old-man-s-war-1/index.md`

This is a standalone script (not a flag on the main tool) since it's a one-time operation.

## Files Modified

- `tools/grab_read_books.py` — ingestion changes (detect re-reads, cross-link, surface goodreads_id)
- `layouts/books/single.html` — template change (render re-read note)
- `tools/backfill_goodreads_ids.py` — new one-time script
- `content/books/*/index.md` — frontmatter updates via backfill

## Testing

- Verify backfill correctly populates `goodreads_id` across all 829 book entries
- Verify Old Man's War entries are cross-linked after backfill
- Verify `hugo serve` renders the re-read note on both Old Man's War pages
- Verify the ingestion script detects and cross-links a simulated re-read
- Verify existing book entries without re-reads are unaffected (no `related_reads` field)
