https://github.com/vivami/proxmox-automation/tree/main

https://andreypicado.com/create-a-virtual-machine-in-proxmox-with-python-and-terraform/

https://github.com/parithosh/proxmox-terraform-ansible/tree/main

after `install.sh`
`cd ./tr`
`terraform init`
`terraform plan -out plan`



```#!/usr/bin/env python3
import argparse
from python_terraform import *

# Create a class with the variables of the new VM and setting the values
class ProxmoxVM(object):
    pass

proxmoxVM = ProxmoxVM()

# Iterate over the arguments passed to the script from CLI and set the values of the proxmox object
for i in vars(args):
    if getattr(args, i) is not None:
        setattr(proxmoxVM, i, getattr(args, i))
    else:
        setattr(proxmoxVM, i, None)

# Invoke Terraform class
tf = Terraform(working_dir='./tf')

# Initialize Terraform
tfInit = tf.init()

# If the init fails, exit the script
if tfInit[0] != 0:
    print("Terraform init failed")
    exit(1)

# Apply Terraform
tfApply = tf.apply(
    skip_plan=True, 
    auto_approve=True,
    var={
        'proxmox_url': proxmoxVM.proxmox_url,
        'proxmox_password': proxmoxVM.proxmox_password,
        'proxmox_user': proxmoxVM.proxmox_user,
        'vm_name': proxmoxVM.vm_name,
        'target_node': proxmoxVM.node_name,
        'qemu_os': proxmoxVM.qemu_os,
        'os_type': proxmoxVM.os_type,
        'iso': proxmoxVM.iso,
        'cores': proxmoxVM.cores,
        'sockets': proxmoxVM.sockets,
        'memory': proxmoxVM.memory,
        'disk_type': proxmoxVM.disk_type,
        'disk_storage': proxmoxVM.disk_container,
        'disk_size': proxmoxVM.disk_size,
        'network_model': proxmoxVM.net_model,
        'network_bridge': proxmoxVM.net_bridge
    }
)

# If the apply fails, exit the script
if tfApply[0] != 0:
    print("Terraform apply failed")
    exit(1)
else:
    print("Terraform apply successful. VM created {}.".format(proxmoxVM.vm_name)) 
```