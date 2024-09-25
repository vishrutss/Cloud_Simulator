import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/VmManagement.css';

function VmManagement() {
    const [vmId, setVmId] = useState('');
    const [status, setStatus] = useState('');
    const [vms, setVms] = useState([]);

    useEffect(() => {
        displayVm();
    }, []);

    const startVm = () => {
        axios.post(`/start_vm/${vmId}`)
            .then(response => {
                setStatus(response.data.message);
                displayVm();
            })
            .catch(error => setStatus(error.response.data.error));
    };

    const stopVm = () => {
        axios.post(`/stop_vm/${vmId}`)
            .then(response => {
                setStatus(response.data.message);
                displayVm();
            })
            .catch(error => setStatus(error.response.data.error));
    };

    const deleteVM = () => {
        axios.delete(`/delete_vm/${vmId}`)
            .then(response => {
                setStatus(response.data.message);
                displayVm();
            })
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
                    setVms([]);
                } else if (vmData.vms && vmData.vms.length > 0) {
                    const vmList = vmData.vms.map(vm => ({
                        id: vm.vm_id,
                        info: `VM ID: ${vm.vm_id}, Status: ${vm.status}` +
                            (vm.pid ? `, PID: ${vm.pid}` : '') +
                            (vm.ip ? `, IP: ${vm.ip}` : '')
                    }));
                    setVms(vmList);
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
            <p>{status}</p>
            <div>
                <h3>Running VMs:</h3>
                <ul>
                    {vms.map(vm => (
                        <li key={vm.id}>{vm.info}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default VmManagement;
