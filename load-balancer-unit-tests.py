from cdktf import Testing
from load_balancer_stack import LoadBalancerStack, LoadBalancerStackConfig
from imports.aws.lb import Lb


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stackUnderTest = LoadBalancerStack(
        app, "LoadBalancerStack",
        LoadBalancerStackConfig(
            tag_name_prefix="prefix-for-testing",
            region="ca-central-1",
            subnet_id="subnet-for-testing"
        ),
    )
    synthesized = Testing.synth(stackUnderTest)

    def test_should_contain_load_balancer(self):
        assert Testing.to_have_resource_with_properties(
            self.synthesized,
            Lb.TF_RESOURCE_TYPE, {
                "internal": True,
                "load_balancer_type": "network",
            }
        )
