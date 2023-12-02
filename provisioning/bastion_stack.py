#!/usr/bin/env python
from constructs import Construct
from base_stack import BaseStack
from imports.aws.vpc_security_group_ingress_rule \
    import VpcSecurityGroupIngressRule
from imports.aws.vpc_security_group_egress_rule \
    import VpcSecurityGroupEgressRule
from imports.aws.instance import Instance
import os


SSH_PORT = 22


class BastionStackConfig():
    tag_name_prefix: str
    region: str
    subnet_id: str
    ami_id: str
    ssh_key_name: str
    bastion_security_group_id: str
    k8s_nodes_security_group_id: str

    def __init__(self,
                 tag_name_prefix: str,
                 region: str,
                 subnet_id: str,
                 ami_id: str,
                 ssh_key_name: str,
                 bastion_security_group_id: str,
                 k8s_nodes_security_group_id: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region
        self.subnet_id = subnet_id
        self.ami_id = ami_id
        self.ssh_key_name = ssh_key_name
        self.bastion_security_group_id = bastion_security_group_id
        self.k8s_nodes_security_group_id = k8s_nodes_security_group_id


class BastionStack(BaseStack):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 config: BastionStackConfig,
                 ):
        super().__init__(scope, id, config.region)

        self._configure_security_rules(
            config.bastion_security_group_id,
            config.k8s_nodes_security_group_id,
            config.tag_name_prefix)

        self._create_instance(
            config.subnet_id,
            config.ami_id,
            config.ssh_key_name,
            config.bastion_security_group_id,
            config.tag_name_prefix)

    def _configure_security_rules(self,
                                  bastion_security_group_id,
                                  k8s_nodes_security_group_id,
                                  tag_name_prefix):
        my_ip_address = os.getenv("MY_IP_ADDRESS")

        if not my_ip_address:
            raise ValueError("MY_IP_ADDRESS environment "
                             "variable is not set.")

        VpcSecurityGroupIngressRule(
            self,
            "ingress-rule",
            description="Allow SSH inbound traffic",
            from_port=SSH_PORT,
            to_port=SSH_PORT,
            ip_protocol="tcp",
            cidr_ipv4=my_ip_address,
            security_group_id=bastion_security_group_id,
            tags={
                "Name": f"{tag_name_prefix}ssh-inbound-traffic"
            },
        )

        VpcSecurityGroupEgressRule(
            self,
            "egress-rule",
            description="Allow SSH outbound traffic",
            from_port=SSH_PORT,
            to_port=SSH_PORT,
            ip_protocol="tcp",
            referenced_security_group_id=k8s_nodes_security_group_id,
            security_group_id=bastion_security_group_id,
            tags={
                "Name": f"{tag_name_prefix}ssh-outbound-traffic"
            }
        )

    def _create_instance(self,
                         subnet_id,
                         ami_id,
                         ssh_key_name,
                         sg_id,
                         tag_name_prefix):
        return Instance(
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
