# Build the Hugo site
build:
	hugo

# Serve the Hugo site locally with drafts and future posts
serve:
	hugo serve --buildDrafts --buildFuture

# Clean, update, and tidy Hugo modules
getmodules:
	hugo mod clean --all && hugo mod get -u ./... && hugo mod tidy

# Preview the site with production settings
preview:
	hugo server --disableFastRender --navigateToChanged --templateMetrics --templateMetricsHints --watch --forceSyncStatic -e production --minify

# Build the site with production settings and optimizations
prod_build:
	hugo --gc --minify --templateMetrics --templateMetricsHints --forceSyncStatic
