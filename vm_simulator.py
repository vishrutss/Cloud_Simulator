import time
import psutil
import json
from multiprocessing import Process

def simulate_vm(vm_id, vm_dict):
    print(f"VM {vm_id} started")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        vm_dict["cpu"] = cpu_usage
        vm_dict["memory"] = mem_usage
        time.sleep(5)

def start_vm(vm_id, vms, manager):
    if vm_id not in vms or vms[vm_id]["status"] == "stopped":
        vm_dict = manager.dict({'pid': None, 'cpu': None, 'memory': None, 'status': 'running'})
        p=Process(target=simulate_vm, args=(vm_id, vm_dict))
        p.start()
        vm_dict['pid'] = p.pid
        vms[vm_id] = vm_dict
        return {"message": f"VM {vm_id} started!"}
    return {"error": f"VM {vm_id} already running!"}

def stop_vm(vm_id, vms):
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
            return {"message": f"VM {vm_id} stopped!"}
        elif vms[vm_id]["status"] == "stopped":
            return {"error": f"VM {vm_id} already stopped!"}
    return {"error": f"VM {vm_id} not found!"}

def delete_vm(vm_id, vms):
    if vm_id in vms:
        if vms[vm_id]["pid"] is not None:
            p = psutil.Process(vms[vm_id]["pid"])
            p.terminate()
            p.wait()
        del vms[vm_id]
        return {"message": f"VM {vm_id} deleted!"}
    return {"error": f"VM {vm_id} not found!"}

def monitor_vm(vm_id, vms):
    if vm_id in vms:
        vm_dict = vms[vm_id]
        return {
            "vm_id": vm_id,
            "status": vm_dict["status"],
            "pid": vm_dict["pid"],
            "cpu": vm_dict["cpu"],
            "memory": vm_dict["memory"]
        }
    return {"error": f"VM {vm_id} not found!"}

def display_vms(vms):
    if len(vms) == 0:
        return {"message": "No VMs running!"}
    vm_list = []
    for vm_id, vm_dict in vms.items():
        vm_list.append({
            "vm_id": vm_id,
            "status": vm_dict.get("status"),
            "pid": vm_dict.get("pid"),
            "cpu": vm_dict.get("cpu"),
            "memory": vm_dict.get("memory")
        })
    print(json.dumps({"vms": vm_list}, indent=4))
    return {"vms": vm_list}
