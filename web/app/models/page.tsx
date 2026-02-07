import { GlassCard, Section } from '@/components/GlassCard';
import { Activity, Database, Cpu } from 'lucide-react';
import { EVIDENCE_LAYERS } from '../../config/evidence_layers';

export default function ModelsPage() {
    return (
        <div className="animate-fade-in pt-24 pb-12">
            <Section>
                <div className="mb-12">
                    <h1 className="heading-hero mb-4">
                        <span className="text-teal-400">Intelligence</span> Architecture
                    </h1>
                    <p className="text-body text-xl max-w-2xl">
                        The ABRISK engine operates on a strict evidence escalation ladder.
                        We prioritize deterministic ground truth before activating probabilistic simulation.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {EVIDENCE_LAYERS.map((layer) => {
                        const active = !layer.isFuture;
                        return (
                            <GlassCard key={layer.id} className={`flex flex-col h-full ${active ? 'border-teal-500/30' : 'opacity-70 grayscale'}`}>
                                <div className="flex justify-between items-start mb-4">
                                    <div className={`p-3 rounded-xl border ${active ? 'bg-teal-500/10 border-teal-500/20 text-teal-400' : 'bg-white/5 border-white/10 text-slate-500'}`}>
                                        {layer.id === 0 ? <Database /> : layer.id === 1 ? <Activity /> : <Cpu />}
                                    </div>
                                    <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wide border ${active
                                        ? 'bg-green-500/10 text-green-400 border-green-500/20'
                                        : 'bg-slate-800 text-slate-500 border-slate-700'
                                        }`}>
                                        {layer.status}
                                    </div>
                                </div>

                                <h3 className="text-lg font-bold text-white mb-2">{layer.name}</h3>
                                <p className="text-sm text-slate-400 mb-6 flex-grow">
                                    {layer.description}
                                </p>

                                <div className="space-y-3 pt-4 border-t border-white/5 text-xs font-mono">
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Input</span>
                                        <span className="text-slate-300 text-right">{layer.input}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Output</span>
                                        <span className="text-slate-300 text-right">{layer.output}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-500">Source</span>
                                        <span className="text-teal-400/80 text-right">{layer.source}</span>
                                    </div>
                                </div>
                            </GlassCard>
                        );
                    })}
                </div>
            </Section>
        </div>
    );
}
