#!/bin/bash

set -e

ip=$(curl -s ifconfig.me)

if [[ -z "$ip" ]]; then
  echo "$(basename $0) - could not retrieve public IP address" >&2
  exit 1
fi

echo "$ip/32"
