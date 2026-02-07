"use client";

import { useConsole } from "@/context/ConsoleContext";
import { DockingResearchCard } from "@/components/DockingResearchCard";
import { Microscope, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function DockingPage() {
    const { determinant, dockingStatus } = useConsole();

    return (
        <div className="space-y-6 animate-fade-in h-full">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Docking Simulation</h2>
                    <p className="text-slate-400 text-sm">In-Silico Binding Feasibility (Research Demo)</p>
                </div>
                {determinant && (
                    <div className="px-3 py-1 bg-teal-500/10 border border-teal-500/20 rounded text-teal-400 text-xs font-mono">
                        Target: {determinant}
                    </div>
                )}
            </div>

            <div className="h-[600px]">
                <DockingResearchCard />
            </div>
        </div>
    );
}
