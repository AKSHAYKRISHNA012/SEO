import React, { useState } from 'react';
import type { AuditResponse } from '../types/audit';
import { ScoreGauge } from './ScoreGauge';
import { OverviewTab } from './tabs/OverviewTab';
import { SeoTab } from './tabs/SeoTab';
import { AeoTab } from './tabs/AeoTab';
import { GeoTab } from './tabs/GeoTab';
import { TechTab } from './tabs/TechTab';
import { SchemaTab } from './tabs/SchemaTab';
import { HistoryTab } from './tabs/HistoryTab';
import { Download, RefreshCw, FileCode, Layers, Search, HelpCircle, Bot, Zap, ShieldCheck } from 'lucide-react';

interface AuditDashboardProps {
  audit: AuditResponse;
  onReAnalyze: () => void;
  onLoadAuditById: (id: number) => void;
}

export const AuditDashboard: React.FC<AuditDashboardProps> = ({
  audit,
  onReAnalyze,
  onLoadAuditById,
}) => {
  const [activeTab, setActiveTab] = useState<string>('overview');

  const handleDownloadPdf = () => {
    if (audit.id) {
      window.open(`/api/audit/${audit.id}/pdf`, '_blank');
    } else {
      alert('Audit report PDF is available after saving.');
    }
  };

  const handleExportJson = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(audit, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `SEO_Intelligence_${audit.domain}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-8">
      {/* Top Bar Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl glass-panel">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono font-bold text-brand-400 uppercase tracking-wider">
              Website Audit Report
            </span>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
              Live Verified Audit
            </span>
            {audit.ai_powered && (
              <span className="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-[10px] font-mono">
                AI Enhanced
              </span>
            )}
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white font-mono tracking-tight">
            {audit.domain}
          </h2>
          <p className="text-xs text-slate-400 font-mono truncate max-w-xl">
            {audit.url} • Analyzed on {audit.analyzed_at}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={onReAnalyze}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs font-mono font-medium transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Re-Analyze
          </button>

          <button
            onClick={handleExportJson}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs font-mono font-medium transition-all"
          >
            <FileCode className="w-3.5 h-3.5 text-brand-400" /> Export JSON
          </button>

          <button
            onClick={handleDownloadPdf}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-600 via-indigo-600 to-brand-700 text-white text-xs font-bold shadow-lg hover:opacity-90 transition-all cursor-pointer"
          >
            <Download className="w-4 h-4" /> Download PDF Report
          </button>
        </div>
      </div>

      {/* Scores Summary Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <ScoreGauge
          score={audit.scores.overall}
          label="Overall Score"
          size="md"
          subtitle="Composite"
        />
        <ScoreGauge
          score={audit.scores.seo}
          label="SEO Score"
          size="md"
          subtitle="Traditional"
        />
        <ScoreGauge
          score={audit.scores.aeo}
          label="AEO Score"
          size="md"
          subtitle="Answer Engine"
        />
        <ScoreGauge
          score={audit.scores.geo}
          label="GEO Score"
          size="md"
          subtitle="AI Engines"
        />
        <ScoreGauge
          score={audit.scores.technical}
          label="Technical"
          size="md"
          subtitle="Speed & Security"
        />
        <ScoreGauge
          score={audit.scores.content}
          label="Content"
          size="md"
          subtitle="Depth & Readability"
        />
      </div>

      {/* Tab List Navigation Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800/80">
        {[
          { id: 'overview', label: 'Overview', icon: Layers },
          { id: 'seo', label: 'SEO Audit', icon: Search },
          { id: 'aeo', label: 'AEO Audit', icon: HelpCircle },
          { id: 'geo', label: 'GEO Audit', icon: Bot },
          { id: 'tech', label: 'Technical & Speed', icon: Zap },
          { id: 'schema', label: 'Structured Data', icon: ShieldCheck },
          { id: 'history', label: 'History & Compare', icon: FileCode },
        ].map((tab) => {
          const IconComponent = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold font-mono whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-brand-600 text-white shadow-glow-blue'
                  : 'bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
              }`}
            >
              <IconComponent className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Content Display */}
      <div>
        {activeTab === 'overview' && (
          <OverviewTab
            scores={audit.scores}
            recommendations={audit.recommendations}
            domain={audit.domain}
            onSelectTab={setActiveTab}
          />
        )}
        {activeTab === 'seo' && (
          <SeoTab
            meta={audit.meta}
            headings={audit.headings}
            content={audit.content}
            links={audit.links}
            images={audit.images}
            url={audit.url}
          />
        )}
        {activeTab === 'aeo' && <AeoTab aeo={audit.aeo} />}
        {activeTab === 'geo' && <GeoTab geo={audit.geo} />}
        {activeTab === 'tech' && <TechTab technical={audit.technical} />}
        {activeTab === 'schema' && <SchemaTab structuredData={audit.structured_data} />}
        {activeTab === 'history' && <HistoryTab onLoadAudit={onLoadAuditById} />}
      </div>
    </div>
  );
};
