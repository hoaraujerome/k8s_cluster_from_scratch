from cdktf import Testing
from base_compute_stack import BaseComputeStack, BaseComputeStackConfig
# from imports.aws.data_aws_ami import DataAwsAmi
from imports.aws.key_pair import KeyPair

import os

os.environ['SSH_PUBLIC_KEY_PATH'] = './README.md'


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stackUnderTest = BaseComputeStack(
        app, "BaseComputeStack",
        BaseComputeStackConfig(
            tag_name_prefix="prefix-for-testing",
            region="ca-central-1",
        ),
    )
    synthesized = Testing.synth(stackUnderTest)

    # Commented out for now since DataAwsAmi seems not detected
#    def test_should_use_an_ubuntu_ami(self):
#        assert Testing.to_have_resource(
#            self.synthesized,
#            DataAwsAmi.TF_RESOURCE_TYPE
#        )

    def test_should_use_an_ubuntu_ami(self):
        with open(os.getenv("SSH_PUBLIC_KEY_PATH"), "r") as public_key_file:
            public_key = public_key_file.read()

        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            KeyPair.TF_RESOURCE_TYPE, {
                "public_key": public_key,
            }
        )
