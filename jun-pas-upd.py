import os
import asyncio
import string
import secrets
import crypt
import ansible_runner
import json

from dotenv import load_dotenv
from onepassword import Client

load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
token = os.getenv("OP_ACCOUNT_TOKEN")
playbook = os.getenv("PLAYBOOK")
inventory = os.getenv("INVENTORY")

def run_playbook(extra_vars):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    r = ansible_runner.run(
        os.path.join(current_dir, playbook), #playbook path
        os.path.join(current_dir, inventory), #inventory path
        extravars=extra_vars
    )
    return r

def password_gen(length, use_digits, use_symbols, use_uppercase, use_lowercase):
    # try/catch for a password creation
    try:
        password = generate(length, use_digits, use_symbols, use_uppercase, use_lowercase)
        return password
    except ValueError as e:
        print(f"Error: {e}")

def encrypt(password):
    # encrypts password according to SHA512 (ansibles')
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(password, salt)

def generate(length, use_digits, use_symbols, use_uppercase, use_lowercase):
    # Very simple password generator
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if len(characters) == 0:
        raise ValueError("At least one character type must be selected")
    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password

async def juni_update_pass(passw=None):
    # pre-env check
    if not (vault_id and item_id and token and playbook and inventory):
        raise Exception("Please double check ENV variables!")
    
    # get onepassword client and fetch the selected object
    client = await Client.authenticate(
        auth=token,
        integration_name="1passint",
        integration_version="v1",
    )
    item = await client.items.get(vault_id, item_id)

    # if you don't pass in a new one, generate one, upd 1pass
    if not passw:
        passw = password_gen(20, True, False, True, True)
    item.fields[0].value = passw
    await client.items.update(item)

    # encrypt & run through ansible
    encrypted = encrypt(passw)
    r = run_playbook({"encrypted_password": encrypted})

    if not (r.status == "successful"):
        print("Ansible script failed!")
        print(json.dump(r, indent=2))