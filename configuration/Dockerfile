FROM ubuntu:22.04

# ***
# Python Installation
# ***
ENV PYTHON_VERSION=3.12
# non interactive needed for software-properties-common
ENV DEBIAN_FRONTEND=noninteractive

# apt list --all-versions XXX
# software-properties-common required for add-apt-repository
# ppa required for python 3.12 https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa/
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get install -y software-properties-common && \
    apt-get install -y make && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python$PYTHON_VERSION && \
    apt-get clean all

RUN python3 --version | awk '{if ($2 < 3.10) exit 1;}'

# ***
# Ansible Installation
# ***

ENV ANSIBLE_VERSION=9.0.1
ENV BOTO3_VERSION=1.34.13

# ssh required for ansible
# jq used for parsing ansible aws inventory
RUN apt-get update && \
    apt-get install -y ssh && \
    apt-get install -y jq && \
    apt-get clean all

ENV ANSIBLE_HOME_DIR=/home/ansible

RUN useradd -m ansible -d $ANSIBLE_HOME_DIR

ENV PATH=$ANSIBLE_HOME_DIR/.local/bin:$PATH

USER ansible

WORKDIR $ANSIBLE_HOME_DIR

# TODO pin version
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --user && \
    rm get-pip.py

RUN python3 -m pip -V || exit 1

RUN python3 -m pip install --user ansible==$ANSIBLE_VERSION

RUN ansible-community --version || exit 1

# Required for AWS dynamic inventory
RUN python3 -m pip install --user boto3==$BOTO3_VERSION

COPY --chown=ansible:ansible ansible.cfg Makefile configuration.sh ./

RUN mkdir .ssh

ENTRYPOINT [ "make" ]

