import os
import ansible_runner

def run_playbook(playbook_path, inventory_path, extra_vars):
    r = ansible_runner.run(
        playbook=playbook_path,
        inventory=inventory_path,
        extravars=extra_vars
    )
    return r

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    playbook_path = os.path.join(current_dir, "msg.yml")
    inventory_path = os.path.join(current_dir, "inventory.ini")
    extra_vars = {"message": "Hello, Ansible!"}

    print(f"Playbook Path: {playbook_path}")
    print(f"Inventory Path: {inventory_path}")

    result = run_playbook(playbook_path, inventory_path, extra_vars)

    print(f"Status: {result.status}")
    print(f"Return code: {result.rc}")

    for event in result.events:
        print(event['stdout'])
