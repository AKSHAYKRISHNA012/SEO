import React from 'react';
import type {
  MetaDataAnalysis, HeadingAnalysis, ContentAnalysis,
  LinkAnalysis, ImageAnalysis
} from '../../types/audit';
import { Search, Globe, AlertCircle, FileText, Image as ImageIcon, Link as LinkIcon, Eye } from 'lucide-react';

interface SeoTabProps {
  meta: MetaDataAnalysis;
  headings: HeadingAnalysis;
  content: ContentAnalysis;
  links: LinkAnalysis;
  images: ImageAnalysis;
  url: string;
}

export const SeoTab: React.FC<SeoTabProps> = ({
  meta,
  headings,
  content,
  links,
  images,
  url,
}) => {
  return (
    <div className="space-y-8">
      {/* 1. Google SERP Simulator Card */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Eye className="w-5 h-5 text-brand-400" />
              Google SERP Result Preview Simulator
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Live simulation of desktop search snippet appearance
            </p>
          </div>
          <span className="px-2.5 py-1 rounded bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-mono">
            Desktop Preview
          </span>
        </div>

        {/* Snippet Box */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5 font-sans">
          <div className="flex items-center gap-2 text-xs text-slate-300 font-mono">
            <Globe className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-emerald-400 text-xs">{url}</span>
          </div>
          <h4 className="text-lg font-medium text-blue-400 hover:underline cursor-pointer tracking-tight">
            {meta.title || 'Missing Page Title'}
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
            {meta.description || 'No meta description found. Search engines will extract random paragraph text from your content.'}
          </p>
        </div>

        {/* Title & Description Length Meters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Title Length:</span>
              <span className={meta.title_status === 'Optimal' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                {meta.title_length} chars ({meta.title_status})
              </span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className={`h-full rounded-full ${meta.title_status === 'Optimal' ? 'bg-emerald-400' : 'bg-amber-400'}`}
                style={{ width: `${Math.min(100, (meta.title_length / 65) * 100)}%` }}
              />
            </div>
            <p className="text-[11px] text-slate-500 font-mono">Recommended length: 50-60 characters</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Meta Description Length:</span>
              <span className={meta.description_status === 'Optimal' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                {meta.description_length} chars ({meta.description_status})
              </span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className={`h-full rounded-full ${meta.description_status === 'Optimal' ? 'bg-emerald-400' : 'bg-amber-400'}`}
                style={{ width: `${Math.min(100, (meta.description_length / 160) * 100)}%` }}
              />
            </div>
            <p className="text-[11px] text-slate-500 font-mono">Recommended length: 120-160 characters</p>
          </div>
        </div>
      </div>

      {/* 2. Headings Analysis */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-400" />
          Heading Architecture & Hierarchy
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-2xl font-bold text-white font-mono">{headings.h1_count}</div>
            <div className="text-xs text-slate-400 font-mono">H1 Tags</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-2xl font-bold text-white font-mono">{headings.h2_count}</div>
            <div className="text-xs text-slate-400 font-mono">H2 Tags</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-2xl font-bold text-white font-mono">{headings.h3_count}</div>
            <div className="text-xs text-slate-400 font-mono">H3 Tags</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <div className="text-2xl font-bold text-white font-mono">{headings.total_headings}</div>
            <div className="text-xs text-slate-400 font-mono">Total Headings</div>
          </div>
        </div>

        {headings.hierarchy_issues.length > 0 && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs space-y-1">
            <div className="font-bold flex items-center gap-1.5 font-mono">
              <AlertCircle className="w-4 h-4" /> Heading Hierarchy Warnings:
            </div>
            <ul className="list-disc list-inside space-y-0.5">
              {headings.hierarchy_issues.map((issue, idx) => (
                <li key={idx}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Headings Tree snippet */}
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 max-h-56 overflow-y-auto font-mono text-xs space-y-1.5">
          <div className="text-slate-500 font-bold mb-2">Heading Structure Tree:</div>
          {headings.headings_tree.map((h, i) => (
            <div key={i} className="flex items-center gap-2" style={{ paddingLeft: `${(h.level - 1) * 16}px` }}>
              <span className="px-1.5 py-0.5 rounded bg-slate-800 text-brand-300 text-[10px] uppercase font-bold">
                {h.tag}
              </span>
              <span className="text-slate-200 truncate">{h.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Content Metrics & Keyword Density Table */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Search className="w-5 h-5 text-emerald-400" />
          Content Depth & Keyword Frequency Analysis
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <span className="text-xs font-mono text-slate-400">Total Word Count</span>
            <div className="text-2xl font-bold text-white font-mono">{content.word_count} words</div>
            <p className="text-[11px] text-slate-400 font-mono">Paragraphs: {content.paragraph_count}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <span className="text-xs font-mono text-slate-400">Flesch Reading Ease</span>
            <div className="text-2xl font-bold text-emerald-400 font-mono">{content.reading_ease_score}/100</div>
            <p className="text-[11px] text-slate-400 font-mono">Difficulty: {content.reading_difficulty}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
            <span className="text-xs font-mono text-slate-400">Content Structure Score</span>
            <div className="text-2xl font-bold text-brand-400 font-mono">{content.content_structure_score}/100</div>
            <p className="text-[11px] text-slate-400 font-mono">Freshness Signals: {content.freshness_signals.length}</p>
          </div>
        </div>

        {/* Keyword Frequency Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-300 font-mono">
            <thead className="bg-slate-900 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="p-3">Keyword</th>
                <th className="p-3 text-center">Frequency</th>
                <th className="p-3 text-right">Density %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {content.top_keywords.map((kw, i) => (
                <tr key={i} className="hover:bg-slate-900/50">
                  <td className="p-3 font-semibold text-white">{kw.keyword}</td>
                  <td className="p-3 text-center">{kw.count} times</td>
                  <td className="p-3 text-right font-bold text-brand-400">{kw.density_percent}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. Link & Image Audit Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Link Distribution */}
        <div className="p-6 rounded-2xl glass-panel space-y-4">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <LinkIcon className="w-5 h-5 text-sky-400" />
            Link Architecture Audit
          </h3>

          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-white font-mono">{links.total_links}</div>
              <div className="text-[10px] text-slate-400 font-mono">Total Links</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-emerald-400 font-mono">{links.internal_links_count}</div>
              <div className="text-[10px] text-slate-400 font-mono">Internal</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-brand-400 font-mono">{links.external_links_count}</div>
              <div className="text-[10px] text-slate-400 font-mono">External</div>
            </div>
          </div>
        </div>

        {/* Image Alt Audit */}
        <div className="p-6 rounded-2xl glass-panel space-y-4">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ImageIcon className="w-5 h-5 text-purple-400" />
            Image Alt Attribute Inspector
          </h3>

          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-white font-mono">{images.total_images}</div>
              <div className="text-[10px] text-slate-400 font-mono">Total Images</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-emerald-400 font-mono">{images.images_with_alt_count}</div>
              <div className="text-[10px] text-slate-400 font-mono">With Alt Text</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-xl font-bold text-rose-400 font-mono">{images.missing_alt_count}</div>
              <div className="text-[10px] text-slate-400 font-mono">Missing Alt</div>
            </div>
          </div>

          {images.sample_missing_alt.length > 0 && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs font-mono space-y-1">
              <span className="font-bold">Missing Alt Images:</span>
              <ul className="list-disc list-inside space-y-0.5 truncate">
                {images.sample_missing_alt.map((imgSrc, i) => (
                  <li key={i} className="truncate">{imgSrc}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
