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
    echo "$1/32"
}

prepare_cdktf_environment() {
    export MY_IP_ADDRESS=$(to_cidr $(get_public_ip))
    export SSH_PUBLIC_KEY_PATH="/home/cdktf/.ssh/id_rsa.pub"
}

deploy() {
    prepare_cdktf_environment
    npx cdktf deploy NetworkingStack BaseComputeStack BastionStack KubernetesNodesStack
}

destroy() {
    prepare_cdktf_environment
    npx cdktf destroy NetworkingStack BaseComputeStack BastionStack KubernetesNodesStack
}

if [ -z "$1" ]; then
    print_usage
fi

case "$1" in
    deploy)
        deploy
        ;;
    destroy)
        destroy
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
