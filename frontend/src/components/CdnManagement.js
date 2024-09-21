import React, { useState } from 'react';
import axios from 'axios';
import '../styles/CdnManagement.css';

function CdnManagement() {
    const [fileName, setFileName] = useState('');
    const [status, setStatus] = useState('');
    const [userLocation, setUserLocation] = useState('');

    const uploadToOrigin = () => {
        const fileInput = document.getElementById('file');
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
            setStatus('No file selected');
            return;
        }
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        axios.post(`/upload_to_origin/${file.name}`, formData)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const deleteFromOrigin = () => {
        axios.delete(`/delete_from_origin/${fileName}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const getFile = () => {
        axios.get(`/get_file/${fileName}/${userLocation}`)
            .then(response => {
                const fileData = response.data;
                if (fileData.message) {
                    setStatus(response.data.message)
                } else {
                    const content = fileData.content;
                    const server = fileData.server;
                    setStatus(`
                        <div>
                            <h3>File Content:</h3>
                            <pre>${content}</pre>
                            <h3>Server:</h3>
                            <p>${server}</p>
                        </div>
                    `);
                }
            })
            .catch(error => setStatus(error.response.data.error));
    };

    return (
        <div className="cdn-management-container">
            <h2>CDN Management</h2>
            <label>File: </label>
            <input type="file" id="file" required />
            <button onClick={uploadToOrigin}>Upload to Origin</button>
            <input type="text" value={fileName} onChange={e => setFileName(e.target.value)} placeholder="Enter file name" required />
            <input type="text" value={userLocation} onChange={e => setUserLocation(e.target.value)} placeholder="Enter user location" required />
            <button onClick={getFile} disabled={!fileName || !userLocation}>Get File</button>
            <button onClick={deleteFromOrigin} disabled={!fileName}>Delete from Origin</button>
            <br />
            <div className="status-message" dangerouslySetInnerHTML={{ __html: status }} />
        </div>
    );
}

export default CdnManagement;