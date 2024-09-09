run "setup_provider" {
  module {
    source = "../../tests/setup/aws_provider"
  }
}

run "check_security_group" {
  variables {
    vpc_id     = "vpcid"
    name       = "test"
    tag_prefix = "prefix-"
  }

  command = plan

  assert {
    condition     = aws_security_group.this.name == var.name
    error_message = "Invalid security group name"
  }

  assert {
    condition     = aws_security_group.this.description == "${var.name} VPC security group"
    error_message = "Invalid security group description"
  }

  assert {
    condition     = aws_security_group.this.vpc_id == var.vpc_id
    error_message = "Invalid security group VPC id"
  }

  assert {
    condition     = aws_security_group.this.tags["Name"] == "prefix-test-security-group"
    error_message = "Invalid security group name tag"
  }
}

run "setup_networking" {
  module {
    source = "./tests/setup/networking"
  }
}

run "create_security_group" {
  variables {
    vpc_id     = run.setup_networking.vpc_id
    name       = "test"
    tag_prefix = "prefix-"
  }

  command = apply

  assert {
    condition     = output.security_group_id == aws_security_group.this.id
    error_message = "Invalid ouput security group id"
  }
}
