# 1PASSINT
jun-pas-upd.py is the file to run
the main file can take an argument (new password), or auto update them

pip install -r requirements.txt
pip install git+ssh://git@github.com/1Password/onepassword-sdk-python.git@v0.1.0-beta.9
install onepass SDK

you do need a .env file with OP_ACCOUNT_TOKEN="<token>", VAULT_ID="<vid>", ITEM_ID="iid"
PLAYBOOK=".yml", INVENTORY=".ini"

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


## ADDITIONAL FILES IN GITHUB
### semail.py
added functionality but waiting on SMTP

### onepass_secret.py
allows for item_id to secret retrieval

### one_password_test.py
finds password, username and switch password, can update/create/delete
uses .ENV for storage
runs an ansible playbook automatically 
saves results to log.json
based on the results send email with log

## slk.py
slack integration for automated message and log sending

## test.yml
script in ansible TO run