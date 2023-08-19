#!/usr/bin/env python
from constructs import Construct
from cdktf import App, Token, TerraformStack
from imports.aws.provider import AwsProvider
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        AwsProvider(self, "AWS", region="ca-central-1")

        aws_vpc_main = Vpc(
            self,
            "vpc",
            # https://cidr.xyz
            cidr_block="10.0.0.0/16",
            # Instances in the VPC can use Amazon-provided DNS server
            enable_dns_support=True,
            # Instances in the VPC will be assigned public DNS hostnames
            # if they have public IP addresses
            enable_dns_hostnames=True,
            tags={
                "Name": "k8s-from-scratch-vpc"
            }
        )

        """
        Private subnets to create a range of IP addresses that we can allocate
        to our instances which do not allow external access (unless through a
        proxy or load balancer): used for both the control plane controllers
        as well as our worker instances
        """
        Subnet(
            self,
            "private-subnet",
            cidr_block="10.0.1.0/24",
            tags={
                "Name": "k8s-from-scratch-private-subnet"
            },
            vpc_id=Token.as_string(aws_vpc_main.id)
        )


app = App()
MyStack(app, "k8s_cluster_from_scratch")

app.synth()
