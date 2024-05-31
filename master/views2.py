import json
import requests
from python_terraform import Terraform, IsFlagged
from config import URL_PROXMOX, USERNAME, PASSWORD

# Initialize Terraform
tf = Terraform()
tf.init()

# Get a Proxmox API token
def get_proxmox_token():
    login_url = f"{URL_PROXMOX}/access/ticket"
    data = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    response = requests.post(login_url, data=data, verify=False)
    response.raise_for_status()
    return response.json()["data"]["ticket"]

# List all nodes
def list_nodes():
    token = get_proxmox_token()
    headers = {
        "Cookie": f"PVEAuthCookie={token}",
    }
    response = requests.get(f"{URL_PROXMOX}/nodes", headers=headers, verify=False)
    response.raise_for_status()
    nodes = response.json()["data"]
    for node in nodes:
        print(f"Node: {node['node']}, Status: {node['status']}")

# Start a VM
def start_vm(vm_id):
    tf.apply(skip_plan=True, var={"action": "start", "vm_id": vm_id})

# Stop a VM
def stop_vm(vm_id):
    tf.apply(skip_plan=True, var={"action": "stop", "vm_id": vm_id})

# Create a VM with Alpine Linux
def create_vm():
    return_code, stdout, stderr = tf.apply(skip_plan=True, var={"action": "create_vm"})
    if return_code != 0:
        print(f"Error creating VM: {stderr}")
    else:
        print(f"VM created successfully: {stdout}")