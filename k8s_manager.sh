#!/bin/bash

set -e

print_usage() {
  echo "Usage: $(basename $0) <plan|provision|create|destroy>"
  exit 1
}

if [ -z "$1" ]; then
  print_usage
fi

run_scans() {
  docker run \
    --rm \
    -it \
    -v "$(pwd)/provisioning:/src:ro" \
    -w /src \
    aquasec/trivy \
    fs \
    --scanners secret,misconfig \
    . \
    --exit-code 1
}

build_terraform_docker_image() {
  pushd provisioning
  docker build -t terraform:local -f Dockerfile .
  popd
}

run_terraform() {
  docker run \
    --rm \
    -it \
    -v ~/.aws:/home/terraform/.aws:ro \
    -v ~/.ssh/id_rsa_k8s_the_hard_way.pub:/home/terraform/.ssh/id_rsa.pub:ro \
    -v ~/.ssh/id_rsa_k8s_the_hard_way:/home/terraform/.ssh/id_rsa:ro \
    -v "$(pwd)/provisioning/main-account:/home/terraform/code/main-account" \
    -v "$(pwd)/provisioning/modules:/home/terraform/code/modules" \
    -v "$(pwd)/provisioning/tests:/home/terraform/code/tests" \
    -e AWS_PROFILE=k8s_the_hard_way \
    -e SKIP_TESTS=${SKIP_TESTS} \
    terraform:local \
    $1
}

plan() {
  run_scans
  build_terraform_docker_image
  run_terraform "plan"
}

provision() {
  run_scans
  build_terraform_docker_image
  run_terraform "deploy"
}

build_configuration_docker_image() {
  pushd configuration
  docker build -t ansible:local -f Dockerfile .
  popd
}

run_ansible() {
  docker run \
    --rm \
    -it \
    -v "$(pwd)/configuration/inventory:/home/ansible/inventory" \
    -v "$(pwd)/configuration/playbooks:/home/ansible/playbooks" \
    -v ~/.ssh/id_rsa_k8s_the_hard_way:/home/ansible/.ssh/id_rsa:ro \
    -v ~/.aws:/home/ansible/.aws:ro \
    -v ~/.k8s_the_hard_way:/home/ansible/.k8s \
    -e AWS_PROFILE=k8s_the_hard_way \
    ansible:local \
    $1
}

create() {
  build_configuration_docker_image
  run_ansible "create-cluster"
}

destroy() {
  build_terraform_docker_image
  run_terraform "destroy"
}

case "$1" in
plan)
  plan
  ;;
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
