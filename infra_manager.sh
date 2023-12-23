#!/bin/bash
 
set -e

print_usage() {
    echo "Usage: $(basename $0) <deploy|destroy>"
    exit 1
}

if [ -z "$1" ]; then
    print_usage
fi

build_cdktf_docker_image() {
    pushd provisioning
    docker build -t cdktf:local -f Dockerfile .
    popd
}

run_cdktf() {
    docker run \
        --rm \
        -it \
        -v ./provisioning/app:/home/cdktf/app \
        -v ./provisioning/cdktf.out:/home/cdktf/cdktf.out \
        -v ~/.ssh/id_rsa.pub:/home/cdktf/.ssh/id_rsa.pub:ro \
        -v ~/.aws:/home/cdktf/.aws:ro \
        cdktf:local \
            $1
}

manage_infrastructure() {
    build_cdktf_docker_image
    run_cdktf $1
}

case "$1" in
    deploy)
        manage_infrastructure "deploy"
        ;;
    destroy)
        manage_infrastructure "destroy"
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
