import requests

requests.urllib3.disable_warnings()

MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Max 2 MB files
FLASK_SECRET = "jksfd$*^^$*ù!fsfshjkhfgks"  # Key for encrypting cookies/session, etc.
BASIC_AUTH_USERNAME = "admin"  # Login
BASIC_AUTH_PASSWORD = "1234"  # Password

# Proxmox info
URL_PROXMOX = "localhost"  # without / at the end
USERNAME = "root"
PASSWORD = "admin"

# Allowed file extensions
ALLOWED_EXTENSIONS = {"csv"}

# Nodes and roles
NODES_LIST = ["pve", "pve1", "pve2"]
ROLE = "Etudiant"
AUTHENTICATION_MODE = "authentification-AD"

# Equivalent mappings
OS_EQUIVALENT = {
    "0": "Alpine",
    "1": "CentOS",
    "2": "Debian",
    "3": "Linux_Autre",
    "4": "WinXP",
    "5": "Win7",
    "6": "Win10",
    "7": "WinSRV2016",
    "8": "WinSRV2019",
    "9": "Win_Autre",
}

TEMPLATE_EQUIVALENT = {
    "CentOS": 105,
    "WinSRV2016": 104,
}

CLASS_EQUIVALENT = {
    "1": "ING1",
    "2": "ING2",
    "3": "IR3",
    "4": "IR4",
    "5": "IR5",
    "6": "Bachelor",
    "7": "M1",
    "8": "M2",
    "9": "Autre",
}
