# Makefile
.PHONY: small-tests medium-tests all-tests deploy

PROVISIONING_SCRIPT = ./provisioning.sh

small-tests:
	@echo "Running small tests"
	cd app; find . -name "*_small_tests.py" | xargs pipenv run pytest -x

medium-tests:
	@echo "Running medium tests"
	cd app; find . -name "*_medium_tests.py" | xargs pipenv run pytest -x

all-tests: small-tests medium-tests

deploy:
	@bash $(PROVISIONING_SCRIPT) deploy 

destroy:
	@bash $(PROVISIONING_SCRIPT) destroy 

