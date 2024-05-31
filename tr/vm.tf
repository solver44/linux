resource "proxmox_vm_qemu" "alpine_vm" {
    name = var.vm_name
    target_node = var.target_node
    iso = var.iso
    # invoke the variable var_vm_cores as a number 
    cores = var.cores
    sockets = var.sockets
    qemu_os = var.qemu_os
    os_type = var.os_type
    memory = var.memory
    disk {
        type = var.disk_type
        storage = var.disk_storage
        size = var.disk_size
    }
    network {
        model = var.network_model
        bridge = var.network_bridge
    }
}