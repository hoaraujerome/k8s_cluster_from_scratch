#!/usr/bin/env python
from constructs import Construct
from base_stack import BaseStack
from imports.aws.data_aws_ami import DataAwsAmi
from imports.aws.instance import Instance
from imports.aws.key_pair import KeyPair
import os


class KubernetesControlPlaneStackConfig():
    tag_name_prefix: str
    region: str
    subnet_id: str

    def __init__(self, tag_name_prefix: str, region: str, subnet_id: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region
        self.subnet_id = subnet_id


class KubernetesControlPlaneStack(BaseStack):
    tag_name_prefix: str

    def __init__(self,
                 scope: Construct,
                 id: str,
                 config: KubernetesControlPlaneStackConfig,
                 ):
        super().__init__(scope, id, config.region)

        self.tag_name_prefix = config.tag_name_prefix

        ami = self._fetch_ubuntu_ami()
        key_pair = self._create_key_pair()
        self._create_instance(
            ami.image_id,
            key_pair.key_name,
            config.subnet_id)

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
            owners=["099720109477"]
        )

    def _create_key_pair(self):
        public_key_file_path = os.getenv("SSH_PUBLIC_KEY_PATH")

        if not public_key_file_path:
            raise ValueError("SSH_PUBLIC_KEY_PATH environment "
                             "variable is not set.")

        with open(public_key_file_path, "r") as public_key_file:
            public_key = public_key_file.read()

        return KeyPair(
            self,
            "key-pair",
            key_name=f"{self.tag_name_prefix}key-pair",
            public_key=public_key
        )

    def _create_instance(self, ami_id, key_name, subnet_id):
        Instance(
            self,
            "instance",
            instance_type="t4g.small",
            ami=ami_id,
            key_name=key_name,
            subnet_id=subnet_id,
            tags={
                "Name": f"{self.tag_name_prefix}control-plane"
            }
        )
