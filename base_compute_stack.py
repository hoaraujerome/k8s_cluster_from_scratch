#!/usr/bin/env python
from constructs import Construct
from base_stack import BaseStack
from imports.aws.data_aws_ami import DataAwsAmi
from imports.aws.key_pair import KeyPair
import os

# https://ubuntu.com/server/docs/cloud-images/amazon-ec2
CANONICAL_AWS_OWNER_ID = "099720109477"


class BaseComputeStackConfig():
    tag_name_prefix: str
    region: str

    def __init__(self, tag_name_prefix: str, region: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region


class BaseComputeStack(BaseStack):
    ubuntu_ami: DataAwsAmi
    key_pair: KeyPair

    def __init__(self,
                 scope: Construct,
                 id: str,
                 config: BaseComputeStackConfig,
                 ):
        super().__init__(scope, id, config.region)

        self.ubuntu_ami = self._fetch_ubuntu_ami()
        self.key_pair = self._create_key_pair(config.tag_name_prefix)

    def _fetch_ubuntu_ami(self):
        return DataAwsAmi(
            self,
            "ubuntu-ami",
            filter=[
                {
                    "name": "name",
                    "values": [
                        "ubuntu/images/hvm-ssd/"
                        "ubuntu-jammy-22.04-arm64-server-*"
                    ]
                },
                {
                    "name": "virtualization-type",
                    "values": ["hvm"]
                }
            ],
            most_recent=True,
            owners=[CANONICAL_AWS_OWNER_ID]
        )

    def _create_key_pair(self, tag_name_prefix):
        public_key_file_path = os.getenv("SSH_PUBLIC_KEY_PATH")

        if not public_key_file_path:
            raise ValueError("SSH_PUBLIC_KEY_PATH environment "
                             "variable is not set.")

        with open(public_key_file_path, "r") as public_key_file:
            public_key = public_key_file.read()

        return KeyPair(
            self,
            "key-pair",
            key_name=f"{tag_name_prefix}ssh-key-pair",
            public_key=public_key
        )
