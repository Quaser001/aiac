"use client";

import { useConsole } from "@/context/ConsoleContext";
import { MutationImpactCard } from "@/components/MutationImpactCard";
import { Activity, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function MutationImpactPage() {
    const { determinant } = useConsole();

    if (!determinant) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-slate-500">
                <Activity className="w-12 h-12 mb-4 opacity-20" />
                <p>Select a resistance determinant in Overview to analyze mutations.</p>
                <Link href="/console/overview" className="mt-4 text-purple-400 hover:text-purple-300 flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Return to Overview
                </Link>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Mutation Internal Impact</h2>
                    <p className="text-slate-400 text-sm">ESM-2 Structural Stability Prediction</p>
                </div>
                {determinant && (
                    <div className="px-3 py-1 bg-purple-500/10 border border-purple-500/20 rounded text-purple-400 text-xs font-mono">
                        Variant: {determinant}
                    </div>
                )}
            </div>

            <div className="max-w-3xl mx-auto">
                <MutationImpactCard determinant={determinant} />
            </div>
        </div>
    );
}
