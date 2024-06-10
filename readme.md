# Documentation For OnePass integration

## Vault Information:
you need 1Password CLI, and a service account token
run export OP_SERVICE_ACCOUNT_TOKEN=<token>
op user get --me, confirms it
op item | op document | op item | op document 

// Commands must be ran with CLI installed

### item_id
op item list
[alt] op item get <"name">

### vault_id
op vault list