# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Harper Reed's Blog - Hugo Development Guide

## Build & Server Commands
- Build: `hugo`
- Serve locally: `hugo serve --buildDrafts --buildFuture` 
- Production build: `hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info`
- Dev with metrics: `hugo server --disableFastRender --navigateToChanged --templateMetrics --watch --forceSyncStatic`
- Update modules: `hugo mod clean --all && hugo mod get -u ./... && hugo mod tidy`

## Python Tools
- Always use `uv run` instead of `python` for running Python scripts
- Run book fetcher: `uv run tools/grab_read_books.py`
- Run link fetcher: `uv run tools/grab_starred_links.py`
- Run micro posts: `uv run tools/grab_micro_posts_fixed.py`
  - Check archive for missing posts: `uv run tools/grab_micro_posts_fixed.py --check-archive`
  - Enable verbose logging: `uv run tools/grab_micro_posts_fixed.py --verbose`
- Run notes deduplicator: `uv run tools/deduplicate_notes.py --notes-dir content/notes --dry-run` (remove `--dry-run` to actually delete duplicates)
- Run micro.blog book sync: `uv run tools/push_books_to_microblog.py`
- Backfill all books: `uv run tools/push_books_to_microblog.py --backfill --limit 50`
- Export books as CSV (with read dates): `uv run tools/push_books_to_microblog.py --csv-export books_for_microblog.csv`

## Multilingual Support
- Supported languages: English (en, default), Spanish (es), Japanese (ja), Korean (ko), and Chinese (zh)
- One content tree: translations are suffix files next to the English original (`content/_index.es.md`, `content/post/<slug>/index.ja.md`) — there are no per-language content directories
- Each language has a translation file in `i18n/<lang>.yaml`; every key must exist in all five files (parity is enforced)
- i18n guardrail: `make check-i18n` runs the checker tests plus `tools/check_i18n.py` (key parity, phantom/dead keys, duplicate ids, language scoping in shortcodes) — run it after touching `i18n/` or templates that call `i18n`
- Placeholder convention: keys with `%s`/`%d` values are called `{{ printf (i18n "key") arg }}`; keys with `{{ . }}` values are called `{{ i18n "key" arg }}` — match the key's value style
- Books, music, links, and notes content exists only on the en site; templates that surface them on translated sites must query `hugo.Sites.Default.RegularPages` (plain `.Pages`/`site.RegularPages` are language-scoped and come back empty)
- To add a new language:
  1. Add language configuration to `config/_default/languages.toml` (include `label` — the switcher shows it)
  2. Add translation file `i18n/<lang_code>.yaml` with every key (copy en.yaml and translate; `make check-i18n` verifies parity)
  3. Add `config/_default/menu.<lang_code>.toml`
  4. Create translated content as suffix files, starting with `content/_index.<lang_code>.md`

## Architecture Overview

### Content Organization
- **Posts**: Long-form content in `/content/posts/`
- **Notes**: Micro-posts in `/content/notes/` (automated from JSON feeds)
- **Links**: Curated links in `/content/links/` (automated from RSS)
- **Books**: Reading list in `/content/books/` (Goodreads integration)
- **Music**: Spotify tracks in `/content/music/`

### Theme System
- Built on `hugo-bearcub` theme with extensive customizations
- Theme variations available: autumn, cyber, academia, etc.
- CSS organized in modular architecture with root color variables

### Content Automation
- Python tools in `/tools/` directory use AI-powered processing (OpenAI integration)
- Registry system prevents duplicate content processing
- Disk caching for API responses and content hashing
- All tools require `uv run` prefix for execution

### CI/CD Integration
- GitHub Actions run automated content updates every 10 minutes
- Netlify deployment with comprehensive security headers
- Multi-level caching strategy for build optimization

## Development Workflow

### Working with Content
- All content uses YAML frontmatter with ISO 8601 date format
- Content files use kebab-case naming
- Images are automatically optimized and processed

### Testing Changes
- Use development server with metrics: `hugo server --disableFastRender --navigateToChanged --templateMetrics --watch --forceSyncStatic`
- Check for duplicate notes before publishing: `uv run tools/deduplicate_notes.py --notes-dir content/notes --dry-run`

### Module Management
- Hugo uses module system for dependency management
- Update all modules: `hugo mod clean --all && hugo mod get -u ./... && hugo mod tidy`

## Code Style Guidelines
- Use standard Go templates for Hugo layouts
- Python: Follow PEP 8 style guide
- Error handling: Use proper logging with levels (info/debug/error)
- File naming: Use kebab-case for content files 
- Date format: ISO 8601 (YYYY-MM-DD) for frontmatter dates
- YAML frontmatter required for all content
- Import order: standard library first, then third-party, then local modules