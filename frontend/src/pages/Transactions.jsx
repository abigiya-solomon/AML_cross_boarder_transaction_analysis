import React, { useState, useEffect } from 'react';
import { Search, Filter, ArrowUpDown, ChevronLeft, ChevronRight, RefreshCw, Eye } from 'lucide-react';
import { RiskBadge } from '../components/RiskBadge';
import { TransactionDetailModal } from '../components/TransactionDetailModal';
import { getTransactions, getTransactionDetail } from '../services/api';

export const Transactions = () => {
  const [data, setData] = useState({ items: [], total: 0, skip: 0, limit: 20 });
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [suspiciousOnly, setSuspiciousOnly] = useState(false);
  const [riskLevel, setRiskLevel] = useState('ALL');
  const [currency, setCurrency] = useState('ALL');
  const [paymentFormat, setPaymentFormat] = useState('ALL');
  const [sortBy, setSortBy] = useState('timestamp');
  const [sortOrder, setSortOrder] = useState('desc');
  const [page, setPage] = useState(1);
  const [selectedTxDetail, setSelectedTxDetail] = useState(null);

  const limit = 15;

  const loadTransactions = async () => {
    setLoading(true);
    try {
      const skip = (page - 1) * limit;
      const res = await getTransactions({
        skip,
        limit,
        suspicious_only: suspiciousOnly,
        risk_level: riskLevel,
        currency,
        payment_format: paymentFormat,
        search: search || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setData(res);
    } catch (err) {
      console.error('Error loading transactions', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTransactions();
  }, [page, suspiciousOnly, riskLevel, currency, paymentFormat, sortBy, sortOrder]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadTransactions();
  };

  const handleRowClick = async (id) => {
    try {
      const detail = await getTransactionDetail(id);
      setSelectedTxDetail(detail);
    } catch (err) {
      console.error('Error fetching transaction detail', err);
    }
  };

  const totalPages = Math.ceil(data.total / limit) || 1;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Transaction Monitoring Registry</h2>
          <p className="text-xs text-slate-400 mt-1">
            Browse, filter, and audit cross-border transactions evaluated by the LightGBM ML model
          </p>
        </div>
        <button
          onClick={loadTransactions}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Refresh Table
        </button>
      </div>

      {/* Filter Control Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search account numbers or Bank IDs..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-xl transition"
          >
            Search
          </button>
        </form>

        {/* Dropdown Filters */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 pt-2 border-t border-slate-800/60 text-xs">
          {/* Suspicious Only Checkbox */}
          <label className="flex items-center gap-2 bg-slate-950 border border-slate-800 px-3 py-2 rounded-xl cursor-pointer hover:border-slate-700 transition">
            <input
              type="checkbox"
              checked={suspiciousOnly}
              onChange={(e) => { setSuspiciousOnly(e.target.checked); setPage(1); }}
              className="rounded bg-slate-900 border-slate-700 text-blue-600 focus:ring-0"
            />
            <span className="font-semibold text-red-400">Suspicious Only</span>
          </label>

          {/* Risk Level Filter */}
          <div>
            <select
              value={riskLevel}
              onChange={(e) => { setRiskLevel(e.target.value); setPage(1); }}
              className="w-full bg-slate-950 border border-slate-800 text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="LOW">Low Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="HIGH">High Risk</option>
              <option value="CRITICAL">Critical Risk</option>
            </select>
          </div>

          {/* Currency Filter */}
          <div>
            <select
              value={currency}
              onChange={(e) => { setCurrency(e.target.value); setPage(1); }}
              className="w-full bg-slate-950 border border-slate-800 text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
            >
              <option value="ALL">All Currencies</option>
              <option value="US Dollar">US Dollar</option>
              <option value="UK Pound">UK Pound</option>
              <option value="Euro">Euro</option>
              <option value="Bitcoin">Bitcoin</option>
              <option value="Swiss Franc">Swiss Franc</option>
              <option value="Canadian Dollar">Canadian Dollar</option>
            </select>
          </div>

          {/* Payment Format Filter */}
          <div>
            <select
              value={paymentFormat}
              onChange={(e) => { setPaymentFormat(e.target.value); setPage(1); }}
              className="w-full bg-slate-950 border border-slate-800 text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
            >
              <option value="ALL">All Formats</option>
              <option value="Wire">Wire Transfer</option>
              <option value="ACH">ACH</option>
              <option value="Cash">Cash</option>
              <option value="Cheque">Cheque</option>
              <option value="Credit Card">Credit Card</option>
              <option value="Bitcoin">Bitcoin</option>
              <option value="Reinvestment">Reinvestment</option>
            </select>
          </div>

          {/* Sort By */}
          <div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500"
            >
              <option value="timestamp">Sort: Timestamp</option>
              <option value="probability">Sort: Risk Probability</option>
              <option value="amount">Sort: Amount</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3.5">ID / Timestamp</th>
                <th className="p-3.5">Sender (From Bank : Account)</th>
                <th className="p-3.5">Receiver (To Bank : Account.1)</th>
                <th className="p-3.5">Amount Paid</th>
                <th className="p-3.5">Format</th>
                <th className="p-3.5">Probability</th>
                <th className="p-3.5">Risk Level</th>
                <th className="p-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {loading ? (
                <tr>
                  <td colSpan={8} className="p-8 text-center text-slate-400">
                    <RefreshCw className="w-5 h-5 animate-spin mx-auto mb-2 text-blue-500" />
                    Fetching transaction records...
                  </td>
                </tr>
              ) : data.items.length === 0 ? (
                <tr>
                  <td colSpan={8} className="p-8 text-center text-slate-400">
                    No transactions match your current search and filter criteria.
                  </td>
                </tr>
              ) : (
                data.items.map((tx) => (
                  <tr
                    key={tx.id}
                    onClick={() => handleRowClick(tx.id)}
                    className="hover:bg-slate-800/60 cursor-pointer transition"
                  >
                    <td className="p-3.5 text-slate-300">
                      <div className="font-semibold text-slate-200">#{tx.id}</div>
                      <div className="text-[11px] text-slate-500 font-sans">{tx.timestamp}</div>
                    </td>
                    <td className="p-3.5 text-slate-300">
                      <span className="text-blue-400 font-medium">Bank {tx.from_bank}</span> : {tx.account}
                    </td>
                    <td className="p-3.5 text-slate-300">
                      <span className="text-emerald-400 font-medium">Bank {tx.to_bank}</span> : {tx.receiver_account}
                    </td>
                    <td className="p-3.5 font-semibold text-slate-100">
                      {tx.amount_paid.toLocaleString()} {tx.payment_currency}
                    </td>
                    <td className="p-3.5 text-slate-400 font-sans">{tx.payment_format}</td>
                    <td className="p-3.5 font-bold text-slate-100">
                      {(tx.probability * 100).toFixed(2)}%
                    </td>
                    <td className="p-3.5 font-sans">
                      <RiskBadge riskLevel={tx.risk_level} label={tx.label} />
                    </td>
                    <td className="p-3.5 text-right font-sans">
                      <button className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition">
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-slate-800 bg-slate-950 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
          <div>
            Showing <span className="font-semibold text-slate-200">{data.items.length}</span> of <span className="font-semibold text-slate-200">{data.total}</span> records
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page === 1}
              className="p-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-3 py-1 font-mono text-slate-300">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page >= totalPages}
              className="p-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Detailed Investigator Modal */}
      {selectedTxDetail && (
        <TransactionDetailModal
          detail={selectedTxDetail}
          onClose={() => setSelectedTxDetail(null)}
        />
      )}
    </div>
  );
};
