#!/usr/bin/env python
from constructs import Construct
from cdktf import Token
from base_stack import BaseStack
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation
# from imports.aws.security_group import SecurityGroup
from imports.aws.nat_gateway import NatGateway
from imports.aws.eip import Eip


AWS_REGION = "ca-central-1"
# ALL_PORT = 0
# K8S_API_PORT = 6443
# PROTOCOL_ALL = "-1"
ALL_IP_ADDRESSES = "0.0.0.0/0"
# https://cidr.xyz
VPC_CIDR_BLOCK = "10.0.0.0/16"
PUBLIC_CIDR_BLOCK = "10.0.2.0/24"


class NetworkingStackConfig():
    tag_name_prefix: str
    region: str

    def __init__(self, tag_name_prefix: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = AWS_REGION


class NetworkingStack(BaseStack):
    region: str
    aws_vpc: Vpc
    aws_public_subnet: Subnet
    aws_private_subnet: Subnet

    def __init__(self, scope: Construct, id: str,
                 config: NetworkingStackConfig):
        super().__init__(scope, id, config.region)

        self.aws_vpc = self._create_vpc(config.tag_name_prefix)

        self.aws_public_subnet = self._create_public_subnet(
            config.tag_name_prefix
        )

#        self.aws_private_subnet = self._create_subnet(
#            "private_subnet",
#            aws_vpc_main.id,
#            "10.0.1.0/24"
#        )
#
#
#        aws_eip = self._create_elastic_ip(aws_internet_gateway)
#
#        self._create_nat_gateway(aws_public_subnet.id, aws_eip.id)

        """
        Set up a route table to route traffic from the private subnet to the
        Internet Gateway
        """
        # self._create_route_table(
        #     aws_vpc_main.id,
        #     aws_internet_gateway.id,
        #     self.aws_private_subnet.id)
        """
        Allow traffic for the VPC
        """
#        self._create_security_group(aws_vpc_main.id, aws_vpc_main.cidr_block)

    def _create_vpc(self, tag_name_prefix):
        return Vpc(
            self,
            "vpc",
            cidr_block=VPC_CIDR_BLOCK,
            # Instances in the VPC can use Amazon-provided DNS server
            enable_dns_support=True,
            # Instances in the VPC will be assigned public DNS hostnames
            # if they have public IP addresses
            enable_dns_hostnames=True,
            tags={
                "Name": f"{tag_name_prefix}vpc"
            }
        )

    def _create_internet_gateway(self, tag_name_prefix):
        return InternetGateway(
            self,
            "internet-gateway",
            tags={
                "Name": f"{tag_name_prefix}internet-gateway"
            },
            vpc_id=self.aws_vpc.id
        )

    def _create_subnet(self, subnet_id, cidr_block, tag_name_prefix):
        return Subnet(
            self,
            subnet_id,
            cidr_block=cidr_block,
            tags={
                "Name": f"{tag_name_prefix}{subnet_id}"
            },
            vpc_id=self.aws_vpc.id
        )

    def _associate_subnet_to_internet_gateway(self,
                                              subnet_id,
                                              internet_gateway_id,
                                              tag_name_prefix):
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
                "Name": f"{tag_name_prefix}route-table"
            },
            vpc_id=Token.as_string(self.aws_vpc.id)
        )

        RouteTableAssociation(
            self,
            "route-table-association",
            route_table_id=aws_route_table.id,
            subnet_id=subnet_id
        )

    def _create_public_subnet(self, tag_name_prefix):
        internet_gateway = self._create_internet_gateway(
            tag_name_prefix
        )

        subnet = self._create_subnet(
            "public_subnet",
            PUBLIC_CIDR_BLOCK,
            tag_name_prefix
        )

        self._associate_subnet_to_internet_gateway(
            subnet.id,
            internet_gateway.id,
            tag_name_prefix
        )

        return subnet

    # TODO to be deleted
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

    def _create_elastic_ip(self, internet_gateway):
        return Eip(
            self,
            "eip",
            domain="vpc",
            tags={
                "Name": f"{self.tag_name_prefix}eip"
            },
            depends_on=[internet_gateway]
        )

    def _create_nat_gateway(self, subnet_id, eip_id):
        return NatGateway(
            self,
            "nat-gateway",
            connectivity_type="public",
            allocation_id=eip_id,
            subnet_id=subnet_id,
            tags={
                "Name": f"{self.tag_name_prefix}nat-gateway"
            }
        )

    # TODO to be deleted
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

#    def _create_security_group(self, vpc_id, vpc_cidr):
#        SecurityGroup(
#            self,
#            "security-group",
#            ingress=[
#                {
#                    "description": "Allow all inbound traffic from VPC",
#                    "fromPort": ALL_PORT,
#                    "toPort": ALL_PORT,
#                    "protocol": PROTOCOL_ALL,
#                    "cidrBlocks": [vpc_cidr],
#                },
#                {
#                    "description": "Allow SSH inbound traffic",
#                    "fromPort": SSH_PORT,
#                    "toPort": SSH_PORT,
#                    "protocol": "tcp",
#                    "cidrBlocks": [ALL_IP_ADDRESSES],
#                },
#                {
#                    "description": "Allow K8S API inbound traffic",
#                    "fromPort": K8S_API_PORT,
#                    "toPort": K8S_API_PORT,
#                    "protocol": "tcp",
#                    "cidrBlocks": [ALL_IP_ADDRESSES],
#                },
#            ],
#            tags={
#                "Name": f"{self.tag_name_prefix}security-group"
#            },
#            vpc_id=vpc_id
#        )
