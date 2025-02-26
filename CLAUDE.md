# CLAUDE.md - Guide for Harper Reed's Blog

## Build & Server Commands
- Build: `hugo`
- Serve locally: `hugo serve --buildDrafts --buildFuture` 
- Production build: `hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info`
- Dev with metrics: `hugo server --disableFastRender --navigateToChanged --templateMetrics --watch --forceSyncStatic`
- Update modules: `hugo mod clean --all && hugo mod get -u ./... && hugo mod tidy`

## Python Tools
- Run book fetcher: `python tools/grab_read_books.py`
- Run link fetcher: `python tools/grab_starred_links.py`
- Run micro posts: `python tools/grab_micro_posts.py`

## Code Style Guidelines
- Use standard Go templates for Hugo layouts
- Python: Follow PEP 8 style guide
- Error handling: Use proper logging with levels (info/debug/error)
- File naming: Use kebab-case for content files 
- Date format: ISO 8601 (YYYY-MM-DD) for frontmatter dates
- YAML frontmatter required for all content
- Import order: standard library first, then third-party, then local modules