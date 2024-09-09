module "k8s-cluster-security-group" {
  source = "../../../modules/network-securitygroup"

  vpc_id     = module.vpc.vpc_id
  name       = "k8s-cluster"
  tag_prefix = local.tag_prefix
}

module "k8s-cluster-security-group-rules" {
  source = "../../../modules/network-securitygrouprules"

  security_group_id = module.k8s-cluster-security-group.security_group_id
  rules = {
    "ssh-inbound-traffic" = {
      description                  = "Allow SSH inbound traffic from bastion"
      direction                    = "inbound"
      from_port                    = local.ssh_port
      to_port                      = local.ssh_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.bastion-security-group.security_group_id
    }
    "https-outbound-traffic" = {
      description = "Allow HTTPS outbound traffic"
      direction   = "outbound"
      from_port   = local.https_port
      to_port     = local.https_port
      ip_protocol = local.tcp_protocol
      cidr_ipv4   = local.anywhere_ip_v4
    }
  }
  tag_prefix = local.tag_prefix
}

module "k8s-cluster-ec2" {
  source = "../../../modules/compute-ec2"

  subnet_id                   = module.vpc.subnet_ids_by_name["${local.tag_prefix}k8s-cluster-subnet"]
  security_group_ids          = [module.k8s-cluster-security-group.security_group_id]
  key_pair_name               = module.bastion-ssh-public-key.key_pair_name
  associate_public_ip_address = false
  tags = {
    Name = "${local.tag_prefix}k8s-control-plane"
    Role = "k8s-control-plane"
  }
}

check "k8s_cluster_health_check" {
  data "external" "ssh_control_plane" {
    program = ["bash", "${path.module}/ssh-private-server.sh"]

    query = {
      bastion_public_dns = module.bastion-ec2.instance_public_dns
      private_server_dns = module.k8s-cluster-ec2.instance_private_dns
    }
  }

  assert {
    condition     = data.external.ssh_control_plane.result["health"] == "ok"
    error_message = "unable to validate SSH ${module.k8s-cluster-ec2.instance_private_dns}"
  }
}
