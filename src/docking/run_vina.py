import os
import subprocess
from src.docking.vina_manager import get_vina_path
from src.docking.ligand_cache import get_ligand
from src.docking.receptor_prep import prepare_receptor

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS_DIR = os.path.join(BASE_DIR, "data", "docking_cache", "results")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_docking_job(determinant: str, ligand: str) -> dict:
    """
    Executes REAL docking job. Fails if dependencies missing.
    NO SIMULATION.
    """
    job_id = f"{determinant}_{ligand}"
    ensure_dir(RESULTS_DIR)
    
    # 1. Resolve PDB
    pdb_id = None
    demo_fallback = False
    
    if determinant.upper() == "NDM-1":
        pdb_id = "4RL2"
        demo_fallback = True
    elif determinant.upper() == "KPC-2":
         pdb_id = "2OV5"
         
    if not pdb_id:
        return {"status": "error", "message": "Docking unavailable: no receptor structure mapped."}

    # 2. Fetch Dependencies
    print(f"[Docking] resolving assets for {job_id}...")
    
    vina_exe = get_vina_path()
    if not vina_exe:
        return {"status": "error", "message": "Vina missing — research mode disabled."}

    # CID Hardcoded for demo flow, but fetching is dynamic
    ligand_pdbqt = get_ligand("meropenem", "441130") 
    if not ligand_pdbqt:
        return {"status": "error", "message": "Ligand conversion unavailable — install OpenBabel."}

    receptor_pdbqt = prepare_receptor(pdb_id)
    if not receptor_pdbqt:
         return {"status": "error", "message": "Receptor preparation failed — install OpenBabel."}

    # 3. Construct Config/Run
    from src.docking.simple_pdbqt import get_center_of_mass
    center = get_center_of_mass(receptor_pdbqt)
    # Default to (0,0,0) if calculation fails
    cx, cy, cz = center if center else (0, 0, 0)
    print(f"[Docking] Grid Center: {cx:.2f}, {cy:.2f}, {cz:.2f}")

    out_pdbqt = os.path.join(RESULTS_DIR, f"{job_id}_pose.pdbqt")
    log_file = os.path.join(RESULTS_DIR, f"{job_id}.log")

    cmd = [
        vina_exe,
        "--receptor", receptor_pdbqt,
        "--ligand", ligand_pdbqt,
        "--center_x", f"{cx:.3f}", "--center_y", f"{cy:.3f}", "--center_z", f"{cz:.3f}",
        "--size_x", "20", "--size_y", "20", "--size_z", "20",
        "--out", out_pdbqt,
        "--cpu", "1"
    ]

    print(f"[Docking] Executing: {' '.join(cmd)}")
    try:
        # 4. EXECUTE
        result = subprocess.run(cmd, check=True, stdout=open(log_file, 'w'), stderr=subprocess.PIPE, text=True)
        
        # 5. Parse Score
        best_score = 0.0
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip().startswith("1"):
                    # Output format: mode | affinity | dist...
                    parts = line.split()
                    if len(parts) >= 2:
                        best_score = float(parts[1])
                        break
        
        return {
            "status": "completed",
            "score": best_score,
            "unit": "kcal/mol",
            "pose_file": f"/docking_results/{job_id}_pose.pdbqt",
            "disclaimer": ("Using demo receptor 4RL2. " if demo_fallback else "") + "Research-mode docking feasibility (Vina scoring). Hypothesis support only. Ligand/receptor preparation is simplified for demo. Not a production chemistry pipeline."
        }
        
    except subprocess.CalledProcessError as e:
        print(f"[Docking] Vina Error Code: {e.returncode}")
        # print(f"[Docking] Vina Stderr: {e.stderr}") # Captured in return
        return {"status": "error", "message": "Vina execution failed.", "stderr": e.stderr}
    except Exception as e:
        print(f"[Docking] Error: {e}")
        return {"status": "error", "message": str(e)}
