import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import VmManagement from './components/VmManagement';
import StorageManagement from './components/StorageManagement';
import CdnManagement from './components/CdnManagement';

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="App">
              <header className="App-header">
                <h1>Cloud Environment Simulator</h1>
                <Link to="/vm-management">
                  <button>Go to VM Management</button>
                </Link>
                <Link to="/storage-management">
                  <button>Go to Storage Management</button>
                </Link>
                <Link to="/cdn-management">
                  <button>Go to CDN Management</button>
                </Link>
              </header>
            </div>
          }
        />
        <Route path="/vm-management" element={<VmManagement />} />
        <Route path="/storage-management" element={<StorageManagement />} />
        <Route path="/cdn-management" element={<CdnManagement />} />
      </Routes>
    </Router>
  );
}

export default App;
