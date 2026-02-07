"use client";

import Link from 'next/link';
import { useState } from 'react';
import { Menu, X, Shield } from 'lucide-react';

const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/product', label: 'Product' },
    { href: '/how-it-works', label: 'How It Works' },
    { href: '/use-cases', label: 'Use Cases' },
    { href: '/console', label: 'App' },
    { href: '/about', label: 'About' },
    { href: '/docs', label: 'Docs' },
];

export function Navigation() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="glass-strong sticky top-0 z-50">
            <div className="container-lg">
                <div className="flex items-center justify-between h-16 px-4">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="p-2 rounded-lg bg-teal-500/10 border border-teal-500/20 group-hover:border-teal-500/40 transition-colors">
                            <Shield className="w-5 h-5 text-teal-400" />
                        </div>
                        <span className="font-semibold text-lg tracking-tight">ABRISK</span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center gap-1">
                        {navLinks.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className="px-4 py-2 rounded-lg text-sm text-slate-300 hover:text-white hover:bg-white/5 transition-all duration-200"
                            >
                                {link.label}
                            </Link>
                        ))}
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="md:hidden p-2 rounded-lg hover:bg-white/5 transition-colors"
                        aria-label="Toggle menu"
                    >
                        {isOpen ? (
                            <X className="w-5 h-5" />
                        ) : (
                            <Menu className="w-5 h-5" />
                        )}
                    </button>
                </div>

                {/* Mobile Navigation */}
                {isOpen && (
                    <div className="md:hidden border-t border-white/10 py-4 px-4 animate-fade-in">
                        <div className="flex flex-col gap-2">
                            {navLinks.map((link) => (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    onClick={() => setIsOpen(false)}
                                    className="px-4 py-3 rounded-lg text-sm text-slate-300 hover:text-white hover:bg-white/5 transition-all duration-200"
                                >
                                    {link.label}
                                </Link>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
}
