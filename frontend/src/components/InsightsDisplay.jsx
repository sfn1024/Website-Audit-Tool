import React from 'react';
import { Sparkles, BarChart, MessageSquare, Target, Layers, Layout } from 'lucide-react';

function InsightsDisplay({ insights }) {
    const blocks = [
        { label: 'SEO Analysis', text: insights.seo_analysis, icon: <BarChart size={16} /> },
        { label: 'Messaging Clarity', text: insights.messaging_clarity, icon: <MessageSquare size={16} /> },
        { label: 'CTA Usage', text: insights.cta_usage, icon: <Target size={16} /> },
        { label: 'Content Depth', text: insights.content_depth, icon: <Layers size={16} /> },
        { label: 'UX Concerns', text: insights.ux_concerns, icon: <Layout size={16} /> },
    ];

    return (
        <div className="card">
            <h2 className="card-title">
                <Sparkles size={20} color="var(--primary)" />
                <span>AI Performance Analysis</span>
            </h2>
            <div className="insights-container">
                {blocks.map((block, idx) => (
                    <div key={idx} className="insight-block">
                        <div className="insight-header">
                            {block.icon}
                            <span>{block.label}</span>
                        </div>
                        <div className="insight-text">{block.text}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default InsightsDisplay;
