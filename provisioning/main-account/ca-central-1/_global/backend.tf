terraform {
  backend "s3" {
    bucket = "kubernetes-the-hard-way-on-aws"
    key    = "tfstate/main-account/ca-central-1/_global"
    region = "ca-central-1"
  }
}
