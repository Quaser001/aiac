"use client";

import { useConsole } from "@/context/ConsoleContext";
import { GlassCard } from "@/components/GlassCard";
import { Beaker, ArrowLeft, Database } from "lucide-react";
import Link from "next/link";

export default function PhenotypePage() {
    const { analysisResult, organism } = useConsole();

    if (!analysisResult) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-slate-500">
                <Beaker className="w-12 h-12 mb-4 opacity-20" />
                <p>No analysis data found.</p>
                <Link href="/console" className="mt-4 text-teal-400 hover:text-teal-300 flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Return to Overview
                </Link>
            </div>
        );
    }

    const { phenotype_evidence } = analysisResult;

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Phenotype Evidence</h2>
                    <p className="text-slate-400 text-sm">Observational MIC Data (BV-BRC)</p>
                </div>
                {organism && (
                    <div className="px-3 py-1 bg-blue-500/10 border border-blue-500/20 rounded text-blue-400 text-xs font-mono">
                        Host: {organism}
                    </div>
                )}
            </div>

            <GlassCard className="p-0 border-blue-500/20 overflow-hidden">
                <div className="p-4 bg-blue-500/5 border-b border-white/5 flex items-center justify-between">
                    <h3 className="text-blue-400 font-bold uppercase tracking-widest text-xs flex items-center gap-2">
                        <Database className="w-4 h-4" />
                        Susceptibility Profile
                    </h3>
                    <span className="text-[10px] text-slate-500">Source: {phenotype_evidence?.source || "N/A"}</span>
                </div>

                {!phenotype_evidence || !phenotype_evidence.evidence ? (
                    <div className="p-8 text-center text-slate-500 text-sm">
                        <p className="mb-2">Evidence available when present in BV-BRC.</p>
                        <p className="text-xs text-slate-600">Phenotype evidence is coverage-dependent.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs text-slate-400 uppercase bg-white/5">
                                <tr>
                                    <th className="px-6 py-3">Antibiotic</th>
                                    <th className="px-6 py-3">Phenotype</th>
                                    <th className="px-6 py-3">MIC</th>
                                    <th className="px-6 py-3">Method</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {phenotype_evidence.evidence.map((row: any, i: number) => (
                                    <tr key={i} className="hover:bg-white/5 transition-colors">
                                        <td className="px-6 py-3 font-medium text-white">{row.antibiotic}</td>
                                        <td className="px-6 py-3">
                                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase
                                                ${row.phenotype === 'Resistant' ? 'bg-red-500/20 text-red-400' :
                                                    row.phenotype === 'Susceptible' ? 'bg-green-500/20 text-green-400' : 'bg-slate-500/20 text-slate-400'}
                                            `}>
                                                {row.phenotype}
                                            </span>
                                        </td>
                                        <td className="px-6 py-3 text-slate-300 font-mono text-xs">{row.mic}</td>
                                        <td className="px-6 py-3 text-slate-500">{row.method}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </GlassCard>
        </div>
    );
}
