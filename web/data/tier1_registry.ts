export interface Tier1Definition {
    pdb: string | null;
    ligand: { name: string; smiles?: string };
    host: string;
    mutations: string[];
    mechanism_type?: string;
    sequencePath?: string; // Path to cached FASTA
}

export const TIER1_REGISTRY: Record<string, Tier1Definition> = {
    "NDM-1": {
        pdb: "4RL2",
        ligand: { name: "Meropenem", smiles: "CC1(C(N2C(S1)C(C2=O)NC(=O)C(C3=CC=CC=C3)C(=O)O)C(=O)O)C" },
        host: "Klebsiella pneumoniae",
        mutations: ["H122Y", "K211R"],
        mechanism_type: "Metallo-β-lactamase (MBL)",
        sequencePath: "/data/tier1/sequences/NDM-1.fasta"
    },
    "KPC-2": {
        pdb: "2OV5",
        ligand: { name: "Ceftazidime", smiles: "CC1(C(N2C(S1)C(C2=O)NC(=O)C(C3=CC=CC=C3)C(=O)O)C(=O)O)C" },
        host: "Escherichia coli",
        mutations: ["S69Y", "I220K"],
        mechanism_type: "Serine carbapenemase",
        sequencePath: "/data/tier1/sequences/KPC-2.fasta"
    },
    "CTX-M-15": {
        pdb: "4HBU",
        ligand: { name: "Cefotaxime", smiles: "" },
        host: "Escherichia coli",
        mutations: ["D240G", "N106S"],
        mechanism_type: "ESBL β-lactamase",
        sequencePath: "/data/tier1/sequences/CTX-M-15.fasta"
    },
    "OXA-48": {
        pdb: "5QB4",
        ligand: { name: "Imipenem", smiles: "" },
        host: "Klebsiella pneumoniae",
        mutations: ["K73R", "R163N"],
        mechanism_type: "Oxacillinase carbapenemase",
        sequencePath: "/data/tier1/sequences/OXA-48.fasta"
    },
    "mecA": {
        pdb: "3ZG5",
        ligand: { name: "Oxacillin", smiles: "" },
        host: "Staphylococcus aureus",
        mutations: ["I108L", "E150K"],
        mechanism_type: "Target alteration (MRSA)",
        sequencePath: "/data/tier1/sequences/mecA.fasta"
    },
    "vanA": {
        pdb: null, // Structure not yet mapped
        ligand: { name: "Vancomycin", smiles: "" },
        host: "Enterococcus faecium",
        mutations: ["H244A", "Y200A"],
        mechanism_type: "Cell wall precursor remodeling",
        sequencePath: "/data/tier1/sequences/vanA.fasta"
    }
};

export const isTier1 = (det: string) => !!TIER1_REGISTRY[det];

// Helper to get sequence path for Tier-1 determinants
export const getTier1SequencePath = (det: string): string | null => {
    return TIER1_REGISTRY[det]?.sequencePath || null;
};

