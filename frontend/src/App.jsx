import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';

import { Dashboard } from './pages/Dashboard';
import { Transactions } from './pages/Transactions';
import { SinglePrediction } from './pages/SinglePrediction';
import { UploadTransactions } from './pages/UploadTransactions';
import { ModelPerformance } from './pages/ModelPerformance';
import { Documentation } from './pages/Documentation';

export function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-slate-950 text-slate-100">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="flex-1 p-6 overflow-y-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/transactions" element={<Transactions />} />
              <Route path="/predict" element={<SinglePrediction />} />
              <Route path="/upload" element={<UploadTransactions />} />
              <Route path="/model-performance" element={<ModelPerformance />} />
              <Route path="/documentation" element={<Documentation />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
