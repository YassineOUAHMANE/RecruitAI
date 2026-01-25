import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import CandidateUpload from './pages/CandidateUpload';
import HRPanel from './pages/HRPanel';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/candidate" element={<CandidateUpload />} />
        <Route path="/hrpanel" element={<HRPanel />} />
        <Route path="/" element={<Navigate to="/candidate" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;