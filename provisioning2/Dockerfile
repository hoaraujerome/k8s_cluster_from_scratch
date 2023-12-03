FROM base:local

# ***
# Terraform Installation
# ***

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | \
      gpg --dearmor | \
      tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
      https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
      tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install -y terraform=1.5.5-1 && \
    apt-get clean all

ENV TERRAFORM_HOME_DIR=/home/terraform

RUN useradd -m terraform -d $TERRAFORM_HOME_DIR

ENV PATH=$TERRAFORM_HOME_DIR/.local/bin:$PATH

USER terraform

WORKDIR $TERRAFORM_HOME_DIR

RUN terraform --version || exit 1