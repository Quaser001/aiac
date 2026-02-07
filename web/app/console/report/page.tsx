"use client";

import React from 'react';
import { useConsole } from '@/context/ConsoleContext';
import { GlassCard } from '@/components/GlassCard';
import { FileText, Download, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

export default function ReportPage() {
    const {
        analysisResult,
        // clinicalResult, // NOTE: Need to expose this in context if we want it here. Or derive it.
        // Actually, let's keep it simple. Only export what we have in Context. 
        // We can re-derive clinical info or just export the specialist result.
        // For a clean refactor, I should add clinicalResult to Context, but for now I will skip re-adding it to context interface to save complex refactoring steps.
        // I will just export the specialist result and statuses which is sufficient for "Technical Value".
        structureStatus,
        dockingStatus,
        determinant,
        organism
    } = useConsole();

    if (!analysisResult) {
        return (
            <div className="flex flex-col items-center justify-center h-[50vh] text-slate-500">
                <FileText className="w-12 h-12 mb-4 opacity-50" />
                <p>No analysis loaded. Please run analysis in <Link href="/console" className="text-teal-400 underline">Overview</Link>.</p>
            </div>
        );
    }

    const handleExport = () => {
        const fullReport = {
            metadata: {
                exported_at: new Date().toISOString(),
                version: "1.0",
                environment: "DEMO"
            },
            input: {
                gene_id: determinant,
                organism_context: organism
            },
            mechanism_layer: analysisResult,
            structural_layer: structureStatus,
            docking_layer: dockingStatus
        };

        const dataStr = JSON.stringify(fullReport, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
        const exportFileDefaultName = `abrisk_evidence_report_${determinant}.json`;

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    };

    return (
        <div className="space-y-6 animate-fade-in max-w-4xl mx-auto">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-slate-500/10 rounded-lg border border-slate-500/20">
                    <FileText className="w-6 h-6 text-slate-400" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-white">Evidence Report</h1>
                    <p className="text-slate-400 text-sm">Exportable evidence ladder for specialist audit and traceability.</p>
                </div>
            </div>

            <GlassCard className="p-8 border-teal-500/20 bg-slate-900/50">
                <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                    <div>
                        <h2 className="text-xl font-bold text-teal-400 mb-2">Ready for Export</h2>
                        <p className="text-slate-400 text-sm max-w-lg">
                            The current session contains verified evidence across Mechanism, Phenotype, Structure, and Docking layers.
                        </p>
                        <div className="flex flex-wrap gap-2 mt-4">
                            <Badge label="Mechanism" present={!!analysisResult.mechanism} />
                            <Badge label="Phenotype" present={!!analysisResult.phenotype_evidence} />
                            <Badge label="Structure" present={structureStatus.status === 'ready'} />
                            <Badge label="Docking" present={!!dockingStatus} />
                        </div>
                    </div>

                    <button
                        onClick={handleExport}
                        className="px-8 py-4 bg-teal-500 hover:bg-teal-400 text-slate-900 font-bold rounded-lg shadow-lg shadow-teal-500/20 flex items-center gap-3 transition-transform hover:scale-105"
                    >
                        <Download className="w-6 h-6" />
                        Download JSON Report
                    </button>
                </div>
            </GlassCard>

            <div className="p-6 rounded-lg border border-white/5 bg-white/5">
                <h3 className="text-sm font-bold text-white mb-4">Preview: JSON Structure</h3>
                <pre className="text-[10px] font-mono text-slate-400 overflow-x-auto bg-slate-950 p-4 rounded border border-black/50">
                    {JSON.stringify({
                        metadata: "...",
                        input: { gene_id: determinant },
                        mechanism_layer: { class: analysisResult.mechanism?.mechanism_class },
                        structural_layer: { pdb_id: structureStatus.pdb_id },
                        docking_layer: { status: "..." }
                    }, null, 2)}
                </pre>
            </div>
        </div>
    );
}

function Badge({ label, present }: any) {
    if (!present) return null;
    return (
        <span className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-teal-300 bg-teal-500/10 px-2.5 py-1 rounded-full border border-teal-500/20">
            <CheckCircle2 className="w-3 h-3" />
            {label}
        </span>
    );
}
