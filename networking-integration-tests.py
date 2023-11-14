from cdktf import Testing
from networking_stack import NetworkingStack, NetworkingStackConfig


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
    fullSynthesized = Testing.full_synth(stack)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
