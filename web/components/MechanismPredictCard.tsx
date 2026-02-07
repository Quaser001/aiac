
"use client";

import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Network, AlertTriangle, PlayCircle, Bot, Info } from 'lucide-react';
import { API_BASE } from '@/lib/api';

interface PredictionResult {
    predicted_class: string;
    confidence: number;
    explanation: string;
    disclaimer: string;
}

export function MechanismPredictCard() {
    const [sequence, setSequence] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<PredictionResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handlePredict = async () => {
        if (!sequence) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const res = await fetch(`${API_BASE}/mechanism/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sequence: sequence.replace(/\s/g, '') }) // Clean whitespace
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Prediction failed");
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
        <GlassCard className="p-6 border-indigo-500/20 mt-6">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/20">
                    <Bot className="w-5 h-5 text-indigo-400" />
                </div>
                <div>
                    <h2 className="text-lg font-bold text-white">Mechanism Prediction</h2>
                    <p className="text-xs text-indigo-400 uppercase tracking-widest font-bold">AI Classifier Layer (ESM-2 + LogReg)</p>
                </div>
            </div>

            <p className="text-sm text-slate-400 mb-6 leading-relaxed">
                Predict the resistance mechanism class for unknown sequences using few-shot embedded classification.
            </p>

            <div className="mb-4">
                <textarea
                    value={sequence}
                    onChange={(e) => setSequence(e.target.value)}
                    placeholder="Paste protein sequence (MKK...)"
                    className="w-full h-24 bg-slate-900/50 border border-white/10 rounded-lg px-4 py-3 text-xs text-slate-300 placeholder-slate-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all font-mono resize-none"
                />
            </div>

            <button
                onClick={handlePredict}
                disabled={loading || !sequence}
                className="btn-primary bg-indigo-600 hover:bg-indigo-500 border-indigo-500 w-full disabled:opacity-50 disabled:cursor-not-allowed justify-center"
            >
                {loading ? (
                    <span className="flex items-center gap-2">
                        <Network className="w-4 h-4 animate-spin" />
                        Running Classifier...
                    </span>
                ) : (
                    "Predict Mechanism Class"
                )}
            </button>

            {error && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400 flex items-center gap-2 mt-4">
                    <AlertTriangle className="w-4 h-4" />
                    {error}
                </div>
            )}

            {result && (
                <div className="animate-fade-in bg-slate-900/50 rounded-xl border border-white/5 overflow-hidden mt-6">
                    <div className="p-4 grid grid-cols-2 gap-4 border-b border-white/5">
                        <div>
                            <span className="text-[10px] text-slate-500 uppercase tracking-widest block mb-1">Predicted Class</span>
                            <div className="text-lg font-bold text-white break-words">{result.predicted_class}</div>
                        </div>
                        <div>
                            <span className="text-[10px] text-slate-500 uppercase tracking-widest block mb-1">Confidence</span>
                            <div className="text-2xl font-mono text-indigo-400">{result.confidence.toFixed(2)}</div>
                        </div>
                    </div>
                    <div className="p-4 bg-white/[0.02]">
                        <p className="text-sm text-slate-300 mb-2 flex items-start gap-2">
                            <Info className="w-4 h-4 text-indigo-400 mt-0.5 shrink-0" />
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
