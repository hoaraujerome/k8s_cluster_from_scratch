# Kubernetes The Hard Way On AWS

## Description

"Kubernetes The Hard Way On AWS" is a learning project aimed at understanding each task required to bootstrap a Kubernetes cluster. Unlike the original [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) by Kelsey Hightower, this project uses Terraform to provision the infrastructure and Ansible to configure the Kubernetes cluster. This project is designed to take the long route to ensure a deep understanding of deploying a Kubernetes cluster on AWS.

## Badges

![Completed](https://img.shields.io/badge/status-completed-brightgreen)
[![Powered by LazyVim](https://img.shields.io/badge/Powered_by-LazyVim-%2307a6c3?style=flat&logo=vim&logoColor=white)](https://lazyvim.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

## Visuals

### Infrastructure

![K8S_Infra_Deployment_Diagram](https://github.com/user-attachments/assets/cd9dc464-9076-40ab-937f-f4d61544c151)

### K8S Cluster

![K8S_Cluster_Deployment_Diagram](https://github.com/user-attachments/assets/461c13b2-5733-4e94-9fe5-503efe222433)

![K8S_Architecture](https://github.com/user-attachments/assets/08c70d21-6128-440f-a8b3-6a96f5fd19cb)

## Installation

### Requirements

- AWS Account
- AWS CLI configured
- Docker

### Steps

1. Setup prerequisites:
   ```sh
   ./provisioning/prereq/bootstrap_prereq.sh
   ```
```mermaid
graph TD
    root[Bootstrap Prerequisites]
    crypto_assets[Crypto Assets]
    terraform_backend[Terraform Backend]
    terraform_sp[Terraform Service Principal]

    root --> crypto_assets
    root --> terraform_backend
    root --> terraform_sp

    crypto_assets --> setup_root_ca[Self-Signed Root CA]
    crypto_assets --> setup_ssh_key[RSA SSH Key]

    setup_root_ca --> create_sa_certificate[Service Accounts Certificate]
    create_sa_certificate --> create_apiserver_certificate[kube-apiserver Certificate]
    create_apiserver_certificate --> create_controllermanager_certificate[kube-controller-manager Certificate]
    create_controllermanager_certificate --> create_admin_certificate[admin Certificate]
    create_admin_certificate --> create_scheduler_certificate[kube-scheduler Certificate]
    create_scheduler_certificate --> create_kubelet_certificate[Kubelet Certificate]
    create_kubelet_certificate --> create_proxy_certificate[kube-proxy Certificate]

    terraform_backend --> create_s3_bucket[S3 Bucket]

    terraform_sp --> create_iam_user[IAM User]
    terraform_sp --> create_iam_policy[IAM Policy]
    create_iam_user --> attach_iam_user_policy[Attach Policy to User]
    create_iam_policy --> attach_iam_user_policy[Attach Policy to User]
```

2. Provision the infrastructure with Terraform:
   ```sh
   ./k8s_manager.sh provision
   # Provision skipping tests: SKIP_TESTS="1" ./k8s_manager.sh provision
   # Plan: ./k8s_manager.sh plan
   ```

```mermaid
graph TD;
    subgraph "For each child module"
        A["Linting & Formatting"] --> B["Unit test"];
        B --> C["Contract test"];
        C --> D["Integration test"];
    end
    D --> E["Security Scanner"];
    E --> F["Linting & Formatting (root module)"];
    F --> G["End-to-end test (root module)"];
```

3. Create the Kubernetes cluster with Ansible:
   ```sh
   ./k8s_manager.sh create
   ```
```mermaid
graph TD;
    A["Control Plane Playbook"] --> B["Worker Node Playbook"];
    B --> C["Smoke Tests Playbook"];
```

4. Delete the cluster and the infrastructure:
   ```sh
   ./k8s_manager.sh destroy
   ```

## Usage

* SSH to the control plane

   ```sh
   ./k8s_manager.sh troubleshoot
   ssh k8s_control_plane
   kubectl get secrets --kubeconfig=admin.kubeconfig
   NAME                      TYPE     DATA   AGE
   kubernetes-the-hard-way   Opaque   1      75s
   ```

* SSH to the worker node

   ```sh
   ./k8s_manager.sh troubleshoot
   ssh k8s_worker_node
   kubectl get nodes --kubeconfig=kubelet.kubeconfig
   NAME     STATUS   ROLES    AGE     VERSION
   node-0   Ready    <none>   5m27s   v1.31.1
   ```

## Contributing

This project is a personal learning endeavor, and contributions are not being accepted at this time.

## Developer Setup

### Requirements

- [pre-commit](https://pre-commit.com/)

### Steps

1. Clone this repo and cd
2. Install `pre-commit` hooks:
   ```sh
   pre-commit install
   ```
3. (Optional) Run pre-commit on all files:
   ```sh
   pre-commit run --all-files
   ```

## Authors and Acknowledgment

- **Hoarau Jerome** - [GitHub](https://github.com/hoaraujerome)

Special thanks to [Kelsey Hightower](https://github.com/kelseyhightower) for the original "Kubernetes The Hard Way".

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more details, see the LICENSE file or visit http://creativecommons.org/licenses/by-nc-sa/4.0/.

## Project Status

This project is **done** and has been completed successfully as a learning project. It is no longer maintained.
