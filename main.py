#!/usr/bin/env python
from cdktf import App
from networking_stack import NetworkingStack, NetworkingStackConfig
from base_compute_stack import BaseComputeStackConfig, BaseComputeStack
# from load_balancer_stack import LoadBalancerStack, LoadBalancerStackConfig
# from kubernetes_controlplane_stack import (
#   KubernetesControlPlaneStack,
#   KubernetesControlPlaneStackConfig
# )
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
  )
)

bastion_stack = BastionStack(
  app, "BastionStack",
  BastionStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
    region=networking_stack.region,
    vpc_id=networking_stack.aws_vpc.id,
    subnet_id=networking_stack.aws_public_subnet.id,
    ami_id=base_compute_stack.ubuntu_ami.id,
    ssh_key_name=base_compute_stack.key_pair.key_name,
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
#
# kubernetes_controlplane_stack = KubernetesControlPlaneStack(
#   app, "KubernetesControlPlaneStack",
#   KubernetesControlPlaneStackConfig(
#     tag_name_prefix=TAG_NAME_PREFIX,
#     region=networking_stack.region,
#     subnet_id=networking_stack.aws_private_subnet.id,
#   )
# )

app.synth()
