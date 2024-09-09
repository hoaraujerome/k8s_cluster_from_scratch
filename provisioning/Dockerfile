FROM hashicorp/terraform:1.8

# jq used by some Terraform checks scripts
RUN apk update && \
    apk add --no-cache \
      make \
      bash \
      curl \
      jq

RUN adduser -D terraform

USER terraform

WORKDIR /home/terraform

COPY --chown=terraform:terraform Makefile provisioning.sh get_public_ip_as_cidr.sh ./

ENTRYPOINT [ "make" ]
