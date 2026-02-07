"use client";

import dynamic from "next/dynamic";
import { useConsole } from "@/context/ConsoleContext";
import { GlassCard } from "@/components/GlassCard";
import { Dna, ArrowLeft, Activity } from "lucide-react";
import Link from "next/link";
export default function MechanismPage() {
    const { analysisResult, determinant } = useConsole();

    if (!analysisResult) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-slate-500">
                <Dna className="w-12 h-12 mb-4 opacity-20" />
                <p>No analysis data found.</p>
                <Link href="/console" className="mt-4 text-teal-400 hover:text-teal-300 flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Return to Overview
                </Link>
            </div>
        );
    }

    const { mechanism, constraints, structure } = analysisResult;

    return (
        <div className="space-y-8 animate-fade-in pb-20">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/5 pb-6">
                <div>
                    <h2 className="text-3xl font-bold text-white mb-2">Mechanism Intelligence</h2>
                    <p className="text-slate-400">Multi-modal analysis of resistance determinant {determinant}</p>
                </div>
                <div className="px-4 py-2 bg-teal-500/10 border border-teal-500/20 rounded-lg text-teal-400 font-mono text-lg tracking-wider">
                    {determinant || mechanism.gene_id}
                </div>
            </div>

            {/* Top Row: Core Classification & Constraints */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <GlassCard className="p-6 border-purple-500/20">
                    <h3 className="text-purple-400 font-bold uppercase tracking-widest text-xs mb-4 flex items-center gap-2">
                        <Dna className="w-4 h-4" />
                        Genetic Classification
                    </h3>
                    <div className="space-y-4">
                        <div className="flex justify-between border-b border-white/5 pb-2">
                            <span className="text-slate-400 text-sm">Mechanism Class</span>
                            <span className="text-white font-medium">{mechanism.mechanism_class || "Unknown"}</span>
                        </div>
                        <div className="flex justify-between border-b border-white/5 pb-2">
                            <span className="text-slate-400 text-sm">Catalytic Type</span>
                            <span className="text-white font-medium">{mechanism.catalytic_type || "N/A"}</span>
                        </div>
                        <div className="mt-4">
                            <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Structural Description</p>
                            <p className="text-sm text-slate-300 leading-relaxed">
                                {mechanism.structural_impact || "No structural data available."}
                            </p>
                        </div>
                    </div>
                </GlassCard>

                <GlassCard className="p-6 border-amber-500/20">
                    <h3 className="text-amber-400 font-bold uppercase tracking-widest text-xs mb-4 flex items-center gap-2">
                        <Activity className="w-4 h-4" />
                        Therapeutic Constraints
                    </h3>
                    <div className="space-y-3">
                        {constraints && constraints.length > 0 ? (
                            constraints.map((c: any, i: number) => (
                                <div key={i} className="bg-amber-500/5 border border-amber-500/10 p-3 rounded">
                                    <h4 className="text-amber-200 text-sm font-semibold mb-1">{c.type}</h4>
                                    <p className="text-slate-400 text-xs">{c.description}</p>
                                </div>
                            ))
                        ) : (
                            <p className="text-slate-500 text-sm">No specific constraints identified.</p>
                        )}
                    </div>
                </GlassCard>
            </div>

            {/* Deep Dive Links */}
            <div className="pt-8 border-t border-white/5 text-center">
                <p className="text-slate-500 text-sm">
                    Additional layers (Structure, Mutation, Docking) available in the sidebar.
                </p>
            </div>
        </div>
    );
}
