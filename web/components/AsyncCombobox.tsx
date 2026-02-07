
import { useState, useEffect, useRef } from "react";
import useSWR from "swr";
import { Check, ChevronsUpDown, Loader2, Search } from "lucide-react";
import { cn } from "@/lib/utils";


interface AsyncComboboxProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    label?: string;
    endpoint?: string;
}

export function AsyncCombobox({ value, onChange, placeholder = "Search...", label, endpoint = "/specialist/genes/search" }: AsyncComboboxProps) {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState("");
    const [options, setOptions] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [debouncedQuery, setDebouncedQuery] = useState("");
    const [mounted, setMounted] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    // Patch 3: Friendly Label Mapping
    const getFriendlyLabel = (gene: string) => {
        if (gene.startsWith("NDM")) return "Carbapenemase (β-lactam inactivation)";
        if (gene.startsWith("CTX-M")) return "ESBL (extended-spectrum β-lactamase)";
        if (gene.startsWith("KPC")) return "Carbapenemase";
        if (gene.startsWith("OXA")) return "Oxacillinase carbapenemase";
        if (gene.startsWith("AAC")) return "Aminoglycoside acetyltransferase";
        if (gene.startsWith("mecA")) return "Methicillin resistance (PBP2a)";
        if (gene.startsWith("vanA")) return "Vancomycin resistance";
        return null;
    };

    useEffect(() => {
        setMounted(true);
    }, []);

    // Sync value
    useEffect(() => {
        if (value && !query) {
            // Keep query empty to avoid triggering search on mount
        }
    }, [value]);

    // Debounce
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedQuery(query);
        }, 300);
        return () => clearTimeout(timer);
    }, [query]);

    // Patch 1: Search-First Logic (1 char trigger)
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const apiBase = API_URL.replace(/\/$/, "");
    const apiPath = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

    const shouldFetch = open && debouncedQuery.length >= 1;
    const fetchUrl = shouldFetch ? `${apiBase}${apiPath}?query=${encodeURIComponent(debouncedQuery)}` : null;

    const fetcher = (url: string) => fetch(url).then(r => {
        if (!r.ok) throw new Error("Backend Unavailable");
        return r.json();
    });

    const { data: swrData, error: swrError, isLoading } = useSWR(fetchUrl, fetcher, {
        keepPreviousData: false, // Don't keep old search results
        onError: (err) => {
            console.error("Search error:", err);
            setOptions([]);
        }
    });

    useEffect(() => {
        if (shouldFetch && swrData) {
            setOptions(swrData);
        } else if (!shouldFetch) {
            setOptions([]); // Clear options if query is too short
        }
    }, [swrData, shouldFetch]);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    if (!mounted) return null;

    return (
        <div className="relative space-y-2" ref={containerRef}>
            {label && (
                <label className="text-xs font-semibold text-teal-400 uppercase tracking-wider">
                    {label}
                </label>
            )}
            <div className="relative">
                <div
                    className="input-glass flex items-center justify-between cursor-pointer py-3 pl-10"
                    onClick={() => setOpen(!open)}
                >
                    <span className={value ? "text-white" : "text-slate-500"}>
                        {value || placeholder}
                    </span>
                    <ChevronsUpDown className="w-4 h-4 text-slate-500 opacity-50" />
                </div>
                <Search className="absolute left-3 top-3.5 w-4 h-4 text-slate-500" />
            </div>

            {open && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-slate-900/95 backdrop-blur-xl border border-white/10 rounded-lg shadow-2xl z-50 overflow-hidden animate-slide-down">
                    <div className="p-2 border-b border-white/5">
                        <input
                            autoFocus
                            className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none p-1"
                            placeholder="Type to search..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                    </div>
                    <div className="max-h-60 overflow-y-auto p-1">
                        {isLoading ? (
                            <div className="flex items-center justify-center py-4 text-slate-500">
                                <Loader2 className="w-4 h-4 animate-spin mr-2" />
                                Loading...
                            </div>
                        ) : !shouldFetch && query.length < 1 ? (
                            <div className="py-8 px-4 text-center text-slate-500 text-xs">
                                Start typing to search...
                            </div>
                        ) : options.length === 0 ? (
                            <div className="py-2 px-3 text-sm text-slate-500">No results found.</div>
                        ) : (
                            options.map((option) => (
                                <div
                                    key={option}
                                    className={cn(
                                        "flex flex-col px-3 py-2 rounded cursor-pointer transition-colors text-sm border-b border-white/5 last:border-0",
                                        value === option ? "bg-teal-500/20" : "hover:bg-white/5"
                                    )}
                                    onClick={() => {
                                        onChange(option);
                                        setOpen(false);
                                        setQuery("");
                                    }}
                                >
                                    <div className="flex items-center justify-between">
                                        <span className={value === option ? "text-teal-300 font-medium" : "text-slate-200"}>
                                            {option}
                                        </span>
                                        {value === option && <Check className="w-3 h-3 text-teal-400" />}
                                    </div>
                                    {getFriendlyLabel(option) && (
                                        <span className="text-[10px] text-slate-500 uppercase tracking-wide mt-0.5">
                                            {getFriendlyLabel(option)}
                                        </span>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
