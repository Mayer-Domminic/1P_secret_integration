import asyncio
import os
import json
from onepassword import Client
from dotenv import load_dotenv
from utilities import password_gen, encrypt, ansi_run

# check readme.md
load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
user_id = os.getenv("USERNAME")
token = os.getenv("OP_ACCOUNT_TOKEN")


if not vault_id or not item_id or not token:
    print('ENV issue!')
    raise Exception("Please double check ENV variables!")

async def main(passw=None):
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

    r = ansi_run("test.yml", "inventory.ini", u, pw, p)

    for event in r.events:
        ar.append(event)

    if not r.status == "successful":
        print(r.status)
        # TODO
    
    with open('log.json', 'w') as f:
        json.dump(ar, f, indent=4)
        # TODO