import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, HelpCircle } from 'lucide-react';
import { RiskBadge } from './RiskBadge';

interface Props {
    riskLevel: string;
    geneDetails?: Array<{
        gene: string;
        family?: string;
        mechanism_explanation?: string;
    }>;
}

export function RiskCard({ riskLevel, geneDetails }: Props) {
    const isHigh = riskLevel === 'HIGH';
    const isMod = riskLevel === 'MODERATE';

    return (
        <div className={`border rounded-lg p-6 shadow-sm ${isHigh ? 'bg-red-50 border-red-200' :
                isMod ? 'bg-amber-50 border-amber-200' :
                    'bg-green-50 border-green-200'
            }`}>
            <div className="flex items-start justify-between mb-6">
                <div className="flex gap-4">
                    {isHigh ? <ShieldAlert className="w-12 h-12 text-red-600" /> :
                        isMod ? <AlertTriangle className="w-12 h-12 text-amber-600" /> :
                            <CheckCircle className="w-12 h-12 text-green-600" />}

                    <div>
                        <h2 className="text-lg font-bold text-slate-800">Risk Stratification</h2>
                        <div className="mt-1">
                            <RiskBadge level={riskLevel} />
                        </div>
                    </div>
                </div>
            </div>

            <div className="space-y-4">
                <h3 className="text-sm font-semibold text-slate-700 uppercase tracking-wider">Detected Mechanisms</h3>

                {geneDetails && geneDetails.length > 0 ? (
                    <div className="space-y-3">
                        {geneDetails.map((g, idx) => (
                            <div key={idx} className="bg-white/60 p-3 rounded border border-black/5">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="font-mono font-bold text-slate-900">{g.gene}</span>
                                    <span className="text-xs text-slate-500 font-mono">{g.family}</span>
                                </div>
                                <p className="text-sm text-slate-700">{g.mechanism_explanation}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-sm text-slate-500 italic">No significant resistance markers detected in this tier.</p>
                )}
            </div>

            <div className="mt-6 pt-4 border-t border-black/10 flex gap-2 items-center text-xs text-slate-500">
                <HelpCircle className="w-4 h-4" />
                <span>Based on sequence identity ({'>'}95%) and structural active-site conservation.</span>
            </div>
        </div>
    );
}
