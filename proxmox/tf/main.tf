resource "proxmox_vm_qemu" "ubuntu-vm" {
  name        = var.vm_name
  target_node = var.target_node

  clone = var.clone_template

  os_type = "cloud-init"

  cores   = var.vm_cores
  memory  = var.vm_memory
  sockets = 1

  disk {
    id           = 0
    size         = var.vm_disk_size
    storage      = var.storage_pool
    type         = "scsi"
    storage_type = "qcow2"
  }

  network {
    id     = 0
    model  = "virtio"
    bridge = var.network_bridge
  }

  ipconfig0 = "ip=dhcp"
  sshkeys = file(var.ssh_public_key_path)

  provisioner "local-exec" {
    command = "echo 'VM is created'"
  }
}

output "vm_ip" {
  value = proxmox_vm_qemu.ubuntu-vm.network.0.ip
}