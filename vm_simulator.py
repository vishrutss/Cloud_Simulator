import time
import psutil
from multiprocessing import Process

def simulate_vm(vm_id, vm_dict):
    print(f"VM {vm_id} started")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        vm_dict["cpu"] = cpu_usage
        vm_dict["memory"] = mem_usage
        time.sleep(1)
        
def start_vm(vm_id, vms, manager):
    if vm_id not in vms:
        vm_dict = manager.dict({'pid': None, 'cpu': None, 'memory': None})
        p=Process(target=simulate_vm, args=(vm_id, vm_dict))
        p.start()
        vm_dict['pid'] = p.pid
        vms[vm_id] = vm_dict
        return {"message": f"VM {vm_id} started!"}
    return {"error": f"VM {vm_id} already running!"}

def stop_vm(vm_id, vms):
    if vm_id in vms and vms[vm_id]["pid"] is not None:
        p = psutil.Process(vms[vm_id]["pid"])
        p.terminate()
        p.wait()
        del vms[vm_id]
        return {"message": f"VM {vm_id} stopped!"}
    return {"error": f"VM {vm_id} not found!"}

def monitor_vm(vm_id, vms):
    if vm_id in vms:
        vm_dict = vms[vm_id]
        return {
            "vm_id": vm_id,
            "status": "running",
            "pid": vm_dict["pid"],
            "cpu": vm_dict["cpu"],
            "memory": vm_dict["memory"]
        }
    return {"error": f"VM {vm_id} not found!"}
