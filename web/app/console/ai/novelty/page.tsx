"use client";

import { useConsole } from "@/context/ConsoleContext";
import { NoveltyScoreCard } from "@/components/NoveltyScoreCard";
import { Scan, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function NoveltyPage() {
    const { determinant } = useConsole();

    if (!determinant) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-slate-500">
                <Scan className="w-12 h-12 mb-4 opacity-20" />
                <p>Select a resistance determinant in Overview to scan for novelty.</p>
                <Link href="/console/overview" className="mt-4 text-cyan-400 hover:text-cyan-300 flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Return to Overview
                </Link>
            </div>
        );
    }
    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Novelty Detection</h2>
                    <p className="text-slate-400 text-sm">Out-of-Distribution Scoring (AE + GMM)</p>
                </div>
            </div>

            <div className="max-w-3xl mx-auto">
                <NoveltyScoreCard determinant={determinant} />
            </div>
        </div>
    );
}
