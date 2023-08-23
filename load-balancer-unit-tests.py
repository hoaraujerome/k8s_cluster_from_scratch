from cdktf import Testing
from networking_stack import NetworkingStack
from load_balancer_stack import LoadBalancerStack
from imports.aws.lb import Lb


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    networking_stack = NetworkingStack(app, "NetworkingStack")
    stackUnderTest = LoadBalancerStack(
        app,
        "LoadBalancerStack",
        networking_stack)
    synthesized = Testing.synth(stackUnderTest)

    def test_should_contain_load_balancer(self):
        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            Lb.TF_RESOURCE_TYPE, {
                "internal": True,
                "load_balancer_type": "network",
            }
        )
