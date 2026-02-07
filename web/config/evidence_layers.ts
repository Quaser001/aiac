
export const EVIDENCE_LAYERS = [
    {
        "id": 0,
        "name": "Mechanism Ontology",
        "status": "ACTIVE",
        "input": "Genotype (Gene Symbol)",
        "output": "Mechanism Class + Drug Risk",
        "source": "CARD Database (v3.2.9)",
        "description": "Deterministic mapping of resistance genes to mechanism families and compromised drug classes.",
        "isFuture": false
    },
    {
        "id": 1,
        "name": "Phenotype Evidence",
        "status": "ACTIVE_SUBSET",
        "input": "Organism Context",
        "output": "MIC Susceptibility Data",
        "source": "BV-BRC / PATRIC",
        "description": "Real-world observational data showing actual resistance levels (MIC) for specific pathogen-drug combinations.",
        "isFuture": false
    },
    {
        "id": 2,
        "name": "Variant Embeddings",
        "status": "READY",
        "input": "Protein Sequence",
        "output": "Functional Similarity Score",
        "source": "ESM-2 / ProtT5",
        "description": "Deep learning embeddings to quantify functional impact of novel mutations beyond homology.",
        "isFuture": true
    },
    {
        "id": 3,
        "name": "Structural Localization",
        "status": "ACTIVE (Demo Cache)",
        "input": "AlphaFold Structure",
        "output": "Active Site Proximity",
        "source": "AlphaFold DB",
        "description": "Mapping mutations to 3D protein structures to determine proximity to catalytic sites.",
        "isFuture": false
    },
    {
        "id": 4,
        "name": "Docking Feasibility",
        "status": "ACTIVE (Research Mode)",
        "input": "DiffDock / GNINA",
        "output": "Binding Affinity (ΔG)",
        "source": "PDB / Zinc15",
        "description": "In-silico docking of antibiotics to mutant structures to predict binding disruption.",
        "isFuture": false
    },
    {
        "id": 5,
        "name": "Molecular Dynamics",
        "status": "FUTURE",
        "input": "OpenMM / GROMACS",
        "output": "Stability Trajectory",
        "source": "HPC Cluster",
        "description": "Full atomistic simulation to validate stability and folding of complex mutants.",
        "isFuture": true
    }
];

export default EVIDENCE_LAYERS;
