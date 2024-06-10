import asyncio
import os
from onepassword import Client
from dotenv import load_dotenv
from pwg import password_gen

# check readme.md
load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
token = os.getenv("OP_ACCOUNT_TOKEN")

async def main(passw=None):
    client = await Client.authenticate(
        auth=token,
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )


    item = await client.items.get(vault_id, item_id)
    print("Original item:", dict(item))
    if not passw:
        passw = password_gen(20, True, True, True, True)
    item.fields[0].value = passw
    # Update the item in the vault (requires elevated permissions)
    # updated_item = await client.items.update(item)
    # print("Updated item in vault:", dict(updated_item))
    # TODO


if __name__ == "__main__":
    asyncio.run(main())