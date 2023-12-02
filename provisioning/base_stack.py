#!/usr/bin/env python
from constructs import Construct
from cdktf import TerraformStack
from imports.aws.provider import AwsProvider


class BaseStack(TerraformStack):
    def __init__(self, scope: Construct, id: str,
                 region: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region=region)
