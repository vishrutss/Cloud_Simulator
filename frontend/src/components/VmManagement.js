import React, { useState } from 'react';
import axios from 'axios';
import '../VmManagement.css';

function VmManagement() {
    const [vmId, setVmId] = useState('');
    const [status, setStatus] = useState('');

    const startVm = () => {
        axios.post(`/start_vm/${vmId}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const stopVm = () => {
        axios.post(`/stop_vm/${vmId}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const deleteVM = () => {
        axios.delete(`/delete_vm/${vmId}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const monitorVm = () => {
        axios.get(`/monitor_vm/${vmId}`)
            .then(response => {
                const vmData = response.data;
                if (vmData.message) {
                    setStatus(vmData.message);
                } else {
                    let vmInfo = `VM ID: ${vmData.vm_id}<br>Status: ${vmData.status}`;                    
                    if (vmData.pid) vmInfo += `<br>PID: ${vmData.pid}`;
                    if (vmData.cpu) vmInfo += `<br>CPU: ${vmData.cpu}`;
                    if (vmData.memory) vmInfo += `<br>Memory: ${vmData.memory}`;
                    if (vmData.ip) vmInfo += `<br>IP: ${vmData.ip}`;
                    setStatus(<div dangerouslySetInnerHTML={{ __html: vmInfo }} />);
                }
            })
            .catch(error => setStatus(error.response.data.error));
    };
    
    const displayVm = () => {
        axios.get(`/display_vms`)
            .then(response => {
                const vmData = response.data;
                if (vmData.message) {
                    setStatus(vmData.message);
                } else if (vmData.vms && vmData.vms.length > 0) {
                    const vmList = vmData.vms.map(vm => {
                        let vmInfo = `VM ID: ${vm.vm_id}, Status: ${vm.status}`;    
                        if (vm.pid) vmInfo += `, PID: ${vm.pid}`;
                        if (vm.cpu) vmInfo += `, CPU: ${vm.cpu}`;
                        if (vm.memory) vmInfo += `, Memory: ${vm.memory}`;
                        if (vm.ip) vmInfo += `, IP: ${vm.ip}`;
                        return <li key={vm.vm_id}>{vmInfo}</li>;
                    });
                    setStatus(<div><h3>Running VMs:</h3><ul>{vmList}</ul></div>);
                }
            })
            .catch(error => setStatus(error.response.data.error));
    }

    return (
        <div className='vm-management-container'>
            <h2>VM Management</h2>
            <input
                type="text"
                value={vmId}
                onChange={e => setVmId(e.target.value)}
                placeholder="Enter VM ID"
                required
            />
            <button onClick={startVm} disabled={!vmId}>Start VM</button>
            <button onClick={stopVm} disabled={!vmId}>Stop VM</button>
            <button onClick={deleteVM} disabled={!vmId}>Delete VM</button>
            <button onClick={monitorVm} disabled={!vmId}>Monitor VM</button>
            <button onClick={displayVm}>Display all VMs</button>
            <p>{status}</p>
        </div>
    );
}

export default VmManagement;
