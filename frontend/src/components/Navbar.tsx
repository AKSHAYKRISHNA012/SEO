import React from 'react';
import { Search, Cpu, History, ShieldCheck, Zap } from 'lucide-react';

interface NavbarProps {
  onSelectPreset: (url: string) => void;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  hasAuditData: boolean;
  onReset: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onSelectPreset,
  activeTab,
  setActiveTab,
  hasAuditData,
  onReset,
}) => {
  return (
    <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80 px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Brand Logo */}
        <div 
          onClick={onReset}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-emerald-400 p-0.5 shadow-glow-blue transition-transform group-hover:scale-105">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Cpu className="w-5 h-5 text-brand-400 animate-pulse-slow" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-white tracking-tight font-sans">
                SEO<span className="text-brand-500">Intelligence</span>
              </span>
              <span className="px-2 py-0.5 text-[10px] font-mono font-semibold rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
                PRO AI
              </span>
            </div>
            <p className="text-[11px] text-slate-400 -mt-0.5 font-mono">
              SEO • AEO • GEO Multi-Engine Analyzer
            </p>
          </div>
        </div>

        {/* Quick URL Preset Chips */}
        <div className="hidden md:flex items-center gap-2 text-xs">
          <span className="text-slate-400 font-mono text-[11px] flex items-center gap-1">
            <Zap className="w-3 h-3 text-amber-400" /> Presets:
          </span>
          {[
            { label: 'Stripe', url: 'https://stripe.com' },
            { label: 'GitHub', url: 'https://github.com' },
            { label: 'Wikipedia', url: 'https://en.wikipedia.org/wiki/Artificial_intelligence' },
            { label: 'TechCrunch', url: 'https://techcrunch.com' },
          ].map((preset) => (
            <button
              key={preset.label}
              onClick={() => onSelectPreset(preset.url)}
              className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:border-brand-500/50 hover:text-white hover:bg-slate-800/80 transition-all font-mono"
            >
              {preset.label}
            </button>
          ))}
        </div>

        {/* Right Navigation Actions */}
        <div className="flex items-center gap-3">
          {hasAuditData && (
            <button
              onClick={onReset}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs font-semibold transition-all"
            >
              <Search className="w-3.5 h-3.5" /> New Audit
            </button>
          )}

          <button
            onClick={() => setActiveTab('history')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              activeTab === 'history'
                ? 'bg-brand-500/20 border-brand-500 text-brand-300'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <History className="w-3.5 h-3.5" /> History
          </button>

          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>AI Ready</span>
          </div>
        </div>
      </div>
    </header>
  );
};
