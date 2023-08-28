

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="config.yaml")

def create_vlan(task):
    command_list = [
        "vlan 10",
        "name sales",
        "vlan 20",
        "name voice"
    ]
    for command in command_list:
        task.run(
            task=netmiko_send_command,
            command_string=command
        )

result = nr.run(task=create_vlan)

print_result(result)