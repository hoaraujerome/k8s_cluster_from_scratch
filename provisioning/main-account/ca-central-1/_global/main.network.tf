module "vpc" {
  source = "../../../modules/network-vpc"

  tag_prefix          = local.tag_prefix
  vpc_ipv4_cidr_block = local.vpc_ipv4_cidr_block
  subnets = {
    "bastion" = {
      name            = local.bastion_component
      ipv4_cidr_block = local.bastion_subnet_ipv4_cidr_block
    }
    "k8s-cluster" = {
      name            = "k8s-cluster"
      ipv4_cidr_block = local.k8s_cluster_subnet_ipv4_cidr_block
    }
  }
}

module "internet-gateway" {
  source = "../../../modules/network-internetgateway"

  vpc_id     = module.vpc.vpc_id
  tag_prefix = local.tag_prefix
}

module "internet-gateway-route-table" {
  source = "../../../modules/network-routetable-all-traffic"

  vpc_id       = module.vpc.vpc_id
  subnet_id    = module.vpc.subnet_ids_by_name["${local.tag_prefix}bastion-subnet"]
  gateway_id   = module.internet-gateway.id
  gateway_type = "igw"
  tag_prefix   = local.tag_prefix
}

module "nat-gateway" {
  source = "../../../modules/network-natgateway"

  subnet_id  = module.vpc.subnet_ids_by_name["${local.tag_prefix}bastion-subnet"]
  tag_prefix = local.tag_prefix

  depends_on = [module.internet-gateway]
}

module "nat-gateway-route-table" {
  source = "../../../modules/network-routetable-all-traffic"

  vpc_id       = module.vpc.vpc_id
  subnet_id    = module.vpc.subnet_ids_by_name["${local.tag_prefix}k8s-cluster-subnet"]
  gateway_id   = module.nat-gateway.id
  gateway_type = "nat"
  tag_prefix   = local.tag_prefix
}
