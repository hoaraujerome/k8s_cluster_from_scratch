locals {
  k8s_api_port = 6443
}

module "k8s-security-groups" {
  source = "../../../modules/network-securitygroup"

  vpc_id     = module.vpc.vpc_id
  names      = [local.k8s_control_plane_component, local.k8s_worker_node_component]
  tag_prefix = local.tag_prefix
}

module "k8s-control-plane-security-group-rules" {
  source = "../../../modules/network-securitygrouprules"

  security_group_id = module.k8s-security-groups.security_group_id[local.k8s_control_plane_component]
  rules = {
    "ssh-inbound-traffic" = {
      description                  = "Allow SSH inbound traffic from bastion"
      direction                    = "inbound"
      from_port                    = local.ssh_port
      to_port                      = local.ssh_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.bastion-security-group.security_group_id[local.bastion_component]
    }
    "k8s-api-inbound-traffic" = {
      description                  = "Allow K8S API inbound traffic from worker node"
      direction                    = "inbound"
      from_port                    = local.k8s_api_port
      to_port                      = local.k8s_api_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.k8s-security-groups.security_group_id[local.k8s_worker_node_component]
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

module "k8s-worker-node-security-group-rules" {
  source = "../../../modules/network-securitygrouprules"

  security_group_id = module.k8s-security-groups.security_group_id[local.k8s_worker_node_component]
  rules = {
    "ssh-inbound-traffic" = {
      description                  = "Allow SSH inbound traffic from bastion"
      direction                    = "inbound"
      from_port                    = local.ssh_port
      to_port                      = local.ssh_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.bastion-security-group.security_group_id[local.bastion_component]
    }
    "https-outbound-traffic" = {
      description = "Allow HTTPS outbound traffic"
      direction   = "outbound"
      from_port   = local.https_port
      to_port     = local.https_port
      ip_protocol = local.tcp_protocol
      cidr_ipv4   = local.anywhere_ip_v4
    }
    "k8s-api-outbound-traffic" = {
      description                  = "Allow K8S API outbound traffic"
      direction                    = "outbound"
      from_port                    = local.k8s_api_port
      to_port                      = local.k8s_api_port
      ip_protocol                  = local.tcp_protocol
      referenced_security_group_id = module.k8s-security-groups.security_group_id[local.k8s_control_plane_component]
    }
  }
  tag_prefix = local.tag_prefix
}

module "k8s-cluster-ec2-control-plane" {
  source = "../../../modules/compute-ec2"

  subnet_id                   = module.vpc.subnet_ids_by_name["${local.tag_prefix}k8s-cluster-subnet"]
  security_group_ids          = [module.k8s-security-groups.security_group_id[local.k8s_control_plane_component]]
  key_pair_name               = module.bastion-ssh-public-key.key_pair_name
  associate_public_ip_address = false
  tags = {
    Name = "${local.tag_prefix}${local.k8s_control_plane_component}"
    Role = local.k8s_control_plane_component
  }
}

module "k8s-cluster-ec2-worker-node" {
  source = "../../../modules/compute-ec2"

  subnet_id                   = module.vpc.subnet_ids_by_name["${local.tag_prefix}k8s-cluster-subnet"]
  security_group_ids          = [module.k8s-security-groups.security_group_id[local.k8s_worker_node_component]]
  key_pair_name               = module.bastion-ssh-public-key.key_pair_name
  associate_public_ip_address = false
  tags = {
    Name = "${local.tag_prefix}${local.k8s_worker_node_component}"
    Role = local.k8s_worker_node_component
  }
}

check "k8s_cluster_control_plane_health_check" {
  data "external" "ssh_control_plane" {
    program = ["bash", "${path.module}/ssh-private-server.sh"]

    query = {
      bastion_public_dns = module.bastion-ec2.instance_public_dns
      private_server_dns = module.k8s-cluster-ec2-control-plane.instance_private_dns
    }
  }

  assert {
    condition     = data.external.ssh_control_plane.result["health"] == "ok"
    error_message = "unable to validate SSH ${module.k8s-cluster-ec2-control-plane.instance_private_dns}"
  }
}

check "k8s_cluster_worker_node_health_check" {
  data "external" "ssh_worker_node" {
    program = ["bash", "${path.module}/ssh-private-server.sh"]

    query = {
      bastion_public_dns = module.bastion-ec2.instance_public_dns
      private_server_dns = module.k8s-cluster-ec2-worker-node.instance_private_dns
    }
  }

  assert {
    condition     = data.external.ssh_worker_node.result["health"] == "ok"
    error_message = "unable to validate SSH ${module.k8s-cluster-ec2-worker-node.instance_private_dns}"
  }
}
