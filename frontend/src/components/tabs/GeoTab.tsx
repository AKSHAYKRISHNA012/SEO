import React from 'react';
import type { GEOAnalysis } from '../../types/audit';
import { Bot, ShieldCheck, Sparkles, Database } from 'lucide-react';

interface GeoTabProps {
  geo: GEOAnalysis;
}

export const GeoTab: React.FC<GeoTabProps> = ({ geo }) => {
  return (
    <div className="space-y-8">
      {/* Hero GEO Banner */}
      <div className="p-6 rounded-2xl glass-panel bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 border-emerald-500/30">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono">
              <Bot className="w-3.5 h-3.5" />
              Generative Engine Optimization (GEO)
            </div>
            <h3 className="text-2xl font-bold text-white">
              AI Search Engine Visibility & Citations
            </h3>
            <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
              GEO focuses on improving the likelihood that a website's information can be extracted, trusted, synthesized, and referenced by generative AI search platforms including Perplexity, ChatGPT Search, Gemini, and Claude.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900 border border-emerald-500/30 text-center shrink-0 w-full md:w-auto">
            <div className="text-3xl font-extrabold text-emerald-400 font-mono">
              {geo.ai_readability_score}<span className="text-xs text-slate-500 font-normal">/100</span>
            </div>
            <div className="text-xs text-slate-300 font-mono mt-1">AI Readability Index</div>
          </div>
        </div>
      </div>

      {/* AI Compatibility Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 rounded-2xl glass-panel space-y-2">
          <div className="text-xs font-mono text-slate-400">Fact Density Score</div>
          <div className="text-3xl font-bold text-white font-mono">{geo.factual_density_score}%</div>
          <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
            <div 
              className="h-full bg-emerald-400 rounded-full" 
              style={{ width: `${geo.factual_density_score}%` }} 
            />
          </div>
          <p className="text-[11px] text-slate-400 font-mono">Ratio of concrete factual statements to filler copy</p>
        </div>

        <div className="p-5 rounded-2xl glass-panel space-y-2">
          <div className="text-xs font-mono text-slate-400">External Citations</div>
          <div className="text-3xl font-bold text-white font-mono">{geo.external_citations_count} links</div>
          <p className="text-[11px] text-slate-400 font-mono">Outbound references strengthening verification trust</p>
        </div>

        <div className="p-5 rounded-2xl glass-panel space-y-2">
          <div className="text-xs font-mono text-slate-400">Trust Signals Verified</div>
          <div className="text-3xl font-bold text-emerald-400 font-mono">{geo.trust_signals.length} signals</div>
          <p className="text-[11px] text-slate-400 font-mono">Author byline, About, Contact, TOS links</p>
        </div>
      </div>

      {/* Extracted Named Entities */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Database className="w-5 h-5 text-emerald-400" />
              Extracted Named Entity Recognition (NER)
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Key brand entities identified for knowledge graph embedding
            </p>
          </div>
          <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-xs font-mono">
            {geo.entities.length} Entities
          </span>
        </div>

        <div className="flex flex-wrap gap-2.5 pt-2">
          {geo.entities.map((e, idx) => (
            <div 
              key={idx}
              className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 flex items-center gap-2 text-xs font-mono"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span className="text-white font-bold">{e.name}</span>
              <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">
                {e.category}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Authority & Trust Signals Checklist */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-indigo-400" />
          Authority & Trust Signals Audit
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            geo.author_info_found ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold">Author Bio / Attribution Tag:</span>
            <span>{geo.author_info_found ? 'Verified' : 'Missing'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            geo.about_page_linked ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold">Navigational About Us Link:</span>
            <span>{geo.about_page_linked ? 'Verified' : 'Missing'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            geo.contact_page_linked ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold">Contact Page Reference:</span>
            <span>{geo.contact_page_linked ? 'Verified' : 'Missing'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            geo.organization_found ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold">Brand / Organization Clarity:</span>
            <span>{geo.organization_found ? 'Verified' : 'Missing'}</span>
          </div>
        </div>
      </div>

      {/* Actionable GEO Recommendations */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-emerald-400" />
          Generative AI Recommendation Strategy
        </h3>

        <div className="space-y-3">
          {geo.geo_recommendations.map((rec, i) => (
            <div key={i} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans flex items-start gap-3">
              <span className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-mono text-[10px] shrink-0 font-bold">
                {i + 1}
              </span>
              <span>{rec}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
