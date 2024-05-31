#!/bin/bash

set -e

# Variables
PROXMOX_API_URL="https://localhost:8006/api2/json"
PROXMOX_USER="admin@pam"
PROXMOX_PASSWORD="admin123"
VM_NAME="alpine-vm"
NODE_NAME="pve"
TEMPLATE_NAME="alpine-template"
ROOT_PASSWORD="admin123"

# Update and install necessary packages
sudo apt update
sudo apt install -y wget curl unzip python3 python3-pip sshpass

# Install Proxmox VE (PVE)
echo "deb [arch=amd64] http://download.proxmox.com/debian jessie pve-no-subscription" > /etc/apt/sources.list.d/pve-install-repo.list
wget -O- "http://download.proxmox.com/debian/key.asc" | apt-key add -
sudo apt-get update && sudo apt-get dist-upgrade

# Install Proxmox VE dependencies
sudo apt install -y proxmox-ve ssh postfix ksm-control-daemon open-iscsi systemd-sysv
sudo apt-get remove os-prober

# Install Terraform
TERRAFORM_VERSION="1.0.11"
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
sudo mv terraform /usr/local/bin/
rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Set up Python environment
pip3 install python-terraform requests

# Create Terraform configuration file
cat <<EOF > tr/main.tf
provider "proxmox" {
  pm_api_url = "$PROXMOX_API_URL"
  pm_user    = "$PROXMOX_USER"
  pm_password = "$PROXMOX_PASSWORD"
  pm_tls_insecure = true
}

data "proxmox_nodes" "nodes" {}

resource "proxmox_vm_qemu" "alpine_vm" {
  name   = "$VM_NAME"
  target_node = "$NODE_NAME"
  clone       = "$TEMPLATE_NAME"
  os_type     = "l26"
  cores       = 2
  sockets     = 1
  memory      = 2048
  scsi0       = "local-lvm:8"
  bootdisk    = "scsi0"
  ipconfig0   = "ip=dhcp"
  agent       = 1
  onboot      = true

  provisioner "remote-exec" {
    inline = [
      "apk update",
      "apk add python3",
    ]

    connection {
      type     = "ssh"
      user     = "root"
      password = "$ROOT_PASSWORD"
      host     = "\${self.network.0.ip}"
    }
  }
}
EOF

# Print completion message
echo "Installation and setup complete."