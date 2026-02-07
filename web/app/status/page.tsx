"use client";

import { GlassCard } from '@/components/GlassCard';
import { Activity, Database, Server, Check, AlertTriangle, CloudOff, Info, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import { Navigation } from '@/components/Navigation';

export default function StatusPage() {
    return (
        <div className="min-h-screen relative overflow-hidden bg-slate-950 font-sans selection:bg-teal-500/30">
            <Navigation />

            <div className="pt-32 pb-12 container-max">
                <div className="mb-12">
                    <h1 className="heading-lg mb-2">System Capability Status</h1>
                    <p className="text-body text-slate-400">Operational status of ABRISK intelligence engines.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                    {/* 1. MECHANISM ENGINE (Active) */}
                    <GlassCard className="border-l-4 border-l-teal-500 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-50">
                            <Activity className="w-16 h-16 text-teal-500/10 group-hover:text-teal-500/20 transition-all" />
                        </div>
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-2 rounded bg-teal-500/10 border border-teal-500/20">
                                <Activity className="w-6 h-6 text-teal-400" />
                            </div>
                            <div>
                                <h3 className="font-bold text-white text-lg">Mechanism Engine</h3>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
                                    <span className="text-xs font-mono text-teal-400 uppercase tracking-widest">Active</span>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Knowledge Base</span>
                                <span className="text-white font-mono">CARD v3.2.9</span>
                            </div>
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Logic Type</span>
                                <span className="text-white font-mono">Deterministic (BLAST/Homology)</span>
                            </div>
                            <div className="p-3 bg-teal-500/5 rounded border border-teal-500/10 text-xs text-teal-300 leading-relaxed">
                                <Check className="w-3 h-3 inline mr-2" />
                                Validated for clinical decision support (Layer 1).
                            </div>
                        </div>
                    </GlassCard>

                    {/* 2. PHENOTYPE ENGINE (Prototype) */}
                    <GlassCard className="border-l-4 border-l-amber-500 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-50">
                            <Database className="w-16 h-16 text-amber-500/10 group-hover:text-amber-500/20 transition-all" />
                        </div>
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-2 rounded bg-amber-500/10 border border-amber-500/20">
                                <Database className="w-6 h-6 text-amber-400" />
                            </div>
                            <div>
                                <h3 className="font-bold text-white text-lg">Phenotype Evidence</h3>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                                    <span className="text-xs font-mono text-amber-400 uppercase tracking-widest">Prototype (Seeded)</span>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Source</span>
                                <span className="text-white font-mono">BV-BRC / PATRIC</span>
                            </div>
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Coverage</span>
                                <span className="text-white font-mono">~20 High-Priority Isolates</span>
                            </div>
                            <div className="p-3 bg-amber-500/5 rounded border border-amber-500/10 text-xs text-amber-300 leading-relaxed">
                                <AlertTriangle className="w-3 h-3 inline mr-2" />
                                Observational only. Not for prevalence inference.
                            </div>
                        </div>
                    </GlassCard>

                    {/* 3. SIMULATION ENGINE (Future) */}
                    <GlassCard className="border-l-4 border-l-slate-700 relative overflow-hidden group opacity-75 grayscale hover:grayscale-0 transition-all">
                        <div className="absolute top-0 right-0 p-4 opacity-50">
                            <Server className="w-16 h-16 text-slate-500/10 group-hover:text-purple-500/20 transition-all" />
                        </div>
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-2 rounded bg-slate-800 border border-slate-700">
                                <CloudOff className="w-6 h-6 text-slate-400" />
                            </div>
                            <div>
                                <h3 className="font-bold text-white text-lg">In-Silico Simulation</h3>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="w-2 h-2 rounded-full bg-slate-700"></span>
                                    <span className="text-xs font-mono text-slate-500 uppercase tracking-widest">Offline (Future Scale)</span>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Engine</span>
                                <span className="text-white font-mono">ESM / AlphaFold3</span>
                            </div>
                            <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                                <span className="text-slate-400">Status</span>
                                <span className="text-white font-mono">Requires GPU Cluster</span>
                            </div>
                            <div className="p-3 bg-white/5 rounded border border-white/10 text-xs text-slate-400 leading-relaxed">
                                <Info className="w-3 h-3 inline mr-2" />
                                Use &quot;Feasibility&quot; endpoints for mock implementation.
                            </div>
                        </div>
                    </GlassCard>

                </div>

                <div className="mt-12 text-center">
                    <Link href="/app" className="btn-primary inline-flex gap-2">
                        Return to Console <ChevronRight className="w-4 h-4" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
