FROM base:local

ENV ANSIBLE_VERSION=9.0.1
ENV BOTO3_VERSION=1.34.13

# ***
# Ansible Installation
# ***

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

COPY --chown=ansible:ansible ansible.cfg ./

