import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ArrowLeftRight, 
  SearchCheck, 
  UploadCloud, 
  BarChart3, 
  ShieldAlert, 
  BookOpen
} from 'lucide-react';

export const Sidebar = () => {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/transactions', label: 'Transactions', icon: ArrowLeftRight },
    { to: '/predict', label: 'Single Prediction', icon: SearchCheck },
    { to: '/upload', label: 'Upload CSV', icon: UploadCloud },
    { to: '/model-performance', label: 'Model Performance', icon: BarChart3 },
    { to: '/documentation', label: 'Documentation', icon: BookOpen },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen sticky top-0">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <div className="p-2.5 bg-blue-600/20 border border-blue-500/30 rounded-xl text-blue-400">
          <ShieldAlert className="w-6 h-6 text-blue-400" />
        </div>
        <div>
          <h1 className="font-bold text-slate-100 text-sm tracking-wide">AML SENTINEL</h1>
          <p className="text-xs text-slate-400">Cross-Border Monitoring</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        <div className="px-3 py-2 text-[11px] font-semibold text-slate-400 tracking-wider uppercase">
          Monitoring & Risk
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 text-xs text-slate-400 space-y-1">
        <div className="flex items-center justify-between text-slate-300 font-medium">
          <span>LightGBM Model</span>
          <span className="text-emerald-400 bg-emerald-400/10 px-1.5 py-0.5 rounded border border-emerald-400/20">Active</span>
        </div>
        <p>Threshold: <span className="font-mono text-slate-300">0.50</span></p>
        <p className="text-[10px] text-slate-400">Precision: 91.67% | Recall: 99.87%</p>
      </div>
    </aside>
  );
};
