"use client";

import dynamic from "next/dynamic";
import { useConsole } from "@/context/ConsoleContext";
import { Box, ArrowLeft, Database, Microscope } from "lucide-react";
import Link from "next/link";
import { GlassCard } from "@/components/GlassCard";
import { TIER1_REGISTRY } from "@/data/tier1_registry";
import { extractResidueNumber } from "@/lib/mutation";
import { useState, useEffect } from "react";

// Dynamic import to prevent SSR hydration mismatch with WebGL refs
const StructureViewer = dynamic(() => import("@/components/StructureViewer"), {
    ssr: false,
    loading: () => <div className="h-[420px] w-full bg-slate-900/50 animate-pulse rounded-xl" />
});

export default function StructurePage() {
    const { determinant, structureStatus } = useConsole();

    // Local state for mutation selection (since context might not hold it yet)
    // Default to first mutation if available
    const [selectedMutation, setSelectedMutation] = useState<string>("");

    const tier1Data = TIER1_REGISTRY[determinant];
    // If Tier-1, use its PDB (or undefined if unmapped). If not, fallback to status or default 4RL2.
    // For vanA (Tier-1 but no PDB), pdbId will be undefined (null in registry), which we handle.
    const pdbId = tier1Data ? (tier1Data.pdb || undefined) : (structureStatus?.pdb_id || "4RL2");

    // Effect to set default mutation when determinant changes
    useEffect(() => {
        if (tier1Data?.mutations?.length) {
            setSelectedMutation(tier1Data.mutations[0]);
        }
    }, [determinant, tier1Data]);

    const highlightResidue = selectedMutation ? extractResidueNumber(selectedMutation) || undefined : undefined;

    // If no determinant, show empty state
    if (!determinant) {
        return (
            <div className="flex flex-col items-center justify-center h-[50vh] text-slate-500">
                <Box className="w-12 h-12 mb-4 opacity-20" />
                <p>Select a determinant in Overview to view structure.</p>
                <Link href="/console/overview" className="mt-4 text-teal-400 hover:text-teal-300 flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Return to Overview
                </Link>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in pb-10">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Structure Intelligence</h2>
                    <p className="text-slate-400 text-sm">Tier-1 Confirmed Structural Localization</p>
                </div>
                {tier1Data ? (
                    <div className="flex items-center gap-2 px-3 py-1 bg-teal-500/10 border border-teal-500/20 rounded-full">
                        <Database className="w-3 h-3 text-teal-400" />
                        <span className="text-teal-400 text-xs font-bold tracking-wide">TIER-1 CONFIRMED</span>
                    </div>
                ) : (
                    <div className="px-3 py-1 bg-purple-500/10 border border-purple-500/20 rounded text-purple-400 text-xs font-mono">
                        PDB: {pdbId}
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:col-span-3 gap-6">
                {/* Main Viewer */}
                <div className="lg:col-span-2">
                    <StructureViewer
                        pdbId={pdbId}
                        highlightResidue={highlightResidue}
                    />

                    <div className="mt-4 flex flex-wrap gap-4 text-xs text-slate-500 font-mono">
                        <div className="flex items-center gap-2">
                            <span className="block w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]"></span>
                            Mutation Highlight ({selectedMutation || "None"})
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="block w-2 h-2 rounded-full bg-gradient-to-r from-blue-500 to-green-500 opacity-50"></span>
                            B-Factor Spectrum
                        </div>
                    </div>
                </div>

                {/* Side Panel (Details) */}
                <div className="space-y-4">
                    {/* Mutation Selector */}
                    <GlassCard className="p-5 border-white/5">
                        <h3 className="text-slate-400 font-bold uppercase tracking-widest text-xs mb-4 flex items-center gap-2">
                            <Microscope className="w-3 h-3" />
                            Target Mutation
                        </h3>

                        {tier1Data ? (
                            <div className="space-y-3">
                                <label className="text-xs text-slate-500">Select Variant</label>
                                <select
                                    value={selectedMutation}
                                    onChange={(e) => setSelectedMutation(e.target.value)}
                                    className="w-full bg-black/40 border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-teal-500/50"
                                >
                                    {tier1Data.mutations.map(m => (
                                        <option key={m} value={m}>{m}</option>
                                    ))}
                                </select>

                                <div className="p-3 bg-slate-900/50 rounded border border-white/5 text-xs text-slate-300">
                                    Residue <span className="text-teal-400 font-bold">{highlightResidue}</span> mapped to structural coordinates.
                                </div>
                            </div>
                        ) : (
                            <p className="text-xs text-slate-500 italic">No mapped mutations for this determinant.</p>
                        )}
                    </GlassCard>

                    <GlassCard className="p-5 border-white/5">
                        <h3 className="text-slate-400 font-bold uppercase tracking-widest text-xs mb-3">
                            Structure Metadata
                        </h3>
                        <div className="space-y-3 text-sm">
                            <div className="flex justify-between border-b border-white/5 pb-2">
                                <span className="text-slate-500">PDB ID</span>
                                <span className="text-white font-mono">{pdbId}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-2">
                                <span className="text-slate-500">Label</span>
                                <span className="text-white text-right w-1/2 truncate">{tier1Data?.mechanism_type || "Unknown Protein"}</span>
                            </div>
                            <div className="flex justify-between pt-1">
                                <span className="text-slate-500">Source</span>
                                <span className="text-teal-400 text-xs bg-teal-950/30 px-2 py-0.5 rounded border border-teal-500/20">RCSB Experimental</span>
                            </div>
                        </div>
                    </GlassCard>
                </div>
            </div>
        </div>
    );
}
