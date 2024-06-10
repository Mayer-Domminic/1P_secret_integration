# 1PASSINT

## Vault Information:
you need 1Password CLI, and a service account token
The CLI only needs to be installed on one computer to find the IDs of the vault/item.
export OP_SERVICE_ACCOUNT_TOKEN=<token>
op user get --me

### item_id
op item list
[alt] op item get <"name">

### vault_id
op vault list
