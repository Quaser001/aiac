import os
import json
import requests
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP_FILE = os.path.join(BASE_DIR, "src", "structural", "structure_map.json")
PUBLIC_STRUCT_DIR = os.path.join(BASE_DIR, "web", "public", "structures")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    target_path = os.path.join(PUBLIC_STRUCT_DIR, f"{pdb_id}.pdb")
    
    if os.path.exists(target_path):
        print(f"Skipping {pdb_id} (already exists)")
        return True

    print(f"Downloading {pdb_id} from {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(target_path, "wb") as f:
                f.write(response.content)
            print(f"Saved to {target_path}")
            return True
        else:
            print(f"Failed to download {pdb_id}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {pdb_id}: {e}")
        return False

def main():
    ensure_dir(PUBLIC_STRUCT_DIR)
    
    with open(MAP_FILE, "r") as f:
        structure_map = json.load(f)
    
    success_count = 0
    for gene, data in structure_map.items():
        if data.get("source") == "PDB":
            if download_pdb(data["pdb_id"]):
                success_count += 1
    
    print(f"Completed. {success_count}/{len(structure_map)} structures ready.")

if __name__ == "__main__":
    main()
