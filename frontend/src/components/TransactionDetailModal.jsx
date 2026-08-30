import React from 'react';
import { X, ShieldAlert, ArrowRight, Building2, User, DollarSign, Calendar, Info } from 'lucide-react';
import { RiskBadge } from './RiskBadge';

export const TransactionDetailModal = ({ detail, onClose }) => {
  if (!detail) return null;

  const { transaction, model_result, engineered_features } = detail;
  const probPercent = (model_result.probability * 100).toFixed(2);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-100">Transaction Investigation #{transaction.id}</h3>
              <p className="text-xs text-slate-400">{transaction.timestamp}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {/* Model Classification Header Card */}
          <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Model Risk Assessment</span>
              <div className="flex items-center gap-3 mt-1.5">
                <span className="text-2xl font-extrabold text-slate-100">{probPercent}%</span>
                <RiskBadge riskLevel={model_result.risk_level} label={model_result.label} />
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Threshold: <span className="font-mono text-slate-300">0.50</span> | Model: <span className="text-slate-300">{model_result.model_name} v{model_result.model_version}</span>
              </p>
            </div>

            {/* Visual Probability Bar */}
            <div className="w-full md:w-64 space-y-1.5">
              <div className="flex justify-between text-xs text-slate-400 font-medium">
                <span>Normal</span>
                <span>Suspicious</span>
              </div>
              <div className="h-3 w-full bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    model_result.prediction === 1 ? 'bg-gradient-to-r from-amber-500 to-red-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${probPercent}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Raw Transaction Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Sender Box */}
            <div className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <User className="w-4 h-4 text-blue-400" /> Sender Information
              </div>
              <div className="space-y-1.5 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Bank ID:</span>
                  <span className="font-mono text-slate-200 font-medium">{transaction.from_bank}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Account Number:</span>
                  <span className="font-mono text-slate-200 font-medium">{transaction.account}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Amount Paid:</span>
                  <span className="font-mono text-slate-200 font-semibold">{transaction.amount_paid.toLocaleString()} {transaction.payment_currency}</span>
                </div>
              </div>
            </div>

            {/* Receiver Box */}
            <div className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <Building2 className="w-4 h-4 text-emerald-400" /> Receiver Information
              </div>
              <div className="space-y-1.5 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Bank ID:</span>
                  <span className="font-mono text-slate-200 font-medium">{transaction.to_bank}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Account Number:</span>
                  <span className="font-mono text-slate-200 font-medium">{transaction.receiver_account}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Amount Received:</span>
                  <span className="font-mono text-slate-200 font-semibold">{transaction.amount_received.toLocaleString()} {transaction.receiving_currency}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Format & Method */}
          <div className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-amber-400" />
              <span className="text-slate-400">Payment Format:</span>
              <span className="font-semibold text-slate-200">{transaction.payment_format}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-slate-400">Cross-Border Transfer:</span>
              <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${
                transaction.from_bank !== transaction.to_bank ? 'bg-blue-500/10 text-blue-400 border-blue-500/30' : 'bg-slate-800 text-slate-300 border-slate-700'
              }`}>
                {transaction.from_bank !== transaction.to_bank ? 'Yes (Inter-bank)' : 'No (Intra-bank)'}
              </span>
            </div>
          </div>

          {/* Engineered Features Breakdown */}
          {engineered_features && (
            <div className="space-y-3">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Info className="w-4 h-4 text-blue-400" /> Engineered Model Features (Inference Inputs)
              </h4>
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 grid grid-cols-2 md:grid-cols-3 gap-3 text-xs">
                {Object.entries(engineered_features).map(([key, val]) => (
                  <div key={key} className="p-2.5 bg-slate-900/60 border border-slate-800/60 rounded-lg">
                    <span className="text-slate-400 block truncate">{key}</span>
                    <span className="font-mono font-semibold text-slate-200 text-sm mt-0.5 block truncate">
                      {typeof val === 'number' ? (Number.isInteger(val) ? val : val.toFixed(4)) : String(val)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/90 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium rounded-xl transition"
          >
            Close Investigation
          </button>
        </div>
      </div>
    </div>
  );
};
