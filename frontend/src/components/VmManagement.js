import React, { useState } from 'react';
import axios from 'axios';

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

    return (
        <div>
            <input
                type="text"
                value={vmId}
                onChange={e => setVmId(e.target.value)}
                placeholder="Enter VM ID"
                required
            />
            <button onClick={startVm} disabled={!vmId}>Start VM</button>
            <button onClick={stopVm} disabled={!vmId}>Stop VM</button>
            <p>{status}</p>
        </div>
    );
}

export default VmManagement;
