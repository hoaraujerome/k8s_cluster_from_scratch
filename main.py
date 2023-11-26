#!/usr/bin/env python
from cdktf import App
from networking_stack import NetworkingStack, NetworkingStackConfig
from base_compute_stack import BaseComputeStackConfig, BaseComputeStack
# from load_balancer_stack import LoadBalancerStack, LoadBalancerStackConfig
from kubernetes_nodes_stack import (
  KubernetesNodesStack,
  KubernetesNodesStackConfig
)
from bastion_stack import BastionStack, BastionStackConfig


TAG_NAME_PREFIX = "k8s-from-scratch-"

app = App()

networking_stack = NetworkingStack(
  app, "NetworkingStack",
  NetworkingStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
  ),
)

base_compute_stack = BaseComputeStack(
  app, "BaseComputeStack",
  BaseComputeStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
    region=networking_stack.region,
    vpc_id=networking_stack.aws_vpc.id,
  )
)

bastion_stack = BastionStack(
  app, "BastionStack",
  BastionStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
    region=networking_stack.region,
    subnet_id=networking_stack.aws_public_subnet.id,
    ami_id=base_compute_stack.ubuntu_ami.id,
    ssh_key_name=base_compute_stack.key_pair.key_name,
    bastion_security_group_id=base_compute_stack.bastion_security_group_id,
    k8s_nodes_security_group_id=base_compute_stack.k8s_nodes_security_group_id,
  )
)

# load_balancer_stack = LoadBalancerStack(
#     app, "LoadBalancerStack",
#     LoadBalancerStackConfig(
#         tag_name_prefix=TAG_NAME_PREFIX,
#         region=networking_stack.region,
#         subnet_id=networking_stack.aws_private_subnet.id
#     ),
# )

kubernetes_nodes_stack = KubernetesNodesStack(
  app, "KubernetesNodesStack",
  KubernetesNodesStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
    region=networking_stack.region,
    subnet_id=networking_stack.aws_private_subnet.id,
    ami_id=base_compute_stack.ubuntu_ami.id,
    ssh_key_name=base_compute_stack.key_pair.key_name,
    bastion_security_group_id=base_compute_stack.bastion_security_group_id,
    k8s_nodes_security_group_id=base_compute_stack.k8s_nodes_security_group_id,
  )
)

app.synth()
