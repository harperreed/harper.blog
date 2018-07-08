build:
	hugo
deploy: build
	git commit -m "updated"
	git push
serve:
	hugo serve
