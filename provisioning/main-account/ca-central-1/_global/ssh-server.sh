#!/bin/bash

# Check if the server DNS is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <server_dns> [bastion_dns] [validation_command]"
  exit 1
fi

SERVER_DNS=${1}
BASTION_DNS=${2}
VALIDATION_COMMAND=${3:-"exit"} # Default validation command is 'exit'

SSH_OPTIONS="-i ~/.ssh/id_rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -o ConnectTimeout=5"

# If BASTION_DNS is provided, test SSH connection to the server through the bastion
if [ -n "${BASTION_DNS}" ]; then
  # Use ProxyCommand to ensure SSH options apply to both bastion and target server
  ssh ${SSH_OPTIONS} -o ProxyCommand="ssh ${SSH_OPTIONS} -W %h:%p ubuntu@${BASTION_DNS}" ubuntu@${SERVER_DNS} "${VALIDATION_COMMAND}"
else
  # Test SSH connection directly to the server
  ssh ${SSH_OPTIONS} ubuntu@${SERVER_DNS} "${VALIDATION_COMMAND}"
fi

# Return the exit status of the SSH command
exit $?
