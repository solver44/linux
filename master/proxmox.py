import time
import requests
from random import randint
from config import URL_PROXMOX, USERNAME, PASSWORD, NODES_LIST, TEMPLATE_EQUIVALENT, OS_EQUIVALENT
from utils import get_vm_status
import logging

r = requests.Session()

print((URL_PROXMOX + "/api2/json/access/ticket"))
def login_proxmox():
    response_prox = r.post(
        (URL_PROXMOX + "/api2/json/access/ticket"),
        verify=False,
        params={"username": USERNAME, "password": PASSWORD},
    ).json()
    logging.info(response_prox)
    return response_prox["data"]["ticket"], response_prox["data"]["CSRFPreventionToken"]

def get_storage(ticket, csrftoken, classe):
    while 1:
        try:
            for node in NODES_LIST:
                response_prox = r.get(
                    URL_PROXMOX + f"/api2/json/nodes/{node}/storage",
                    verify=False,
                    cookies={"PVEAuthCookie": ticket},
                    headers={"CSRFPreventionToken": csrftoken},
                )
                for storage in response_prox.json()["data"]:
                    if storage["storage"].lower() == classe.lower():
                        return storage["storage"]
        except:
            logging.error("Error getting storages")
            time.sleep(randint(5, 15))

def request_clone_vm(ticket, csrftoken, student, vm_name, storage, nom_table, template_node, clone_os, target_node):
    logging.info(f"Starting the VM clone {nom_table} for {student['email']} VM: {student['id_vm']}")
    while 1:
        try:
            response_prox = r.post(
                URL_PROXMOX + f"/api2/json/nodes/{template_node}/qemu/{clone_os}/clone",
                verify=False,
                params={
                    "newid": int(student["id_vm"]),
                    "name": vm_name,
                    "full": 1,
                    "storage": f"{storage}",
                    "target": target_node
                },
                cookies={"PVEAuthCookie": ticket},
                headers={"CSRFPreventionToken": csrftoken},
            )
            if response_prox.status_code in [200, 500]:
                break
            else:
                logging.warning(f"Restart clone {vm_name} {response_prox.status_code} {response_prox.text}")
                time.sleep(randint(5, 15))
        except:
            time.sleep(randint(5, 15))

    if response_prox.status_code == 200 or response_prox.status_code == 500:
        while True:
            is_cloned = get_vm_status(ticket, csrftoken, target_node, student["id_vm"])
            if is_cloned.json()["data"]["name"] == vm_name:
                break
            time.sleep(randint(5, 15))

        logging.info(f"VM: {student['id_vm']} OS: {clone_os}, User: {student['email']} cloned")

        for _ in range(2):
            response_prox = r.put(
                URL_PROXMOX + f"/api2/json/access/acl",
                verify=False,
                params={
                    "path": f"/vms/{student['id_vm']}",
                    "users": f"{student['email'].split('@')[0]}@{authentication_mode}",
                    "roles": role,
                },
                cookies={"PVEAuthCookie": ticket},
                headers={"CSRFPreventionToken": csrftoken},
            )
            if response_prox.status_code == 200:
                logging.info(f"VM: {student['id_vm']} OS: {clone_os}, User: {student['email']} right set")
                table_db.update({"is_cloned": True, "node": target_node}, where("id_vm") == student["id_vm"])
                break
            time.sleep(randint(5, 15))
        else:
            logging.error(f"VM: {student['id_vm']} OS: {clone_os}, User: {student['email']} right not set\n {response_prox.status_code}\n{response_prox.text}")

def clone_vm(nom_table, db):
    ticket, csrftoken = login_proxmox()
    template_node = NODES_LIST[0]

    classe = next(classe_name for classe_id, classe_name in CLASS_EQUIVALENT.items() if classe_name.lower() == nom_table.split("-")[1].lower()).lower()
    storage = get_storage(ticket, csrftoken, classe)

    os_name = next(os_name for os_id, os_name in OS_EQUIVALENT.items() if os_name.lower() == nom_table.split("-")[::-1][0].lower())
    clone_os = TEMPLATE_EQUIVALENT[os_name]

    threads = []
    for student in db.table(nom_table).all():
        target_node = NODES_LIST[1] if int(student["id_vm"]) % 2 == 0 and len(NODES_LIST) > 1 else NODES_LIST[0]
        vm_name = f"{os_name}-{student['email']}".split("@")[0]
        t = Thread(target=request_clone_vm, args=[ticket, csrftoken, student, vm_name, storage, nom_table, template_node, clone_os, target_node])
        threads.append(t)
        t.start()
        time.sleep(0.5)

    for t in threads:
        t.join()

    logging.info("Threads clone finished")

def request_delete_vm(ticket, csrftoken, target_node, student):
    logging.info(f"Starting VM removal {student['id_vm']} of {student['email']}")
    while True:
        try:
            response_prox = r.post(
                URL_PROXMOX + f"/api2/json/nodes/{target_node}/qemu/{student['id_vm']}/status/stop",
                verify=False,
                params={"timeout": 5},
                cookies={"PVEAuthCookie": ticket},
                headers={"CSRFPreventionToken": csrftoken},
            )
            if response_prox.status_code in [200, 500]:
                break
            else:
                logging.warning(f"Restart delete {student['id_vm']} {response_prox.status_code} {response_prox.text}")
                time.sleep(randint(5, 15))
        except:
            time.sleep(randint(5, 15))

    if response_prox.status_code == 200:
        while True:
            is_stopped = get_vm_status(ticket, csrftoken, target_node, student["id_vm"])
            if is_stopped.json()["data"]["qmpstatus"] == "stopped":
                break
            time.sleep(randint(5, 15))

        logging.info(f"VM {student['id_vm']} stopped")
        for _ in range(2):
            response_prox = r.delete(
                URL_PROXMOX + f"/api2/json/nodes/{target_node}/qemu/{student['id_vm']}",
                verify=False,
                cookies={"PVEAuthCookie": ticket},
                headers={"CSRFPreventionToken": csrftoken},
            )
            if response_prox.status_code == 200:
                logging.info(f"VM: {student['id_vm']}, User: {student['email']} deleted")
                break
            time.sleep(randint(5, 15))
        else:
            logging.error(f"VM: {student['id_vm']}, User: {student['email']} not deleted")

def delete_vm(nom_table, db):
    ticket, csrftoken = login_proxmox()
    threads = []
    for student in db.table(nom_table).all():
        target_node = NODES_LIST[1] if int(student["id_vm"]) % 2 == 0 and len(NODES_LIST) > 1 else NODES_LIST[0]
        t = Thread(target=request_delete_vm, args=[ticket, csrftoken, target_node, student])
        threads.append(t)
        t.start()
        time.sleep(0.5)

    for t in threads:
        t.join()

    logging.info("Threads delete finished")
