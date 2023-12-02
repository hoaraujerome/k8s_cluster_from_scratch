#!/usr/bin/env python
from constructs import Construct
from base_stack import BaseStack
from imports.aws.lb import Lb


class LoadBalancerStackConfig():
    tag_name_prefix: str
    region: str
    subnet_id: str

    def __init__(self, tag_name_prefix: str, region: str, subnet_id: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = region
        self.subnet_id = subnet_id


class LoadBalancerStack(BaseStack):
    tag_name_prefix: str

    def __init__(self,
                 scope: Construct,
                 id: str,
                 config: LoadBalancerStackConfig,
                 ):
        super().__init__(scope, id, config.region)

        self.tag_name_prefix = config.tag_name_prefix

        """
        Access the Kubernetes API from the outside world
        """
        self._create_network_load_balancer(
            config.subnet_id
        )

    def _create_network_load_balancer(self, subnet_id):
        Lb(
            self,
            "network-load-balancer",
            internal=True,
            load_balancer_type="network",
            subnets=[subnet_id],
            tags={
                "Name": f"{self.tag_name_prefix}load-balancer"
            },
        )
