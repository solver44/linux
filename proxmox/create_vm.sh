#!/bin/bash

cd ./tf

# Initialize and apply Terraform configuration
terraform init
terraform apply -auto-approve

# Get the VM IP address from Terraform output
VM_IP=$(terraform output -raw vm_ip)

cd ../ansible
# Create Ansible inventory file
cat <<EOL > inventory.ini
[proxmox_vms]
ubuntu-vm ansible_host=$VM_IP ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa
EOL

ansible-playbook -i inventory.ini playbook.yml