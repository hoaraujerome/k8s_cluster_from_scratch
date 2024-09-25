#!/bin/bash

# set -x

AWS_PROFILE="k8s_the_hard_way_prereq"
AWS_CLI_TAG="2.16.5"
CURRENT_SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
USER_POLICY_FILENAME="user_policy.json"
KEY_FILE="$HOME/.ssh/id_rsa_k8s_the_hard_way"
K8S_CRYPTO_ASSETS_DIRECTORY="$HOME/.k8s_the_hard_way"

setup_ssh_key() {
  ssh-keygen -t rsa -b 2048 -f "$KEY_FILE" -N ""
}

setup_root_ca() {
  mkdir -p ${K8S_CRYPTO_ASSETS_DIRECTORY}

  openssl genrsa -out ${K8S_CRYPTO_ASSETS_DIRECTORY}/ca.key 4096

  openssl req -x509 -new -sha512 -noenc \
    -key ${K8S_CRYPTO_ASSETS_DIRECTORY}/ca.key -days 365 \
    -config ${CURRENT_SCRIPT_DIRECTORY}/ca.conf \
    -out ${K8S_CRYPTO_ASSETS_DIRECTORY}/ca.crt
}

setup_crypto_assets() {
  setup_ssh_key
  setup_root_ca
}

run_aws_command() {
  docker run \
    --rm \
    -it \
    -v ~/.aws:/root/.aws:ro \
    -v ${CURRENT_SCRIPT_DIRECTORY}/user_policy.json:/aws/${USER_POLICY_FILENAME}:ro \
    amazon/aws-cli:${AWS_CLI_TAG} \
    ${@} --profile ${AWS_PROFILE}
}

create_terraform_backend() {
  run_aws_command "s3 mb s3://kubernetes-the-hard-way-on-aws"
}

create_user() {
  user_name="k8s_the_hard_way"
  policy_name="${user_name}_policy"

  run_aws_command "iam" "create-user" "--user-name" "${user_name}"

  run_aws_command "iam create-policy" "--policy-name" "${policy_name}" "--policy-document" "file://${USER_POLICY_FILENAME}"
  output=$(run_aws_command "iam" "list-policies" "--query" "Policies[?PolicyName=='${policy_name}'].Arn" "--output" "json")
  policy_arn=$(echo "$output" | sed -n 's/.*"\(arn:aws:iam:[^"]*\)".*/\1/p')

  run_aws_command "iam" "attach-user-policy" "--policy-arn" "${policy_arn}" "--user-name" "${user_name}"
}

main() {
  setup_crypto_assets
  create_terraform_backend
  create_user
}

main
