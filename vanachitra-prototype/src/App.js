import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Upload from './components/Upload';
import './styles.css';
import './upload.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
