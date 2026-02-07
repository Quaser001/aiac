# ABRISK Future Architecture: High-Compute Extensions

**Status**: Design Specification (Phase 6)
**Constraint**: "Architect Only" - No current implementation.

## 1. Overview
ABRISK is currently a lightweight, CPU-bound API service. Future capabilities (AlphaFold structure prediction, AutoDock Vina, GROMACS MD) require significant GPU resources and long execution times.
To maintain system responsiveness, we define a **Sidecar Worker Pattern**.

## 2. Infrastructure Design

```mermaid
graph LR
    A[Client] -->|POST /analyze/genome| B[FastAPI Gateway];
    B -->|Fast Path| C[GeneParser & RiskStratifier];
    C -->|JSON| B;
    B -->|Slow Path Request?| D[Redis Queue];
    D --> E[GPU Worker Node];
    E -->|AlphaFold/Docking| F[Object Storage (S3)];
    E -->|Result Update| G[Postgres DB];
    B <-->|Poll Status| G;
```

### Components
1.  **FastAPI Gateway (Existing)**: continues to serve immediate risk reports based on *pre-computed* or *sequence-only* data.
2.  **Job Queue (Future)**: Redis/RabbitMQ to buffer simulation requests.
3.  **GPU Worker Nodes (Future)**:
    - Dedicated heavy instances (e.g., A100s).
    - **Container A**: AlphaFold2 (Structure Prediction).
    - **Container B**: AutoDock Vina (Ligand Binding).
4.  **Storage**:
    - **S3-compatible**: To store large PDB files and MD trajectories.
    - **PostgreSQL**: To store job status and pointers to S3 files.

## 3. Integration Points

### A. Structure Prediction (AlphaFold)
*   **Trigger**: When `GeneParser` detects a sequence with <90% identity to known structures AND `RiskStratifier` tags it as "High Priority Variant".
*   **Action**: Dispatch job to generate PDB.
*   **Usage**: Once generated, the PDB is fed back into the `Biological Logic` (Step 2) for geometric active-site analysis.

### B. Molecular Docking
*   **Trigger**: User request for specific antibiotic binding affinity against a newly found variant.
*   **Input**: PDB (from AlphaFold) + Antibiotic Structure (SDF).
*   **Action**: Run AutoDock Vina.
*   **Output**: Binding Energy ($\Delta G$).
*   **Risk Logic Update**: If $\Delta G$ > Threshold (weaker binding), increase Risk Tier.

## 4. Verification & Trust
*   **Audit Trail**: All simulation parameters (temperature, forcefield, seed) must be logged.
*   **Confidence Metrics**: AlphaFold pLDDT scores must be presented to the user. "Low Confidence" regions must trigger a warning, not a firm decision.

## 5. Security & Governance
*   **Q: Why not run this locally?** A: Computational cost and dependency hell.
*   **Partnership Dependency**: Access to proprietary molecule libraries or high-spec cloud compute (e.g., Google Cloud Life Sciences) is required for scale.
