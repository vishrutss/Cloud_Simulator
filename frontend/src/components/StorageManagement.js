import React, { useState } from 'react';
import axios from 'axios';
import '../styles/StorageManagement.css';

function StorageManagement() {
    const [bucketName, setBucketName] = useState('');
    const [fileName, setFileName] = useState('');
    const [status, setStatus] = useState('');

    const createBucket = () => {
        axios.post(`/create_bucket/${bucketName}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const uploadFile = () => {
        const fileInput = document.getElementById('file');
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
            setStatus('No file selected');
            return;
        }
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        axios.post(`/upload_file/${bucketName}/${file.name}`, formData)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const deleteFile = () => {
        axios.delete(`/delete_file/${bucketName}/${fileName}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    const deleteBucket = () => {
        axios.delete(`/delete_bucket/${bucketName}`)
            .then(response => setStatus(response.data.message))
            .catch(error => setStatus(error.response.data.error));
    };

    return (
        <div className="storage-management-container">
            <h2>Storage Management</h2>
            <label>Bucket Name: </label>
            <input type="text" value={bucketName} onChange={e => setBucketName(e.target.value)} placeholder='Enter bucket name' required />
            <button onClick={createBucket} disabled={!bucketName}>Create Bucket</button>
            <button onClick={deleteBucket} disabled={!bucketName}>Delete Bucket</button>
            <br />
            <label>File: </label>
            <input type="file" id="file" />
            <button onClick={uploadFile}>Upload File</button>
            <input type="text" value={fileName} onChange={e => setFileName(e.target.value)} placeholder="Enter file name" required/>
            <button onClick={deleteFile} disabled={!fileName || !bucketName}>Delete File</button>
            <br />
            <div className="status-message" dangerouslySetInnerHTML={{ __html: status }} />
        </div>
    );
}

export default StorageManagement;