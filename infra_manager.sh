#!/bin/bash
 
set -e

print_usage() {
    echo "Usage: $(basename $0) <deploy|destroy>"
    exit 1
}

if [ -z "$1" ]; then
    print_usage
fi

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

# TODO commmon code with destroy
# TODO build cdk:local 
deploy() {
    run_cdktf "deploy"
}

case "$1" in
    deploy)
        deploy
        ;;
    destroy)
        run_cdktf "destroy"
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
