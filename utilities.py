import string
import secrets
import crypt
import os
import ansible_runner

def run_playbook(playbook_path, inventory_path, extra_vars):
    r = ansible_runner.run(
        playbook=playbook_path,
        inventory=inventory_path,
        extravars=extra_vars
    )
    return r

def ansi_run(playbook, inventory, username, upw, pw):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    playbook_path = os.path.join(current_dir, playbook)
    inventory_path = os.path.join(current_dir, inventory)
    extra_vars = {"user": username, "pass": upw, "encrypted_password": pw}

    result = run_playbook(playbook_path, inventory_path, extra_vars)

    return result

def encrypt(password):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(password, salt)

def generate(length, use_digits, use_symbols, use_uppercase, use_lowercase):
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

def password_gen(length, use_digits, use_symbols, use_uppercase, use_lowercase):
    try:
        password = generate(length, use_digits, use_symbols, use_uppercase, use_lowercase)
        return password
    except ValueError as e:
        print(f"Error: {e}")
