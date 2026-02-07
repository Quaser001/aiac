import { GlassCard } from '@/components/GlassCard';
import { Database, Shield, ChevronDown, ChevronUp, Link as LinkIcon, Microscope, Info } from 'lucide-react';
import { useState } from 'react';

// Reuse types from page.tsx (or ideally move to shared types file)
interface PhenotypeRecord {
    antibiotic: string;
    phenotype: string;
    mic: string;
    method: string;
    standard: string;
    isolate: string;
}

interface SpecialistResult {
    gene_id: string;
    mechanism: {
        gene_id: string;
        mechanism_class: string;
        structural_impact: string;
        catalytic_type: string;
        full_name?: string;
    };
    constraints: Array<{ type: string; description: string }>;
    disclaimer: string;
    phenotype_evidence?: {
        organism_name: string;
        source: string;
        evidence: PhenotypeRecord[];
    };
}

interface ProvenanceDrawerProps {
    data: SpecialistResult;
}

export function ProvenanceDrawer({ data }: ProvenanceDrawerProps) {
    const [isOpen, setIsOpen] = useState(false);

    if (!data) return null;

    return (
        <div className="mt-8 border-t border-white/10 pt-4 animate-fade-in">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center justify-between w-full px-4 py-3 bg-white/[0.02] hover:bg-white/5 border border-white/5 rounded-lg transition-all group"
            >
                <div className="flex items-center gap-3">
                    <Database className="w-4 h-4 text-slate-400 group-hover:text-teal-400 transition-colors" />
                    <span className="text-sm font-medium text-slate-300 group-hover:text-white uppercase tracking-wider">
                        Provenance & Evidence Details
                    </span>
                </div>
                {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-500" />
                ) : (
                    <ChevronDown className="w-4 h-4 text-slate-500" />
                )}
            </button>

            {isOpen && (
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6 animate-slide-down">
                    {/* LEFT: CARD Mechanism Details */}
                    <GlassCard className="bg-slate-900/40">
                        <div className="flex items-center gap-2 mb-4 border-b border-white/10 pb-2">
                            <Shield className="w-4 h-4 text-teal-500" />
                            <h4 className="text-xs font-bold text-teal-500 uppercase tracking-widest">
                                Mechanism Authority (CARD)
                            </h4>
                        </div>

                        <div className="space-y-4 font-mono text-xs">
                            <div>
                                <p className="text-slate-500 mb-1">Gene Name</p>
                                <p className="text-white text-sm font-semibold">{data.mechanism.full_name || data.gene_id}</p>
                            </div>
                            <div>
                                <p className="text-slate-500 mb-1">Classification</p>
                                <div className="flex flex-wrap gap-2">
                                    <span className="px-2 py-1 bg-white/5 rounded border border-white/10 text-slate-300">
                                        {data.mechanism.mechanism_class}
                                    </span>
                                    <span className="px-2 py-1 bg-white/5 rounded border border-white/10 text-slate-300">
                                        {data.mechanism.catalytic_type}
                                    </span>
                                </div>
                            </div>
                            <div>
                                <p className="text-slate-500 mb-1">Ontology Source</p>
                                <p className="text-slate-300 flex items-center gap-2">
                                    <LinkIcon className="w-3 h-3" />
                                    CARD v3.2.9 (Comprehensive Antibiotic Resistance Database)
                                </p>
                            </div>
                        </div>
                    </GlassCard>

                    {/* RIGHT: Phenotype / Surveillance Metadata */}
                    <GlassCard className="bg-slate-900/40">
                        <div className="flex items-center gap-2 mb-4 border-b border-white/10 pb-2">
                            <Microscope className="w-4 h-4 text-blue-400" />
                            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest">
                                Surveillance Metadata
                            </h4>
                        </div>

                        {data.phenotype_evidence ? (
                            <div className="space-y-4 font-mono text-xs">
                                <div>
                                    <p className="text-slate-500 mb-1">Observation Context</p>
                                    <p className="text-white text-sm">{data.phenotype_evidence.organism_name}</p>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-slate-500 mb-1">Source Dataset</p>
                                        <p className="text-blue-200">{data.phenotype_evidence.source}</p>
                                    </div>
                                    <div>
                                        <p className="text-slate-500 mb-1">Record Count</p>
                                        <p className="text-blue-200">{data.phenotype_evidence.evidence.length} Isolates</p>
                                    </div>
                                </div>
                                <div className="p-2 bg-blue-500/10 border border-blue-500/10 rounded">
                                    <div className="flex gap-2 items-start">
                                        <Info className="w-3 h-3 text-blue-400 shrink-0 mt-0.5" />
                                        <p className="text-blue-300/80 leading-relaxed text-[10px]">
                                            Testing Standards: EUCAST / CLSI.<br />
                                            Methods: Broth microdilution, Vitek 2.<br />
                                            Evidence represents specific isolate observations, not population-wide prevalence.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-center p-4">
                                <p className="text-slate-500 italic">
                                    No organism-specific phenotype evidence selected.
                                </p>
                                <p className="text-[10px] text-slate-600 mt-2">
                                    Select an organism context to view MIC observations.
                                </p>
                            </div>
                        )}
                    </GlassCard>
                </div>
            )}
        </div>
    );
}
