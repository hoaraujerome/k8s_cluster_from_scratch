# Kubernetes The Hard Way On AWS

## Description

"Kubernetes The Hard Way On AWS" is a learning project aimed at understanding each task required to bootstrap a Kubernetes cluster. Unlike the original [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) by Kelsey Hightower, this project uses Terraform to provision the infrastructure and Ansible to configure the Kubernetes cluster. This project is designed to take the long route to ensure a deep understanding of deploying a Kubernetes cluster on AWS.

## Badges

![Work in Progress](https://img.shields.io/badge/status-work_in_progress-yellow)
[![Powered by LazyVim](https://img.shields.io/badge/Powered_by-LazyVim-%2307a6c3?style=flat&logo=vim&logoColor=white)](https://lazyvim.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)


## Visuals

### Infrastructure

![image](https://github.com/user-attachments/assets/5dade7ac-d416-48c1-acfe-ae3330d97e69)

### K8S Cluster

**WIP**

## Installation

### Requirements

- AWS Account
- AWS CLI
- Docker
- SSH Key Pair
- **WIP**

### Steps

1. Provision the infrastructure with Terraform:
   ```sh
   ./k8s_manager.sh provision
   # Provision skipping tests: SKIP_TESTS="1" ./k8s_manager.sh provision
   # Plan: ./k8s_manager.sh plan
   ```

2. Configure the Kubernetes cluster with Ansible: **WIP**

## Usage

### Infrastructure
   ```sh
   # SSH to the control plane
   ssh -J ubuntu@<bastion_public_dns> ubuntu@<control_plane_private_dns>
   ```

### K8S Cluster

**WIP**

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
