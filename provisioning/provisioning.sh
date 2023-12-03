#!/bin/bash

set -e

print_usage() {
    echo "Usage: $(basename $0) <deploy|destroy>"
    exit 1
}

get_public_ip() {
    local ip=$(curl -s ifconfig.me)

    if [[ -z "$ip" ]]; then
        echo "$(basename $0) - get_public_ip - could not retrieve public IP address" >&2
        exit 1
    fi

    echo "$ip"
}

to_cidr() {
    local ip=$1
    echo "$ip/32"
}

deploy() {
  local my_ip_address=$(to_cidr $(get_public_ip))
  export MY_IP_ADDRESS=$my_ip_address
  cd provisioning && cdktf deploy NetworkingStack BaseComputeStack BastionStack KubernetesNodesStack
}

if [ -z "$1" ]; then
    print_usage
fi

case "$1" in
    deploy)
        deploy
        ;;
    destroy)
        # Add your destruction code here
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
