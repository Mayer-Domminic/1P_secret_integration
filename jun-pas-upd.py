'''
Created: 6/24
Last Modified: 6/13/24
Author: Domminic Mayer

Function: Retrieve onepass information and send that information to ansible files for updating juniper root passwords.

TODO: 
encorporate palo alto network systems for pswd rotations
alerting when something does go wrong -> slack?
successful running -> logging

'''

import os
import asyncio
import string
import secrets
import crypt
import ansible_runner
import json
from onepassword import Client
from dotenv import load_dotenv

load_dotenv()
vault_id = os.getenv("VAULT")
juniper = os.getenv("JUNIPER")
ansible = os.getenv("ANSIBLE")
token = os.getenv("OP_ACCOUNT_TOKEN")

playbook = "juniper-root-pwd-upd.yml"
inventory = "test.yml"

def run_playbook(extra_vars):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    r = ansible_runner.run(
        playbook=os.path.join(current_dir, playbook), #playbook path
        inventory=os.path.join(current_dir, inventory), #inventory path
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
    if not (vault_id and juniper and token and ansible):
        raise Exception("Please double check ENV variables!")
    
    # get onepassword client and fetch the objects
    client = await Client.authenticate(
        auth=token,
        integration_name="1passint",
        integration_version="v1",
    )
    item = await client.items.get(vault_id, juniper)
    ansible_item = await client.items.get(vault_id, ansible)

    # if you don't pass in a new one, generate one, upd 1pass
    if not passw:
        passw = password_gen(20, True, True, True, True)
    item.fields[0].value = passw
    await client.items.update(item)

    encrypted = encrypt(passw)
    ansible_user = ansible_item.fields[0].value
    ansible_pass = ansible_item.fields[1].value
    r = run_playbook({"encrypted_password": encrypted, "user": ansible_user, "pass": ansible_pass})

    ar = []
    for event in r.events:
        ar.append(event)
    with open('log.json', 'w') as f:
        json.dump(ar, f, indent=4)
    # makes a nicer looking response

    if not (r.status == "successful"):
        print("Ansible script failed!")

if __name__ == "__main__":
    asyncio.run(juni_update_pass())