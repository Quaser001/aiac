"use client";

import { Section, FeatureCard } from '@/components/GlassCard';
import { Microscope, Stethoscope, Building2 } from 'lucide-react';

export default function UseCasesPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            <Section className="text-center">
                <h1 className="heading-hero mb-6">
                    Built for <span className="text-teal-400">Specialists</span>
                </h1>
                <p className="text-body max-w-2xl mx-auto text-lg">
                    Tailored intelligence for the rapid response teams fighting antimicrobial resistance.
                    <br />
                    <span className="text-sm opacity-60 mt-2 block">(Not intended for consumer self-diagnosis)</span>
                </p>
            </Section>

            <Section>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <FeatureCard
                        variant="clinical"
                        icon={<Stethoscope className="w-6 h-6" />}
                        title="Infectious Disease Clinicians"
                        description="Bedside decision support. Quickly verify if a detected genotype implies resistance to last-line therapies like carbapenems."
                    />
                    <FeatureCard
                        variant="specialist"
                        icon={<Microscope className="w-6 h-6" />}
                        title="Microbiology Lab Directors"
                        description="Audit automated panels. Resolve discrepancies between phenotypic growth and genotypic detection with mechanism-first evidence."
                    />
                    <FeatureCard
                        variant="default"
                        icon={<Building2 className="w-6 h-6" />}
                        title="Stewardship Committees"
                        description="Ecosystem-level surveillance. Track the prevalence of high-risk mechanisms (e.g., NDM-1) across facilities to guide policy."
                    />
                </div>
            </Section>
        </div>
    );
}
