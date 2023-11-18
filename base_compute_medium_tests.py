from cdktf import Testing
from base_compute_stack import BaseComputeStack, BaseComputeStackConfig

import os

os.environ['SSH_PUBLIC_KEY_PATH'] = './README.md'


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stack = BaseComputeStack(
        app, "BaseComputeStack",
        BaseComputeStackConfig(
            tag_name_prefix="prefix-for-testing",
            region="region-for-testing",
        ),
    )
    fullSynthesized = Testing.full_synth(stack)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
