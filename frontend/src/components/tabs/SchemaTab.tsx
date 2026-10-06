import React, { useState } from 'react';
import type { StructuredDataAnalysis } from '../../types/audit';
import { FileCode, AlertCircle, Copy, Check, Sparkles } from 'lucide-react';

interface SchemaTabProps {
  structuredData: StructuredDataAnalysis;
}

export const SchemaTab: React.FC<SchemaTabProps> = ({ structuredData }) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = (jsonObj: any, index: number) => {
    navigator.clipboard.writeText(JSON.stringify(jsonObj, null, 2));
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="space-y-8">
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <FileCode className="w-5 h-5 text-brand-400" />
              JSON-LD Structured Data Inspector
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Validates Schema.org entities embedded on the page
            </p>
          </div>
          <span className="px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-300 text-xs font-mono">
            {structuredData.detected_schemas.length} Schemas Detected
          </span>
        </div>

        {/* Detected Schema Badges */}
        <div className="flex flex-wrap gap-2 pt-2">
          {structuredData.schema_types.length > 0 ? (
            structuredData.schema_types.map((st, i) => (
              <span key={i} className="px-3 py-1 rounded-xl bg-slate-900 border border-brand-500/30 text-brand-300 font-mono text-xs font-bold">
                @{st}
              </span>
            ))
          ) : (
            <span className="text-xs text-rose-400 font-mono">No JSON-LD schema markup detected on this webpage.</span>
          )}
        </div>
      </div>

      {/* Recommended Schemas List */}
      {structuredData.recommended_schemas.length > 0 && (
        <div className="p-6 rounded-2xl bg-slate-900/90 border border-amber-500/30 space-y-3">
          <h4 className="text-sm font-bold text-amber-300 flex items-center gap-2 font-mono">
            <Sparkles className="w-4 h-4 text-amber-400" /> Recommended Schema Additions:
          </h4>
          <div className="space-y-2">
            {structuredData.recommended_schemas.map((rec, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 font-sans">
                {rec}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Schema Items Code Cards */}
      <div className="space-y-6">
        {structuredData.detected_schemas.map((s, idx) => (
          <div key={idx} className="p-6 rounded-2xl glass-panel space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 rounded bg-brand-500/20 text-brand-300 font-mono text-xs font-bold">
                  @{s.type}
                </span>
                <span className="text-xs text-slate-400 font-mono">Schema Entity #{idx + 1}</span>
              </div>

              <button
                onClick={() => handleCopy(s.raw_json, idx)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs font-mono transition-all"
              >
                {copiedIndex === idx ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-400" /> Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" /> Copy JSON-LD
                  </>
                )}
              </button>
            </div>

            {s.warnings.length > 0 && (
              <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono space-y-1">
                {s.warnings.map((w, wi) => (
                  <div key={wi} className="flex items-center gap-1.5">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            )}

            <pre className="p-4 rounded-xl bg-slate-950 text-emerald-400 font-mono text-xs overflow-x-auto border border-slate-800/80 max-h-80 leading-relaxed">
              <code>{JSON.stringify(s.raw_json, null, 2)}</code>
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};
