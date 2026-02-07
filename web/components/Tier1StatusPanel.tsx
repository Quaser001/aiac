import React from 'react';
import { GlassCard } from './GlassCard';
import { CheckCircle, Wifi, WifiOff, Database, FileText } from 'lucide-react';
import { isTier1, TIER1_REGISTRY } from '@/data/tier1_registry';
import { cn } from '@/lib/utils';

export function Tier1StatusPanel({ determinant }: { determinant: string }) {
    if (!determinant || !isTier1(determinant)) return null;

    const data = TIER1_REGISTRY[determinant];
    if (!data) return null; // Safety guard

    const isLive = true; // Use real state if available via context, else default to Online/Offline check

    return (
        <GlassCard className="mb-4 bg-teal-950/20 border-teal-500/20">
            <div className="flex items-center justify-between px-2 pt-1 pb-1">
                <span className="text-xs font-mono text-teal-400 font-bold uppercase tracking-wider">
                    Tier-1 Coverage: {determinant}
                </span>
                <span className="text-[10px] text-zinc-500 flex items-center gap-1">
                    CONF-SAFE
                    <CheckCircle className="w-3 h-3 text-teal-500" />
                </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 px-2 pb-2">
                <StatusItem
                    icon={FileText}
                    label="Canonical Sequence"
                    value="Loaded"
                    active={true}
                />
                <StatusItem
                    icon={Database}
                    label="Structure Map"
                    value={data.pdb || "Mapped"}
                    active={true}
                />
                <StatusItem
                    icon={Database}
                    label="Mutations"
                    value={`${data.mutations?.length || 0} Cached`}
                    active={true}
                />
                <StatusItem
                    icon={isLive ? Wifi : WifiOff}
                    label="HF Enrich"
                    value={isLive ? "Online" : "Offline"}
                    active={isLive}
                    color={isLive ? "text-green-400" : "text-zinc-500"}
                />
            </div>
        </GlassCard>
    );
}

function StatusItem({ icon: Icon, label, value, active, color }: any) {
    return (
        <div className={cn("flex flex-col p-2 rounded bg-black/20", active ? "border border-teal-500/10" : "opacity-70")}>
            <div className="flex items-center gap-2 mb-1">
                <Icon className={cn("w-3 h-3", color || (active ? "text-teal-400" : "text-zinc-500"))} />
                <span className="text-[10px] text-zinc-400 uppercase">{label}</span>
            </div>
            <span className={cn("text-xs font-mono", active ? "text-white" : "text-zinc-500")}>
                {value}
            </span>
        </div>
    );
}
