from cdktf import Testing
from bastion_stack import (
  BastionStack, BastionStackConfig
)
from imports.aws.security_group import SecurityGroup
from imports.aws.vpc_security_group_ingress_rule \
    import VpcSecurityGroupIngressRule
from imports.aws.instance import Instance
import os


SSH_PORT = 22
AMI_TEST_ID = "ami-0e0e0e0e0e0e0e0e"
SUBNET_TEST_ID = "XXXXXXXXXXXXXXXXXXXXXXX"
SSH_KEY_TEST_NAME = "ssh-key-name-for-testing"


os.environ['MY_IP_ADDRESS'] = '1.1.1.1/32'


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stack = BastionStack(
        app, "BastionStack",
        BastionStackConfig(
            tag_name_prefix="tag-name-prefix-for-testing",
            region="region-for-testing",
            vpc_id="vpc-id-for-testing",
            subnet_id=SUBNET_TEST_ID,
            ami_id=AMI_TEST_ID,
            ssh_key_name=SSH_KEY_TEST_NAME,
        )
    )
    synthesized = Testing.synth(stack)

    def test_should_contain_security_group(self):
        assert Testing.to_have_resource(
            self.synthesized,
            SecurityGroup.TF_RESOURCE_TYPE
        )

        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            VpcSecurityGroupIngressRule.TF_RESOURCE_TYPE, {
                "from_port": SSH_PORT,
                "to_port": SSH_PORT,
                "ip_protocol": "tcp",
                "cidr_ipv4": os.environ['MY_IP_ADDRESS']
            })

    def test_should_contain_instance(self):
        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            Instance.TF_RESOURCE_TYPE, {
                "instance_type": "t4g.small",
                "ami": AMI_TEST_ID,
                "key_name": SSH_KEY_TEST_NAME,
                "subnet_id": SUBNET_TEST_ID,
                "associate_public_ip_address": True,
            }
        )
