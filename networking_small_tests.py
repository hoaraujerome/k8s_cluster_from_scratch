from cdktf import Testing
from networking_stack import (
  NetworkingStack, NetworkingStackConfig, VPC_CIDR_BLOCK, PUBLIC_CIDR_BLOCK
)
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation
# from imports.aws.security_group import SecurityGroup


ALL_IP_ADDRESSES = "0.0.0.0/0"


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stack = NetworkingStack(
        app, "NetworkingStack",
        NetworkingStackConfig(
            tag_name_prefix="prefix-for-testing",
        ),
    )
    synthesized = Testing.synth(stack)

    def test_should_contain_vpc(self):
        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            Vpc.TF_RESOURCE_TYPE, {
                "cidr_block": VPC_CIDR_BLOCK,
                "enable_dns_support": True,
                "enable_dns_hostnames": True,
            })

    def test_should_contain_public_subnet(self):
        assert Testing.to_have_resource(
            self.synthesized,
            InternetGateway.TF_RESOURCE_TYPE
        )

        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            Subnet.TF_RESOURCE_TYPE, {
                "cidr_block": PUBLIC_CIDR_BLOCK,
            }
        )

        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            RouteTable.TF_RESOURCE_TYPE, {
                "route": [
                    {
                        "cidr_block": ALL_IP_ADDRESSES,
                    },
                ]
            }
        )

        assert Testing.to_have_resource(
            self.synthesized,
            RouteTableAssociation.TF_RESOURCE_TYPE
        )

#    def test_should_contain_private_subnet(self):
#        assert Testing.to_have_resource_with_properties(
#            self.synthesized,
#            Subnet.TF_RESOURCE_TYPE, {
#                "cidr_block": "10.0.1.0/24",
#            }
#        )

# def test_should_contain_route_table(self):
#     assert Testing.to_have_resource_with_properties(
#         self.synthesized,
#         RouteTable.TF_RESOURCE_TYPE, {
#             "route": [
#                 {
#                     "cidr_block": "0.0.0.0/0",
#                 },
#             ]
#         }
#     )

# def test_should_contain_route_table_association(self):
#     assert Testing.to_have_resource(
#         self.synthesized,
#         RouteTableAssociation.TF_RESOURCE_TYPE
#     )

#    def test_should_contain_security_group(self):
#        assert Testing.to_have_resource_with_properties(
#            self.synthesized,
#            SecurityGroup.TF_RESOURCE_TYPE, {
#                "ingress": [
#                    {
#                        "from_port": 0,
#                        "to_port": 0,
#                        "protocol": "-1",
#                    },
#                    {
#                        "from_port": 22,
#                        "to_port": 22,
#                        "protocol": "tcp",
#                        "cidr_blocks": [
#                            "0.0.0.0/0"
#                        ]
#                    },
#                    {
#                        "from_port": 6443,
#                        "to_port": 6443,
#                        "protocol": "tcp",
#                        "cidr_blocks": [
#                            "0.0.0.0/0"
#                        ]
#                    },
#                ],
#            }
#        )
