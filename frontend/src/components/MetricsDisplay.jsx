import React from 'react';
import { Type, Hash, Pointer, Link2, Image, FileText, AlertCircle as AlertIcon } from 'lucide-react';

function MetricsDisplay({ metrics }) {
    const items = [
        { label: 'Word Count', value: metrics.word_count, icon: <Type size={18} /> },
        { label: 'H1 Headings', value: metrics.heading_counts.h1, icon: <Hash size={18} /> },
        { label: 'H2 Headings', value: metrics.heading_counts.h2, icon: <Hash size={18} /> },
        { label: 'H3 Headings', value: metrics.heading_counts.h3, icon: <Hash size={18} /> },
        { label: 'CTA Actions', value: metrics.cta_count, icon: <Pointer size={18} /> },
        { label: 'Internal Links', value: metrics.links.internal, icon: <Link2 size={18} /> },
        { label: 'External Links', value: metrics.links.external, icon: <Link2 size={18} /> },
        { label: 'Total Images', value: metrics.images.total, icon: <Image size={18} /> },
        { label: 'Missing Alt %', value: `${metrics.images.missing_alt_pct.toFixed(1)}%`, icon: <AltStatus metric={metrics.images.missing_alt_pct} /> },
    ];

    return (
        <div className="card">
            <h2 className="card-title">
                <FileText size={20} />
                <span>Factual Metrics</span>
            </h2>
            <div className="metrics-list">
                {items.map((item, idx) => (
                    <div key={idx} className="metric-item">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <span style={{ color: 'var(--primary)', display: 'flex' }}>{item.icon}</span>
                            <span className="metric-label">{item.label}</span>
                        </div>
                        <span className="metric-value">{item.value}</span>
                    </div>
                ))}

                <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                        Meta Information
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <div>
                            <div className="metric-label">Title Tag</div>
                            <div style={{ fontSize: '0.9rem', fontWeight: '500' }}>{metrics.meta.title || 'N/A'}</div>
                            <div style={{ fontSize: '0.75rem', color: metrics.meta.title_length > 60 ? 'var(--error)' : 'var(--success)' }}>
                                {metrics.meta.title_length} characters
                            </div>
                        </div>
                        <div style={{ marginTop: '0.5rem' }}>
                            <div className="metric-label">Meta Description</div>
                            <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                                {metrics.meta.description || 'Missing meta description'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Helper to show alert icon if missing alt % is high
function AltStatus({ metric }) {
    if (metric > 20) return <AlertIcon size={18} color="var(--error)" />;
    return <Image size={18} />;
}

export default MetricsDisplay;
