import React from 'react';
import { BookOpen, ShieldCheck, Database, GitBranch, Layers, Lock } from 'lucide-react';

export const Documentation = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto text-slate-200">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-slate-100 tracking-tight">AML System Documentation & ML Architecture</h2>
        <p className="text-xs text-slate-400 mt-1">
          Technical specifications, anti-data-leakage rules, and inference pipeline design
        </p>
      </div>

      {/* Cards */}
      <div className="space-y-6 text-sm">
        {/* Anti-Data Leakage Rule */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 text-amber-400 font-bold uppercase tracking-wider text-xs">
            <Lock className="w-4 h-4" /> 1. Critical Anti-Data-Leakage Rule (Temporal Boundaries)
          </div>
          <p className="text-slate-300 leading-relaxed text-xs">
            The dataset intentionally uses strict chronological partitioning:
          </p>
          <div className="grid grid-cols-3 gap-3 text-xs font-mono text-center my-3">
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-blue-400 font-bold block">Training</span>
              <span className="text-slate-400">Sept 1 – Sept 16</span>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-amber-400 font-bold block">Validation</span>
              <span className="text-slate-400">Sept 17 – Sept 20</span>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-emerald-400 font-bold block">Test</span>
              <span className="text-slate-400">Sept 21 – Sept 28</span>
            </div>
          </div>
          <p className="text-slate-400 text-xs leading-relaxed">
            All sender, receiver, and relationship historical behavioral features are derived exclusively from the training period. Future transaction data is strictly prohibited from leaking into historical feature aggregations.
          </p>
        </div>

        {/* Account Composite Key */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 text-blue-400 font-bold uppercase tracking-wider text-xs">
            <Database className="w-4 h-4" /> 2. Account Identification & Composite Keys
          </div>
          <p className="text-slate-300 text-xs leading-relaxed">
            Account number alone is not globally unique across banks. The effective account identity is:
          </p>
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl font-mono text-xs text-blue-400">
            Account Key = Bank ID + "_" + Account Number
          </div>
          <p className="text-slate-400 text-xs">
            Sender account key: <span className="font-mono text-slate-300">From Bank + Account</span> | Receiver account key: <span className="font-mono text-slate-300">To Bank + Account.1</span>
          </p>
        </div>

        {/* Feature Pipeline */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 text-purple-400 font-bold uppercase tracking-wider text-xs">
            <Layers className="w-4 h-4" /> 3. Feature Pipeline & One-Hot Encoding Consistency
          </div>
          <p className="text-slate-300 text-xs leading-relaxed">
            Raw transactions produce 43 engineered input features (39 numeric + 4 categorical). The preprocessor transforms them into 80 one-hot feature columns stored in <span className="font-mono text-slate-200">processed_feature_names.pkl</span>.
          </p>
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-[11px] text-slate-400 space-y-1">
            <p>Raw Input &rarr; 43 Engineered Features &rarr; SimpleImputer &amp; StandardScaler &amp; OneHotEncoder &rarr; 80 Columns DataFrame &rarr; LightGBM.predict_proba()</p>
          </div>
        </div>

        {/* Fixed Threshold */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 text-emerald-400 font-bold uppercase tracking-wider text-xs">
            <ShieldCheck className="w-4 h-4" /> 4. Classification Threshold
          </div>
          <p className="text-slate-300 text-xs leading-relaxed">
            The application enforces a fixed threshold of <span className="font-mono font-bold text-slate-100">0.50</span>. Transactions with suspicious probability &ge; 0.50 are classified as <span className="text-red-400 font-bold">SUSPICIOUS</span>.
          </p>
        </div>
      </div>
    </div>
  );
};
