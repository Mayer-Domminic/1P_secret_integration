import asyncio
import os
from onepassword import Client
from dotenv import load_dotenv


# check readme.md
load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
token = os.getenv("OP_ACCOUNT_TOKEN")

async def main(passw):
    client = await Client.authenticate(
        auth=token,
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )

    item = await client.items.get(vault_id, item_id)
    print(dict(item))
    item.fields[0].value = passw
    print(item)

    # updated_item = await client.items.update(item)
    # NEED ELEVATED PERMS
    # print(dict(updated_item))
    # TODO


if __name__ == "__main__":
    password = "TEST"
    asyncio.run(main(password))