#!/usr/bin/env python
from constructs import Construct
from cdktf import Token
from base_stack import BaseStack
from imports.aws.lb import Lb

TAG_NAME_PREFIX = "k8s-from-scratch-"


class LoadBalancerStack(BaseStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        """
        Access the Kubernetes API from the outside world
        """
        # self._create_network_load_balancer(aws_private_subnet.id)

    def _create_network_load_balancer(self, subnet_id):
        Lb(
            self,
            "network-load-balancer",
            internal=True,
            load_balancer_type="network",
            subnets=[Token.as_string(subnet_id)],
            tags={
                "Name": f"{TAG_NAME_PREFIX}load-balancer"
            },
        )
