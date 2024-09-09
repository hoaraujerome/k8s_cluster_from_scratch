terraform {
  backend "s3" {
    bucket = "kubernetes-the-hard-way-on-aws"
    key    = "tfstate/main-account/ca-central-1/beta"
    region = "ca-central-1"
  }
}
