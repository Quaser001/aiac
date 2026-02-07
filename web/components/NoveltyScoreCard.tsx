
"use client";

import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Radar, AlertTriangle, Fingerprint, Activity } from 'lucide-react';
import { API_BASE } from '@/lib/api';

interface NoveltyScoreCardProps {
    determinant: string;
}

interface NoveltyResult {
    novelty_score: number;
    category: string;
    explanation: string;
    disclaimer: string;
}

export function NoveltyScoreCard({ determinant }: NoveltyScoreCardProps) {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<NoveltyResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleRunScan = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const res = await fetch(`${API_BASE}/novelty/score`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ determinant })
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Scan failed");
            }

            const data = await res.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <GlassCard className="p-6 border-cyan-500/20 mt-6">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
                    <Fingerprint className="w-5 h-5 text-cyan-400" />
                </div>
                <div>
                    <h2 className="text-lg font-bold text-white">Novel Variant Detection</h2>
                    <p className="text-xs text-cyan-400 uppercase tracking-widest font-bold">AI Surveillance Layer (ESM-2 Embeddings)</p>
                </div>
            </div>

            <p className="text-sm text-slate-400 mb-6 leading-relaxed">
                Scan sequence embeddings against a known reference bank to identify potential out-of-distribution (novel) variants.
            </p>

            {!result && (
                <button
                    onClick={handleRunScan}
                    disabled={loading}
                    className="btn-secondary w-full text-center justify-center border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 disabled:opacity-50 disabled:cursor-not-allowed py-3"
                >
                    {loading ? (
                        <span className="flex items-center justify-center gap-2">
                            <Activity className="w-4 h-4 animate-spin" />
                            Scanning Vector Space...
                        </span>
                    ) : (
                        "Run Novelty Scan"
                    )}
                </button>
            )}

            {error && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400 flex items-center gap-2 mt-4">
                    <AlertTriangle className="w-4 h-4" />
                    {error}
                </div>
            )}

            {result && (
                <div className="animate-fade-in bg-slate-900/50 rounded-xl border border-white/5 overflow-hidden mt-4">
                    <div className="p-4 flex items-center justify-between border-b border-white/5">
                        <div>
                            <span className="text-[10px] text-slate-500 uppercase tracking-widest block mb-1">Novelty Score</span>
                            <div className="text-2xl font-mono text-white">{result.novelty_score.toFixed(2)}</div>
                        </div>
                        <div className="text-right">
                            <div className={`px-3 py-1 rounded-full text-xs font-bold border ${result.novelty_score < 0.3 ? 'bg-green-500/10 border-green-500/20 text-green-400' :
                                result.novelty_score < 0.7 ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                                    'bg-red-500/10 border-red-500/20 text-red-400'
                                }`}>
                                {result.category}
                            </div>
                        </div>
                    </div>
                    <div className="p-4 bg-white/[0.02]">
                        <p className="text-sm text-slate-300 mb-2 flex items-start gap-2">
                            <Radar className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
                            {result.explanation}
                        </p>
                        <p className="text-[10px] text-slate-600 italic border-t border-white/5 pt-2 mt-2">
                            {result.disclaimer}
                        </p>
                    </div>
                </div>
            )}
        </GlassCard>
    );
}
