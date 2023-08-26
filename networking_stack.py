#!/usr/bin/env python
from constructs import Construct
from cdktf import Token
from base_stack import BaseStack
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation
from imports.aws.security_group import SecurityGroup

ALL_IP_ADDRESSES = "0.0.0.0/0"
ALL_PORT = 0
SSH_PORT = 22
K8S_API_PORT = 6443
PROTOCOL_ALL = "-1"


class NetworkingStackConfig():
    tag_name_prefix: str
    region: str

    def __init__(self, tag_name_prefix: str, region: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region


class NetworkingStack(BaseStack):
    tag_name_prefix: str
    region: str
    aws_private_subnet: Subnet

    def __init__(self, scope: Construct, id: str,
                 config: NetworkingStackConfig):
        super().__init__(scope, id, config.region)

        self.region = config.region
        self.tag_name_prefix = config.tag_name_prefix

        aws_vpc_main = self._create_vpc()
        """
        Private subnets to create a range of IP addresses that we can allocate
        to our instances which do not allow external access (unless through a
        proxy or load balancer): used for both the control plane controllers
        as well as our worker instances
        """
        self.aws_private_subnet = self._create_private_subnet(aws_vpc_main.id)
        """
        Instances need some way to connect and communicate with the internet
        since we are on a private network. So we need to provision a gateway
        we can use to proxy our traffic through
        """
        aws_internet_gateway = self._create_internet_subway(aws_vpc_main.id)
        """
        Set up a route table to route traffic from the private subnet to the
        Internet Gateway
        """
        self._create_route_table(
            aws_vpc_main.id,
            aws_internet_gateway.id,
            self.aws_private_subnet.id)
        """
        Allow traffic for the VPC
        """
        self._create_security_group(aws_vpc_main.id, aws_vpc_main.cidr_block)

    def _create_vpc(self):
        return Vpc(
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
                "Name": f"{self.tag_name_prefix}vpc"
            }
        )

    def _create_private_subnet(self, vpc_id):
        return Subnet(
            self,
            "private-subnet",
            cidr_block="10.0.1.0/24",
            tags={
                "Name": f"{self.tag_name_prefix}private-subnet"
            },
            vpc_id=vpc_id
        )

    def _create_internet_subway(self, vpc_id):
        return InternetGateway(
            self,
            "internet-gateway",
            tags={
                "Name": f"{self.tag_name_prefix}internet-gateway"
            },
            vpc_id=vpc_id
        )

    def _create_route_table(self, vpc_id, internet_gateway_id, subnet_id):
        aws_route_table = RouteTable(
            self,
            "route-table",
            route=[
                {
                    "cidrBlock": ALL_IP_ADDRESSES,
                    "gatewayId": internet_gateway_id
                }
            ],
            tags={
                "Name": f"{self.tag_name_prefix}route-table"
            },
            vpc_id=Token.as_string(vpc_id)
        )

        RouteTableAssociation(
            self,
            "route-table-association",
            route_table_id=aws_route_table.id,
            subnet_id=subnet_id
        )

    def _create_security_group(self, vpc_id, vpc_cidr):
        SecurityGroup(
            self,
            "security-group",
            ingress=[
                {
                    "description": "Allow all inbound traffic from VPC",
                    "fromPort": ALL_PORT,
                    "toPort": ALL_PORT,
                    "protocol": PROTOCOL_ALL,
                    "cidrBlocks": [vpc_cidr],
                },
                {
                    "description": "Allow SSH inbound traffic",
                    "fromPort": SSH_PORT,
                    "toPort": SSH_PORT,
                    "protocol": "tcp",
                    "cidrBlocks": [ALL_IP_ADDRESSES],
                },
                {
                    "description": "Allow K8S API inbound traffic",
                    "fromPort": K8S_API_PORT,
                    "toPort": K8S_API_PORT,
                    "protocol": "tcp",
                    "cidrBlocks": [ALL_IP_ADDRESSES],
                },
            ],
            tags={
                "Name": f"{self.tag_name_prefix}security-group"
            },
            vpc_id=vpc_id
        )
