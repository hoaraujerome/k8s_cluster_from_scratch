#!/usr/bin/env python

import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from constructs import Construct  # noqa: E402
from cdktf import TerraformStack  # noqa: E402
from imports.aws.provider import AwsProvider  # noqa: E402


class BaseStack(TerraformStack):
    def __init__(self, scope: Construct, id: str,
                 region: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region=region)
