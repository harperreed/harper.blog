.PHONY: build serve getmodules check check-i18n check-contrast tools-test preview dev prod_build prod_build_verbose gitlog

# Run every local verification: tools tests, i18n hygiene, contrast sweep
check: tools-test check-i18n check-contrast

# Run the Python tools test suite
tools-test:
	cd tools && uv run ruff check . && uv run pytest -q

# Build the Hugo site
build:
	hugo

# Serve the Hugo site locally with drafts and future posts
serve:
	hugo serve --buildDrafts --buildFuture

# Clean, update, and tidy Hugo modules
getmodules:
	hugo mod clean --all && hugo mod get -u ./... && hugo mod tidy

# Check i18n hygiene: key parity, phantom/dead keys, language-scoping regressions
check-i18n:
	cd tools && uv run pytest test_check_i18n.py -q && uv run check_i18n.py

# Check WCAG AA contrast across every theme palette (light + dark cascade)
check-contrast:
	cd tools && uv run check_contrast.py

# Preview the site with production settings
preview:
	hugo server --disableFastRender --navigateToChanged --watch --forceSyncStatic -e production --minify

# Development build with template metrics
dev:
	hugo server --buildDrafts --buildFuture --disableFastRender --navigateToChanged --templateMetrics --templateMetricsHints --watch --forceSyncStatic

prod_build_verbose:
	hugo --cleanDestinationDir --templateMetrics --templateMetricsHints --minify --forceSyncStatic --gc --logLevel info

	
	
# Build the site with production settings and optimizations
prod_build:
	hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info

gitlog:
	printf '# Git log\n\n' > gitlog.md
	git log --pretty=format:'- **%ad**: %s' --date=short | \
		grep -v 'Auto update spotify tracks' | \
		grep -v 'Auto update micro posts with registry' | \
		grep -v 'Auto update micro posts' >> gitlog.md
	sed -i '' '/Updated gitlog/d' "gitlog.md"
	git commit -m "Updated gitlog" gitlog.md
