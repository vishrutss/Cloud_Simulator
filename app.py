from flask import Flask, jsonify
from vm_simulator import start_vm, stop_vm, monitor_vm, delete_vm, display_vms
from multiprocessing import Manager

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Cloud Simulator is running!"})

@app.route('/start_vm/<int:vm_id>', methods=['POST'])
def start_vm_route(vm_id):
    message = start_vm(vm_id, vms, manager)
    return jsonify(message)

@app.route('/stop_vm/<int:vm_id>', methods=['POST'])
def stop_vm_route(vm_id):
    message = stop_vm(vm_id, vms)
    return jsonify(message)

@app.route('/delete_vm/<int:vm_id>', methods=['DELETE'])
def delete_vm_route(vm_id):
    message = delete_vm(vm_id, vms)
    return jsonify(message)

@app.route('/monitor_vm/<int:vm_id>', methods=['GET'])
def monitor_vm_route(vm_id):
    return jsonify(monitor_vm(vm_id, vms))

@app.route('/display_vms', methods=['GET'])
def display_vms_route():
    return jsonify(display_vms(vms))

if __name__ == '__main__':
    manager = Manager()
    vms = manager.dict()
    app.run(debug=True)
