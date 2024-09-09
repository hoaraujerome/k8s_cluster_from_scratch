#!/bin/bash

set -e

ROOT_MODULE_BASE_PATH="code/main-account/ca-central-1"
GLOBAL_ROOT_MODULE_PATH="${ROOT_MODULE_BASE_PATH}/_global"
BETA_ROOT_MODULE_PATH="${ROOT_MODULE_BASE_PATH}/beta"

print_usage() {
  echo "Usage: $(basename $0) <plan|deploy|destroy>"
  exit 1
}

setup_terraform_vars_for_global() {
  export TF_VAR_my_ipv4_address=$(/home/terraform/get_public_ip_as_cidr.sh)
  export TF_VAR_ssh_public_key_path="/home/terraform/.ssh/id_rsa.pub"
}

run_linter() {
  pushd code
  echo "$(basename $0) - run_linter - terraform fmt"
  terraform fmt -check -recursive
  popd
}

run_tests() {
  if [ -n "${SKIP_TESTS}" ]; then
    echo "Skipping tests"
    return
  fi

  for dir in code/modules/*/; do
    echo "Testing module: ${dir}"
    pushd "$dir"
    terraform init
    terraform test
    popd
  done
}

unset_terraform_vars_for_global() {
  unset TF_VAR_my_ipv4_address
  unset TF_VAR_ssh_public_key_path
}

terraform_plan() {
  terraform init -backend=false
  terraform validate
  terraform init
  terraform plan
}

plan() {
  run_linter
  run_tests

  pushd "${GLOBAL_ROOT_MODULE_PATH}"
  setup_terraform_vars_for_global
  terraform_plan
  unset_terraform_vars_for_global
  popd

  #  pushd "${BETA_ROOT_MODULE_PATH}"
  #  terraform_plan
  #  popd
}

terraform_apply() {
  terraform init
  terraform plan -out=tfplan
  terraform apply "tfplan"
}

deploy() {
  run_linter
  run_tests

  pushd "${GLOBAL_ROOT_MODULE_PATH}"
  setup_terraform_vars_for_global
  terraform_apply
  unset_terraform_vars_for_global
  popd

  #  pushd "${BETA_ROOT_MODULE_PATH}"
  #  terraform_apply
  #  popd
}

terraform_destroy() {
  terraform init
  terraform destroy
}

destroy() {
  pushd "${GLOBAL_ROOT_MODULE_PATH}"
  setup_terraform_vars_for_global
  terraform_destroy
  unset_terraform_vars_for_global
  popd

  #  pushd "${BETA_ROOT_MODULE_PATH}"
  #  terraform_destroy
  #  popd
}

if [ -z "$1" ]; then
  print_usage
fi

case "$1" in
plan)
  plan
  ;;
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
