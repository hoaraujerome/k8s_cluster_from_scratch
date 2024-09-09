resource "aws_security_group" "this" {
  name        = var.name
  description = "${var.name} VPC security group"
  vpc_id      = var.vpc_id
  tags = {
    Name = "${var.tag_prefix}${var.name}-security-group"
  }
}
