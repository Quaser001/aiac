"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import {
    LayoutDashboard,
    Dna,
    Beaker,
    Microscope,
    BrainCircuit,
    Activity,
    Scan,
    Box,
    ChevronLeft,
    ChevronRight
} from "lucide-react";

const NAV_ITEMS = [
    { label: "Overview", href: "/console", icon: LayoutDashboard },
    { label: "Mechanism", href: "/console/mechanism", icon: Dna },
    { label: "Phenotype", href: "/console/phenotype", icon: Beaker },
    { label: "Structure", href: "/console/structure", icon: Box },
    { label: "Docking", href: "/console/docking", icon: Microscope },
    { label: "Mutation Impact", href: "/console/ai/impact", icon: Activity },
    { label: "Novelty Scan", href: "/console/ai/novelty", icon: Scan },
    { label: "Prediction", href: "/console/ai/predict", icon: BrainCircuit },
];

export function Sidebar({ collapsed, setCollapsed }: { collapsed: boolean; setCollapsed: (v: boolean) => void }) {
    const pathname = usePathname();

    return (
        <aside
            className={cn(
                "h-screen border-r border-white/10 bg-slate-900/80 backdrop-blur-md hidden lg:flex flex-col fixed left-0 top-16 bottom-0 z-40 transition-all duration-300",
                collapsed ? "w-20" : "w-64"
            )}
        >
            <div className="flex items-center justify-between p-4 mb-2">
                {!collapsed && (
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest animate-fade-in">
                        Console Modules
                    </span>
                )}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-1 rounded hover:bg-white/5 text-slate-500 hover:text-white transition-colors ml-auto"
                >
                    {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
                </button>
            </div>

            <nav className="space-y-1 px-2 flex-1 overflow-y-auto custom-scrollbar">
                {NAV_ITEMS.map((item) => {
                    const isActive = pathname?.startsWith(item.href);
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg transition-all",
                                isActive
                                    ? "bg-teal-500/10 text-teal-400 border border-teal-500/20"
                                    : "text-slate-400 hover:text-white hover:bg-white/5",
                                collapsed && "justify-center px-2"
                            )}
                            title={collapsed ? item.label : undefined}
                        >
                            <item.icon className={cn("w-5 h-5 shrink-0", isActive ? "text-teal-400" : "text-slate-500")} />
                            {!collapsed && <span className="truncate">{item.label}</span>}
                        </Link>
                    )
                })}
            </nav>

            <div className="mt-auto p-4 border-t border-white/5 bg-slate-900/50">
                <StatusIndicator collapsed={collapsed} />
            </div>
        </aside>
    );
}

function StatusIndicator({ collapsed }: { collapsed: boolean }) {
    const [isOnline, setIsOnline] = useState(false);

    useEffect(() => {
        const checkHealth = async () => {
            try {
                const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const res = await fetch(`${API_URL}/health`);
                setIsOnline(res.ok);
            } catch (e) {
                setIsOnline(false);
            }
        };

        checkHealth();
        const interval = setInterval(checkHealth, 30000); // Check every 30s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className={cn(
            "rounded border transition-colors flex flex-col gap-2 p-2",
            isOnline
                ? "bg-indigo-500/10 border-indigo-500/20"
                : "bg-red-500/10 border-red-500/20"
        )}>
            <div className="flex items-center gap-3 px-1">
                <span className={cn(
                    "flex w-2 h-2 rounded-full animate-pulse shrink-0",
                    isOnline ? "bg-green-500" : "bg-red-500"
                )} />
                {!collapsed && (
                    <div className="overflow-hidden">
                        <p className={cn(
                            "text-xs font-medium mb-0.5 truncate",
                            isOnline ? "text-indigo-300" : "text-red-400"
                        )}>
                            System Status
                        </p>
                        <p className="text-[10px] text-slate-400 truncate">
                            {isOnline ? "Backend Online" : "Backend Offline"}
                        </p>
                    </div>
                )}
            </div>

            {!collapsed && isOnline && <LiveInferenceToggle />}
        </div>
    );
}

// Custom Toggle UI used below

function LiveInferenceToggle() {
    const [liveEnabled, setLiveEnabled] = useState(false);

    // Initial State Fetch
    useEffect(() => {
        fetch("http://localhost:8000/system/mode")
            .then(res => res.json())
            .then(data => setLiveEnabled(data.mode === "online"))
            .catch(() => { });
    }, []);

    const toggleMode = async () => {
        const newMode = !liveEnabled ? "online" : "offline";
        setLiveEnabled(!liveEnabled); // Optimistic update
        try {
            await fetch("http://localhost:8000/system/mode", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mode: newMode })
            });
        } catch (e) {
            setLiveEnabled(liveEnabled); // Revert on error
        }
    };

    return (
        <div className="flex items-center gap-2 mt-2 pt-2 border-t border-white/5 opacity-80 hover:opacity-100 transition-opacity">
            <span className={cn("w-2 h-2 rounded-full", liveEnabled ? "bg-amber-400 animate-pulse" : "bg-slate-600")} />
            <div className="flex-1">
                <p className="text-[10px] text-slate-300 font-medium">Research Mode</p>
                <p className="text-[9px] text-slate-500">{liveEnabled ? "ONLINE: Live Inference" : "OFFLINE: Cached Demo"}</p>
            </div>
            <button
                onClick={toggleMode}
                className={cn(
                    "w-8 h-4 rounded-full relative transition-colors border border-white/10",
                    liveEnabled ? "bg-teal-500/20 border-teal-500/50" : "bg-slate-800"
                )}
            >
                <div className={cn(
                    "absolute top-0.5 w-3 h-3 rounded-full transition-all",
                    liveEnabled ? "right-0.5 bg-teal-400" : "left-0.5 bg-slate-500"
                )} />
            </button>
        </div>
    );
}
