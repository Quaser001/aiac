"use client";

import Link from 'next/link';
import { Shield, Database, Activity, ArrowRight, Lock, CheckCircle, Search, Microscope } from 'lucide-react';
import { Section, GlassCard } from '@/components/GlassCard';

export default function Home() {
  return (
    <div className="animate-fade-in divide-y divide-white/5">

      {/* 1. HERO SECTION */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-4 overflow-hidden">
        {/* Abstract Background Element */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-teal-500/10 blur-[120px] rounded-full opacity-50 pointer-events-none" />

        <div className="container-max relative z-10 text-center">
          {/* Trust Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-medium mb-8 animate-fade-in">
            <Shield className="w-3 h-3" />
            <span>CARD-Backed Decision Intelligence</span>
          </div>

          {/* Headline */}
          <h1 className="heading-hero mb-6 max-w-4xl mx-auto">
            Structure-Informed <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-teal-200">
              Antibiotic Risk Stratification
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-body text-lg md:text-xl max-w-2xl mx-auto mb-10">
            Mechanism-grounded intelligence for clinicians and researchers.
            Moving beyond black-box predictions to verifiable structural provenance.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/app" className="btn-primary flex items-center gap-2 min-w-[160px] justify-center text-base">
              Open Application
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/docs" className="btn-secondary flex items-center gap-2 min-w-[160px] justify-center text-base">
              Documentation
            </Link>
          </div>
        </div>
      </section>

      {/* 2. DATA CREDIBILITY STRIP */}
      <div className="border-y border-white/5 bg-white/[0.01]">
        <div className="container-max py-8">
          <div className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
            <div className="flex items-center gap-3">
              <Database className="w-5 h-5 text-slate-300" />
              <span className="font-mono text-sm tracking-wide">POWERED BY CARD v3.2</span>
            </div>
            <div className="hidden md:block w-px h-8 bg-white/10" />
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-slate-300" />
              <span className="font-mono text-sm tracking-wide">MECHANISM-FIRST REASONING</span>
            </div>
            <div className="hidden md:block w-px h-8 bg-white/10" />
            <div className="flex items-center gap-3">
              <Lock className="w-5 h-5 text-slate-300" />
              <span className="font-mono text-sm tracking-wide">NO PHI / LOCAL EXECUTION</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. HOW IT WORKS (Horizontal Flow) */}
      <Section>
        <div className="text-center mb-16">
          <h2 className="heading-lg mb-4">From Genotype to Risk Profile</h2>
          <p className="text-body max-w-xl mx-auto">
            ABRISK separates clinical decision support from specialist research tools,
            ensuring appropriate context for every user.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connecting Line (Desktop) */}
          <div className="hidden md:block absolute top-12 left-[20%] right-[20%] h-px bg-gradient-to-r from-teal-500/0 via-teal-500/20 to-teal-500/0" />

          {/* Step 1 */}
          <div className="relative text-center">
            <div className="w-24 h-24 mx-auto bg-slate-900 border border-white/10 rounded-2xl flex items-center justify-center mb-6 relative z-10 shadow-xl">
              <Search className="w-10 h-10 text-teal-400" />
            </div>
            <h3 className="heading-md mb-2">1. Detect</h3>
            <p className="text-body text-sm">
              Input resistance genes (e.g., NDM-1). System identifies exact variants.
            </p>
          </div>

          {/* Step 2 */}
          <div className="relative text-center">
            <div className="w-24 h-24 mx-auto bg-slate-900 border border-white/10 rounded-2xl flex items-center justify-center mb-6 relative z-10 shadow-xl">
              <Microscope className="w-10 h-10 text-specialist" />
            </div>
            <h3 className="heading-md mb-2">2. Analyze</h3>
            <p className="text-body text-sm">
              Map to CARD mechanisms. Verify structural constraints and enzyme kinetics.
            </p>
          </div>

          {/* Step 3 */}
          <div className="relative text-center">
            <div className="w-24 h-24 mx-auto bg-slate-900 border border-white/10 rounded-2xl flex items-center justify-center mb-6 relative z-10 shadow-xl">
              <Activity className="w-10 h-10 text-clinical-light" />
            </div>
            <h3 className="heading-md mb-2">3. Stratify</h3>
            <p className="text-body text-sm">
              Generate clinical risk tiers. Flag compromised drug classes with confidence scores.
            </p>
          </div>
        </div>
      </Section>

      {/* 4. EVIDENCE ESCALATION ARCHITECTURE */}
      <div className="border-y border-white/5 bg-slate-900/50 backdrop-blur-sm">
        <div className="container-max py-16">
          <div className="text-center mb-12">
            <h2 className="heading-lg mb-4">Evidence Escalation Architecture</h2>
            <p className="text-body max-w-2xl mx-auto">
              ABRISK escalates analysis from deterministic ground truth to advanced simulation only when necessary.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
            <div className="p-6 rounded-xl border border-white/5 bg-white/[0.02]">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-teal-500/10 rounded-lg text-teal-400">
                  <Database className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white">Curated Mechanisms</h3>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                Instant validation against the Comprehensive Antibiotic Resistance Database (CARD), the global gold standard for resistance ontology.
              </p>
            </div>

            <div className="p-6 rounded-xl border border-white/5 bg-white/[0.02]">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                  <Activity className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white">Lab Phenotype Evidence</h3>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                Real-world observational data (MIC values) from the BV-BRC database, providing concrete susceptibility baselines for specific organisms.
              </p>
            </div>

            <div className="p-6 rounded-xl border border-white/5 bg-white/[0.02]">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400">
                  <Lock className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white">Future Simulation</h3>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                Advanced modules including AlphaFold structural mapping and DiffDock binding simulations, ready to be activated with high-performance compute.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 5. BUILT FOR (Audience) */}
      <Section className="bg-white/[0.01]">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <GlassCard className="h-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-clinical/10 rounded-lg">
                <CheckCircle className="w-5 h-5 text-clinical-light" />
              </div>
              <h3 className="heading-md">Clinicians</h3>
            </div>
            <p className="text-body text-sm mb-6">
              Rapid decision support for antibiotic selection when resistance markers are confirmed.
            </p>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex gap-2">✔ Risk Tiers</li>
              <li className="flex gap-2">✔ Drug Class Impact</li>
            </ul>
          </GlassCard>

          <GlassCard className="h-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-specialist/10 rounded-lg">
                <CheckCircle className="w-5 h-5 text-specialist-light" />
              </div>
              <h3 className="heading-md">Researchers</h3>
            </div>
            <p className="text-body text-sm mb-6">
              Deep mechanism intelligence with full provenance tracking to the CARD database.
            </p>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex gap-2">✔ Mechanism Details</li>
              <li className="flex gap-2">✔ Structural Analysis</li>
            </ul>
          </GlassCard>

          <GlassCard className="h-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-teal-500/10 rounded-lg">
                <CheckCircle className="w-5 h-5 text-teal-400" />
              </div>
              <h3 className="heading-md">Public Health</h3>
            </div>
            <p className="text-body text-sm mb-6">
              Surveillance insights grounded in structural biology rather than opaque machine learning.
            </p>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex gap-2">✔ Population Risk</li>
              <li className="flex gap-2">✔ Traceable Data</li>
            </ul>
          </GlassCard>
        </div>
      </Section>

      {/* 5. SAFETY & DISCLAIMER (Restrained) */}
      <Section className="text-center">
        <div className="max-w-2xl mx-auto">
          <h3 className="heading-md text-slate-300 mb-4">Clinical Restraint</h3>
          <p className="text-caption leading-relaxed">
            ABRISK is a decision support system, not a diagnostic device.
            All outputs represent genotype-based risk signals and must be validated
            with phenotypic testing and professional clinical judgment.
          </p>
        </div>
      </Section>

    </div>
  );
}
