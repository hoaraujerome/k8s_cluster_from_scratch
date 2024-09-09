run "setup_provider" {
  module {
    source = "../../tests/setup/aws_provider"
  }
}

run "check_vpc_with_no_subnet" {
  variables {
    vpc_ipv4_cidr_block = "1.1.1.0/28"
    tag_prefix          = "prefix-"
  }

  command = plan

  assert {
    condition     = aws_vpc.this.cidr_block == var.vpc_ipv4_cidr_block
    error_message = "Invalid VPC CIDR block"
  }

  assert {
    condition     = aws_vpc.this.enable_dns_support == true
    error_message = "Invalid VPC enable DNS support"
  }

  assert {
    condition     = aws_vpc.this.enable_dns_hostnames == true
    error_message = "Invalid VPC enable DNS hostnames"
  }

  assert {
    condition     = aws_vpc.this.tags["Name"] == "prefix-vpc"
    error_message = "Invalid VPC tag name"
  }

  assert {
    condition     = length(aws_subnet.this) == 0
    error_message = "Invalid subnet"
  }
}

run "check_vpc_with_one_subnet" {
  variables {
    vpc_ipv4_cidr_block = "1.1.1.0/28"
    subnets = {
      "bastion" = {
        name            = "bastion"
        ipv4_cidr_block = "10.1.1.0/24"
      }
    }
    tag_prefix = "px-"
  }

  command = plan

  assert {
    condition     = length(aws_subnet.this) == 1
    error_message = "Invalid subnet"
  }

  assert {
    condition     = aws_subnet.this["bastion"].cidr_block == var.subnets.bastion.ipv4_cidr_block
    error_message = "Invalid bastion subnet CIDR block"
  }

  assert {
    condition     = aws_subnet.this["bastion"].tags["Name"] == "px-${var.subnets.bastion.name}-subnet"
    error_message = "Invalid bastion subnet tag name"
  }
}

run "check_vpc_with_three_subnets" {
  variables {
    vpc_ipv4_cidr_block = "1.1.1.0/28"
    subnets = {
      "bastion" = {
        name            = "bastion"
        ipv4_cidr_block = "10.1.1.0/24"
      }
      "transit" = {
        name            = "transit"
        ipv4_cidr_block = "10.1.2.0/24"
      }
      "foo" = {
        name            = "foo"
        ipv4_cidr_block = "10.1.3.0/24"
      }
    }
    tag_prefix = "px-"
  }

  command = plan

  assert {
    condition     = length(aws_subnet.this) == 3
    error_message = "Invalid subnet"
  }

  assert {
    condition     = aws_subnet.this["bastion"].cidr_block == var.subnets.bastion.ipv4_cidr_block
    error_message = "Invalid bastion subnet CIDR block"
  }

  assert {
    condition     = aws_subnet.this["bastion"].tags["Name"] == "px-${var.subnets.bastion.name}-subnet"
    error_message = "Invalid bastion subnet tag name"
  }

  assert {
    condition     = aws_subnet.this["transit"].cidr_block == var.subnets.transit.ipv4_cidr_block
    error_message = "Invalid transit subnet CIDR block"
  }

  assert {
    condition     = aws_subnet.this["transit"].tags["Name"] == "px-${var.subnets.transit.name}-subnet"
    error_message = "Invalid transit subnet tag name"
  }

  assert {
    condition     = aws_subnet.this["foo"].cidr_block == var.subnets.foo.ipv4_cidr_block
    error_message = "Invalid foo subnet CIDR block"
  }

  assert {
    condition     = aws_subnet.this["foo"].tags["Name"] == "px-${var.subnets.foo.name}-subnet"
    error_message = "Invalid foo subnet tag name"
  }
}

run "create_vpc_with_no_subnet" {
  variables {
    vpc_ipv4_cidr_block = "10.1.0.0/16"
  }

  command = apply

  assert {
    condition     = output.vpc_id == aws_vpc.this.id
    error_message = "Invalid ouput VPC id"
  }

  assert {
    condition     = output.subnet_ids_by_name == {}
    error_message = "Invalid ouput subnets ids by name"
  }
}

run "create_vpc_with_three_subnets" {
  variables {
    vpc_ipv4_cidr_block = "10.1.0.0/16"
    subnets = {
      "bastion" = {
        name            = "bastion"
        ipv4_cidr_block = "10.1.1.0/24"
      }
      "transit" = {
        name            = "transit"
        ipv4_cidr_block = "10.1.2.0/24"
      }
      "foo" = {
        name            = "foo"
        ipv4_cidr_block = "10.1.3.0/24"
      }
    }
  }

  command = apply

  assert {
    condition     = aws_subnet.this["bastion"].vpc_id == aws_vpc.this.id
    error_message = "Invalid bastion subnet VPC id"
  }

  assert {
    condition     = output.subnet_ids_by_name["bastion-subnet"] == aws_subnet.this["bastion"].id
    error_message = "Invalid ouput bastion subnet id"
  }

  assert {
    condition     = output.subnet_ids_by_name["transit-subnet"] == aws_subnet.this["transit"].id
    error_message = "Invalid ouput transit subnet id"
  }
  assert {
    condition     = output.subnet_ids_by_name["foo-subnet"] == aws_subnet.this["foo"].id
    error_message = "Invalid ouput foo subnet id"
  }
}
