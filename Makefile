build:
	hugo
deploy: build
	git commit -m "updated" -a
	git push
serve:
	hugo serve
