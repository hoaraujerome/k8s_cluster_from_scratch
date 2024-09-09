#!/bin/bash

# jq will ensure that the values are properly quoted
# and escaped for consumption by the shell.
eval "$(jq -r '@sh "BASTION_DNS=\(.bastion_public_dns) PRIVATE_SERVER_DNS=\(.private_server_dns)"')"

# Placeholder for whatever data-fetching logic this script implements
STATUS="nok"

# Test HTTPS outbound
VALIDATION_COMMAND="curl -s -o /dev/null https://www.google.com"

./ssh-server.sh ${PRIVATE_SERVER_DNS} ${BASTION_DNS} "${VALIDATION_COMMAND}"

if [ $? -eq 0 ]; then
  STATUS="ok"
fi

# Safely produce a JSON object containing the result value.
# jq will ensure that the value is properly quoted
# and escaped to produce a valid JSON string.
jq -n --arg status "${STATUS}" '{"health":$status}'
