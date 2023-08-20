#!/usr/bin/env python
from constructs import Construct
from cdktf import App, Token, TerraformStack
from imports.aws.provider import AwsProvider
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation

TAG_NAME_PREFIX = "k8s-from-scratch-"


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
                "Name": f"{TAG_NAME_PREFIX}vpc"
            }
        )

        """
        Private subnets to create a range of IP addresses that we can allocate
        to our instances which do not allow external access (unless through a
        proxy or load balancer): used for both the control plane controllers
        as well as our worker instances
        """
        aws_private_subnet = Subnet(
            self,
            "private-subnet",
            cidr_block="10.0.1.0/24",
            tags={
                "Name": f"{TAG_NAME_PREFIX}private-subnet"
            },
            vpc_id=Token.as_string(aws_vpc_main.id)
        )
        """
        Instances need some way to connect and communicate with the internet
        since we are on a private network. So we need to provision a gateway
        we can use to proxy our traffic through
        """
        aws_internet_gateway = InternetGateway(
            self,
            "internet-gateway",
            tags={
                "Name": f"{TAG_NAME_PREFIX}internet-gateway"
            },
            vpc_id=Token.as_string(aws_vpc_main.id)
        )

        aws_route_table = RouteTable(
            self,
            "route-table",
            route=[
                {
                    "cidrBlock": "0.0.0.0/0",
                    "gatewayId": Token.as_string(aws_internet_gateway.id)
                }
            ],
            tags={
                "Name": f"{TAG_NAME_PREFIX}route-table"
            },
            vpc_id=Token.as_string(aws_vpc_main.id)
        )

        RouteTableAssociation(
            self,
            "route-table-association",
            route_table_id=Token.as_string(aws_route_table.id),
            subnet_id=Token.as_string(aws_private_subnet.id)
        )


app = App()
MyStack(app, "k8s_cluster_from_scratch")

app.synth()
