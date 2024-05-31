#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y wget unzip software-properties-common

# Install Terraform
TERRAFORM_VERSION="1.0.10"
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
sudo mv terraform /usr/local/bin/
rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Verify Terraform installation
terraform -v

# Install Ansible
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Verify Ansible installation
ansible --version

echo "Terraform and Ansible installation completed."