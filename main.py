#!/usr/bin/env python
from cdktf import App
from networking_stack import NetworkingStack
from load_balancer_stack import LoadBalancerStack


TAG_NAME_PREFIX = "k8s-from-scratch-"


app = App()
networking_stack = NetworkingStack(app, "NetworkingStack")
load_balancer_stack = LoadBalancerStack(
    app,
    "LoadBalancerStack",
    networking_stack)
app.synth()
