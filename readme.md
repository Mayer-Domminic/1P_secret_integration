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

## semail.py
added functionality but waiting on SMTP

## onepass_secret.py
allows for item_id to secret retrieval

## one_password_test.py
finds password, username and switch password, can update/create/delete
uses .ENV for storage
runs an ansible playbook automatically 
saves results to log.json
based on the results send email with log