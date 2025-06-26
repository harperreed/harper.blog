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

## Multilingual Support
- Supported languages: English (en), Spanish (es), Japanese (ja), and Korean (ko)
- Content directories:
  - English: `content/`
  - Spanish: `content.es/`
  - Japanese: `content.ja/`
  - Korean: `content.ko/`
- Each language has its own translation file in the `i18n/` directory
- To add a new language:
  1. Add language configuration to `config/_default/languages.toml`
  2. Create content directory: `content.<lang_code>/`
  3. Add translation file: `i18n/<lang_code>.yaml`
  4. Create translated content starting with `_index.md`

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