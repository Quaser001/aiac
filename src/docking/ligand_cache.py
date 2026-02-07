import os
import requests
import subprocess
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLIC_LIGAND_DIR = os.path.join(BASE_DIR, "web", "public", "ligands")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_ligand(name: str, cid: str) -> str:
    """
    Fetches ligand SDF from PubChem and converts to PDBQT using OpenBabel.
    Returns path to PDBQT file or None if failed.
    """
    ensure_dir(PUBLIC_LIGAND_DIR)
    sdf_path = os.path.join(PUBLIC_LIGAND_DIR, f"{name}.sdf")
    pdbqt_path = os.path.join(PUBLIC_LIGAND_DIR, f"{name}.pdbqt")

    # 1. Check Cache
    if os.path.exists(pdbqt_path):
        return pdbqt_path

    # 2. Fetch SDF
    if not os.path.exists(sdf_path):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/SDF"
        print(f"[Ligand] Downloading {name} (CID {cid}) from PubChem...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(sdf_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"[Ligand] PubChem Failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"[Ligand] Download Error: {e}")
            return None

    # 3. Convert to PDBQT (Strict Dependency)
    try:
        # Verify obabel exists
        subprocess.run(["obabel", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"[Ligand] Converting {name} to PDBQT...")
        subprocess.run([
            "obabel", sdf_path, "-O", pdbqt_path, "--gen3d"
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if os.path.exists(pdbqt_path):
            return pdbqt_path
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"[Ligand] OpenBabel not found. Attempting native fallback...")
        try:
            from src.docking.simple_pdbqt import sdf_to_pdbqt
            success = sdf_to_pdbqt(sdf_path, pdbqt_path)
            if success and os.path.exists(pdbqt_path):
                print(f"[Ligand] Native fallback successful.")
                return pdbqt_path
            else:
                 print(f"[Ligand] Native fallback failed.")
        except Exception as e:
            print(f"[Ligand] Fallback Error: {e}")
            
        return None
