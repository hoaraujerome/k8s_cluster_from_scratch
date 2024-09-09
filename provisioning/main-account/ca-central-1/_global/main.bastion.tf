module "bastion-security-group" {
  source = "../../../modules/network-securitygroup"

  vpc_id     = module.vpc.vpc_id
  name       = "bastion"
  tag_prefix = local.tag_prefix
}

module "bastion-security-group-rules" {
  source = "../../../modules/network-securitygrouprules"

  security_group_id = module.bastion-security-group.security_group_id
  rules = {
    "ssh-inbound-traffic" = {
      description = "Allow SSH inbound traffic"
      direction   = "inbound"
      from_port   = local.ssh_port
      to_port     = local.ssh_port
      ip_protocol = local.tcp_protocol
      cidr_ipv4   = var.my_ipv4_address
    }
    "ssh-outbound-traffic" = {
      description                  = "Allow SSH outbound traffic"
      direction                    = "outbound"
      from_port                    = local.ssh_port
      to_port                      = local.ssh_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.k8s-cluster-security-group.security_group_id
    }
  }
  tag_prefix = local.tag_prefix
}

module "bastion-ssh-public-key" {
  source = "../../../modules/compute-sshpublickey"

  public_key_path = var.ssh_public_key_path
  tag_prefix      = local.tag_prefix
}

module "bastion-ec2" {
  source = "../../../modules/compute-ec2"

  subnet_id                   = module.vpc.subnet_ids_by_name["${local.tag_prefix}bastion-subnet"]
  security_group_ids          = [module.bastion-security-group.security_group_id]
  key_pair_name               = module.bastion-ssh-public-key.key_pair_name
  associate_public_ip_address = true
  tags = {
    Name = "${local.tag_prefix}bastion"
    Role = "bastion"
  }
}

check "bastion_health_check" {
  data "external" "ssh_bastion" {
    program = ["bash", "${path.module}/ssh-bastion.sh"]

    query = {
      bastion_public_dns = module.bastion-ec2.instance_public_dns
    }
  }

  assert {
    condition     = data.external.ssh_bastion.result["health"] == "ok"
    error_message = "unable to validate SSH ${module.bastion-ec2.instance_public_dns}"
  }
}
