import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                // Base colors
                slate: {
                    850: '#1e293b',
                    950: '#020617',
                },
                // Accent Colors
                teal: {
                    DEFAULT: '#14b8a6',
                    50: '#f0fdfa',
                    100: '#ccfbf1',
                    200: '#99f6e4',
                    300: '#5eead4',
                    400: '#2dd4bf',
                    500: '#14b8a6',
                    600: '#0d9488',
                    700: '#0f766e',
                    800: '#115e59',
                    900: '#134e4a',
                },
                clinical: {
                    DEFAULT: '#3b82f6',
                    light: '#93c5fd',
                    dark: '#1d4ed8',
                },
                specialist: {
                    DEFAULT: '#8b5cf6',
                    light: '#c4b5fd',
                    dark: '#6d28d9',
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
                'biotech-hero': ['Inter', 'system-ui', 'sans-serif'], /* For explicit heavy tracking usage */
            },
            backgroundImage: {
                "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
                "gradient-dark": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            },
            backdropBlur: {
                xs: '2px',
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'slide-up': 'slideUp 0.5s ease-out forwards',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
            boxShadow: {
                'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.36)',
                'glow-teal': '0 0 40px -10px rgba(20, 184, 166, 0.5)',
                'glow-clinical': '0 0 40px -10px rgba(59, 130, 246, 0.5)',
                'glow-specialist': '0 0 40px -10px rgba(139, 92, 246, 0.5)',
            },
        },
    },
    plugins: [],
};

export default config;
