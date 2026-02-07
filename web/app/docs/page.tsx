"use client";

import { Section, GlassCard } from '@/components/GlassCard';
import { ArrowRight, Check } from 'lucide-react';
import Link from 'next/link';

export default function DocsPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            <Section className="max-w-4xl">
                <h1 className="heading-hero mb-8">
                    Verified <span className="text-teal-400">Golden Path</span>
                </h1>

                <p className="text-body text-lg mb-12">
                    Follow this standard operating procedure to verify the ABRISK intelligence engine.
                    This demo focuses on the high-risk carbapenemase <strong>NDM-1</strong>.
                </p>

                <div className="space-y-4">
                    <GlassCard className="flex gap-4 items-start">
                        <div className="w-8 h-8 rounded-full bg-teal-500/10 flex items-center justify-center shrink-0 border border-teal-500/20 text-teal-400 font-bold">1</div>
                        <div>
                            <h3 className="heading-md mb-1">Launch Application</h3>
                            <p className="text-body text-sm mb-2">Navigate to the Analysis Console.</p>
                            <Link href="/app" className="text-teal-400 text-sm hover:underline flex items-center gap-1">Open Console <ArrowRight className="w-3 h-3" /></Link>
                        </div>
                    </GlassCard>

                    <GlassCard className="flex gap-4 items-start">
                        <div className="w-8 h-8 rounded-full bg-teal-500/10 flex items-center justify-center shrink-0 border border-teal-500/20 text-teal-400 font-bold">2</div>
                        <div>
                            <h3 className="heading-md mb-1">Select Determinant</h3>
                            <p className="text-body text-sm">
                                In the gene search box, type or select <strong>NDM-1</strong>.
                            </p>
                        </div>
                    </GlassCard>

                    <GlassCard className="flex gap-4 items-start">
                        <div className="w-8 h-8 rounded-full bg-teal-500/10 flex items-center justify-center shrink-0 border border-teal-500/20 text-teal-400 font-bold">3</div>
                        <div>
                            <h3 className="heading-md mb-1">Add Phenotype Context (Optional)</h3>
                            <p className="text-body text-sm">
                                Select <strong>Klebsiella pneumoniae</strong> from the organism dropdown to view
                                real-world surveillance data (MIC distributions).
                            </p>
                        </div>
                    </GlassCard>

                    <GlassCard className="flex gap-4 items-start">
                        <div className="w-8 h-8 rounded-full bg-teal-500/10 flex items-center justify-center shrink-0 border border-teal-500/20 text-teal-400 font-bold">4</div>
                        <div>
                            <h3 className="heading-md mb-1">Analyze & Verify</h3>
                            <p className="text-body text-sm mb-3">
                                Click &quot;Analyze&quot;. Verify the following outputs:
                            </p>
                            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm text-slate-400">
                                <li className="flex gap-2"><Check className="w-4 h-4 text-green-500" /> Mechanism: Metallo-beta-lactamase</li>
                                <li className="flex gap-2"><Check className="w-4 h-4 text-green-500" /> Risk Tier: 1 (High)</li>
                                <li className="flex gap-2"><Check className="w-4 h-4 text-green-500" /> Drugs: Carbapenems, Cephalosporins</li>
                                <li className="flex gap-2"><Check className="w-4 h-4 text-green-500" /> Phenotype: Resistant (&gt;32 mg/L)</li>
                            </ul>
                        </div>
                    </GlassCard>
                </div>

            </Section>
        </div>
    );
}
