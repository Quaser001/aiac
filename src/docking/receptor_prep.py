import os
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_DIR = os.path.join(BASE_DIR, "data", "docking_cache", "receptors")
PUBLIC_STRUCT_DIR = os.path.join(BASE_DIR, "web", "public", "structures")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_receptor(pdb_id: str) -> str:
    """
    Converts cached PDB to PDBQT using OpenBabel.
    Returns path to PDBQT or None on failure.
    """
    ensure_dir(CACHE_DIR)
    pdb_path = os.path.join(PUBLIC_STRUCT_DIR, f"{pdb_id}.pdb")
    pdbqt_path = os.path.join(CACHE_DIR, f"{pdb_id}.pdbqt")

    if os.path.exists(pdbqt_path):
        return pdbqt_path
    
    if not os.path.exists(pdb_path):
        print(f"[Receptor] PDB {pdb_id} source not found.")
        return None

    # Strict Conversion
    print(f"[Receptor] Converting {pdb_id} to PDBQT...")
    try:
        subprocess.run(["obabel", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Simple conversion - remove waters, add hydrogens implicit in default
        subprocess.run([
            "obabel", pdb_path, "-O", pdbqt_path, "-xr" # -xr to preserve rigid? Standard: just -O
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if os.path.exists(pdbqt_path):
            return pdbqt_path
            
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[Receptor] OpenBabel missing. Attempting standard fallback conversion...")
        try:
             from src.docking.simple_pdbqt import pdb_to_pdbqt
             success = pdb_to_pdbqt(pdb_path, pdbqt_path)
             if success and os.path.exists(pdbqt_path):
                 print(f"[Receptor] Fallback successful.")
                 return pdbqt_path
        except Exception as e:
             print(f"[Receptor] Fallback error: {e}")
        
        return None

    return None
