#!/bin/bash
 
set -e

print_usage() {
    echo "Usage: $(basename $0) <provision|create|destroy>"
    exit 1
}

if [ -z "$1" ]; then
    print_usage
fi

build_provisioning_docker_image() {
    docker build -t base:local -f Dockerfile.base .
    pushd provisioning
    docker build -t cdktf:local -f Dockerfile .
    popd
}

run_cdktf() {
    docker run \
        --rm \
        -it \
        -v ./provisioning/app:/home/cdktf/app \
        -v ~/.ssh/id_rsa.pub:/home/cdktf/.ssh/id_rsa.pub:ro \
        -v ~/.aws:/home/cdktf/.aws:ro \
        cdktf:local \
            $1
}

provision() {
    build_provisioning_docker_image
    run_cdktf "all-tests"
    run_cdktf "deploy"
}

build_configuration_docker_image() {
    docker build -t base:local -f Dockerfile.base .
    pushd configuration
    docker build -t ansible:local -f Dockerfile .
    popd
}

run_ansible() {
    docker run \
	    --rm \
	    -it \
	    -v ./configuration/inventory:/home/ansible/inventory \
	    -v ./configuration/playbooks:/home/ansible/playbooks \
	    -v ~/.ssh/id_rsa:/home/ansible/.ssh/id_rsa:ro \
	    -v ~/.aws:/home/ansible/.aws:ro \
	    ansible:local \
		    $1
}

create() {
    build_configuration_docker_image
    run_ansible "create-cluster"
}

destroy() {
    build_provisioning_docker_image
    run_cdktf "destroy"
}

case "$1" in
    provision)
        provision
        ;;
    create)
        create
        ;;
    destroy)
        destroy
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
