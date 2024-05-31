variable "proxmox_api_url" {
  description = "The Proxmox API URL"
  type        = string
  default     = "http://localhost:8006/api2/json"
}

variable "proxmox_user" {
  description = "The Proxmox user"
  type        = string
  default     = "root@pam"
}

variable "proxmox_password" {
  description = "The Proxmox password"
  type        = string
}

variable "vm_name" {
  description = "The name of the VM"
  type        = string
  default     = "ubuntu-vm"
}

variable "target_node" {
  description = "The Proxmox node to deploy the VM"
  type        = string
}

variable "clone_template" {
  description = "The template to clone"
  type        = string
}

variable "vm_cores" {
  description = "The number of CPU cores"
  type        = number
  default     = 2
}

variable "vm_memory" {
  description = "The amount of memory in MB"
  type        = number
  default     = 2048
}

variable "vm_disk_size" {
  description = "The size of the VM disk"
  type        = string
  default     = "20G"
}

variable "storage_pool" {
  description = "The storage pool to use for the VM disk"
  type        = string
  default     = "local-lvm"
}

variable "network_bridge" {
  description = "The network bridge to use for the VM"
  type        = string
  default     = "vmbr0"
}

variable "ssh_public_key_path" {
  description = "The path to the SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_private_key_path" {
  description = "The path to the SSH private key"
  type        = string
  default     = "~/.ssh/id_rsa"
}
