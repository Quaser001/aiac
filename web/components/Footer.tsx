import Link from 'next/link';
import { Shield, AlertTriangle } from 'lucide-react';

export function Footer() {
    return (
        <footer className="border-t border-white/5 mt-auto">
            <div className="container-lg px-4 py-12">


                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Brand */}
                    <div className="md:col-span-2">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="p-2 rounded-lg bg-teal-500/10 border border-teal-500/20">
                                <Shield className="w-5 h-5 text-teal-400" />
                            </div>
                            <span className="font-semibold text-lg">ABRISK</span>
                        </div>
                        <p className="text-caption max-w-md">
                            Structure-informed antibiotic risk stratification and mechanism intelligence
                            for clinicians and researchers combating antimicrobial resistance.
                        </p>
                    </div>

                    {/* Platform Links */}
                    <div>
                        <h4 className="font-medium mb-4 text-sm text-white">Platform</h4>
                        <div className="flex flex-col gap-2">
                            <Link href="/product" className="text-caption hover:text-white transition-colors">Product</Link>
                            <Link href="/how-it-works" className="text-caption hover:text-white transition-colors">How It Works</Link>
                            <Link href="/use-cases" className="text-caption hover:text-white transition-colors">Use Cases</Link>
                            <Link href="/app" className="text-caption hover:text-white transition-colors">Application</Link>
                        </div>
                    </div>

                    {/* Resources */}
                    <div>
                        <h4 className="font-medium mb-4 text-sm text-white">Resources</h4>
                        <div className="flex flex-col gap-2">
                            <Link href="/docs" className="text-caption hover:text-white transition-colors">Documentation</Link>
                            <Link href="/about" className="text-caption hover:text-white transition-colors">About</Link>
                            <a
                                href="https://card.mcmaster.ca"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-caption hover:text-white transition-colors"
                            >
                                CARD Database ↗
                            </a>
                        </div>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="border-t border-white/5 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
                    © 2026 ABRISK.

                    <p className="text-xs text-slate-500">
                        Data source: Comprehensive Antibiotic Resistance Database (CARD)
                    </p>
                </div>
            </div>
        </footer>
    );
}
