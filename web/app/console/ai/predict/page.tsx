"use client";

import { MechanismPredictCard } from "@/components/MechanismPredictCard";
import { BrainCircuit } from "lucide-react";

export default function PredictPage() {
    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Mechanism Prediction</h2>
                    <p className="text-slate-400 text-sm">Sequence-to-Mechanism Classifier (ProtBERT)</p>
                </div>
            </div>

            <div className="max-w-3xl mx-auto">
                <MechanismPredictCard />
            </div>
        </div>
    );
}
