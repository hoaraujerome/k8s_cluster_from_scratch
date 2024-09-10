# Kubernetes The Hard Way On AWS

## Description

"Kubernetes The Hard Way On AWS" is a learning project aimed at understanding each task required to bootstrap a Kubernetes cluster. Unlike the original [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) by Kelsey Hightower, this project uses Terraform to provision the infrastructure and Ansible to configure the Kubernetes cluster. This project is designed to take the long route to ensure a deep understanding of deploying a Kubernetes cluster on AWS.

## Badges

![Work in Progress](https://img.shields.io/badge/status-work_in_progress-yellow)
[![Powered by LazyVim](https://img.shields.io/badge/Powered_by-LazyVim-%2307a6c3?style=flat&logo=vim&logoColor=white)](https://lazyvim.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)


## Visuals (TODO)

![Kubernetes Cluster](images/k8s_cluster.png)

## Installation

### Requirements (TODO)

- AWS Account
- Terraform
- Ansible
- kubectl

### Steps (TODO)

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/kubernetes-the-hard-way-on-aws.git
   cd kubernetes-the-hard-way-on-aws
   ```

2. **Provision the infrastructure with Terraform:**
   ```sh
   terraform init
   terraform apply
   ```

3. **Configure the Kubernetes cluster with Ansible:**
   ```sh
   ansible-playbook -i inventory main.yml
   ```

## Usage (TODO)

After the installation, you can interact with your Kubernetes cluster using `kubectl`. Here is a simple example:

```sh
kubectl get nodes
```

Expected output:
```
NAME           STATUS   ROLES    AGE   VERSION
ip-10-0-0-1    Ready    master   10m   v1.20.0
ip-10-0-0-2    Ready    <none>   10m   v1.20.0
```

## Support

If you need help, you can reach out via:

- [GitHub Issues](https://github.com/hoaraujerome/kubernetes-the-hard-way-on-aws/issues)

## Roadmap

- Implement high availability for the Kubernetes cluster
- Develop a hub-and-spoke network topology

## Contributing

This project is a personal learning endeavor, and contributions are not being accepted at this time.

## Authors and Acknowledgment

- **Hoarau Jerome** - [GitHub](https://github.com/hoaraujerome)

Special thanks to [Kelsey Hightower](https://github.com/kelseyhightower) for the original "Kubernetes The Hard Way".

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more details, see the LICENSE file or visit http://creativecommons.org/licenses/by-nc-sa/4.0/.

## Project Status

This project is a work in progress and is actively maintained.
