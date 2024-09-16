"""
Cloud Simulator Flask Application

This module sets up a Flask web application to manage virtual machines (VMs) using
multiprocessing. It provides routes to start, stop, monitor, and display VMs.

Routes:
    / - Home route that returns a message indicating the Cloud Simulator is running.
    /start_vm/<int:vm_id> - Route to start a VM with the given ID.
    /stop_vm/<int:vm_id> - Route to stop a VM with the given ID.
    /monitor_vm/<int:vm_id> - Route to monitor a VM with the given ID.
    /display_vms - Route to display all running VMs.

Dependencies:
    - Flask
    - multiprocessing
    - vm_simulator (custom module)
"""

from multiprocessing import Manager
from flask import Flask, jsonify
from vm_simulator import start_vm, stop_vm, monitor_vm, delete_vm, display_vms

app = Flask(__name__)

manager, vms = None, None

@app.route('/')
def home():
    """
    Home route that returns a message indicating the Cloud Simulator is running.
    Returns:
        JSON response with a message.
    """
    return jsonify({"message": "Cloud Simulator is running!"})

@app.route('/start_vm/<int:vm_id>', methods=['POST'])
def start_vm_route(vm_id):
    """
    Route to start a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to start.
    Returns:
        JSON response with a message indicating the result of the operation.
    """
    message = start_vm(vm_id, vms, manager)
    return jsonify(message)

@app.route('/stop_vm/<int:vm_id>', methods=['POST'])
def stop_vm_route(vm_id):
    """
    Route to stop a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to stop.
    Returns:
        JSON response with a message indicating the result of the operation.
    """
    message = stop_vm(vm_id, vms)
    return jsonify(message)

@app.route('/delete_vm/<int:vm_id>', methods=['DELETE'])
def delete_vm_route(vm_id):
    """
    Route to delete a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to delete.
    Returns:
        JSON response with a message indicating the result of the operation.
    """
    message = delete_vm(vm_id, vms)
    return jsonify(message)

@app.route('/monitor_vm/<int:vm_id>', methods=['GET'])
def monitor_vm_route(vm_id):
    """
    Route to monitor a VM with the given ID.
    Args:
        vm_id (int): The ID of the VM to monitor.
    Returns:
        JSON response with the status of the VM.
    """
    return jsonify(monitor_vm(vm_id, vms))

@app.route('/display_vms', methods=['GET'])
def display_vms_route():
    """
    Route to display all VMs.
    Returns:
        JSON response with the status of all VMs.
    """
    return jsonify(display_vms(vms))

if __name__ == '__main__':
    manager = Manager()
    vms = manager.dict()
    app.run(debug=True)
