#!/bin/bash

echo "ceate_vm_9000.sh started..."

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get update
apt-get install libguestfs-tools -y

ISO_NAME=alpine-standard-3.20.0-x86_64.iso

cd ./iso

# virt-customize -a $ISO_NAME --install qemu-guest-agent
# virt-customize -a $ISO_NAME --run-command "useradd -m -s /bin/bash admin"
# virt-customize -a $ISO_NAME --root-password password:admin

qm create 9000 --force --full 1 --storage local-lvm --memory 1024 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci
qm importdisk 9000 $ISO_NAME local

# Configure the VM to use the imported disk
qm set 9000 --scsi0 local-lvm:vm-9000-disk-0
qm set 9000 --boot order=scsi0
qm set 9000 --serial0 socket --vga serial0
qm set 9000 --agent 1
qm template 9000

echo "cerate_vm_9000 completed."