import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import VmManagementPage from './components/VmManagementPage';

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
              </header>
            </div>
          } 
        />
        <Route path="/vm-management" element={<VmManagementPage />} />
      </Routes>
    </Router>
  );
}

export default App;
