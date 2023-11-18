from cdktf import Testing
from base_stack import BaseStack
from imports.aws.provider import AwsProvider


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stackUnderTest = BaseStack(
        app, "BaseStack", "region-for-testing",
    )
    synthesized = Testing.synth(stackUnderTest)

    def test_should_use_aws(self):
        assert Testing.to_have_provider_with_properties(
            self.synthesized,
            AwsProvider.TF_RESOURCE_TYPE, {
                "region": "region-for-testing",
            }
        )
