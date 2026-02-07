"use client";

import React, { useEffect } from 'react';
import { GlassCard } from '@/components/GlassCard';
import { AsyncCombobox } from '@/components/AsyncCombobox';
import { EvidenceLadder } from '@/components/EvidenceLadder';
import { Loader2, Info, ArrowRight, ShieldCheck, Activity } from 'lucide-react';
import { useConsole } from '@/context/ConsoleContext';
import Link from 'next/link';
import { API_BASE } from '@/lib/api';
import { TIER1_REGISTRY, isTier1 } from '@/data/tier1_registry';

export default function ConsoleOverviewPage() {
    const {
        determinant,
        setDeterminant,
        organism,
        setOrganism,
        setLigand,
        analysisResult,
        setAnalysisResult,
        setStructureStatus,
        setDockingStatus,
        isDemoMode,
        setIsDemoMode
    } = useConsole();

    // Auto-sync Tier-1 Defaults
    useEffect(() => {
        if (determinant && isTier1(determinant)) {
            const def = TIER1_REGISTRY[determinant];
            setOrganism(def.host);
            setLigand(def.ligand.name);
        }
    }, [determinant, setOrganism, setLigand]);

    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState<string | null>(null);

    const handleAnalyze = async () => {
        // ... (rest of function)
        if (!determinant) return;
        setLoading(true);
        setError(null);

        try {
            // 1. Mechanism Analysis (Layer 2A/1.5)
            const res = await fetch(`${API_BASE}/specialist/analyze/mechanism`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    gene_id: determinant,
                    family: 'Unknown',
                    organism_context: organism || null
                }),
            });

            if (!res.ok) throw new Error("Analysis failed");
            const data = await res.json();
            setAnalysisResult(data);

            // 2. Structure Status Check (Layer 3)
            try {
                const structRes = await fetch(`${API_BASE}/structure/${determinant}`);
                if (structRes.ok) {
                    const structData = await structRes.json();
                    setStructureStatus(structData);
                }
            } catch (e) {
                console.warn("Structure check failed", e);
            }

            // 3. Docking Status Check (Layer 4)
            try {
                const dockingRes = await fetch(`${API_BASE}/docking/status`);
                if (dockingRes.ok) {
                    const dockingData = await dockingRes.json();
                    setDockingStatus(dockingData);
                }
            } catch (e) {
                console.warn("Docking check failed", e);
            }

        } catch (err: any) {
            console.error("Analysis Error:", err);
            const msg = err.message === "Failed to fetch"
                ? "Backend offline or API unreachable"
                : err.message;
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8 animate-fade-in">
            {/* Header / Config */}
            <div className="flex flex-col xl:flex-row gap-8 items-start">

                {/* Intro Card */}
                <div className="flex-1">
                    <h2 className="text-2xl font-bold text-white mb-2">Evidence Overview</h2>
                    <p className="text-slate-400 max-w-2xl">
                        Configure the resistance determinant and organism context to generate a multi-layered evidence report.
                        Navigate through the specialized modules on the left to inspect specific data layers.
                    </p>
                </div>

                {/* Analysis Configurator */}
                <GlassCard className="w-full xl:w-[450px] p-6 border-teal-500/20 bg-slate-900/50">
                    <h3 className="text-teal-400 font-bold uppercase tracking-widest text-xs mb-4 flex items-center gap-2">
                        <Activity className="w-4 h-4" />
                        Analysis Configuration
                    </h3>

                    <div className="space-y-4">
                        <div>
                            <AsyncCombobox
                                label="Resistance Determinant (CARD)"
                                placeholder="e.g. NDM-1, KPC-2..."
                                value={determinant}
                                onChange={(val) => setDeterminant(val)}
                            />
                            {/* Tier-1 Chips */}
                            <div className="flex flex-wrap gap-2 mt-2">
                                {Object.keys(TIER1_REGISTRY ?? {}).map((chip: string) => (
                                    <button
                                        key={chip}
                                        onClick={() => setDeterminant(chip)}
                                        className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wide border transition-all
                                            ${determinant === chip
                                                ? 'bg-teal-500/20 border-teal-500 text-teal-400'
                                                : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                                            }`}
                                    >
                                        {chip}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div>
                            <AsyncCombobox
                                label="Host Organism (Optional)"
                                placeholder="e.g. Klebsiella pneumoniae"
                                value={organism}
                                onChange={(val) => setOrganism(val)}
                                endpoint="/specialist/phenotype/organisms/search"
                            />
                            {/* Host Organism Chips */}
                            <div className="flex flex-wrap gap-2 mt-2">
                                {[...new Set(Object.values(TIER1_REGISTRY ?? {}).map(v => v.host))].map((chip: string) => (
                                    <button
                                        key={chip}
                                        onClick={() => setOrganism(chip)}
                                        className={`px-2 py-0.5 rounded text-[10px] italic font-mono border transition-all
                                            ${organism === chip
                                                ? 'bg-blue-500/20 border-blue-500 text-blue-400'
                                                : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                                            }`}
                                    >
                                        {chip}
                                    </button>
                                ))}                            </div>
                            <p className="text-[10px] text-slate-500 mt-2 pl-1">
                                * Suggestions based on BV-BRC data.
                            </p>
                        </div>

                        <button
                            onClick={handleAnalyze}
                            disabled={loading || !determinant}
                            className={`w-full py-2.5 rounded font-bold text-sm uppercase tracking-wide transition-all
                                ${loading
                                    ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                                    : 'bg-teal-500 hover:bg-teal-400 text-slate-900 shadow-lg shadow-teal-900/20'
                                }
                            `}
                        >
                            {loading ? (
                                <div className="flex items-center justify-center gap-2">
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Analyzing...
                                </div>
                            ) : (
                                "Run Multi-Layer Analysis"
                            )}
                        </button>

                        <div className="flex items-center justify-between pt-2 border-t border-white/5">
                            <span className="text-[10px] text-slate-500 font-medium uppercase tracking-wider" title="Tier-1 deterministic evidence (offline-safe)">
                                Conference Demo Mode
                            </span>
                            <button
                                onClick={() => setIsDemoMode(!isDemoMode)}
                                className={`flex items-center gap-2 px-2 py-1 rounded text-[10px] font-bold border transition-all ${isDemoMode
                                    ? "bg-green-500/10 border-green-500/30 text-green-400"
                                    : "bg-amber-500/10 border-amber-500/30 text-amber-400"
                                    }`}
                            >
                                {isDemoMode ? (
                                    <>
                                        <ShieldCheck className="w-3 h-3" />
                                        DEMO (OFFLINE SECURE)
                                    </>
                                ) : (
                                    <>
                                        <Activity className="w-3 h-3" />
                                        ONLINE (RESEARCH)
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </GlassCard>
            </div>

            {/* Error Display */}
            {error && (
                <div className="p-4 bg-red-500/10 border border-red-500/20 rounded text-red-400 text-sm">
                    Analysis Error: {error}
                </div>
            )}

            {/* Results Grid */}
            {analysisResult && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    {/* Evidence Ladder Summary */}
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <h3 className="heading-md">Evidence Ladder Status</h3>
                            <span className="text-xs text-green-400 flex items-center gap-1 bg-green-500/10 px-2 py-1 rounded border border-green-500/20">
                                <ShieldCheck className="w-3 h-3" />
                                Analysis Complete
                            </span>
                        </div>
                        <EvidenceLadder activeLayers={[1, 2, 3, 4]} />
                    </div>

                    {/* Quick Links / Navigation Cards */}
                    <div className="space-y-4">
                        <h3 className="heading-md">Deep Dive Modules</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                            <NavCard
                                title="Mechanism"
                                desc="CARD Ontology & Classification"
                                href="/console/mechanism"
                            />
                            <NavCard
                                title="Phenotype"
                                desc="BV-BRC MIC Evidence"
                                href="/console/phenotype"
                            />
                            <NavCard
                                title="Structure"
                                desc="3Dmol.js Provenance"
                                href="/console/structure"
                            />
                            <NavCard
                                title="Mutation Impact"
                                desc="ESM-2 Structural Impact"
                                href="/console/ai/impact"
                            />
                        </div>
                    </div>
                </div>
            )}

            {!analysisResult && !loading && (
                <div className="flex flex-col items-center justify-center py-20 opacity-50">
                    <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-4">
                        <Activity className="w-8 h-8 text-slate-600" />
                    </div>
                    <p className="text-slate-500 text-sm">Waiting for analysis parameters...</p>
                </div>
            )}

        </div>
    );
}

function NavCard({ title, desc, href }: { title: string, desc: string, href: string }) {
    return (
        <Link href={href} className="group block">
            <GlassCard className="h-full p-4 border-teal-500/10 hover:border-teal-500/40 hover:bg-teal-500/5 transition-all cursor-pointer">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-teal-400 font-bold uppercase tracking-wider text-xs">{title}</span>
                    <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-teal-400 transition-colors" />
                </div>
                <p className="text-slate-400 text-sm">{desc}</p>
            </GlassCard>
        </Link>
    );
}
