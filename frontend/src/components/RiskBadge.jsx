import React from 'react';

export const RiskBadge = ({ riskLevel, label }) => {
  const level = (riskLevel || '').toUpperCase();
  const isSuspicious = label === 'Suspicious';

  let bgClass = 'bg-slate-800 text-slate-300 border-slate-700';
  let dotClass = 'bg-slate-400';

  if (level === 'CRITICAL' || isSuspicious) {
    bgClass = 'bg-red-500/10 text-red-400 border-red-500/30';
    dotClass = 'bg-red-500 animate-pulse';
  } else if (level === 'HIGH') {
    bgClass = 'bg-orange-500/10 text-orange-400 border-orange-500/30';
    dotClass = 'bg-orange-500';
  } else if (level === 'MEDIUM') {
    bgClass = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    dotClass = 'bg-amber-500';
  } else if (level === 'LOW' || label === 'Normal') {
    bgClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    dotClass = 'bg-emerald-500';
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${bgClass}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotClass}`}></span>
      {riskLevel ? `${riskLevel} RISK` : label}
    </span>
  );
};
