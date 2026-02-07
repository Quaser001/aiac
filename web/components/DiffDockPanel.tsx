
import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import { Box, Play, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
// TIER1_REGISTRY imported below

interface DiffDockPanelProps {
    determinant: string;
}

import { useConsole } from '@/context/ConsoleContext';
import { isTier1, TIER1_REGISTRY } from '@/data/tier1_registry';

export function DiffDockPanel({ determinant }: DiffDockPanelProps) {
    const { ligand, setLigand, isDemoMode } = useConsole();

    // Local loading/result state remains local as it's panel-specific
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [useDynamicBind, setUseDynamicBind] = useState(false);
    const [refining, setRefining] = useState(false);
    const [refinedResult, setRefinedResult] = useState<any>(null);

    // Initial ligand set if empty and regular usage (Safety fallback)
    // But mostly rely on OverviewPage sync.


    const handleRunDiffDock = async () => {
        setLoading(true);
        setResult(null);
        setRefinedResult(null);
        try {
            // 1. Run DiffDock
            const res = await fetch("http://localhost:8000/docking/diffdock/run", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-abrisk-mode": isDemoMode ? "offline" : "online"
                },
                body: JSON.stringify({ determinant, ligand })
            });
            const data = await res.json();
            setResult(data);

            // 2. Run DynamicBind (if enabled and DiffDock successful)
            if (useDynamicBind && data.status === "success") {
                setRefining(true);
                try {
                    const refRes = await fetch("http://localhost:8000/docking/dynamicbind/refine", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ determinant, pose_data: "top_pose" })
                    });
                    const refData = await refRes.json();
                    setRefinedResult(refData);
                } catch (e) {
                    console.error("Refinement failed", e);
                } finally {
                    setRefining(false);
                }
            }

        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <GlassCard className="p-6 border-purple-500/20 bg-purple-950/10">
            <div className="flex items-center gap-3 mb-4">
                <Box className="w-5 h-5 text-teal-400" />
                <div>
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Tier-1 Binding Feasibility</h3>
                    <p className="text-[10px] text-teal-400">Experimental Evidence + Vina Re-docking</p>
                </div>
            </div>

            <div className="flex flex-col gap-3 mb-4">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={ligand}
                        onChange={(e) => setLigand(e.target.value)}
                        className="bg-black/30 border border-white/10 rounded px-3 py-1 text-xs text-white grow font-mono"
                        placeholder="Ligand SMILES or Name"
                    />
                    <button
                        onClick={handleRunDiffDock}
                        disabled={loading || !determinant}
                        className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded text-xs font-bold transition-colors disabled:opacity-50 flex items-center gap-2"
                    >
                        {loading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}
                        Generate
                    </button>
                </div>

                {/*                 
                 <div className="flex items-center gap-2 px-1">
                    <input
                        type="checkbox"
                        id="db-toggle"
                        checked={useDynamicBind}
                        onChange={(e) => setUseDynamicBind(e.target.checked)}
                        className="rounded border-white/20 bg-black/30 text-purple-500 focus:ring-purple-500/50"
                    />
                    <label htmlFor="db-toggle" className="text-xs text-slate-300 select-none cursor-pointer flex items-center gap-1.5">
                        Refine with DynamicBind
                        <span className="text-[9px] px-1 py-0.5 rounded bg-purple-500/20 text-purple-300 uppercase font-bold">Research</span>
                    </label>
                </div> 
*/}
            </div>

            {result && (
                <div className="animate-in fade-in slide-in-from-bottom-2 space-y-3">
                    {result.status === "success" ? (
                        <>
                            {/* Standard Results */}
                            <div className="p-3 bg-green-500/10 border border-green-500/20 rounded relative">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-xs font-bold text-green-400 flex items-center gap-1">
                                        <CheckCircle className="w-3 h-3" /> Binding Confirmed
                                    </span>
                                    {result.provenance && (
                                        <span className={cn(
                                            "text-[9px] px-1.5 py-0.5 rounded border uppercase font-bold tracking-wider ml-auto mr-2",
                                            result.provenance.includes("LIVE")
                                                ? "bg-indigo-500/20 border-indigo-500/40 text-indigo-300"
                                                : "bg-slate-700/40 border-slate-600 text-slate-400"
                                        )}>
                                            {result.provenance}
                                        </span>
                                    )}
                                    <span className="text-xs font-mono text-white">{result.score} kcal/mol</span>
                                </div>
                                <div className="text-[10px] text-slate-400 font-mono mb-2">
                                    Confidence: {(result.confidence * 100).toFixed(0)}% • Site: {result.binding_site}
                                </div>
                                <div className="flex gap-1">
                                    {result.poses?.map((p: string, i: number) => (
                                        <div key={i} className="px-2 py-1 bg-black/40 rounded text-[9px] text-zinc-400 border border-white/5">
                                            {p}
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Refinement Results */}
                            {useDynamicBind && (
                                <div className="animate-in fade-in slide-in-from-bottom-2 duration-700">
                                    {refining ? (
                                        <div className="p-3 bg-blue-500/5 border border-blue-500/10 rounded flex items-center gap-2">
                                            <Loader2 className="w-3 h-3 text-blue-400 animate-spin" />
                                            <span className="text-xs text-blue-300">Refining pose with induced fit...</span>
                                        </div>
                                    ) : refinedResult && refinedResult.status === 'success' ? (
                                        <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded mt-2">
                                            <div className="flex items-center justify-between mb-1">
                                                <span className="text-xs font-bold text-blue-400">DynamicBind Refinement</span>
                                                <span className="text-xs font-mono text-white font-bold">{refinedResult.refined_score} kcal/mol</span>
                                            </div>
                                            <p className="text-[10px] text-zinc-300 leading-relaxed">
                                                {refinedResult.structural_shift}
                                            </p>
                                        </div>
                                    ) : (
                                        <div className="p-2 bg-slate-800/50 rounded mt-2">
                                            <span className="text-[10px] text-slate-500 italic">
                                                {refinedResult?.message || "Refinement pending..."}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            )}
                        </>
                    ) : (
                        <div className={cn(
                            "p-3 rounded border",
                            result.status === 'unmapped'
                                ? "bg-slate-800/50 border-slate-700/50 text-slate-400"
                                : "bg-amber-500/10 border-amber-500/20 text-amber-500"
                        )}>
                            <div className="flex items-center gap-2 text-xs font-bold mb-1">
                                {result.status === 'unmapped' ? (
                                    <>
                                        <div className="w-2 h-2 rounded-full bg-slate-500" />
                                        Research Mode: Evidence Pending
                                    </>
                                ) : (
                                    <>
                                        <AlertTriangle className="w-3 h-3" />
                                        {result.message || "Docking failed"}
                                    </>
                                )}
                            </div>
                            <div className="text-[10px] opacity-70">
                                {result.disclaimer || (result.status === 'unmapped' ? "Specific ligand-determinant pair not yet cached for demo." : "")}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </GlassCard>
    );
}
