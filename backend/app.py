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
from flask import Flask, jsonify, request
from vm_simulator import start_vm, stop_vm, monitor_vm, delete_vm, display_vms
from cdn import upload_to_origin, delete_from_origin, serve_from_nearest_edge
from storage import create_bucket, upload_file, delete_file, delete_bucket

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

# Virtual Machine Routes

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


# Storage Routes

@app.route('/create_bucket/<bucket_name>', methods=['POST'])
def create_storage_bucket(bucket_name):
    """
    Route to create a new bucket with the specified name.
    Args:
        bucket_name (str): The name of the bucket to create.
    Returns:
        JSON response with the result of the operation.
    """
    result = create_bucket(bucket_name)
    return jsonify(result)

@app.route('/upload_file/<bucket_name>/<file_name>', methods=['POST'])
def upload_storage_file(bucket_name, file_name):
    """
    Route to upload a file to the specified bucket.
    Args:
        bucket_name (str): The name of the bucket to upload the file to.
        file_name (str): The name of the file to upload.
    Returns:
        JSON response with the result of the operation.
    """
    file = request.files['file']
    file_content = file.read()
    result = upload_file(bucket_name, file_name, file_content)
    return jsonify(result)

@app.route('/delete_file/<bucket_name>/<file_name>', methods=['DELETE'])
def delete_storage_file(bucket_name, file_name):
    """
    Route to delete a file from the specified bucket.
    Args:
        bucket_name (str): The name of the bucket to delete the file from.
        file_name (str): The name of the file to delete.
    Returns:
        JSON response with the result of the operation.
    """
    result = delete_file(bucket_name, file_name)
    return jsonify(result)

@app.route('/delete_bucket/<bucket_name>', methods=['DELETE'])
def delete_storage_bucket(bucket_name):
    """
    Route to delete a bucket with the specified name.
    Args:
        bucket_name (str): The name of the bucket to delete.
    Returns:
        JSON response with the result of the operation.
    """
    result = delete_bucket(bucket_name)
    return jsonify(result)

# CDN Routes

@app.route('/upload_to_origin/<file_name>', methods=['POST'])
def upload_to_origin_server(file_name):
    """
    Route to upload a file to the origin server.
    Args:
        file_name (str): The name of the file to upload.
    Returns:
        JSON response with the result of the operation.
    """
    file = request.files['file']
    file_content = file.read()
    result = upload_to_origin(file_name, file_content)
    return jsonify(result)

@app.route('/get_file/<file_name>/<int:user_location>', methods=['GET'])
def get_file_from_nearest_edge(file_name, user_location):
    """
    Route to serve a file from the nearest edge server based on the user's location.
    Args:
        file_name (str): The name of the file to serve.
        user_location (int): The location of the user.
    Returns:
        JSON response with the content of the file and the server it was served from.
    """
    result = serve_from_nearest_edge(file_name, user_location)
    return jsonify(result)

@app.route('/delete_from_origin/<file_name>', methods=['DELETE'])
def delete_from_origin_server(file_name):
    """
    Route to delete a file from the origin server and all edge servers.
    Args:
        file_name (str): The name of the file to delete.
    Returns:
        JSON response with the result of the operation.
    """
    result = delete_from_origin(file_name)
    return jsonify(result)

if __name__ == '__main__':
    manager = Manager()
    vms = manager.dict()
    app.run(debug=True)
