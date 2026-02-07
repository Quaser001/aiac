"use client";

import React, { useEffect, useRef, useState } from "react";

type Props = {
    pdbId?: string;
    highlightResidue?: number;
};

export default function StructureViewer({
    pdbId = "4RL2",
    highlightResidue,
}: Props) {
    const containerRef = useRef<HTMLDivElement | null>(null);
    const viewerRef = useRef<any>(null);

    const [status, setStatus] = useState<
        "idle" | "loading" | "ready" | "error"
    >("idle");

    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // ✅ WebGL Support Check
    function checkWebGL(): boolean {
        try {
            const canvas = document.createElement("canvas");
            return !!(
                window.WebGLRenderingContext &&
                (canvas.getContext("webgl") || canvas.getContext("experimental-webgl"))
            );
        } catch {
            return false;
        }
    }

    async function loadStructure() {
        if (!containerRef.current) return;

        // ✅ Handle Unmapped Structure (e.g. vanA)
        if (!pdbId) {
            setStatus("idle"); // or custom 'unmapped' state
            // We'll handle render below
            return;
        }

        setStatus("loading");
        setErrorMsg(null);

        // ✅ WebGL unavailable
        if (!checkWebGL()) {
            setStatus("error");
            setErrorMsg("WebGL is disabled or unsupported on this device.");
            return;
        }

        // ✅ Prevent React double-init crashes
        if (viewerRef.current) {
            viewerRef.current.clear();
            viewerRef.current = null;
        }

        try {
            // ✅ Dynamic import of 3Dmol
            const $3Dmol = await import("3dmol");

            // ✅ Force container height (prevents invisible viewer)
            containerRef.current.style.height = "420px";

            // ✅ Create viewer
            viewerRef.current = $3Dmol.createViewer(containerRef.current, {
                backgroundColor: "black",
            });

            // ✅ Fetch PDB file
            const pdbUrl = `/structures/${pdbId}.pdb`;
            console.log("[StructureViewer] Fetching PDB:", pdbUrl);

            const res = await fetch(pdbUrl);

            if (!res.ok) {
                // Treat missing file as "Unmapped/Pending" for demo safety
                console.warn(`PDB missing: ${pdbUrl}`);
                setStatus("idle"); // Render the neutral "Unmapped" state
                return;
            }

            const pdbText = await res.text();

            // ✅ Load model
            viewerRef.current.addModel(pdbText, "pdb");
            viewerRef.current.setStyle({}, { cartoon: { color: "spectrum" } });

            // ✅ Highlight mutation residue
            if (highlightResidue) {
                viewerRef.current.setStyle(
                    { resi: highlightResidue },
                    { stick: { radius: 0.3, color: "red" } }
                );
            }

            viewerRef.current.zoomTo();
            viewerRef.current.render();

            setStatus("ready");
        } catch (err: any) {
            console.error("[StructureViewer ERROR]", err);

            setStatus("error");
            setErrorMsg(err.message || "Viewer failed to load.");
        }
    }

    // ✅ Auto-load on mount or pdbId change
    useEffect(() => {
        loadStructure();

        return () => {
            if (viewerRef.current) {
                viewerRef.current.clear();
                viewerRef.current = null;
            }
        };
    }, [pdbId]);

    return (
        <div className="w-full rounded-2xl border border-white/10 bg-black/20 p-4 relative overflow-hidden" style={{ maxWidth: "100%" }}>
            <h3 className="text-sm font-semibold text-white/70 mb-2">
                Structural Localization ({pdbId})
            </h3>

            {status === "loading" && (
                <p className="text-yellow-400 text-sm">Loading structure...</p>
            )}

            {status === "error" && (
                <div className="text-red-400 text-sm space-y-2">
                    <p>Structure Viewer Failed</p>
                    <p className="text-white/50">{errorMsg}</p>

                    <button
                        onClick={loadStructure}
                        className="px-3 py-1 rounded-lg bg-white/10 hover:bg-white/20"
                    >
                        Retry
                    </button>
                </div>
            )}

            {/* Unmapped State */}
            {!pdbId && (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500 bg-slate-900/50">
                    <div className="p-4 bg-slate-800/80 rounded-full mb-3">
                        {/* Neutral Icon */}
                        <svg className="w-8 h-8 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                    </div>
                    <p className="text-sm font-medium">Structure not yet mapped</p>
                    <p className="text-xs opacity-60">High-resolution PDB pending.</p>
                </div>
            )}

            {/* VIEWER CONTAINER */}
            <div
                ref={containerRef}
                className="w-full rounded-xl mt-3"
                style={{ minHeight: "420px", position: "relative" }}
            />
        </div>
    );
}
