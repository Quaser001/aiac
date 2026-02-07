import React from 'react';
import { GlassCard } from './GlassCard';
import { Check, Lock, ArrowDown, Database, Activity, Calculator, Box, Cpu } from 'lucide-react';
import { EVIDENCE_LAYERS } from '../config/evidence_layers';

interface EvidenceLadderProps {
    activeLayers: number[]; // Array of layer IDs that are currently active
}

export function EvidenceLadder({ activeLayers }: EvidenceLadderProps) {
    return (
        <GlassCard className="border-teal-500/20 bg-teal-500/5">
            <div className="flex items-center gap-3 mb-6 border-b border-teal-500/10 pb-4">
                <div className="p-2 rounded-lg bg-teal-500/10 border border-teal-500/20">
                    <Activity className="w-5 h-5 text-teal-400" />
                </div>
                <div>
                    <h3 className="heading-md text-white mb-0.5">Evidence Escalation Ladder</h3>
                    <p className="text-body text-xs">
                        Multi-modal analysis pipeline status.
                    </p>
                </div>
            </div>

            <div className="relative">
                {/* Vertical Line */}
                <div className="absolute left-6 top-4 bottom-4 w-0.5 bg-white/10" />

                <div className="space-y-6">
                    {EVIDENCE_LAYERS.map((layer, index) => {
                        const isActive = activeLayers.includes(layer.id);
                        const isNext = !isActive && activeLayers.includes(layer.id - 1);

                        // Icon selection
                        let Icon = Database;
                        if (layer.id === 1) Icon = Activity;
                        if (layer.id === 2) Icon = Calculator;
                        if (layer.id === 3) Icon = Box;
                        if (layer.id >= 4) Icon = Cpu;

                        return (
                            <div key={layer.id} className="relative pl-14 group">
                                {/* Connector Dot */}
                                <div className={`absolute left-3 top-1 w-6 h-6 rounded-full border flex items-center justify-center z-10 transition-all ${isActive
                                    ? 'bg-green-500 border-green-400 shadow-[0_0_10px_rgba(34,197,94,0.3)]'
                                    : 'bg-slate-900 border-slate-700 text-slate-500'
                                    }`}>
                                    {isActive ? (
                                        <Check className="w-3.5 h-3.5 text-white" />
                                    ) : (
                                        <Lock className="w-3 h-3" />
                                    )}
                                </div>

                                {/* Content */}
                                <div className={`transition-all ${isActive ? 'opacity-100' : 'opacity-50'}`}>
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className={`text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded ${isActive
                                            ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                                            : 'bg-white/5 text-slate-400 border border-white/5'
                                            }`}>
                                            {layer.status === 'ACTIVE_SUBSET' ? 'ACTIVE' : layer.status}
                                        </span>
                                        <span className="text-xs text-slate-500 font-mono">
                                            {layer.source}
                                        </span>
                                    </div>

                                    <h4 className={`text-sm font-semibold mb-1 ${isActive ? 'text-white' : 'text-slate-400'}`}>
                                        {layer.name}
                                    </h4>

                                    <p className="text-[10px] text-slate-400 leading-relaxed max-w-sm">
                                        {layer.description}
                                    </p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="mt-6 pt-4 border-t border-teal-500/10 flex gap-2 text-[10px] text-teal-300/50 italic">
                <ArrowDown className="w-3 h-3" />
                Higher layers require exponential compute resources.
            </div>
        </GlassCard>
    );
}
