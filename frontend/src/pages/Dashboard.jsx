import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  ArrowLeftRight, 
  Percent, 
  AlertTriangle, 
  TrendingUp, 
  Building2, 
  RefreshCw,
  Search
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';
import { StatCard } from '../components/StatCard';
import { RiskBadge } from '../components/RiskBadge';
import { TransactionDetailModal } from '../components/TransactionDetailModal';
import { getDashboardStats, getTransactions, getTransactionDetail } from '../services/api';

const COLORS = ['#10b981', '#f59e0b', '#f97316', '#ef4444'];

export const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentTx, setRecentTx] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTxDetail, setSelectedTxDetail] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const statsRes = await getDashboardStats();
      const txRes = await getTransactions({ limit: 8, sort_by: 'timestamp', sort_order: 'desc' });
      setStats(statsRes);
      setRecentTx(txRes.items || []);
    } catch (err) {
      console.error('Failed to load dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRowClick = async (id) => {
    try {
      const detail = await getTransactionDetail(id);
      setSelectedTxDetail(detail);
    } catch (err) {
      console.error('Error fetching transaction detail', err);
    }
  };

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mr-2 text-blue-500" /> Loading AML Dashboard Analytics...
      </div>
    );
  }

  const kpis = stats?.kpis || {
    total_transactions: 0,
    suspicious_transactions: 0,
    suspicious_rate: 0,
    average_risk_probability: 0,
    high_risk_transactions: 0,
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">AML Transaction Monitoring Dashboard</h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time inference pipeline powered by LightGBM model (Threshold = 0.50)
          </p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Refresh Analytics
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Transactions"
          value={kpis.total_transactions.toLocaleString()}
          subtitle="Processed in database"
          icon={ArrowLeftRight}
          color="blue"
        />
        <StatCard
          title="Suspicious Transactions"
          value={kpis.suspicious_transactions.toLocaleString()}
          subtitle="Flagged by LightGBM"
          icon={ShieldAlert}
          color="red"
        />
        <StatCard
          title="Suspicious Rate"
          value={`${kpis.suspicious_rate}%`}
          subtitle="Relative laundering ratio"
          icon={Percent}
          color="amber"
        />
        <StatCard
          title="Avg Risk Probability"
          value={`${(kpis.average_risk_probability * 100).toFixed(2)}%`}
          subtitle="Average model score"
          icon={TrendingUp}
          color="purple"
        />
        <StatCard
          title="High Risk Alerts"
          value={kpis.high_risk_transactions.toLocaleString()}
          subtitle="Risk score ≥ 0.70"
          icon={AlertTriangle}
          color="emerald"
        />
      </div>

      {/* Time-Series Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Suspicious Transactions Over Time */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-200">Suspicious Transactions Over Time</h3>
              <p className="text-xs text-slate-400">Daily laundering counts detected</p>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20 font-medium">
              Temporal Trend
            </span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.suspicious_over_time || []}>
                <defs>
                  <linearGradient id="colorSusp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Area type="monotone" dataKey="suspicious" stroke="#ef4444" fillOpacity={1} fill="url(#colorSusp)" name="Suspicious Tx" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Transaction Volume Over Time */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-200">Total Volume Over Time</h3>
              <p className="text-xs text-slate-400">Overall transaction volume breakdown</p>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
              Activity Stream
            </span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.volume_over_time || []}>
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Area type="monotone" dataKey="total" stroke="#3b82f6" fillOpacity={1} fill="url(#colorTotal)" name="Total Tx" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Distribution Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Payment Format Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-200">Payment Format Distribution</h3>
          <div className="h-52 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.payment_format_distribution || []} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" fontSize={10} />
                <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={10} width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} name="Total" />
                <Bar dataKey="suspicious_count" fill="#ef4444" radius={[0, 4, 4, 0]} name="Suspicious" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Currency Distribution */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-200">Receiving Currency Volume</h3>
          <div className="h-52 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.currency_distribution || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={9} interval={0} angle={-30} textAnchor="end" />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Total" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution Pie */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-200">Risk Severity Levels</h3>
          <div className="h-52 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.risk_distribution || []}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={75}
                  paddingAngle={4}
                >
                  {(stats?.risk_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Transactions Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-200">Recent Monitored Transactions</h3>
            <p className="text-xs text-slate-400">Click any row to inspect engineered features and model inference rationale</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider font-semibold">
              <tr>
                <th className="p-3">Timestamp</th>
                <th className="p-3">Sender</th>
                <th className="p-3">Receiver</th>
                <th className="p-3">Amount</th>
                <th className="p-3">Format</th>
                <th className="p-3">Probability</th>
                <th className="p-3">Risk Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {recentTx.map((tx) => (
                <tr
                  key={tx.id}
                  onClick={() => handleRowClick(tx.id)}
                  className="hover:bg-slate-800/60 cursor-pointer transition"
                >
                  <td className="p-3 text-slate-300">{tx.timestamp}</td>
                  <td className="p-3 text-slate-300">Bank {tx.from_bank} / Acc {tx.account}</td>
                  <td className="p-3 text-slate-300">Bank {tx.to_bank} / Acc {tx.receiver_account}</td>
                  <td className="p-3 font-semibold text-slate-100">{tx.amount_paid.toLocaleString()} {tx.payment_currency}</td>
                  <td className="p-3 text-slate-400 font-sans">{tx.payment_format}</td>
                  <td className="p-3 font-bold text-slate-100">{(tx.probability * 100).toFixed(2)}%</td>
                  <td className="p-3 font-sans">
                    <RiskBadge riskLevel={tx.risk_level} label={tx.label} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
