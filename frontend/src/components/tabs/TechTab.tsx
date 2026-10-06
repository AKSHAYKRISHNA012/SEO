import React from 'react';
import type { TechnicalSEOAnalysis } from '../../types/audit';
import { ShieldCheck, Zap, Server, CheckCircle2, XCircle } from 'lucide-react';

interface TechTabProps {
  technical: TechnicalSEOAnalysis;
}

export const TechTab: React.FC<TechTabProps> = ({ technical }) => {
  const getSpeedRating = (ms: number) => {
    if (ms < 800) return { label: 'Fast (Optimal)', color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/30' };
    if (ms < 2000) return { label: 'Moderate', color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/30' };
    return { label: 'Slow (Needs Fix)', color: 'text-rose-400', bg: 'bg-rose-500/10 border-rose-500/30' };
  };

  const speed = getSpeedRating(technical.response_time_ms);

  return (
    <div className="space-y-8">
      {/* Response Speed Meter */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Server Latency & Response Time
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Time to first byte (TTFB) and full HTML response fetch
            </p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-mono font-bold border ${speed.bg} ${speed.color}`}>
            {speed.label}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center pt-2">
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-3xl font-bold text-white font-mono">{technical.response_time_ms} ms</div>
            <div className="text-xs text-slate-400 font-mono mt-1">Response Latency</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-3xl font-bold text-emerald-400 font-mono">{technical.status_code}</div>
            <div className="text-xs text-slate-400 font-mono mt-1">HTTP Status Code</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-3xl font-bold text-brand-400 font-mono">{technical.redirect_count}</div>
            <div className="text-xs text-slate-400 font-mono mt-1">HTTP Redirects</div>
          </div>
        </div>
      </div>

      {/* Technical SEO Standards Grid */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          Core Technical SEO & Security Checklist
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            technical.is_https ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
          }`}>
            <span className="font-bold flex items-center gap-2">
              {technical.is_https ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              HTTPS Encryption Protocol
            </span>
            <span>{technical.is_https ? 'Enabled' : 'Disabled (Critical)'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            technical.has_mobile_viewport ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
          }`}>
            <span className="font-bold flex items-center gap-2">
              {technical.has_mobile_viewport ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              Mobile Viewport Tag
            </span>
            <span>{technical.has_mobile_viewport ? 'Configured' : 'Missing (Critical)'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            technical.robots_txt_found ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold flex items-center gap-2">
              {technical.robots_txt_found ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              robots.txt Accessibility
            </span>
            <span>{technical.robots_txt_found ? 'Found' : 'Missing'}</span>
          </div>

          <div className={`p-4 rounded-xl border flex items-center justify-between ${
            technical.sitemap_xml_found ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-slate-900 border-slate-800 text-slate-400'
          }`}>
            <span className="font-bold flex items-center gap-2">
              {technical.sitemap_xml_found ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              sitemap.xml Index File
            </span>
            <span>{technical.sitemap_xml_found ? 'Found' : 'Missing'}</span>
          </div>
        </div>
      </div>

      {/* HTTP Response Headers Inspector */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Server className="w-5 h-5 text-sky-400" />
          HTTP Server Response Headers
        </h3>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs font-mono">
          <div className="flex justify-between border-b border-slate-800 pb-2">
            <span className="text-slate-400">Server Signature:</span>
            <span className="text-white font-bold">{technical.server_header || 'Hidden / Cloudflare'}</span>
          </div>
          <div className="flex justify-between border-b border-slate-800 pb-2">
            <span className="text-slate-400">Cache-Control:</span>
            <span className="text-white font-bold">{technical.cache_control || 'Default'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Final Resolved URL:</span>
            <span className="text-emerald-400 font-bold truncate max-w-md">{technical.final_url}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
