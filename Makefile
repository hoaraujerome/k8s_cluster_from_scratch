# Makefile
.PHONY: unit-tests run-integration-tests all-tests

unit-tests:
	echo "Running unit tests"
	pipenv run pytest ./main-unit-tests.py

run-integration-tests:
	echo "Running integration tests"
	pipenv run pytest ./main-integration-tests.py

all-tests: unit-tests run-integration-tests
 
