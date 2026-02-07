import React from 'react';

type RiskLevel = 'HIGH' | 'MODERATE' | 'LOW' | 'UNKNOWN';

interface Props {
    level: string;
}

export function RiskBadge({ level }: Props) {
    const normalized = (level?.toUpperCase() || 'UNKNOWN') as RiskLevel;

    const styles = {
        HIGH: "bg-red-100 text-red-800 border-red-200",
        MODERATE: "bg-amber-100 text-amber-800 border-amber-200",
        LOW: "bg-green-100 text-green-800 border-green-200",
        UNKNOWN: "bg-slate-100 text-slate-800 border-slate-200"
    };

    return (
        <span className={`px-3 py-1 rounded-full text-sm font-bold border ${styles[normalized]}`}>
            {normalized} RISK
        </span>
    );
}
