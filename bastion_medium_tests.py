from cdktf import Testing
from bastion_stack import BastionStack, BastionStackConfig
import os


os.environ['MY_IP_ADDRESS'] = '1.1.1.1/32'


# The tests below are example tests, you can find more information at
# https://cdk.tf/testing
class TestApplication:
    app = Testing.app()
    stack = BastionStack(
        app, "BastionStack",
        BastionStackConfig(
            tag_name_prefix="tag-name-prefix-for-testing",
            region="region-for-testing",
            vpc_id="vpc-id-for-testing",
            subnet_id="subnet-id-for-testing",
            ami_id="ami-id-for-testing",
            ssh_key_name="ssh-key-name-for-testing",
        )
    )
    fullSynthesized = Testing.full_synth(stack)

    def test_to_be_valid_terraform_pass(self):
        assert Testing.to_be_valid_terraform(self.fullSynthesized)
