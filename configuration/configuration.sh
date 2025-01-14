#!/bin/bash

set -e

print_usage() {
  echo "Usage: $(basename $0) <create_cluster|troubleshoot>"
  exit 1
}

generate_ssh_config_file() {
  local ansible_inventory=$(ansible-inventory --list)

  local hostname=$(echo $ansible_inventory | jq -r '.bastion.hosts[0]')
  # Create the SSH config file
  cat <<EOF >~/.ssh_config
Host bastion
  User ubuntu
  HostName $hostname
  StrictHostKeyChecking no
EOF

  hostnames=$(echo $ansible_inventory | jq -r '.k8s_control_plane.hosts[]')
  for hostname in $hostnames; do
    cat <<EOF >>~/.ssh_config
Host $hostname
  ProxyJump bastion
Host k8s_control_plane
  HostName $hostname
  User ubuntu
  ProxyJump bastion
  StrictHostKeyChecking no
EOF
  done

  hostnames=$(echo $ansible_inventory | jq -r '.k8s_worker_node.hosts[]')
  for hostname in $hostnames; do
    cat <<EOF >>~/.ssh_config
Host $hostname
  ProxyJump bastion
Host k8s_worker_node
  HostName $hostname
  User ubuntu
  ProxyJump bastion
  StrictHostKeyChecking no
EOF
  done

  mv ~/.ssh_config ~/.ssh/config
}

create_cluster() {
  generate_ssh_config_file
  ansible-playbook playbooks/k8s-init-control-plane.yaml
  ansible-playbook playbooks/k8s-init-worker-node.yaml
  ansible-playbook playbooks/k8s-smoke-tests.yaml
}

troubleshoot() {
  generate_ssh_config_file
}

if [ -z "$1" ]; then
  print_usage
fi

case "$1" in
create_cluster)
  create_cluster
  ;;
troubleshoot)
  troubleshoot
  ;;
*)
  echo "$(basename $0) - invalid option: $1" >&2
  print_usage
  ;;
esac
