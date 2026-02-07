"use client";

import React, { createContext, useContext, useState, ReactNode } from 'react';

// Types
interface StructureStatus {
    status: 'ready' | 'missing' | 'unavailable';
    pdb_id?: string;
    message?: string;
}

interface DockingStatus {
    status: 'ready' | 'missing' | 'complete';
    ligand?: string;
    receptor?: string;
    affinity?: number;
}

interface AnalysisResult {
    matchType: string;
    // Add other fields as they appear in the real result. 
    // Using any for flexibility during refactor, but strict types prefered.
    [key: string]: any;
}

interface ConsoleContextType {
    determinant: string;
    organism: string;
    ligand: string;
    isDemoMode: boolean;
    analysisResult: AnalysisResult | null;
    structureStatus: StructureStatus;
    dockingStatus: DockingStatus;

    setDeterminant: (val: string) => void;
    setOrganism: (val: string) => void;
    setLigand: (val: string) => void;
    setIsDemoMode: (val: boolean) => void;
    setAnalysisResult: (val: AnalysisResult | null) => void;
    setStructureStatus: (val: StructureStatus) => void;
    setDockingStatus: (val: DockingStatus) => void;
    resetAnalysis: () => void;
}

const ConsoleContext = createContext<ConsoleContextType | undefined>(undefined);

export function ConsoleProvider({ children }: { children: ReactNode }) {
    const [determinant, setDeterminant] = useState('');
    const [organism, setOrganism] = useState('');
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [structureStatus, setStructureStatus] = useState<StructureStatus>({ status: 'unavailable' });
    const [dockingStatus, setDockingStatus] = useState<DockingStatus>({ status: 'missing' });

    const [ligand, setLigand] = useState('');
    const [isDemoMode, setIsDemoMode] = useState(false); // Default to False (Online/Research)

    const resetAnalysis = () => {
        setAnalysisResult(null);
        setStructureStatus({ status: 'unavailable' });
        setDockingStatus({ status: 'missing' });
        setLigand('');
    };

    return (
        <ConsoleContext.Provider value={{
            determinant,
            organism,
            ligand,
            isDemoMode,
            analysisResult,
            structureStatus,
            dockingStatus,
            setDeterminant,
            setOrganism,
            setLigand,
            setIsDemoMode,
            setAnalysisResult,
            setStructureStatus,
            setDockingStatus,
            resetAnalysis
        }}>
            {children}
        </ConsoleContext.Provider>
    );
}

export function useConsole() {
    const context = useContext(ConsoleContext);
    if (context === undefined) {
        throw new Error('useConsole must be used within a ConsoleProvider');
    }
    return context;
}
