import React from 'react';

interface ScoreGaugeProps {
  score: number;
  label: string;
  size?: 'sm' | 'md' | 'lg';
  subtitle?: string;
  className?: string;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({
  score,
  label,
  size = 'md',
  subtitle,
  className = ''
}) => {
  const getScoreColor = (s: number) => {
    if (s >= 80) return { stroke: '#10b981', bg: 'bg-emerald-500/10', text: 'text-emerald-400', badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' };
    if (s >= 60) return { stroke: '#f59e0b', bg: 'bg-amber-500/10', text: 'text-amber-400', badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30' };
    return { stroke: '#f43f5e', bg: 'bg-rose-500/10', text: 'text-rose-400', badge: 'bg-rose-500/20 text-rose-300 border-rose-500/30' };
  };

  const colors = getScoreColor(score);
  
  const dimensions = {
    sm: { radius: 28, strokeWidth: 5, sizePx: 68, fontSize: 'text-base' },
    md: { radius: 42, strokeWidth: 7, sizePx: 100, fontSize: 'text-2xl' },
    lg: { radius: 56, strokeWidth: 9, sizePx: 132, fontSize: 'text-3xl' }
  }[size];

  const circumference = 2 * Math.PI * dimensions.radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className={`flex flex-col items-center justify-center p-4 rounded-xl glass-panel ${colors.bg} ${className}`}>
      <div className="relative flex items-center justify-center">
        <svg
          width={dimensions.sizePx}
          height={dimensions.sizePx}
          className="transform -rotate-90"
        >
          <circle
            cx={dimensions.sizePx / 2}
            cy={dimensions.sizePx / 2}
            r={dimensions.radius}
            stroke="#1e293b"
            strokeWidth={dimensions.strokeWidth}
            fill="transparent"
          />
          <circle
            cx={dimensions.sizePx / 2}
            cy={dimensions.sizePx / 2}
            r={dimensions.radius}
            stroke={colors.stroke}
            strokeWidth={dimensions.strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className={`font-bold ${dimensions.fontSize} ${colors.text}`}>
            {score}
          </span>
          <span className="text-[10px] text-slate-400 uppercase font-mono">/100</span>
        </div>
      </div>
      <span className="mt-2 text-sm font-semibold text-slate-200 tracking-wide text-center">
        {label}
      </span>
      {subtitle && (
        <span className="text-xs text-slate-400 mt-0.5 font-mono text-center">
          {subtitle}
        </span>
      )}
    </div>
  );
};
