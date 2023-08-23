from cdktf import Testing
from networking_stack import NetworkingStack
from load_balancer_stack import LoadBalancerStack


# TODO make it work
# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    networking_stack = NetworkingStack(app, "NetworkingStack")
    stackUnderTest = LoadBalancerStack(
        app,
        "LoadBalancerStack",
        networking_stack)
    fullSynthesized = Testing.full_synth(stackUnderTest)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
