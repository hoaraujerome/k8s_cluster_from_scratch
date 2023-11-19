from cdktf import Testing
from base_compute_stack import BaseComputeStack, BaseComputeStackConfig
from imports.aws.data_aws_ami import DataAwsAmi
from imports.aws.key_pair import KeyPair

import os

CANONICAL_AWS_OWNER_ID = "099720109477"

os.environ['SSH_PUBLIC_KEY_PATH'] = './README.md'


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stackUnderTest = BaseComputeStack(
        app, "BaseComputeStack",
        BaseComputeStackConfig(
            tag_name_prefix="prefix-for-testing",
            region="region-for-testing",
        ),
    )
    synthesized = Testing.synth(stackUnderTest)

    def test_should_use_an_ubuntu_ami(self):
        ami_filter = [
            {
                "name": "name",
                "values": [
                    "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-arm64-server-*"
                ]
            },
            {
                "name": "virtualization-type",
                "values": ["hvm"]
            }
        ]

        assert Testing.to_have_data_source_with_properties(
            self.synthesized,
            DataAwsAmi.TF_RESOURCE_TYPE, {
                "most_recent": True,
                "owners": [CANONICAL_AWS_OWNER_ID],
                "filter": ami_filter,
            }
        )

    def test_should_contain_key_pair_with_given_public_key(self):
        with open(os.getenv("SSH_PUBLIC_KEY_PATH"), "r") as public_key_file:
            public_key = public_key_file.read()

        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            KeyPair.TF_RESOURCE_TYPE, {
                "public_key": public_key,
            }
        )
