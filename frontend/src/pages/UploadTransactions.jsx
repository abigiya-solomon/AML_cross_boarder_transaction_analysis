import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, RefreshCw, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { uploadCSV } from '../services/api';

export const UploadTransactions = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const summary = await uploadCSV(file);
      setResult(summary);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process CSV upload');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-slate-100 tracking-tight">Batch CSV Transaction Upload & Audit</h2>
        <p className="text-xs text-slate-400 mt-1">
          Upload bulk transaction datasets for batch feature engineering and automated LightGBM ML risk scoring
        </p>
      </div>

      {/* Main Upload Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="border-2 border-dashed border-slate-800 hover:border-blue-500/50 rounded-2xl p-8 text-center bg-slate-950/60 transition cursor-pointer relative">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            />
            <UploadCloud className="w-12 h-12 mx-auto text-blue-400 mb-3" />
            <p className="text-sm font-semibold text-slate-200">
              {file ? file.name : 'Click or Drag & Drop transaction CSV file here'}
            </p>
            <p className="text-xs text-slate-500 mt-1">
              Supports standard IBM AML HI-Medium transaction columns
            </p>
          </div>

          {file && (
            <div className="flex items-center justify-between p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs">
              <div className="flex items-center gap-2 text-slate-300 font-mono">
                <FileText className="w-4 h-4 text-blue-400" />
                <span>{file.name} ({(file.size / 1024).toFixed(1)} KB)</span>
              </div>
              <button
                type="submit"
                disabled={loading}
                className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg flex items-center gap-2 transition disabled:opacity-50"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <UploadCloud className="w-4 h-4" />}
                {loading ? 'Processing Batch CSV...' : 'Start Batch Inference'}
              </button>
            </div>
          )}
        </form>

        {error && (
          <div className="p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            {error}
          </div>
        )}

        {/* Upload Result Summary */}
        {result && (
          <div className="bg-slate-950 border border-slate-800 rounded-2xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
                <CheckCircle2 className="w-5 h-5" /> Batch Processing Complete
              </div>
              <span className="text-xs font-mono text-slate-400">{result.filename}</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center py-2">
              <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-xs text-slate-400">Total Rows</span>
                <p className="text-xl font-bold text-slate-100 mt-0.5">{result.total_rows.toLocaleString()}</p>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-xs text-slate-400">Processed</span>
                <p className="text-xl font-bold text-blue-400 mt-0.5">{result.processed_count.toLocaleString()}</p>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-xs text-slate-400">Suspicious Flagged</span>
                <p className="text-xl font-bold text-red-400 mt-0.5">{result.suspicious_count.toLocaleString()}</p>
              </div>
              <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-xs text-slate-400">Suspicious Rate</span>
                <p className="text-xl font-bold text-amber-400 mt-0.5">{result.suspicious_rate}%</p>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => navigate('/transactions')}
                className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition"
              >
                View Processed Transactions in Registry <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* CSV Template Guidance */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Required CSV Headers Checklist</h4>
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto">
          Timestamp, From Bank, Account, To Bank, Account.1, Amount Received, Receiving Currency, Amount Paid, Payment Currency, Payment Format
        </div>
      </div>
    </div>
  );
};
