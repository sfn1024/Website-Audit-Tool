import React from 'react';
import { ClipboardList, MoveRight, HelpCircle } from 'lucide-react';

function RecommendationsList({ recommendations }) {
    if (!recommendations || recommendations.length === 0) return null;

    return (
        <div className="card">
            <h2 className="card-title">
                <ClipboardList size={20} />
                <span>Prioritized Recommendations</span>
            </h2>
            <div className="recommendations-list">
                {recommendations
                    .sort((a, b) => a.priority - b.priority)
                    .map((rec, idx) => (
                        <div key={idx} className="rec-item">
                            <div className="rec-header">
                                <span className={`priority-pill priority-${rec.priority}`}>
                                    P{rec.priority}
                                </span>
                                <strong style={{ fontSize: '0.95rem' }}>{rec.title}</strong>
                            </div>
                            <div className="rec-body">
                                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <HelpCircle size={16} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: '2px' }} />
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                        {rec.reasoning}
                                    </div>
                                </div>
                                <div className="rec-action">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontWeight: '700', fontSize: '0.75rem', marginBottom: '0.25rem', textTransform: 'uppercase' }}>
                                        <MoveRight size={14} />
                                        <span>Action Item</span>
                                    </div>
                                    <div>{rec.action}</div>
                                </div>
                            </div>
                        </div>
                    ))}
            </div>
        </div>
    );
}

export default RecommendationsList;
