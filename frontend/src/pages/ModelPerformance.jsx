import React, { useState, useEffect } from 'react';
import { BarChart3, CheckCircle2, ShieldCheck, AlertCircle, Cpu, Award } from 'lucide-react';
import { getModelInfo } from '../services/api';

export const ModelPerformance = () => {
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    getModelInfo().then(setModelInfo).catch(console.error);
  }, []);

  const metrics = modelInfo?.evaluation_metrics || {
    precision: 0.9167,
    recall: 0.9987,
    f1_score: 0.9559,
    roc_auc: 0.9659,
    pr_auc: 0.9673,
    threshold: 0.50,
  };

  const cm = modelInfo?.confusion_matrix || {
    true_negatives: 473,
    false_positives: 71,
    false_negatives: 1,
    true_positives: 781,
    total_test_samples: 1326,
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
            <Award className="w-4 h-4" /> Selected Model Evaluation
          </div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">LightGBM Performance & Benchmark Validation</h2>
          <p className="text-xs text-slate-400 mt-1">
            Official test set evaluation results on unseen chronological test period (Sept 21–28)
          </p>
        </div>
        <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-400 font-semibold flex items-center gap-2 self-start md:self-auto">
          <ShieldCheck className="w-4 h-4" /> Selected Production Classifier
        </div>
      </div>

      {/* Key Metric Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 text-center">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">Precision</span>
          <p className="text-2xl font-extrabold text-blue-400">{(metrics.precision * 100).toFixed(2)}%</p>
          <span className="text-[10px] text-slate-500 block">TP / (TP + FP)</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">Recall</span>
          <p className="text-2xl font-extrabold text-emerald-400">{(metrics.recall * 100).toFixed(2)}%</p>
          <span className="text-[10px] text-slate-500 block">TP / (TP + FN)</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">F1 Score</span>
          <p className="text-2xl font-extrabold text-purple-400">{(metrics.f1_score * 100).toFixed(2)}%</p>
          <span className="text-[10px] text-slate-500 block">Harmonic Mean</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">ROC-AUC</span>
          <p className="text-2xl font-extrabold text-amber-400">{(metrics.roc_auc * 100).toFixed(2)}%</p>
          <span className="text-[10px] text-slate-500 block">Discriminative ability</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">PR-AUC</span>
          <p className="text-2xl font-extrabold text-red-400">{(metrics.pr_auc * 100).toFixed(2)}%</p>
          <span className="text-[10px] text-slate-500 block">Imbalanced class ranking</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">Threshold</span>
          <p className="text-2xl font-extrabold text-slate-100 font-mono">{metrics.threshold.toFixed(2)}</p>
          <span className="text-[10px] text-slate-500 block">Fixed decision boundary</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Confusion Matrix Card */}
        <div className="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-blue-400" /> Final Test Confusion Matrix
          </h3>

          <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="grid grid-cols-3 text-center text-xs font-semibold">
              <div></div>
              <div className="text-slate-400 pb-2">Predicted Normal</div>
              <div className="text-slate-400 pb-2">Predicted Suspicious</div>
            </div>

            {/* Actual Normal Row */}
            <div className="grid grid-cols-3 gap-3 items-center text-center">
              <div className="text-slate-400 text-xs font-semibold text-left">Actual Normal</div>
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
                <span className="text-xs text-emerald-400 block font-semibold">TN</span>
                <span className="text-xl font-bold text-slate-100 font-mono">{cm.true_negatives}</span>
              </div>
              <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl">
                <span className="text-xs text-amber-400 block font-semibold">FP</span>
                <span className="text-xl font-bold text-slate-100 font-mono">{cm.false_positives}</span>
              </div>
            </div>

            {/* Actual Suspicious Row */}
            <div className="grid grid-cols-3 gap-3 items-center text-center">
              <div className="text-slate-400 text-xs font-semibold text-left">Actual Suspicious</div>
              <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
                <span className="text-xs text-red-400 block font-semibold">FN</span>
                <span className="text-xl font-bold text-slate-100 font-mono">{cm.false_negatives}</span>
              </div>
              <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl">
                <span className="text-xs text-blue-400 block font-semibold">TP</span>
                <span className="text-xl font-bold text-slate-100 font-mono">{cm.true_positives}</span>
              </div>
            </div>
          </div>

          <div className="text-xs text-slate-400 space-y-1.5 pt-2">
            <p><span className="font-semibold text-slate-200">Recall Insight:</span> Detected 781 out of 782 total laundering cases (99.87%), missing only 1 single laundering transaction (FN=1).</p>
            <p><span className="font-semibold text-slate-200">Precision Insight:</span> Correctly identified laundering 91.67% of the time when flagging suspicious activity.</p>
          </div>
        </div>

        {/* Model Selection Benchmark List */}
        <div className="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-400" /> Benchmark Classifier Comparison
          </h3>
          <p className="text-xs text-slate-400">
            LightGBM was selected after 5-fold chronological cross-validation across 7 candidate algorithms:
          </p>

          <div className="space-y-2">
            {[
              { name: 'LightGBM', selected: true, reason: 'Selected (Highest PR-AUC: 96.73%, Recall: 99.87%)' },
              { name: 'HistGradientBoosting', selected: false, reason: 'High ROC-AUC, but lower PR-AUC than LightGBM' },
              { name: 'Random Forest', selected: false, reason: 'Strong baseline, lower recall on temporal shift' },
              { name: 'Extra Trees', selected: false, reason: 'Competitive F1 score, overfit on training history' },
              { name: 'XGBoost', selected: false, reason: 'Good precision, slightly higher variance across folds' },
              { name: 'CatBoost', selected: false, reason: 'Strong categorical handling, slower inference latency' },
              { name: 'Logistic Regression', selected: false, reason: 'Linear baseline, underfitted complex interaction terms' },
            ].map((m) => (
              <div
                key={m.name}
                className={`p-3 rounded-xl border flex items-center justify-between text-xs ${
                  m.selected
                    ? 'bg-blue-600/10 border-blue-500/40 text-slate-100 font-medium'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400'
                }`}
              >
                <div className="flex items-center gap-2">
                  <CheckCircle2 className={`w-4 h-4 ${m.selected ? 'text-blue-400' : 'text-slate-600'}`} />
                  <span className="font-bold">{m.name}</span>
                </div>
                <span className="text-[11px] text-slate-400">{m.reason}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
