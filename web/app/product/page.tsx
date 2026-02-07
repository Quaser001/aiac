"use client";

import { Section, GlassCard, FeatureCard } from '@/components/GlassCard';
import { Activity, Shield, Database, Check, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function ProductPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            {/* Header */}
            <Section className="text-center">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-medium mb-6">
                    <span>The Platform</span>
                </div>
                <h1 className="heading-hero mb-6">
                    Multi-Layered <br /><span className="text-teal-400">Decision Intelligence</span>
                </h1>
                <p className="text-body max-w-2xl mx-auto text-lg">
                    ABRISK integrates genomic detection with structural modeling and phenotypic evidence.
                    One platform, three levels of verifiable truth.
                </p>
            </Section>

            {/* Layer 1: Clinical */}
            <Section>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                    <div>
                        <div className="p-2 w-fit rounded-lg bg-clinical/10 border border-clinical/20 mb-4">
                            <Activity className="w-6 h-6 text-clinical-light" />
                        </div>
                        <h2 className="heading-xl mb-4">Layer 1: Clinical Risk</h2>
                        <p className="text-body mb-6">
                            Instant stratification of resistance markers into actionable risk tiers.
                            We map detected genes to compromised drug classes using CARD&apos;s curated ontology.
                        </p>
                        <ul className="space-y-3 mb-8">
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-clinical shrink-0" />
                                <span>Binary Risk Tiers (High / Moderate)</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-clinical shrink-0" />
                                <span>Impacted Availability Reports</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-clinical shrink-0" />
                                <span>Rapid Triage Logic</span>
                            </li>
                        </ul>
                    </div>
                    <GlassCard className="border-clinical/20 bg-clinical/5 relative overflow-hidden h-[300px] flex items-center justify-center">
                        <div className="text-center">
                            <div className="text-4xl font-bold text-clinical mb-2">Tier 1</div>
                            <div className="text-sm text-clinical-light uppercase tracking-widest">High Risk Confirmed</div>
                        </div>
                    </GlassCard>
                </div>
            </Section>

            {/* Layer 2: Specialist */}
            <Section>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center md:flex-row-reverse">
                    <div className="order-2 md:order-1">
                        <GlassCard className="border-specialist/20 bg-specialist/5 relative overflow-hidden h-[300px] flex items-center justify-center">
                            <div className="text-center">
                                <div className="text-4xl font-bold text-specialist mb-2">NDM-1</div>
                                <div className="text-sm text-specialist-light uppercase tracking-widest">Metallo-beta-lactamase</div>
                            </div>
                        </GlassCard>
                    </div>
                    <div className="order-1 md:order-2">
                        <div className="p-2 w-fit rounded-lg bg-specialist/10 border border-specialist/20 mb-4">
                            <Shield className="w-6 h-6 text-specialist-light" />
                        </div>
                        <h2 className="heading-xl mb-4">Layer 2: Mechanism Engine</h2>
                        <p className="text-body mb-6">
                            Deep structural insight for researchers. Understand <em>why</em> resistance occurs
                            based on catalytic type and enzyme kinetics.
                        </p>
                        <ul className="space-y-3 mb-8">
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-specialist shrink-0" />
                                <span>Enzyme Classification (e.g., MBL)</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-specialist shrink-0" />
                                <span>Structural Impact Analysis</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-specialist shrink-0" />
                                <span>Full CARD Provenance</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </Section>

            {/* Layer 3: Phenotype */}
            <Section>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                    <div>
                        <div className="p-2 w-fit rounded-lg bg-teal-500/10 border border-teal-500/20 mb-4">
                            <Database className="w-6 h-6 text-teal-400" />
                        </div>
                        <h2 className="heading-xl mb-4">Layer 3: Phenotype Evidence</h2>
                        <p className="text-body mb-6">
                            Bridge the gap between genotype and phenotype. Overlay your analysis with
                            real-world MIC observations from verified surveillance data.
                        </p>
                        <ul className="space-y-3 mb-8">
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-teal-400 shrink-0" />
                                <span>Organism-Specific Context</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-teal-400 shrink-0" />
                                <span>Minimum Inhibitory Concentrations (MIC)</span>
                            </li>
                            <li className="flex items-start gap-3 text-slate-300 text-sm">
                                <Check className="w-5 h-5 text-teal-400 shrink-0" />
                                <span>Testing Standards (EUCAST / CLSI)</span>
                            </li>
                        </ul>
                    </div>
                    <GlassCard className="border-teal-500/20 bg-teal-500/5 relative overflow-hidden h-[300px] flex items-center justify-center">
                        <div className="space-y-4 text-center">
                            <div className="px-4 py-2 bg-slate-900 rounded border border-white/10 text-xs font-mono text-teal-400">
                                MIC: &gt;32 mg/L (Resistant)
                            </div>
                            <div className="px-4 py-2 bg-slate-900 rounded border border-white/10 text-xs font-mono text-teal-400">
                                Method: Broth Microdilution
                            </div>
                        </div>
                    </GlassCard>
                </div>
            </Section>

            <Section className="text-center">
                <Link href="/app" className="btn-primary inline-flex gap-2">
                    Start Analysis <ArrowRight className="w-4 h-4" />
                </Link>
            </Section>
        </div>
    );
}
