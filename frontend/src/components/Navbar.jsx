import React, { useState, useEffect } from 'react';
import { ShieldCheck, Activity, Clock } from 'lucide-react';
import { getHealth } from '../services/api';

export const Navbar = () => {
  const [health, setHealth] = useState({ status: 'checking', model_loaded: false, model: 'LightGBM' });
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: 'unhealthy', model_loaded: false, model: 'LightGBM' }));

    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <h2 className="text-sm font-semibold text-slate-200">AML Transaction Monitoring Platform</h2>
        <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
          Production ML Pipeline
        </span>
      </div>

      <div className="flex items-center gap-6 text-xs text-slate-400">
        {/* System Health */}
        <div className="flex items-center gap-2">
          <Activity className="w-3.5 h-3.5 text-blue-400" />
          <span>Status:</span>
          {health.status === 'healthy' ? (
            <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
              <ShieldCheck className="w-3.5 h-3.5" /> Healthy
            </span>
          ) : (
            <span className="text-red-400 font-medium">Offline</span>
          )}
        </div>

        {/* Current UTC Clock */}
        <div className="flex items-center gap-1.5 font-mono text-slate-300">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{currentTime.toISOString().replace('T', ' ').substring(0, 19)} UTC</span>
        </div>
      </div>
    </header>
  );
};
