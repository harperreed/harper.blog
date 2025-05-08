# CLAUDE.md - Guide for Harper Reed's Blog

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

## Code Style Guidelines
- Use standard Go templates for Hugo layouts
- Python: Follow PEP 8 style guide
- Error handling: Use proper logging with levels (info/debug/error)
- File naming: Use kebab-case for content files 
- Date format: ISO 8601 (YYYY-MM-DD) for frontmatter dates
- YAML frontmatter required for all content
- Import order: standard library first, then third-party, then local modules