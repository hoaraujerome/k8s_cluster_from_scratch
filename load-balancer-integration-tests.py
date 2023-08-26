from cdktf import Testing
from load_balancer_stack import LoadBalancerStack, LoadBalancerStackConfig


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stackUnderTest = LoadBalancerStack(
        app, "LoadBalancerStack",
        LoadBalancerStackConfig(
            tag_name_prefix="prefix-for-testing",
            region="region-for-testing",
            subnet_id="subnet-for-testing"
        ),
    )
    fullSynthesized = Testing.full_synth(stackUnderTest)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
