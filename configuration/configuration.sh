#!/bin/bash
 
set -e

print_usage() {
    echo "Usage: $(basename $0) <create_cluster>"
    exit 1
}

# get_public_ip() {
#     local ip=$(curl -s ifconfig.me)
# 
#     if [[ -z "$ip" ]]; then
#         echo "$(basename $0) - get_public_ip - could not retrieve public IP address" >&2
#         exit 1
#     fi
# 
#     echo "$ip"
# }
# 
# to_cidr() {
#     echo "$1/32"
# }
# 
# prepare_cdktf_environment() {
#     export MY_IP_ADDRESS=$(to_cidr $(get_public_ip))
#     export SSH_PUBLIC_KEY_PATH="/home/cdktf/.ssh/id_rsa.pub"
# }
generate_ssh_config_file() {
    local ansible_inventory=$(ansible-inventory --list)

    local hostname=$(echo $ansible_inventory | jq -r '.bastion.hosts[0]')
    # Create the SSH config file
    cat << EOF > ~/.ssh_config
Host bastion
  User ubuntu
  HostName $hostname
EOF

     hostnames=$(echo $ansible_inventory | jq -r '.k8s_master_node.hosts[]')
     for hostname in $hostnames; do
       echo "Host $hostname" >> ~/.ssh_config
       echo "  ProxyJump bastion" >> ~/.ssh_config
     done

     mv ~/.ssh_config ~/.ssh/config
}

create_cluster() {
    generate_ssh_config_file
    ansible-playbook playbooks/k8s-init-master-nodes.yaml
}

# destroy() {
#     prepare_cdktf_environment
#     npx cdktf destroy NetworkingStack BaseComputeStack BastionStack KubernetesNodesStack
# }

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
