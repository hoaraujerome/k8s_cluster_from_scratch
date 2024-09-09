variable "vpc_id" {
  type     = string
  nullable = false
}

variable "name" {
  type     = string
  nullable = false
}

variable "tag_prefix" {
  type    = string
  default = ""
}
