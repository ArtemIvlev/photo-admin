import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PhotoTree from './components/PhotoTree';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Photo Admin</h1>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<PhotoTree />} />
        </Routes>
      </main>
    </div>
  );
}

export default App; 