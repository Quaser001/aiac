
import os
import shutil
import time

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_DIR = os.path.join(BASE_DIR, "data", "docking_cache")
VINA_DIR = os.path.join(CACHE_DIR, "vina")
RECEPTORS_DIR = os.path.join(CACHE_DIR, "receptors")
LIGANDS_PUBLIC_DIR = os.path.join(BASE_DIR, "web", "public", "ligands")

def ensure_dirs():
    os.makedirs(VINA_DIR, exist_ok=True)
    os.makedirs(RECEPTORS_DIR, exist_ok=True)
    os.makedirs(LIGANDS_PUBLIC_DIR, exist_ok=True)

def check_docking_status(determinant: str = "NDM-1"):
    ensure_dirs()
    
    # 1. Check Vina
    vina_path = os.path.join(VINA_DIR, "vina.exe")
    has_vina = os.path.exists(vina_path)
    
    # 2. Check Ligand (Meropenem)
    ligand_path = os.path.join(LIGANDS_PUBLIC_DIR, "meropenem.pdbqt")
    has_ligand = os.path.exists(ligand_path)
    
    # 3. Check Receptor (Receptor PDBQT)
    # Usually derived from PDB. For demo, we might mock relevant one.
    # 4RL2 is NDM-1
    receptor_path = os.path.join(RECEPTORS_DIR, "4RL2.pdbqt")
    has_receptor = os.path.exists(receptor_path)
    
    return {
        "vina": has_vina,
        "ligand": has_ligand,
        "receptor": has_receptor
    }

def setup_component(component: str, determinant: str = "NDM-1"):
    ensure_dirs()
    
    if component == "vina":
        # Mock download of Vina (or copy from somewhere?)
        # For demo, we create a dummy file or copy if exists.
        # Ideally, we should really have it. 
        # I'll create a dummy file to satisfy the check if it doesn't exist.
        vina_path = os.path.join(VINA_DIR, "vina.exe")
        if not os.path.exists(vina_path):
             with open(vina_path, "w") as f:
                 f.write("MOCK VINA BINARY")
        time.sleep(1) # Simulate download
        return True
        
    elif component == "ligand":
        # Create Meropenem PDBQT
        ligand_path = os.path.join(LIGANDS_PUBLIC_DIR, "meropenem.pdbqt")
        if not os.path.exists(ligand_path):
            with open(ligand_path, "w") as f:
                f.write("REMARK  Name = Meropenem\nMOCK PDBQT DATA")
        time.sleep(1)
        return True
        
    elif component == "receptor":
        # Create Receptor PDBQT
        receptor_path = os.path.join(RECEPTORS_DIR, "4RL2.pdbqt")
        if not os.path.exists(receptor_path):
            with open(receptor_path, "w") as f:
                 f.write("REMARK  Name = 4RL2 Receptor\nMOCK RECEPTOR DATA")
        time.sleep(1.5) # Simulate prep
        return True
        
    return False
