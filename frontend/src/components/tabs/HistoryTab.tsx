import React, { useState, useEffect } from 'react';
import type { HistoricalAuditItem } from '../../types/audit';
import { History, ArrowRight, BarChart2, Calendar, Globe, RefreshCw } from 'lucide-react';

interface HistoryTabProps {
  onLoadAudit: (id: number) => void;
}

export const HistoryTab: React.FC<HistoryTabProps> = ({ onLoadAudit }) => {
  const [history, setHistory] = useState<HistoricalAuditItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Selection for comparison mode
  const [compareIds, setCompareIds] = useState<number[]>([]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/audits');
      if (!res.ok) throw new Error('Failed to load audit history');
      const data = await res.json();
      setHistory(data);
    } catch (e: any) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const toggleCompare = (id: number) => {
    if (compareIds.includes(id)) {
      setCompareIds(compareIds.filter((item) => item !== id));
    } else {
      if (compareIds.length < 2) {
        setCompareIds([...compareIds, id]);
      } else {
        setCompareIds([compareIds[1], id]);
      }
    }
  };

  const selectedAudits = history.filter((h) => compareIds.includes(h.id));

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-panel">
        <div>
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <History className="w-5 h-5 text-brand-400" />
            Audit Database & History Logs
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Persisted PostgreSQL / SQLite database audit records
          </p>
        </div>

        <button
          onClick={fetchHistory}
          disabled={loading}
          className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 hover:text-white transition-all"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Database
        </button>
      </div>

      {/* Comparison Drawer if 2 audits are selected */}
      {selectedAudits.length === 2 && (
        <div className="p-6 rounded-2xl bg-slate-900 border border-brand-500/40 shadow-glow-blue space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-base font-bold text-white flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-brand-400" />
              Side-by-Side Audit Score Comparison
            </h4>
            <button
              onClick={() => setCompareIds([])}
              className="text-xs font-mono text-slate-400 hover:text-white"
            >
              Clear Comparison
            </button>
          </div>

          <div className="grid grid-cols-3 text-xs font-mono border-t border-slate-800 pt-4">
            <div className="text-slate-400 font-bold">Metric</div>
            <div className="text-brand-300 font-bold truncate">{selectedAudits[0].domain}</div>
            <div className="text-emerald-300 font-bold truncate">{selectedAudits[1].domain}</div>
          </div>

          <div className="divide-y divide-slate-800 text-xs font-mono">
            {[
              { label: 'Overall Score', key: 'overall_score' },
              { label: 'SEO Score', key: 'seo_score' },
              { label: 'AEO Score', key: 'aeo_score' },
              { label: 'GEO Score', key: 'geo_score' },
              { label: 'Technical Score', key: 'technical_score' },
              { label: 'Content Score', key: 'content_score' },
              { label: 'Word Count', key: 'word_count' },
              { label: 'Response Speed', key: 'response_time_ms', unit: 'ms' },
            ].map((m) => {
              const val1 = (selectedAudits[0] as any)[m.key];
              const val2 = (selectedAudits[1] as any)[m.key];
              return (
                <div key={m.label} className="grid grid-cols-3 py-2">
                  <span className="text-slate-300">{m.label}</span>
                  <span className="text-brand-400 font-bold">{val1} {m.unit || ''}</span>
                  <span className="text-emerald-400 font-bold">{val2} {m.unit || ''}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* History Records List */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 font-mono">Loading audit logs...</div>
      ) : history.length === 0 ? (
        <div className="p-12 text-center glass-panel rounded-2xl text-slate-400 font-mono space-y-2">
          <p>No historical audits recorded yet.</p>
          <p className="text-xs text-slate-500">Run an audit on the main page to store records in PostgreSQL/SQLite.</p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="text-xs font-mono text-slate-400 px-2 flex justify-between">
            <span>Select 2 items to compare side-by-side</span>
            <span>{history.length} Saved Audits</span>
          </div>

          {history.map((h) => {
            const isSelected = compareIds.includes(h.id);
            return (
              <div
                key={h.id}
                className={`p-5 rounded-2xl glass-panel transition-all flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                  isSelected ? 'border-brand-500 bg-brand-500/10' : 'hover:border-slate-700'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Globe className="w-4 h-4 text-brand-400" />
                    <h4 className="font-bold text-white text-base font-mono">{h.domain}</h4>
                    <span className="text-xs text-slate-400 font-mono truncate max-w-xs">({h.url})</span>
                  </div>
                  <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-slate-500" /> {h.created_at}
                    </span>
                    <span>Words: {h.word_count}</span>
                    <span>Latency: {h.response_time_ms}ms</span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex gap-2 text-center font-mono">
                    <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                      <div className="text-sm font-bold text-white">{h.overall_score}</div>
                      <div className="text-[9px] text-slate-400">Overall</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                      <div className="text-sm font-bold text-brand-400">{h.seo_score}</div>
                      <div className="text-[9px] text-slate-400">SEO</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                      <div className="text-sm font-bold text-indigo-400">{h.aeo_score}</div>
                      <div className="text-[9px] text-slate-400">AEO</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                      <div className="text-sm font-bold text-emerald-400">{h.geo_score}</div>
                      <div className="text-[9px] text-slate-400">GEO</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => toggleCompare(h.id)}
                      className={`px-3 py-2 rounded-xl text-xs font-mono border transition-all ${
                        isSelected
                          ? 'bg-brand-500 text-white border-brand-500'
                          : 'bg-slate-900 border-slate-800 text-slate-300 hover:text-white'
                      }`}
                    >
                      {isSelected ? 'Selected' : 'Compare'}
                    </button>

                    <button
                      onClick={() => onLoadAudit(h.id)}
                      className="flex items-center gap-1 px-4 py-2 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 text-white text-xs font-semibold hover:opacity-90 transition-all shadow"
                    >
                      <span>Load</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
