# Makefile
.PHONY: unit-tests run-integration-tests all-tests

unit-tests:
	echo "Running unit tests"
	find . -name "*-unit-tests.py" | xargs pipenv run pytest

run-integration-tests:
	echo "Running integration tests"
	find . -name "*-integration-tests.py" | xargs pipenv run pytest

all-tests: unit-tests run-integration-tests
 
