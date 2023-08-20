# import pytest
from cdktf import Testing
from main import MyStack


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestMain:
    app = Testing.app()
    stack = MyStack(app, "k8s_cluster_from_scratch")
    fullSynthesized = Testing.full_synth(stack)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
