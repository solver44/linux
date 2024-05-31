variable "proxmox_url" {
    type = string
    default = "https://localhost:8006/api2/json"
    
}

variable "proxmox_user" {
    type = string
    default = "root@pam"
    
}

variable "proxmox_password" {
    type = string
    default = "root"
}

variable "vm_name" {
    type = string
    default = "source1"
    
}

variable "target_node" {
    type = string
    default = "pve"
    
}

variable "qemu_os" {
    type = string
    default = "l26"
    
}

variable "os_type" {
    type = string
    default = "alpine"
    
}

variable "iso" {
    type = string
    default = "local:iso/alpine-standard-3.20.0-x86_64.iso"
    
}

variable "cores" {
    type = number
    default = 2
    
}

variable "sockets" {
    type = number
    default = 1
    
}

variable "memory" {
    type = number
    default = 1024
    
}

variable "disk_type" {
    type = string
    default = "ide"
    
}

variable "disk_storage" {
    type = string
    default = "local-lvm"
    
}

variable "disk_size" {
    type = string
    default = "16G"
    
}

variable "network_model" {
    type = string
    default = "virtio"
    
}

variable "network_bridge" {
    type = string
    default = "vmbr0"
    
}