"use client";

import { Section, GlassCard } from '@/components/GlassCard';
import { ArrowDown } from 'lucide-react';

export default function HowItWorksPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            <Section className="text-center">
                <h1 className="heading-hero mb-6">
                    Traceable <span className="text-teal-400">Logic Flow</span>
                </h1>
                <p className="text-body max-w-2xl mx-auto text-lg mb-12">
                    No black boxes. ABRISK follows a deterministic, evidence-based path
                    from raw sequence data to clinical insight.
                </p>
            </Section>

            <Section>
                <div className="max-w-3xl mx-auto space-y-8 relative">
                    {/* Connecting Line */}
                    <div className="absolute left-[28px] top-8 bottom-8 w-px bg-white/10" />

                    {/* Step 1 */}
                    <div className="relative flex gap-8 items-start">
                        <div className="w-14 h-14 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center shrink-0 z-10">
                            <span className="text-xl font-bold text-white">1</span>
                        </div>
                        <GlassCard className="flex-1">
                            <h3 className="heading-md mb-2 text-teal-400">Deterministic Mapping</h3>
                            <p className="text-body text-sm mb-4">
                                The system receives a gene symbol (e.g., &quot;NDM-1&quot;) or sequence.
                                It queries the Comprehensive Antibiotic Resistance Database (CARD)
                                using strict homology cutoffs.
                            </p>
                            <div className="px-3 py-2 bg-slate-950 rounded border border-white/5 font-mono text-xs text-slate-400">
                                Query: SELECT * FROM resistance_genes WHERE symbol = &apos;NDM-1&apos;
                            </div>
                        </GlassCard>
                    </div>

                    {/* Step 2 */}
                    <div className="relative flex gap-8 items-start">
                        <div className="w-14 h-14 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center shrink-0 z-10">
                            <span className="text-xl font-bold text-white">2</span>
                        </div>
                        <GlassCard className="flex-1">
                            <h3 className="heading-md mb-2 text-specialist-light">Mechanism Resolution</h3>
                            <p className="text-body text-sm mb-4">
                                The gene is linked to its biological mechanism (e.g., &quot;beta-lactamase&quot;).
                                The system retrieves structural properties, catalytic types, and
                                known substrate profiles.
                            </p>
                        </GlassCard>
                    </div>

                    {/* Step 3 */}
                    <div className="relative flex gap-8 items-start">
                        <div className="w-14 h-14 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center shrink-0 z-10">
                            <span className="text-xl font-bold text-white">3</span>
                        </div>
                        <GlassCard className="flex-1">
                            <h3 className="heading-md mb-2 text-clinical-light">Risk Stratification</h3>
                            <p className="text-body text-sm mb-4">
                                Based on the mechanism, drug classes are flagged as compromised.
                                A risk score (1-3) is assigned based on the severity of the resistance
                                (e.g., carbapenemases = Tier 1).
                            </p>
                        </GlassCard>
                    </div>

                    {/* Step 4 */}
                    <div className="relative flex gap-8 items-start">
                        <div className="w-14 h-14 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center shrink-0 z-10 opacity-50">
                            <span className="text-xl font-bold text-white">4</span>
                        </div>
                        <GlassCard className="flex-1 border-dashed opacity-75">
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="heading-md text-slate-400">Simulation (Future)</h3>
                                <span className="text-xs uppercase tracking-widest text-slate-500">Preview</span>
                            </div>
                            <p className="text-body text-sm">
                                Future modules will run AlphaFold3 binding simulations to determine
                                if novel mutations affect drug binding affinity.
                            </p>
                        </GlassCard>
                    </div>

                </div>
            </Section>
        </div>
    );
}
