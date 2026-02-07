"use client";

import { Section, GlassCard } from '@/components/GlassCard';

export default function AboutPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            <Section className="max-w-4xl">
                <h1 className="heading-hero mb-8">
                    Mission: <br /><span className="text-teal-400">Decodable Biology</span>
                </h1>

                <div className="space-y-12">
                    <div>
                        <h2 className="heading-xl mb-4">Why ABRISK?</h2>
                        <p className="text-body text-lg">
                            Antimicrobial resistance (AMR) is the silent pandemic. As pathogens evolve faster than we ensure new drugs,
                            we rely heavily on rapid diagnostics. However, detecting a gene is not enough—we need to understand
                            what that gene <em>does</em> to the drug. ABRISK bridges the gap between raw sequence data and
                            clinical pharmacology.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <GlassCard>
                            <h3 className="heading-md mb-2">Mechanism Over Black Boxes</h3>
                            <p className="text-body text-sm">
                                We reject opaque AI models for clinical decisions. Every prediction in ABRISK
                                is grounded in a verifiable biological mechanism sourced from the CARD oncology.
                                If we say &quot;Resistant&quot;, we tell you exactly which enzyme causes it.
                            </p>
                        </GlassCard>
                        <GlassCard>
                            <h3 className="heading-md mb-2">Open Trust</h3>
                            <p className="text-body text-sm">
                                Our data provenance is open. We link directly to isolate records and
                                peer-reviewed mechanism definitions. Trust is built on traceability.
                            </p>
                        </GlassCard>
                    </div>
                </div>
            </Section>
        </div>
    );
}
