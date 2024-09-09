module "beta-spoke-vpc" {
  source = "../../../modules/network-vpc"

  tag_prefix          = local.tag_prefix
  vpc_ipv4_cidr_block = local.vpc_ipv4_cidr_block
  subnets = {
    "k8s-cluster" = {
      name            = "k8s-cluster"
      ipv4_cidr_block = local.k8s_cluster_subnet_ipv4_cidr_block
    }
  }
}
