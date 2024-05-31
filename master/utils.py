from config import ALLOWED_EXTENSIONS, URL_PROXMOX
import requests
import time
from random import randint

def get_vm_status(ticket, csrftoken, node, id_vm):
    while True:
        try:
            response_prox = requests.get(
                URL_PROXMOX + f"/api2/json/nodes/{node}/qemu/{id_vm}/status/current",
                verify=False,
                cookies={"PVEAuthCookie": ticket},
                headers={"CSRFPreventionToken": csrftoken},
            )
            if response_prox.status_code == 500:
                time.sleep(randint(5, 15))
                continue
            break
        except:
            continue
    return response_prox

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS