import React, { useState } from 'react';
import { Type, Hash, Pointer, Link2, Image, FileText, Info, X, AlertCircle as AlertIcon } from 'lucide-react';

function MetricsDisplay({ metrics }) {
    const [selectedMetric, setSelectedMetric] = useState(null);

    const items = [
        { label: 'Word Count', value: metrics.word_count, icon: <Type size={18} /> },
        { label: 'H1 Headings', value: metrics.heading_counts.h1, icon: <Hash size={18} />, list: metrics.heading_counts.h1_list },
        { label: 'H2 Headings', value: metrics.heading_counts.h2, icon: <Hash size={18} />, list: metrics.heading_counts.h2_list },
        { label: 'H3 Headings', value: metrics.heading_counts.h3, icon: <Hash size={18} />, list: metrics.heading_counts.h3_list },
        { label: 'CTA Actions', value: metrics.cta_count, icon: <Pointer size={18} /> },
        { label: 'Internal Links', value: metrics.links.internal, icon: <Link2 size={18} />, list: metrics.links.internal_list },
        { label: 'External Links', value: metrics.links.external, icon: <Link2 size={18} />, list: metrics.links.external_list },
        { label: 'Total Images', value: metrics.images.total, icon: <Image size={18} />, subValue: `(With Alt: ${metrics.images.with_alt} / Without Alt: ${metrics.images.without_alt})` },
        { label: 'Missing Alt %', value: `${metrics.images.missing_alt_pct.toFixed(1)}%`, subValue: `(${metrics.images.without_alt} / ${metrics.images.total} images)`, icon: <AltStatus metric={metrics.images.missing_alt_pct} /> },
    ];

    return (
        <div className="card">
            <h2 className="card-title">
                <FileText size={20} />
                <span>Factual Metrics</span>
            </h2>
            <div className="metrics-list">
                {items.map((item, idx) => (
                    <div key={idx} className="metric-item-container">
                        <div className="metric-item">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <span style={{ color: 'var(--primary)', display: 'flex' }}>{item.icon}</span>
                                <span className="metric-label">{item.label}</span>
                                {item.list && item.list.length > 0 && (
                                    <button
                                        className="info-btn"
                                        onClick={() => setSelectedMetric(item)}
                                        title="View Details"
                                    >
                                        <Info size={14} />
                                    </button>
                                )}
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                <div className="metric-value">{item.value}</div>
                                {item.subValue && <div className="metric-sub-value">{item.subValue}</div>}
                            </div>
                        </div>
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

            {/* Modal Popup */}
            {selectedMetric && (
                <div className="modal-overlay" onClick={() => setSelectedMetric(null)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>{selectedMetric.label} Details</h3>
                            <button className="close-btn" onClick={() => setSelectedMetric(null)}>
                                <X size={18} />
                            </button>
                        </div>
                        <div className="modal-body">
                            <ul>
                                {selectedMetric.list.map((li, i) => (
                                    <li key={i}>{li}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

// Helper to show alert icon if missing alt % is high
function AltStatus({ metric }) {
    if (metric > 20) return <AlertIcon size={18} color="var(--error)" />;
    return <Image size={18} />;
}

export default MetricsDisplay;
