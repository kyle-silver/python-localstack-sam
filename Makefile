build:
	pipenv lock -r > requirements.txt
	sam build