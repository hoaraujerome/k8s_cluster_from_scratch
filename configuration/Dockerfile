FROM ubuntu:22.04

# non interactive needed for software-properties-common
ENV DEBIAN_FRONTEND=noninteractive

# apt list --all-versions XXX
# software-properties-common required for add-apt-repository
# ppa required for python 3.12 https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa/
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 && \
    apt-get clean all

# TODO https://pip.pypa.io/en/stable/installation/