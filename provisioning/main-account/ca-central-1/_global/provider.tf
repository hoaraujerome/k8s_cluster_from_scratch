terraform {
  required_version = "~> 1.8.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.53.0"
    }

    external = {
      source  = "hashicorp/external"
      version = "2.3.3"
    }
  }
}
