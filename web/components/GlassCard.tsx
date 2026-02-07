import { ReactNode } from 'react';

interface GlassCardProps {
    children: ReactNode;
    variant?: 'default' | 'clinical' | 'specialist' | 'strong';
    className?: string;
    glow?: boolean;
}

export function GlassCard({
    children,
    variant = 'default',
    className = '',
    glow = false
}: GlassCardProps) {
    const baseClasses = 'p-6 rounded-xl transition-all duration-300';

    const variantClasses = {
        default: 'glass hover:bg-white/[0.05]',
        clinical: 'glass border-clinical/20 hover:border-clinical/40',
        specialist: 'glass border-specialist/20 hover:border-specialist/40',
        strong: 'glass-strong',
    };

    const glowClasses = {
        default: glow ? 'glow-teal' : '',
        clinical: glow ? 'glow-clinical' : '',
        specialist: glow ? 'glow-specialist' : '',
        strong: '',
    };

    return (
        <div className={`${baseClasses} ${variantClasses[variant]} ${glowClasses[variant]} ${className}`}>
            {children}
        </div>
    );
}

// Section Component for consistent page sections
interface SectionProps {
    children: ReactNode;
    className?: string;
    id?: string;
}

export function Section({ children, className = '', id }: SectionProps) {
    return (
        <section id={id} className={`section ${className}`}>
            <div className="container-max">
                {children}
            </div>
        </section>
    );
}

// Feature Card with icon
interface FeatureCardProps {
    icon: ReactNode;
    title: string;
    description: string;
    variant?: 'default' | 'clinical' | 'specialist';
}

export function FeatureCard({ icon, title, description, variant = 'default' }: FeatureCardProps) {
    const accentColors = {
        default: 'text-teal-400',
        clinical: 'text-clinical-light',
        specialist: 'text-specialist-light',
    };

    return (
        <GlassCard variant={variant}>
            <div className={`w-12 h-12 rounded-lg glass flex items-center justify-center mb-4 ${accentColors[variant]}`}>
                {icon}
            </div>
            <h3 className={`heading-md mb-2 ${accentColors[variant]}`}>{title}</h3>
            <p className="text-body">{description}</p>
        </GlassCard>
    );
}
