FROM base:local

# ***
# Ansible Installation
# ***

ENV ANSIBLE_HOME_DIR=/home/ansible

RUN useradd -m ansible -d $ANSIBLE_HOME_DIR

ENV PATH=$ANSIBLE_HOME_DIR/.local/bin:$PATH

USER ansible

WORKDIR $ANSIBLE_HOME_DIR

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --user && \
    rm get-pip.py

RUN python3 -m pip -V || exit 1

RUN python3 -m pip install --user ansible==9.0.1

RUN ansible-community --version || exit 1