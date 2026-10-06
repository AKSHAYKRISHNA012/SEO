import React from 'react';
import type { AEOAnalysis } from '../../types/audit';
import { HelpCircle, CheckCircle2, XCircle, Sparkles, MessageSquare, List, Table } from 'lucide-react';

interface AeoTabProps {
  aeo: AEOAnalysis;
}

export const AeoTab: React.FC<AeoTabProps> = ({ aeo }) => {
  return (
    <div className="space-y-8">
      {/* Hero Banner Card */}
      <div className="p-6 rounded-2xl glass-panel bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-900 border-indigo-500/30">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-mono">
              <HelpCircle className="w-3.5 h-3.5" />
              Answer Engine Optimization (AEO)
            </div>
            <h3 className="text-2xl font-bold text-white">
              Featured Snippets & Direct Answer Readiness
            </h3>
            <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
              AEO ensures your web page directly answers user query intent with structured lists, tables, and concise 40-50 word answer paragraphs formatted for instant extraction by search engine snippet modules and voice assistants.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900 border border-indigo-500/30 text-center shrink-0 w-full md:w-auto">
            <div className="text-3xl font-extrabold text-indigo-400 font-mono">
              {aeo.aeo_readiness_score}<span className="text-xs text-slate-500 font-normal">/100</span>
            </div>
            <div className="text-xs text-slate-300 font-mono mt-1">AEO Readiness Score</div>
          </div>
        </div>
      </div>

      {/* Structured Answer Elements Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl glass-panel text-center">
          <MessageSquare className="w-5 h-5 text-indigo-400 mx-auto mb-1" />
          <div className="text-xl font-bold text-white font-mono">{aeo.concise_paragraphs_count}</div>
          <div className="text-xs text-slate-400 font-mono">Concise Answers (&lt;60w)</div>
        </div>

        <div className="p-4 rounded-xl glass-panel text-center">
          <List className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
          <div className="text-xl font-bold text-white font-mono">{aeo.lists_count}</div>
          <div className="text-xs text-slate-400 font-mono">Structured Lists</div>
        </div>

        <div className="p-4 rounded-xl glass-panel text-center">
          <Table className="w-5 h-5 text-amber-400 mx-auto mb-1" />
          <div className="text-xl font-bold text-white font-mono">{aeo.tables_count}</div>
          <div className="text-xs text-slate-400 font-mono">Data Tables</div>
        </div>

        <div className="p-4 rounded-xl glass-panel text-center">
          <HelpCircle className="w-5 h-5 text-brand-400 mx-auto mb-1" />
          <div className="text-xl font-bold text-white font-mono">{aeo.faq_sections_count}</div>
          <div className="text-xs text-slate-400 font-mono">FAQ Sections</div>
        </div>
      </div>

      {/* Featured Snippet Opportunities List */}
      {aeo.featured_snippet_opportunities.length > 0 && (
        <div className="p-5 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-200 space-y-2">
          <div className="font-bold text-sm flex items-center gap-2 font-mono">
            <Sparkles className="w-4 h-4 text-indigo-400" /> Featured Snippet Optimization Opportunities:
          </div>
          <ul className="list-disc list-inside text-xs space-y-1">
            {aeo.featured_snippet_opportunities.map((opp, idx) => (
              <li key={idx} className="leading-relaxed">{opp}</li>
            ))}
          </ul>
        </div>
      )}

      {/* High-Intent Question & Answer Table */}
      <div className="p-6 rounded-2xl glass-panel space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Extracted & Generated User Questions</h3>
            <p className="text-xs text-slate-400 font-mono">
              Evaluates if existing page content answers core user queries and provides AI-recommended answers
            </p>
          </div>
          <span className="px-2.5 py-1 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-xs font-mono">
            {aeo.question_count} Questions
          </span>
        </div>

        <div className="space-y-4">
          {aeo.questions.map((q, i) => (
            <div 
              key={i}
              className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-[10px] font-bold">
                    Q{i + 1}
                  </span>
                  <h4 className="font-bold text-white text-base">{q.question}</h4>
                </div>

                <div className="flex items-center gap-2">
                  {q.existing_answer_found ? (
                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Answer Found
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/30 text-xs font-mono">
                      <XCircle className="w-3.5 h-3.5" /> Answer Missing
                    </span>
                  )}
                  <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-xs font-mono">
                    Quality: {q.answer_quality_score}/100
                  </span>
                </div>
              </div>

              {q.existing_answer_snippet && (
                <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-xs text-slate-300">
                  <span className="font-bold text-slate-400 font-mono block mb-1">Existing Answer Snippet on Page:</span>
                  <p className="italic">"{q.existing_answer_snippet}"</p>
                </div>
              )}

              <div className="p-3.5 rounded-lg bg-indigo-950/30 border border-indigo-500/20 text-xs space-y-1">
                <span className="font-bold text-indigo-300 font-mono flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400" /> Recommended Featured Snippet Answer:
                </span>
                <p className="text-slate-200 leading-relaxed font-sans">{q.recommended_answer}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
