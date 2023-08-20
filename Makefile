# Makefile

.PHONY: test

test:
	pipenv run pytest ./main-test.py
