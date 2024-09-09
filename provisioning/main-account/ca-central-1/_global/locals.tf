locals {
  tag_prefix                         = "k8s-the-hard-way-"
  vpc_ipv4_cidr_block                = "10.0.0.0/16"
  bastion_subnet_ipv4_cidr_block     = "10.0.1.0/24"
  k8s_cluster_subnet_ipv4_cidr_block = "10.0.2.0/24"
  ssh_port                           = 22
  https_port                         = 443
  tcp_protocol                       = "tcp"
  anywhere_ip_v4                     = "0.0.0.0/0"
}
