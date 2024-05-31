from flask import Flask, render_template, request, Response, jsonify
from tinydb import TinyDB, where
from config import OS_EQUIVALENT, CLASS_EQUIVALENT, URL_PROXMOX, USERNAME, PASSWORD
from proxmox import clone_vm, delete_vm
from utils import allowed_file
from werkzeug.utils import secure_filename
import logging
import csv
from datetime import datetime
from proxmoxer import ProxmoxAPI

db = TinyDB("./database/proxmox-class.json", indent=3)

# Replace with your Proxmox credentials and server address
proxmox = ProxmoxAPI(host=URL_PROXMOX, user=USERNAME, password=PASSWORD, verify_ssl=False)

def details():
    classe = request.args.get("classe")
    os = request.args.get("os")
    table_promo = db.table(f"classe-{classe}-os-{os}".lower())
    return render_template(
        "details.html",
        liste_eleve=table_promo.all(),
        classe=classe,
        os=os,
        url_proxmox=URL_PROXMOX,
        url_proxmox_troncat=URL_PROXMOX.split("://")[1],
    )

def create_vm():
    if "os" not in request.form:
        logging.error("None empty os")
        return Response(status=404)

    os = request.form["os"]
    name = request.form["name"]
    requestType = request.form["request"]

    node = request.json.get('node')
    vmid = proxmox.cluster.nextid.get()
    proxmox.nodes(node).qemu.post(
        vmid=vmid,
        name=name,
        memory=512,
        net0='virtio,bridge=vmbr0',
        ide2='local:iso/alpine-standard-3.20.0-x86_64.iso,media=cdrom',
        boot='order=ide2;ide0',
        cores=1,
        cpu='host',
        ostype='l26'
    )
    # Optionally, start the VM and install Python3
    proxmox.nodes(node).qemu(vmid).status.start.post()
    # Here you can add additional steps to install Python3 via a script or cloud-init
    return jsonify({'status': 'success', 'vmid': vmid})


def delete_class():
    content = request.json
    nom_table = f"classe-{content['classe']}-os-{content['os']}".lower()
    delete_vm(nom_table, db)
    db.drop_table(nom_table)
    logging.info(f"Table {nom_table} dropped")
    return "", 201