import json
import os
from cryptography.fernet import Fernet

VAULT_FILE = "vault.json"
KEY_FILE = "master.key"

# -------------------------------------------
# Load or create encryption key
# -------------------------------------------
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()

    return Fernet(key)


# -------------------------------------------
# Load encrypted vault
# -------------------------------------------
def load_vault():
    cipher = load_key()

    if not os.path.exists(VAULT_FILE):
        return {}

    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = cipher.decrypt(encrypted)
        return json.loads(decrypted)
    except:
        return {}  # empty vault if corrupted


# -------------------------------------------
# Save encrypted vault
# -------------------------------------------
def save_vault(vault):
    cipher = load_key()
    data = json.dumps(vault, indent=4).encode()
    encrypted = cipher.encrypt(data)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
