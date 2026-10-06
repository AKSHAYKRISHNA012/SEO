import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { LandingPage } from './components/LandingPage';
import { AuditDashboard } from './components/AuditDashboard';
import type { AuditResponse } from './types/audit';

export function App() {
  const [currentAudit, setCurrentAudit] = useState<AuditResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (url: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to analyze website. Ensure URL is publicly accessible.');
      }

      const data: AuditResponse = await res.json();
      setCurrentAudit(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected network error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadAuditById = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/audit/${id}`);
      if (!res.ok) throw new Error('Audit record not found.');
      const data: AuditResponse = await res.json();
      setCurrentAudit(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load historical audit.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setCurrentAudit(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        onSelectPreset={handleAnalyze}
        activeTab={currentAudit ? 'dashboard' : 'home'}
        setActiveTab={() => {}}
        hasAuditData={currentAudit !== null}
        onReset={handleReset}
      />

      <main className="flex-1">
        {currentAudit ? (
          <AuditDashboard
            audit={currentAudit}
            onReAnalyze={() => handleAnalyze(currentAudit.url)}
            onLoadAuditById={handleLoadAuditById}
          />
        ) : (
          <LandingPage
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
            error={error}
          />
        )}
      </main>
    </div>
  );
}

export default App;
