import React from 'react';

export const StatCard = ({ title, value, subtitle, icon: Icon, color = 'blue' }) => {
  const colorStyles = {
    blue: 'bg-blue-500/10 border-blue-500/20 text-blue-400',
    red: 'bg-red-500/10 border-red-500/20 text-red-400',
    amber: 'bg-amber-500/10 border-amber-500/20 text-amber-400',
    emerald: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400',
    purple: 'bg-purple-500/10 border-purple-500/20 text-purple-400',
  };

  const style = colorStyles[color] || colorStyles.blue;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm hover:border-slate-700 transition">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2 rounded-lg border ${style}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-3">
        <div className="text-2xl font-bold text-slate-100 tracking-tight">{value}</div>
        {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
};
