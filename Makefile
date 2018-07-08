build:
	hugo
deploy: build
	git add docs/*
	git commit -m "Updated docs" docs
	git push
serve:
	hugo serve
