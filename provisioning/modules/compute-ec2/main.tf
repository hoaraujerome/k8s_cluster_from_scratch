locals {
  ami_ubuntu_prefix_name       = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-arm64-server-*"
  ami_hardware_virtual_machine = "hvm"
  # https://ubuntu.com/server/docs/cloud-images/amazon-ec2
  ami_canonical_aws_owner_id = "099720109477"
  ec2_instance_type          = "t4g.small"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = [local.ami_ubuntu_prefix_name]
  }

  filter {
    name   = "virtualization-type"
    values = [local.ami_hardware_virtual_machine]
  }

  owners = [local.ami_canonical_aws_owner_id]
}

resource "aws_instance" "this" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = local.ec2_instance_type
  subnet_id                   = var.subnet_id
  associate_public_ip_address = var.associate_public_ip_address
  vpc_security_group_ids      = var.security_group_ids
  key_name                    = var.key_pair_name

  root_block_device {
    encrypted = true
  }

  metadata_options {
    http_tokens = "required"
  }

  tags = var.tags
}
