.PHONY: build
build:
	pipenv lock -r > requirements.txt
	sam build

start: build
	sam local start-lambda