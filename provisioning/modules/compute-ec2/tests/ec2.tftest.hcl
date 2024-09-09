run "setup_aws_provider" {
  module {
    source = "../../tests/setup/aws_provider"
  }
}

run "check_ec2" {
  variables {
    subnet_id                   = "subnetid"
    security_group_ids          = ["sg1", "sg2"]
    key_pair_name               = "keypairname"
    associate_public_ip_address = true
    tags = {
      Name = "prefix-ec2"
      Role = "myrole"
    }
  }

  command = plan

  assert {
    condition     = aws_instance.this.instance_type == "t4g.small"
    error_message = "Invalid instance type"
  }

  assert {
    condition     = aws_instance.this.subnet_id == var.subnet_id
    error_message = "Invalid instance subnet id"
  }

  assert {
    condition     = aws_instance.this.vpc_security_group_ids == toset(var.security_group_ids)
    error_message = "Invalid instance VPC SG ids"
  }

  assert {
    condition     = aws_instance.this.key_name == var.key_pair_name
    error_message = "Invalid instance key name"
  }

  assert {
    condition     = aws_instance.this.associate_public_ip_address == var.associate_public_ip_address
    error_message = "Invalid instance associate public IP address"
  }

  assert {
    condition     = aws_instance.this.root_block_device[0].encrypted == true
    error_message = "Invalid instance encrypted for the root block device"
  }

  assert {
    condition     = aws_instance.this.metadata_options[0].http_tokens == "required"
    error_message = "Invalid instance http tokens for metadata options"
  }

  assert {
    condition     = aws_instance.this.ami == data.aws_ami.ubuntu.id
    error_message = "Invalid instance ami id"
  }

  assert {
    condition     = aws_instance.this.tags == var.tags
    error_message = "Invalid instance tags"
  }

  assert {
    condition     = data.aws_ami.ubuntu.most_recent == true
    error_message = "Invalid ami most recent"
  }

  assert {
    condition     = startswith(data.aws_ami.ubuntu.name, "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-arm64-server") == true
    error_message = "Invalid ami name"
  }

  assert {
    # For some reasons, the == seems not working between 2 lists here
    # condition     = data.aws_ami.ubuntu.owners == ["099720109477"]
    condition     = alltrue([for owner in data.aws_ami.ubuntu.owners : contains(["099720109477"], owner)])
    error_message = "Invalid ami owners"
  }
}

run "setup_networking" {
  module {
    source = "./tests/setup/networking"
  }
}

run "create_ec2" {
  variables {
    subnet_id                   = run.setup_networking.subnet_id
    associate_public_ip_address = false
  }

  command = apply

  assert {
    condition     = aws_instance.this.associate_public_ip_address == var.associate_public_ip_address
    error_message = "Invalid instance associate public IP address"
  }

  assert {
    condition     = output.instance_public_dns != null
    error_message = "Invalid instance public dns"
  }

  assert {
    condition     = output.instance_private_dns != null
    error_message = "Invalid instance private dns"
  }
}
