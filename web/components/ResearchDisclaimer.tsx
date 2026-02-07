import React from 'react';
import { Beaker } from 'lucide-react';

export function ResearchDisclaimer() {
    return (
        <div className="bg-slate-900 border border-slate-700 rounded-md p-4 mb-6 text-slate-300 text-sm flex gap-4 items-start">
            <Beaker className="w-5 h-5 text-purple-400 mt-1 flex-shrink-0" />
            <div>
                <h4 className="font-bold text-purple-400 mb-1">SPECIALIST INTELLIGENCE LAYER (2A/2B)</h4>
                <p>
                    Outputs here are <strong>in silico hypotheses</strong> for research prioritization only.
                    <br />
                    • DO NOT use for clinical decision making.
                    <br />
                    • Validation required (Wet Lab / Molecular Dynamics).
                </p>
            </div>
        </div>
    );
}
