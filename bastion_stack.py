#!/usr/bin/env python
from constructs import Construct
from base_stack import BaseStack
from imports.aws.security_group import SecurityGroup
from imports.aws.vpc_security_group_ingress_rule \
    import VpcSecurityGroupIngressRule
from imports.aws.instance import Instance


MY_IP_ADDRESS = "66.11.34.104/32"
SSH_PORT = 22


class BastionStackConfig():
    tag_name_prefix: str
    region: str
    vpc_id: str
    subnet_id: str
    ami_id: str
    ssh_key_name: str

    def __init__(self,
                 tag_name_prefix: str,
                 region: str,
                 vpc_id: str,
                 subnet_id: str,
                 ami_id: str,
                 ssh_key_name: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region
        self.vpc_id = vpc_id
        self.subnet_id = subnet_id
        self.ami_id = ami_id
        self.ssh_key_name = ssh_key_name


class BastionStack(BaseStack):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 config: BastionStackConfig,
                 ):
        super().__init__(scope, id, config.region)

        sg = self._create_security_group(
            config.vpc_id,
            config.tag_name_prefix)

        self._create_instance(
            config.subnet_id,
            config.ami_id,
            config.ssh_key_name,
            sg.id,
            config.tag_name_prefix)

    def _create_security_group(self, vpc_id, tag_name_prefix):
        sg = SecurityGroup(
            self,
            "security-group",
            vpc_id=vpc_id,
            tags={
                "Name": f"{tag_name_prefix}bastion-security-group"
            },
        )

        VpcSecurityGroupIngressRule(
            self,
            "ingress-rule",
            description="Allow SSH inbound traffic",
            from_port=SSH_PORT,
            to_port=SSH_PORT,
            ip_protocol="tcp",
            cidr_ipv4=MY_IP_ADDRESS,
            security_group_id=sg.id,
            tags={
                "Name": f"{tag_name_prefix}ssh-inbound-traffic"
            },
        )

        return sg

    def _create_instance(self,
                         subnet_id,
                         ami_id,
                         ssh_key_name,
                         sg_id,
                         tag_name_prefix):
        Instance(
            self,
            "instance",
            instance_type="t4g.small",
            ami=ami_id,
            key_name=ssh_key_name,
            subnet_id=subnet_id,
            associate_public_ip_address=True,
            vpc_security_group_ids=[sg_id],
            tags={
                "Name": f"{tag_name_prefix}bastion"
            }
        )
