from onepassword import Client
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
vault_id = os.getenv("VAULT_ID")
item_id = os.getenv("ITEM_ID")
token = os.getenv("OP_ACCOUNT_TOKEN")

async def get_password():
    client = await Client.authenticate(
        auth=token,
        integration_name="grab pass",
        integration_version="v0.1",
    )
    return (await client.items.get(vault_id, item_id)).fields[0].value


if __name__ == "__main__":
    print(asyncio.run(get_password()))