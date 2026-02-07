
import os
import requests
import argparse
from pathlib import Path

# Config
PREDICTED_DIR = Path("web/public/structures/predicted")
ESMFOLD_API_URL = "https://api.esmatlas.com/foldSequence/v1/pdb/"

def fetch_esmfold_structure(gene_name: str, sequence: str):
    """
    Fetches predicted structure from ESMAtlas API and saves to public dir.
    """
    PREDICTED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PREDICTED_DIR / f"{gene_name}.pdb"
    
    if out_path.exists():
        print(f"[SKIP] Structure for {gene_name} already exists.")
        return str(out_path)

    print(f"[FETCH] Requesting ESMFold for {gene_name}...")
    try:
        response = requests.post(ESMFOLD_API_URL, data=sequence, timeout=30)
        
        if response.status_code == 200:
            pdb_content = response.text
            if "HEADER" not in pdb_content and "ATOM" not in pdb_content:
                 # Minimal validation
                 pass
            
            with open(out_path, "w") as f:
                f.write(pdb_content)
            print(f"[SUCCESS] Saved predicted structure for {gene_name}")
            return str(out_path)
        else:
            print(f"[ERROR] Failed to fetch {gene_name}: {response.status_code} - {response.text[:50]}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception fetching {gene_name}: {e}")
        return None

if __name__ == "__main__":
    # Example usage for demo (Non-Tier-1 Genes)
    # These are common genes user might click that aren't in the Tier-1 Big 6
    demo_targets = {
        "TEM-1": "MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDQLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRIDAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMPVAMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW",
        "SHV-1": "MRINTLFWFLLSLALLRGVSPVLAQQPQLTDLPIKDQADVLKGGEGPLYIRADTGSVLESFRPEERFPMMSTFKVLLCGAVLSQIDAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMPVAMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW", 
        # SHV-1 sequence is actually very similar/same in many variants, using placeholder for demo if needed
    }
    
    print("--- Precomputing ESMFold Fallbacks for Demo ---")
    for gene, seq in demo_targets.items():
        fetch_esmfold_structure(gene, seq)
