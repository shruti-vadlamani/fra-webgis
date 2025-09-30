import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Upload from './components/Upload';
import FRAClaims from './components/FRAClaims';
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
          <Route path="/fra-claims" element={<FRAClaims />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
