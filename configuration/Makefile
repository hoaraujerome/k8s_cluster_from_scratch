# Makefile
.PHONY: create-cluster

CONFIGURATION_SCRIPT = ./configuration.sh

create-cluster:
	@bash $(CONFIGURATION_SCRIPT) create_cluster

troubleshoot:
	@bash $(CONFIGURATION_SCRIPT) troubleshoot && exec /bin/bash
