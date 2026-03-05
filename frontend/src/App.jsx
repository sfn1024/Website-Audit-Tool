import React, { useState } from 'react';
import { Search, Loader2, Gauge, AlertCircle, CheckCircle2 } from 'lucide-react';
import AuditForm from './components/AuditForm';
import MetricsDisplay from './components/MetricsDisplay';
import InsightsDisplay from './components/InsightsDisplay';
import RecommendationsList from './components/RecommendationsList';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAudit = async (url) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Audit failed. Please check the URL and try again.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container header-content">
          <div className="logo">
            <Gauge size={28} />
            <span>AuditTool</span>
          </div>
          <div className="tagline" style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Internal Agency Analysis v1.0
          </div>
        </div>
      </header>

      <main className="container">
        <section className="audit-section">
          <h1>Website Audit Tool</h1>
          <p>Get instant factual metrics and AI-driven strategic insights for any URL.</p>
          <AuditForm onAudit={handleAudit} loading={loading} />
        </section>

        {error && (
          <div className="error-box">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertCircle size={20} />
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {result && (
          <div className="results-grid">
            <MetricsDisplay metrics={result.metrics} />

            {result.insights ? (
              <>
                <InsightsDisplay insights={result.insights} />
                <RecommendationsList recommendations={result.insights.recommendations} />
              </>
            ) : (
              <div className="card full-width-fallback" style={{ textAlign: 'center', padding: '3rem' }}>
                <AlertCircle size={48} color="var(--warning)" style={{ marginBottom: '1rem', marginLeft: 'auto', marginRight: 'auto', display: 'block' }} />
                <h2>AI Insights Unavailable</h2>
                <p style={{ color: 'var(--text-muted)' }}>
                  Factual metrics were extracted, but AI analysis failed.
                  Check your Gemini API key in the backend configuration.
                </p>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="container" style={{ margin: '4rem auto 2rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p>&copy; {new Date().getFullYear()} Agency Internal Tool. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
