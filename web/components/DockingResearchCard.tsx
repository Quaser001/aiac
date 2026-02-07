
"use client";

import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Microscope, Zap, Database, Info, AlertTriangle } from 'lucide-react';
import { API_BASE } from '@/lib/api';

export function DockingResearchCard() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const handleRunDemo = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        // Simulate request to backend
        try {
            const res = await fetch(`${API_BASE}/docking/research-demo`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    determinant: "NDM-1",
                    ligand: "Meropenem"
                })
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Demo failed");
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
        <GlassCard className="p-6 border-purple-500/20 mt-6 bg-purple-900/5">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
                    <Microscope className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                    <h2 className="text-lg font-bold text-white">Binding Feasibility (Research Mode)</h2>
                    <p className="text-xs text-purple-400 uppercase tracking-widest font-bold">Research Showcase • DiffDock-Simulated</p>
                </div>
            </div>

            <p className="text-sm text-slate-400 mb-6 leading-relaxed">
                Demonstrates AI-driven small molecule docking potential. Currently in showcase mode with precomputed high-fidelity assets for conference stability.
            </p>

            <div className="flex flex-col md:flex-row gap-4 mb-6">
                <div className="flex-1 bg-slate-900/50 p-3 rounded-lg border border-white/5 flex items-center justify-between">
                    <span className="text-xs text-slate-500 uppercase tracking-wider">Showcase Determinant</span>
                    <span className="text-white font-mono font-bold">NDM-1</span>
                </div>
                <div className="flex-1 bg-slate-900/50 p-3 rounded-lg border border-white/5 flex items-center justify-between">
                    <span className="text-xs text-slate-500 uppercase tracking-wider">Ligand</span>
                    <span className="text-white font-mono font-bold">Meropenem</span>
                </div>
            </div>

            {!result && (
                <button
                    onClick={handleRunDemo}
                    disabled={loading}
                    className="btn-primary w-full justify-center bg-purple-600 hover:bg-purple-500 border-purple-500 py-4"
                >
                    {loading ? (
                        <span className="flex items-center gap-2">
                            <Zap className="w-4 h-4 animate-spin" />
                            Initializing Research Runtime...
                        </span>
                    ) : (
                        "Run Binding Feasibility Demo"
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
                <div className="animate-fade-in space-y-4">
                    <div className="bg-slate-900/50 rounded-xl border border-white/5 overflow-hidden mt-4">
                        <div className="p-4 flex items-center justify-between border-b border-white/5 bg-purple-500/5">
                            <div>
                                <span className="text-[10px] text-purple-300 uppercase tracking-widest block mb-1">Binding Affinity</span>
                                <div className="text-3xl font-mono text-white">{result.binding_score} <span className="text-sm text-slate-500">kcal/mol</span></div>
                            </div>
                            <div className="text-right">
                                <div className="text-xs text-purple-400 font-bold bg-purple-500/10 px-3 py-1 rounded-full border border-purple-500/20">
                                    Strong Binding
                                </div>
                            </div>
                        </div>
                        <div className="p-4">
                            <div className="flex items-start gap-2 p-3 bg-white/5 rounded-lg border border-white/5 text-xs text-slate-300 font-mono mb-2">
                                <Database className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                                <div>
                                    <div className="mb-1 text-purple-300">ASSET RETRIEVED:</div>
                                    <div>POSE_FILE: {result.pose_file}</div>
                                    <div>CONFIDENCE_SCORE: Demo High-Fidelity</div>
                                </div>
                            </div>
                            <p className="text-[10px] text-slate-500 italic mt-2 border-t border-white/5 pt-2">
                                {result.disclaimer}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            <div className="mt-6 pt-6 border-t border-white/5">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 opacity-50">
                        <input type="checkbox" disabled className="rounded border-slate-600 bg-slate-800 text-purple-500" />
                        <span className="text-xs text-slate-500">Enable Full Docking (Future HPC Mode)</span>
                    </div>
                    <span className="text-[10px] text-slate-600 bg-slate-900 px-2 py-1 rounded border border-white/5">Coming Q3 2026</span>
                </div>
            </div>
        </GlassCard>
    );
}
