# import pytest
from cdktf import Testing
from networking_stack import NetworkingStack


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stack = NetworkingStack(app, "NetworkingStack")
    fullSynthesized = Testing.full_synth(stack)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
