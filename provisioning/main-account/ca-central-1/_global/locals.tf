locals {
  tag_prefix                         = "k8s-the-hard-way-"
  vpc_ipv4_cidr_block                = "10.0.0.0/16"
  bastion_subnet_ipv4_cidr_block     = "10.0.1.0/24"
  k8s_cluster_subnet_ipv4_cidr_block = "10.0.2.0/24"
  ssh_port                           = 22
  tcp_protocol                       = "tcp"
  anywhere_ip_v4                     = "0.0.0.0/0"
  bastion_component                  = "bastion"
  k8s_worker_node_component          = "k8s-worker-node"
  k8s_control_plane_component        = "k8s-control-plane"
}
