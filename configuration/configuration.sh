#!/bin/bash

set -e

print_usage() {
  echo "Usage: $(basename $0) <create_cluster>"
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
EOF

  hostnames=$(echo $ansible_inventory | jq -r '.k8s_control_plane.hosts[]')
  for hostname in $hostnames; do
    echo "Host $hostname" >>~/.ssh_config
    echo "  ProxyJump bastion" >>~/.ssh_config
  done

  mv ~/.ssh_config ~/.ssh/config
}

create_cluster() {
  generate_ssh_config_file
  ansible-playbook playbooks/k8s-init-control-plane.yaml
}

if [ -z "$1" ]; then
  print_usage
fi

case "$1" in
create_cluster)
  create_cluster
  ;;
*)
  echo "$(basename $0) - invalid option: $1" >&2
  print_usage
  ;;
esac
