import React, { useState } from 'react';
import { Search, Sparkles, Bot, HelpCircle, CheckCircle2, ArrowRight, Globe } from 'lucide-react';

interface LandingPageProps {
  onAnalyze: (url: string) => void;
  isLoading: boolean;
  error?: string | null;
}

export const LandingPage: React.FC<LandingPageProps> = ({
  onAnalyze,
  isLoading,
  error
}) => {
  const [inputUrl, setInputUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputUrl.trim()) {
      onAnalyze(inputUrl.trim());
    }
  };

  const sampleUrls = [
    { name: 'Stripe', url: 'https://stripe.com' },
    { name: 'GitHub', url: 'https://github.com' },
    { name: 'Wikipedia (AI)', url: 'https://en.wikipedia.org/wiki/Artificial_intelligence' },
    { name: 'TechCrunch', url: 'https://techcrunch.com' },
  ];

  return (
    <div className="min-h-[calc(100vh-65px)] flex flex-col justify-between">
      {/* Hero Section */}
      <section className="relative pt-12 pb-20 px-4 lg:px-8 max-w-7xl mx-auto w-full text-center">
        {/* Glow backdrop */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-brand-600/20 via-purple-600/20 to-emerald-500/15 blur-[120px] rounded-full pointer-events-none -z-10" />

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-mono mb-8 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-brand-400 animate-spin-slow" />
          <span>Next-Gen Search Engine & AI Search Intelligence</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.15]">
          Understand How Search Engines & <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-400 via-indigo-300 to-emerald-400">AI Engines</span> See Your Website.
        </h1>

        {/* Subtitle */}
        <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-3xl mx-auto font-normal leading-relaxed">
          Analyze your website's <strong className="text-white">SEO</strong>, <strong className="text-white">Answer Engine Optimization (AEO)</strong>, and <strong className="text-white">Generative Engine Optimization (GEO)</strong> from one intelligent SaaS dashboard.
        </p>

        {/* URL Input Form */}
        <form onSubmit={handleSubmit} className="mt-10 max-w-2xl mx-auto">
          <div className="relative flex items-center p-2 rounded-2xl glass-panel border border-slate-700/80 shadow-glow-blue focus-within:border-brand-500 transition-all">
            <Globe className="w-5 h-5 text-slate-400 ml-3 shrink-0" />
            <input
              type="text"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              placeholder="Enter URL (e.g., https://yourwebsite.com)..."
              disabled={isLoading}
              className="w-full bg-transparent px-3 py-3 text-white placeholder-slate-500 focus:outline-none text-sm font-mono"
            />
            <button
              type="submit"
              disabled={isLoading || !inputUrl.trim()}
              className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 via-indigo-600 to-brand-700 text-white font-semibold text-sm hover:opacity-90 disabled:opacity-50 transition-all shadow-lg shrink-0 cursor-pointer"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>Analyze Website</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="mt-3 text-sm text-rose-400 bg-rose-500/10 border border-rose-500/30 px-4 py-2.5 rounded-xl font-mono text-left">
              ⚠️ {error}
            </div>
          )}

          {/* Quick Preset Buttons */}
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-400">
            <span className="font-mono">Try sample sites:</span>
            {sampleUrls.map((s) => (
              <button
                key={s.name}
                type="button"
                onClick={() => {
                  setInputUrl(s.url);
                  onAnalyze(s.url);
                }}
                className="px-2.5 py-1 rounded-lg bg-slate-900/90 border border-slate-800 text-slate-300 hover:text-white hover:border-brand-500/50 font-mono transition-all"
              >
                {s.name}
              </button>
            ))}
          </div>
        </form>

        {/* 3 Core Pillars Section */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto text-left">
          {/* SEO Card */}
          <div className="p-6 rounded-2xl glass-panel-hover border border-slate-800/80">
            <div className="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-400 mb-4">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">1. Traditional SEO</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-4">
              Metadata validation, H1-H6 heading hierarchy trees, keyword density, internal/external links, and core technical health.
            </p>
            <ul className="text-xs font-mono text-slate-300 space-y-2">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Google SERP Preview Simulator</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Image Alt Text Audit</span>
              </li>
            </ul>
          </div>

          {/* AEO Card */}
          <div className="p-6 rounded-2xl glass-panel-hover border border-slate-800/80">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-4">
              <HelpCircle className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">2. AEO (Answer Engine)</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-4">
              Optimize for Google Featured Snippets, Voice Search, and direct Q&A blocks with high-intent question scoring.
            </p>
            <ul className="text-xs font-mono text-slate-300 space-y-2">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                <span>Featured Snippet Targeter</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                <span>AI Recommended Answers</span>
              </li>
            </ul>
          </div>

          {/* GEO Card */}
          <div className="p-6 rounded-2xl glass-panel-hover border border-slate-800/80">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4">
              <Bot className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">3. GEO (AI Engine)</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-4">
              Prepare your brand for Perplexity, ChatGPT Search, Gemini, and Claude citations with entity graphs and authority signals.
            </p>
            <ul className="text-xs font-mono text-slate-300 space-y-2">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Named Entity Extraction</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Fact-to-Fluff Readability Ratio</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Interactive Sample Audit Metrics Teaser */}
        <div className="mt-16 p-8 rounded-3xl glass-panel border border-slate-800/80 max-w-5xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="text-left">
              <span className="text-xs font-mono text-brand-400 uppercase tracking-widest font-semibold">
                Live Audit Preview
              </span>
              <h4 className="text-2xl font-bold text-white mt-1">
                Multi-Dimensional 0-100 Scoring Engine
              </h4>
              <p className="text-slate-400 text-sm mt-1 max-w-md">
                Generates instant quantitative benchmarks across 6 foundational web metrics with automated PDF report creation.
              </p>
            </div>

            <div className="grid grid-cols-3 sm:grid-cols-6 gap-3 w-full md:w-auto">
              {[
                { label: 'Overall', score: 82, color: 'text-emerald-400' },
                { label: 'SEO', score: 86, color: 'text-emerald-400' },
                { label: 'AEO', score: 78, color: 'text-amber-400' },
                { label: 'GEO', score: 73, color: 'text-amber-400' },
                { label: 'Tech', score: 91, color: 'text-emerald-400' },
                { label: 'Content', score: 84, color: 'text-emerald-400' },
              ].map((m) => (
                <div key={m.label} className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center">
                  <div className={`text-xl font-bold font-mono ${m.color}`}>{m.score}</div>
                  <div className="text-[10px] text-slate-400 uppercase font-mono mt-0.5">{m.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500 font-mono">
        SEO Intelligence Platform • Built for SEO Analysts, Digital Marketing Teams & AI Product Architects
      </footer>
    </div>
  );
};
