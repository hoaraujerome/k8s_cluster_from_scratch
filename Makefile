# Makefile
.PHONY: small-tests medium-tests all-tests

small-tests:
	@echo "Running small tests"
	@find . -name "*_small_tests.py" | xargs pipenv run pytest -x

medium-tests:
	@echo "Running medium tests"
	@find . -name "*_medium_tests.py" | xargs pipenv run pytest -x

all-tests: small-tests medium-tests

