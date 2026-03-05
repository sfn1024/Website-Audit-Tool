import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

function AuditForm({ onAudit, loading }) {
    const [url, setUrl] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (url.trim()) {
            onAudit(url.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-group">
            <input
                type="url"
                placeholder="https://example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                disabled={loading}
            />
            <button type="submit" disabled={loading || !url.trim()}>
                {loading ? (
                    <>
                        <Loader2 size={20} className="loading-spinner" />
                        <span>Analyzing...</span>
                    </>
                ) : (
                    <>
                        <Search size={20} />
                        <span>Audit Site</span>
                    </>
                )}
            </button>
        </form>
    );
}

export default AuditForm;
