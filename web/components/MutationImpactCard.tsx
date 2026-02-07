
"use client";

import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Zap, AlertTriangle, CheckCircle, Activity, Info } from 'lucide-react';
import { isTier1, TIER1_REGISTRY } from '@/data/tier1_registry';
import { cn } from '@/lib/utils';
import { API_BASE } from '@/lib/api';

interface MutationImpactCardProps {
    determinant: string;
    mutationValue?: string;
    onMutationChange?: (val: string) => void;
}

interface ImpactResult {
    determinant: string;
    mutation: string;
    impact_score: number;
    risk_level: string;
    interpretation: string;
    saprot?: {
        score: number;
        label: string;
        model: string;
        status?: string;
        provenance?: string;
    };
    eve?: {
        score: number;
        label: string;
        model: string;
        status?: string;
        provenance?: string;
    };
    disclaimer: string;
}

export function MutationImpactCard({ determinant, mutationValue, onMutationChange }: MutationImpactCardProps) {
    const [localMutation, setLocalMutation] = useState("");

    // Use controlled or uncontrolled
    const mutation = mutationValue !== undefined ? mutationValue : localMutation;
    const setMutation = onMutationChange || setLocalMutation;

    const [availableVariants, setAvailableVariants] = useState<string[]>([]);
    const [fetchingVariants, setFetchingVariants] = useState(false);

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ImpactResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Fetch variants when determinant changes
    React.useEffect(() => {
        const fetchVariants = async () => {
            // Tier-1 Cache Lock (Conference Safe)
            // Tier-1 Cache Lock (Conference Safe)
            // Tier-1 Cache Lock (Conference Safe)
            if (determinant && isTier1(determinant)) {
                const truth = TIER1_REGISTRY[determinant];
                setAvailableVariants([...(truth.mutations || [])]);
                return;
            }

            setFetchingVariants(true);
            setLocalMutation(""); // Reset local selection
            if (onMutationChange) onMutationChange("");

            try {
                const res = await fetch(`${API_BASE}/mutation/variants?determinant=${determinant}`);
                if (res.ok) {
                    const data = await res.json();
                    setAvailableVariants(data.variants || []);
                } else {
                    setAvailableVariants([]);
                }
            } catch (e) {
                console.error("Failed to fetch variants", e);
                setAvailableVariants([]);
            } finally {
                setFetchingVariants(false);
            }
        };
        fetchVariants();
    }, [determinant]);

    const handleRunAnalysis = async () => {
        if (!mutation) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const res = await fetch(`${API_BASE}/mutation/impact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ determinant, mutation })
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Analysis failed");
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
        <GlassCard className="p-6 border-purple-500/20">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
                    <Zap className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                    <h2 className="text-lg font-bold text-white">Mutation Functional Impact</h2>
                    <div className="flex items-center gap-2 mt-1">
                        <p className="text-xs text-purple-400 uppercase tracking-widest font-bold">AI Research Layer (ESM-2)</p>

                        {/* Scope Badge */}
                        {determinant && isTier1(determinant) ? (
                            <span className="text-[9px] px-1.5 py-0.5 rounded border bg-green-500/10 border-green-500/30 text-green-400 font-bold uppercase tracking-wider">
                                🟢 Tier-1 Deep Evidence
                            </span>
                        ) : (
                            <span className="text-[9px] px-1.5 py-0.5 rounded border bg-blue-500/10 border-blue-500/30 text-blue-400 font-bold uppercase tracking-wider">
                                🔵 CARD Evidence Context
                            </span>
                        )}
                    </div>
                </div>
            </div>

            <p className="text-sm text-slate-400 mb-6 leading-relaxed">
                Estimate the functional disruption of point mutations using protein language models (ESM-2).
            </p>

            <div className="flex gap-3 mb-6">
                <div className="relative grow">
                    <select
                        value={mutation}
                        onChange={(e) => setMutation(e.target.value)}
                        disabled={fetchingVariants}
                        className="w-full bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all font-mono appearance-none"
                    >
                        <option value="">
                            {fetchingVariants ? "Loading variants..." : "Select a precomputed mutation variant"}
                        </option>
                        {availableVariants.map((v) => (
                            <option key={v} value={v}>
                                {v}
                            </option>
                        ))}
                    </select>
                    <label className="absolute -top-2 left-3 px-1 bg-[#0f172a] text-[10px] text-purple-400 font-bold">MUTATION</label>

                    {/* Fallback msg if no variants */}
                    {!fetchingVariants && availableVariants.length === 0 && (
                        <p className="text-xs text-amber-500 mt-1">No precomputed mutation variants available yet.</p>
                    )}
                </div>
                <button
                    onClick={handleRunAnalysis}
                    disabled={loading || !mutation}
                    className="btn-primary bg-purple-600 hover:bg-purple-500 border-purple-500 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                >
                    {loading ? (
                        <span className="flex items-center gap-2">
                            <Activity className="w-4 h-4 animate-spin" />
                            Running...
                        </span>
                    ) : (
                        "Run Impact Score"
                    )}
                </button>
            </div>

            {error && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400 flex items-center gap-2 mb-4">
                    <AlertTriangle className="w-4 h-4" />
                    {error}
                </div>
            )}

            {result && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        {/* 1. ESM-2 Score (Sequence) */}
                        <div className="p-4 rounded-lg bg-teal-950/30 border border-teal-500/20 relative">
                            {/* Provenance Badge */}
                            {result.saprot?.provenance && (
                                <div className={cn(
                                    "absolute top-2 right-2 text-[8px] font-bold px-1.5 py-0.5 rounded border uppercase tracking-wider",
                                    result.saprot.provenance.includes("LIVE")
                                        ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-400"
                                        : "bg-slate-700/50 border-slate-600 text-slate-400"
                                )}>
                                    {result.saprot.provenance}
                                </div>
                            )}

                            <span className="text-[10px] uppercase text-teal-400 font-bold tracking-wider block mb-2">
                                ESM-2 (Sequence Only)
                            </span>
                            <div className="flex items-end gap-3">
                                <span className="text-3xl font-mono text-white font-bold">
                                    {result.impact_score.toFixed(3)}
                                </span>
                                <span className={cn(
                                    "text-xs px-2 py-1 rounded font-bold uppercase",
                                    result.risk_level === "High" ? "bg-red-500/20 text-red-400" :
                                        result.risk_level === "Moderate" ? "bg-amber-500/20 text-amber-400" :
                                            "bg-teal-500/20 text-teal-400"
                                )}>
                                    {result.risk_level} Risk
                                </span>
                            </div>
                        </div>

                        {/* 2. SaProt Score (Structure Aware) - NEW */}
                        <div className="p-4 rounded-lg bg-purple-900/20 border border-purple-500/30 relative overflow-hidden">
                            <div className="absolute top-0 right-0 px-2 py-1 bg-purple-500 text-[9px] text-white font-bold">
                                ProteinGym SOTA
                            </div>
                            <span className="text-[10px] uppercase text-purple-300 font-bold tracking-wider block mb-2">
                                SaProt (Structure Aware)
                            </span>
                            {result.saprot && result.saprot.status !== 'missing' ? (
                                <div>
                                    <div className="flex items-end gap-3 mb-1">
                                        <span className="text-3xl font-mono text-white font-bold">
                                            {result.saprot.score?.toFixed(3) || "N/A"}
                                        </span>
                                        <span className="text-xs text-purple-200">
                                            {result.saprot.label}
                                        </span>
                                    </div>
                                    <div className="text-[9px] text-purple-400/60 font-mono mt-1">
                                        Model: {result.saprot.model || "SaProt_650M_3Di"}
                                    </div>
                                </div>
                            ) : (
                                <div className="text-xs text-purple-400/50 italic h-full flex items-center">
                                    Structure-aware score not available for this variant.
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="p-3 rounded border border-white/5 bg-white/5">
                        <div className="flex gap-2">
                            <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                            <p className="text-xs text-slate-300 leading-relaxed">
                                {result.interpretation}
                                {result.saprot?.status !== 'missing' && (
                                    <span className="block mt-1 text-purple-300">
                                        Note: Structural analysis confirms {result.saprot?.label?.toLowerCase() || "impact"}.
                                    </span>
                                )}
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </GlassCard>
    );
}
