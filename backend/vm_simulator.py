"""
VM Simulator Module

This module provides functionality to simulate virtual machines (VMs) using the `psutil` library
to monitor CPU and memory usage. It uses multiprocessing to run each VM simulation in a separate
process.

Functions:
    simulate_vm(vm_id, vm_dict): Simulates a VM by periodically updating its CPU and memory usage.

Dependencies:
    - time
    - psutil
    - json
    - multiprocessing
"""

import time
from multiprocessing import Process
import json
import psutil
from ip_assignment import assign_ip, create_network, delete_network, networks

def simulate_vm(vm_id, vm_dict):
    """
    Simulates a VM by periodically updating its CPU and memory usage.
    Args:
        vm_id (int): The ID of the VM.
        vm_dict (dict): A shared dictionary to store VM information.
    """
    print(f"VM {vm_id} started")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        vm_dict["cpu"] = cpu_usage
        vm_dict["memory"] = mem_usage
        time.sleep(5)

def start_vm(vm_id, vms, manager):
    """
    Starts a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to start.
        vms (dict): A dictionary containing information about running VMs.
        manager (Manager): A multiprocessing Manager object.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    if vm_id not in vms or vms[vm_id]["status"] == "stopped":
        network_id = create_network(vm_id)
        ip = assign_ip(network_id)
        vm_dict = manager.dict({'pid': None,
                                'cpu': None,
                                'memory': None,
                                'status': 'running',
                                'ip': ip
                                })
        p=Process(target=simulate_vm, args=(vm_id, vm_dict))
        p.start()
        vm_dict['pid'] = p.pid
        vms[vm_id] = vm_dict
        networks[network_id]["vms"].append(vm_id)
        return {"message": f"VM {vm_id} started!"}
    return {"message": f"VM {vm_id} already running!"}

def stop_vm(vm_id, vms):
    """
    Stops a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to stop.
        vms (dict): A dictionary containing information about running VMs.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    if vm_id in vms:
        if vms[vm_id]["status"] == "running":
            vm_dict = vms[vm_id]
            if vm_dict["pid"] is not None:
                p = psutil.Process(vm_dict["pid"])
                p.terminate()
                p.wait()
            vm_dict["status"] = "stopped"
            vm_dict["pid"] = None
            vm_dict["cpu"] = None
            vm_dict["memory"] = None
            vm_dict["ip"] = None
            delete_network(vm_id)
            return {"message": f"VM {vm_id} stopped!"}
        return {"message": f"VM {vm_id} already stopped!"}
    return {"message": f"VM {vm_id} not found!"}

def delete_vm(vm_id, vms):
    """
    Deletes a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to delete.
        vms (dict): A dictionary containing information about running VMs.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    if vm_id in vms:
        if vms[vm_id]["pid"] is not None:
            p = psutil.Process(vms[vm_id]["pid"])
            p.terminate()
            p.wait()
        delete_network(vm_id)
        del vms[vm_id]
        return {"message": f"VM {vm_id} deleted!"}
    return {"message": f"VM {vm_id} not found!"}

def monitor_vm(vm_id, vms):
    """
    Monitors a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to monitor.
        vms (dict): A dictionary containing information about running VMs.
    Returns:
        dict: A dictionary containing the status of the VM.
    """
    if vm_id in vms:
        vm_dict = vms[vm_id]
        return {
            "vm_id": vm_id,
            "status": vm_dict["status"],
            "pid": vm_dict["pid"],
            "cpu": vm_dict["cpu"],
            "memory": vm_dict["memory"],
            "ip": vm_dict["ip"]
        }
    return {"message": f"VM {vm_id} not found!"}

def display_vms(vms):
    """
    Displays all VMs.
    Args:
        vms (dict): A dictionary containing information about running VMs.
    Returns:
        dict: A dictionary containing the status of all VMs.
    """
    if len(vms) == 0:
        return {"message": "No VMs running!"}
    vm_list = []
    for vm_id, vm_dict in vms.items():
        vm_list.append({
            "vm_id": vm_id,
            "status": vm_dict.get("status"),
            "pid": vm_dict.get("pid"),
            "cpu": vm_dict.get("cpu"),
            "memory": vm_dict.get("memory"),
            "ip": vm_dict.get("ip")
        })
    print(json.dumps({"vms": vm_list}, indent=4))
    return {"vms": vm_list}
