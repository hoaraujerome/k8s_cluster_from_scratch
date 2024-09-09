output "instance_public_dns" {
  value = aws_instance.this.public_dns
}

output "instance_private_dns" {
  value = aws_instance.this.private_dns
}
