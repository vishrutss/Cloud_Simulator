"""
IP Assignment Module
This module handles the creation, assignment, and deletion of network IPs 
for virtual machines (VMs) in a simulated cloud environment.

Functions:
- assign_ip(network_id): Assigns a random IP address within the specified network.
- create_network(vm_id): Creates a new network for the given VM ID.
- delete_network(vm_id): Deletes the network associated with the given VM ID if no 
VMs are left in the network.

Global Variables:
- networks: A dictionary storing network information, where the key is the network
ID and the value is a dictionary containing a list of VMs in the network.
"""
import random

networks = {}

def assign_ip(network_id):
    """
    Assigns a random IP address within the specified network.
    Args:
        network_id (int): The ID of the network to assign the IP address from.
    Returns:
        str: The assigned IP address.
    """
    ip = f"192.168.{network_id}.{random.randint(1, 254)}"
    return ip

def create_network(vm_id):
    """
    Creates a new network for the given VM ID.
    Args:
        vm_id (int): The ID of the VM to create the network for.
    Returns:
        int: The ID of the created network.
    """
    network_id = vm_id
    networks[network_id] = {"vms": []}
    return network_id

def delete_network(vm_id):
    """
    Deletes the network associated with the given VM ID if no VMs are left in the network.
    Args:
        vm_id (int): The ID of the VM to delete the network for.
    """
    for network_id, network in list(networks.items()):
        if vm_id in network["vms"]:
            network["vms"].remove(vm_id)
            if len(network["vms"]) == 0:
                del networks[network_id]
                print(f"Network {network_id} deleted because no VMs are left.")
