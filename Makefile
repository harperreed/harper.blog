build:
	jekyll build
gitlog:
	git log --pretty=format:'- **%ad**: %s' --date=short >_includes/gitlog.md
	git commit -m "Updated gitlog" _includes/gitlog.md
deploy: build
	s3_website push
serve:
	jekyll serve -w --incremental
