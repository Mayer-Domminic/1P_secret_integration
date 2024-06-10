import asyncio
import os
import json
from onepassword import Client
from dotenv import load_dotenv
from utilities import password_gen, encrypt, ansi_run
from semail import send_email
from slk import message


# check readme.md
load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
user_id = os.getenv("USERNAME")
token = os.getenv("OP_ACCOUNT_TOKEN")
playbook = os.getenv("PLAYBOOK")
inventory = os.getenv("INVENTORY")


async def main(passw=None):
    if not vault_id or not item_id or not token or not playbook or not inventory:
        print('ENV issue!')
        raise Exception("Please double check ENV variables!")
    
    client = await Client.authenticate(
        auth=token,
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )

    item = await client.items.get(vault_id, item_id)
    # user stuff
    user = await client.items.get(vault_id, user_id)

    if not passw:
        passw = password_gen(20, True, False, True, True)
    item.fields[0].value = passw
    await client.items.update(item)
    encrypted = encrypt(passw)
    return user.fields[0].value, user.fields[1].value, encrypted


if __name__ == "__main__":
    ar = []
    p, u, pw = asyncio.run(main())
    r = ansi_run(playbook, inventory, u, pw, p)

    for event in r.events:
        ar.append(event)
    with open('log.json', 'w') as f:
        # TODO
        # I added just the play recap FOR NOW
        json.dump(ar[int(len(ar))-1], f, indent=4)
    
    subject = f"{ playbook } : { r.status }"
    receiver_email = "test@gmail.com"
    # send_email(subject, receiver_email, "See log attached!", "log.json")
    print(r.status)
    message(r.status)