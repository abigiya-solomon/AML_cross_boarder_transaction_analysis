import React, { useState } from 'react';
import { SearchCheck, ShieldAlert, Sparkles, RefreshCw, CheckCircle2, AlertOctagon } from 'lucide-react';
import { predictSingle } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export const SinglePrediction = () => {
  const [formData, setFormData] = useState({
    timestamp: '2022-09-21 12:30:00',
    from_bank: 20,
    account: '100234',
    to_bank: 3196,
    receiver_account: '884129',
    amount_received: 15000.0,
    receiving_currency: 'US Dollar',
    amount_paid: 15000.0,
    payment_currency: 'US Dollar',
    payment_format: 'Wire',
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name.includes('bank') || name.includes('amount') ? (value === '' ? '' : Number(value)) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictSingle(formData);
      setResult(res);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-slate-100 tracking-tight">Manual Single Transaction Inference</h2>
        <p className="text-xs text-slate-400 mt-1">
          Enter raw transaction attributes to compute feature engineering and LightGBM suspiciousness probability
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Input Form */}
        <div className="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <SearchCheck className="w-4 h-4 text-blue-400" /> Transaction Inputs
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Timestamp (YYYY-MM-DD HH:MM:SS)</label>
              <input
                type="text"
                name="timestamp"
                value={formData.timestamp}
                onChange={handleChange}
                required
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1">From Bank ID</label>
                <input
                  type="number"
                  name="from_bank"
                  value={formData.from_bank}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Sender Account</label>
                <input
                  type="text"
                  name="account"
                  value={formData.account}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1">To Bank ID</label>
                <input
                  type="number"
                  name="to_bank"
                  value={formData.to_bank}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Receiver Account</label>
                <input
                  type="text"
                  name="receiver_account"
                  value={formData.receiver_account}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1">Amount Paid</label>
                <input
                  type="number"
                  name="amount_paid"
                  value={formData.amount_paid}
                  onChange={handleChange}
                  required
                  step="any"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Amount Received</label>
                <input
                  type="number"
                  name="amount_received"
                  value={formData.amount_received}
                  onChange={handleChange}
                  required
                  step="any"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-400 block mb-1">Payment Currency</label>
                <select
                  name="payment_currency"
                  value={formData.payment_currency}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
                >
                  <option value="US Dollar">US Dollar</option>
                  <option value="UK Pound">UK Pound</option>
                  <option value="Euro">Euro</option>
                  <option value="Bitcoin">Bitcoin</option>
                  <option value="Swiss Franc">Swiss Franc</option>
                  <option value="Canadian Dollar">Canadian Dollar</option>
                </select>
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Receiving Currency</label>
                <select
                  name="receiving_currency"
                  value={formData.receiving_currency}
                  onChange={handleChange}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
                >
                  <option value="US Dollar">US Dollar</option>
                  <option value="UK Pound">UK Pound</option>
                  <option value="Euro">Euro</option>
                  <option value="Bitcoin">Bitcoin</option>
                  <option value="Swiss Franc">Swiss Franc</option>
                  <option value="Canadian Dollar">Canadian Dollar</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Payment Format</label>
              <select
                name="payment_format"
                value={formData.payment_format}
                onChange={handleChange}
                className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
              >
                <option value="Wire">Wire</option>
                <option value="ACH">ACH</option>
                <option value="Cash">Cash</option>
                <option value="Cheque">Cheque</option>
                <option value="Credit Card">Credit Card</option>
                <option value="Bitcoin">Bitcoin</option>
                <option value="Reinvestment">Reinvestment</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition disabled:opacity-50 mt-4"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              {loading ? 'Executing ML Inference...' : 'Run AML Risk Assessment'}
            </button>
          </form>
        </div>

        {/* Prediction Results Panel */}
        <div className="lg:col-span-6 space-y-6">
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl text-xs flex items-center gap-2">
              <AlertOctagon className="w-4 h-4 flex-shrink-0" />
              {error}
            </div>
          )}

          {result ? (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-base font-bold text-slate-100">Inference Assessment Output</h3>
                  <p className="text-xs text-slate-400">Processed through fitted ColumnTransformer & LightGBM</p>
                </div>
                <RiskBadge riskLevel={result.risk_level} label={result.label} />
              </div>

              {/* Large Probability Display */}
              <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-3">
                <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Suspicious Risk Probability</span>
                <div className="text-4xl font-extrabold text-slate-100 tracking-tight">
                  {(result.probability * 100).toFixed(2)}%
                </div>
                <div className="h-3 w-full bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700 max-w-md mx-auto">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      result.prediction === 1 ? 'bg-gradient-to-r from-amber-500 to-red-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${(result.probability * 100).toFixed(2)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-slate-400">
                  Classification: <span className={`font-bold ${result.prediction === 1 ? 'text-red-400' : 'text-emerald-400'}`}>{result.label.toUpperCase()}</span> (Threshold: 0.50)
                </p>
              </div>

              {/* Behavioral Features Breakdown */}
              {result.engineered_features && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Derived Behavioral Features (43 Inputs)
                  </h4>
                  <div className="bg-slate-950 border border-slate-800 rounded-xl p-3 max-h-64 overflow-y-auto grid grid-cols-2 gap-2 text-[11px] font-mono">
                    {Object.entries(result.engineered_features).map(([k, v]) => (
                      <div key={k} className="p-2 bg-slate-900/60 rounded border border-slate-800/80">
                        <span className="text-slate-400 block truncate">{k}</span>
                        <span className="text-slate-200 font-semibold truncate block">
                          {typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(4)) : String(v)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center text-slate-400 space-y-3">
              <SearchCheck className="w-10 h-10 mx-auto text-slate-600" />
              <h4 className="text-sm font-semibold text-slate-300">Ready for Inference</h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Fill out the transaction inputs on the left and click "Run AML Risk Assessment" to view LightGBM probability and feature breakdowns.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
