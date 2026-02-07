# ABRISK Conference Demo Checklist

**Version**: 1.0 (Phase 20 Golden Master)
**Status**: Feature Complete & Hardened

## 1. Preparation (10 mins before demo)

### Environment
1.  **Network**: Not required (if assets cached), but recommended for backup CDN loads (Fonts/Tailwind).
2.  **Display**: 1920x1080 recommended.

### Startup
Open two terminals:

**Terminal 1 (Backend)**:
```bash
cd AIAIC
python -m uvicorn src.api.main:app --port 8000
```
*Wait for "Application startup complete".*

**Terminal 2 (Frontend)**:
```bash
cd AIAIC/web
npm run start
```
*Wait for "Ready on http://localhost:3000".*

## 2. The Demo Flow (Golden Path)

### Step 1: Introduction
- Open `http://localhost:3000`.
- Show **Landing Page**: "Antibiotic Risk Stratification".
- Click **"Open Application"**.

### Step 2: Analysis Console
- **Action**: Click the **"Load Demo Scenario (NDM-1 + Klebsiella)"** button (Top Left).
- **Observation**:
    - Input fills automatically.
    - "Analyzing..." spinner appears.
    - Results populate in < 2 seconds.

### Step 3: Explanation (The Evidence Ladder)
1.  **Mechanism (Layer 2)**:
    - Card: **NDM-1 (Metallo-Beta-Lactamase)**.
    - highlight: "Antibiotic Inactivation".
2.  **Clinical Impact (Layer 1)**:
    - Card: **High Risk Tier**.
    - Impact: **Carbapenem, Cephalosporin, Penicillin**.
3.  **Phenotype (Layer 2.5)**:
    - Show "Phenotype Evidence" panel (Blue).
    - Point out: **Klebsiella pneumoniae** context.
    - Point out: **Meropenem MIC > 32** (Resistant).
4.  **Structure (Layer 3)**:
    - Show 3D Viewer (Green/Black).
    - Rotate protein (NDM-1).

### Step 4: The "Wow" Moment (Docking)
- Scroll to **Docking Feasibility** (Purple Panel).
- **Action**: Click **"Run Docking Demo"**.
- **Wait**: ~5-10 seconds (Real Vina calculation).
- **Observation**:
    - Result appears: **-7.2 kcal/mol** (approx).
    - **Disclaimer**: Point out "Hypothesis support only".
    - Viewer updates: Ligand (Green stick) appears in pocket.

### Step 5: Wrap Up
- **Action**: Click **"top-right Export icon"** or **"Export Report"** button (on Clinical Card).
- **Observation**: `abrisk_evidence_report.json` downloads.
- Open JSON to show comprehensive data trail.

## 3. Troubleshooting

- **"Vina missing"**: Ensure `data/docking_cache/vina/vina.exe` exists.
- **"Structure not mapped"**: Only NDM-1 and KPC-2 have PDBs in demo map.
- **Backend Error**: check Terminal 1 logs.

## 4. Disclaimers (Verbal)
"This tool supports decision making by stratifying risk. It does not prescribe medication. Docking Results are for research hypothesis generation only."
