import React from 'react';
import type { ScoreBreakdown, RecommendationItem } from '../../types/audit';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { AlertTriangle, CheckCircle, ArrowRight } from 'lucide-react';

interface OverviewTabProps {
  scores: ScoreBreakdown;
  recommendations: RecommendationItem[];
  domain: string;
  onSelectTab: (tab: string) => void;
}

export const OverviewTab: React.FC<OverviewTabProps> = ({
  scores,
  recommendations,
  domain,
  onSelectTab,
}) => {
  const radarData = [
    { subject: 'SEO', score: scores.seo, fullMark: 100 },
    { subject: 'AEO', score: scores.aeo, fullMark: 100 },
    { subject: 'GEO', score: scores.geo, fullMark: 100 },
    { subject: 'Technical', score: scores.technical, fullMark: 100 },
    { subject: 'Content', score: scores.content, fullMark: 100 },
  ];

  const criticals = recommendations.filter((r) => r.priority === 'Critical');
  const warnings = recommendations.filter((r) => r.priority === 'Warning');
  const tips = recommendations.filter((r) => r.priority === 'Tip');

  return (
    <div className="space-y-8">
      {/* Top Overview Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Radar Chart Card */}
        <div className="lg:col-span-1 p-6 rounded-2xl glass-panel flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-bold text-white mb-1">Score Radar Profile</h3>
            <p className="text-xs text-slate-400 font-mono">
              Multi-dimensional audit coverage balance for {domain}
            </p>
          </div>
          
          <div className="w-full h-64 my-2">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Radar name="Domain Audit" dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-center text-xs font-mono text-slate-400">
            Overall Health Index: <strong className="text-brand-400 text-sm">{scores.overall}/100</strong>
          </div>
        </div>

        {/* Priority Summary & Action Plan Overview */}
        <div className="lg:col-span-2 p-6 rounded-2xl glass-panel space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-bold text-white">Action Plan Summary</h3>
              <p className="text-xs text-slate-400 font-mono">
                {recommendations.length} total recommendations generated for optimization
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-1 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-mono font-bold">
                {criticals.length} Critical
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-mono font-bold">
                {warnings.length} Warnings
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-mono font-bold">
                {tips.length} Tips
              </span>
            </div>
          </div>

          {/* Core Audit Category Banners */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div 
              onClick={() => onSelectTab('seo')}
              className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-brand-500/40 cursor-pointer transition-all flex items-center justify-between"
            >
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase">Traditional SEO</span>
                <div className="text-2xl font-bold text-white">{scores.seo}<span className="text-xs text-slate-500 font-normal">/100</span></div>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500" />
            </div>

            <div 
              onClick={() => onSelectTab('aeo')}
              className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/40 cursor-pointer transition-all flex items-center justify-between"
            >
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase">Answer Engine (AEO)</span>
                <div className="text-2xl font-bold text-white">{scores.aeo}<span className="text-xs text-slate-500 font-normal">/100</span></div>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500" />
            </div>

            <div 
              onClick={() => onSelectTab('geo')}
              className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/40 cursor-pointer transition-all flex items-center justify-between"
            >
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase">Generative Engine (GEO)</span>
                <div className="text-2xl font-bold text-white">{scores.geo}<span className="text-xs text-slate-500 font-normal">/100</span></div>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500" />
            </div>

            <div 
              onClick={() => onSelectTab('tech')}
              className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-sky-500/40 cursor-pointer transition-all flex items-center justify-between"
            >
              <div>
                <span className="text-xs font-mono text-slate-400 uppercase">Technical & Speed</span>
                <div className="text-2xl font-bold text-white">{scores.technical}<span className="text-xs text-slate-500 font-normal">/100</span></div>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Actionable Recommendation Checklist Section */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Prioritized Action Plan Checklist
        </h3>

        <div className="space-y-4">
          {recommendations.map((rec) => {
            const isCritical = rec.priority === 'Critical';
            const isWarning = rec.priority === 'Warning';
            
            const badgeClass = isCritical
              ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
              : isWarning
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
              : 'bg-brand-500/10 border-brand-500/30 text-brand-300';

            return (
              <div 
                key={rec.id}
                className="p-5 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition-all space-y-3"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase border ${badgeClass}`}>
                        {rec.priority}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">
                        {rec.category}
                      </span>
                      <h4 className="font-bold text-slate-100 text-base">{rec.title}</h4>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{rec.description}</p>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800/80 space-y-2">
                  <div className="text-xs font-semibold text-brand-300 font-mono flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> Action Step:
                  </div>
                  <p className="text-xs text-slate-300 font-sans">{rec.action_step}</p>

                  {rec.code_example && (
                    <div className="mt-2 pt-2 border-t border-slate-800">
                      <div className="text-[10px] font-mono text-slate-400 flex items-center gap-1 mb-1">
                        Implementation Code Example:
                      </div>
                      <pre className="p-2.5 rounded bg-slate-900 text-emerald-300 text-xs font-mono overflow-x-auto border border-slate-800">
                        <code>{rec.code_example}</code>
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
