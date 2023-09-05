#!/usr/bin/env python
from cdktf import App
from networking_stack import NetworkingStack, NetworkingStackConfig
from load_balancer_stack import LoadBalancerStack, LoadBalancerStackConfig
from kubernetes_controlplane_stack import (
  KubernetesControlPlaneStack,
  KubernetesControlPlaneStackConfig
)


TAG_NAME_PREFIX = "k8s-from-scratch-"

app = App()

networking_stack = NetworkingStack(
    app, "NetworkingStack",
    NetworkingStackConfig(
        tag_name_prefix=TAG_NAME_PREFIX,
        region="ca-central-1"
    ),
)

load_balancer_stack = LoadBalancerStack(
    app, "LoadBalancerStack",
    LoadBalancerStackConfig(
        tag_name_prefix=TAG_NAME_PREFIX,
        region=networking_stack.region,
        subnet_id=networking_stack.aws_private_subnet.id
    ),
)

kubernetes_controlplane_stack = KubernetesControlPlaneStack(
  app, "KubernetesControlPlaneStack",
  KubernetesControlPlaneStackConfig(
    tag_name_prefix=TAG_NAME_PREFIX,
    region=networking_stack.region,
    subnet_id=networking_stack.aws_private_subnet.id,
  )
)

app.synth()
