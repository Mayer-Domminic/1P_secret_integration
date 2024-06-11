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

## slk.py
slack integration for automated message and log sending

## test.yml
script in ansible TO run



## DHCP Request:
Jun 10 12:34:56 dhcp-server dhcpd[1234]: DHCPREQUEST for 192.168.1.100 from 00:11:22:33:44:55 (client-hostname) via eth0
on commit {
    set ClientIP = binary-to-ascii(10, 8, ".", leased-address);
    set ClientMAC = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set ClientHostname = pick-first-value(option host-name, "unknown");
    execute("/usr/local/bin/dhcp-commit.sh", ClientIP, ClientMAC, ClientHostname);
}
On commit parse this information from the DHCP request, then I want to ensure the request MAC address is the correct one from the core switch side. 
Get mac address from interface and ensure everything is okay, I want to also find this hostname attribute and add provisioning to the config file updating relevant ips and the hostname

dhcp-commit.sh
#!/bin/bash

ClientIP=$1
ClientMAC=$2
ClientHostname=$3

# Log the information
echo "DHCP Lease committed:"
echo "IP Address: $ClientIP"
echo "MAC Address: $ClientMAC"
echo "Hostname: $ClientHostname"
echo "Timestamp: $(date)"

# Check if the MAC address is valid from the core switch side
# Replace 'core-switch' with the actual command or script to get the MAC address from the switch
# Here is a placeholder command (you need to replace it with your actual command to check MAC address from switch)
VALID_MAC=$(ssh user@core-switch "show mac address-table | grep $ClientMAC")

if [ -z "$VALID_MAC" ]; then
    echo "Invalid MAC address: $ClientMAC" >> /var/log/dhcp-errors.log
    exit 1
fi

# Add provisioning to the config file
CONFIG_FILE="/etc/your_config_file.conf"

# Backup the existing config file
cp "$CONFIG_FILE" "$CONFIG_FILE.bak"

# Update the config file with the new IP and hostname
echo "Updating config file with IP: $ClientIP and Hostname: $ClientHostname"
sed -i "/\[clients\]/a \\$ClientHostname $ClientIP" "$CONFIG_FILE"

# Optionally, restart any services that depend on this config file
# sudo systemctl restart your-service

# Log the update
echo "Provisioning completed for $ClientHostname with IP $ClientIP" >> /var/log/dhcp-updates.log
