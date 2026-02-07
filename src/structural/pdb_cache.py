
import os
import requests
import json

class PDBCache:
    def __init__(self, 
                 map_path: str = "data/structure_map.json",
                 cache_dir: str = "data/structures"):
        self.map_path = map_path
        self.cache_dir = cache_dir
        self.structure_map = self._load_map()
        
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        with open(self.map_path, 'r') as f:
            return json.load(f)

    def get_pdb_id(self, determinant: str) -> str:
        # Default fallback if unknown
        if determinant not in self.structure_map:
            # Fallback to NDM-1 (4RL2) for demo if unknown, or return None?
            # Creating a consistent experience:
            return "4RL2" 
        return self.structure_map[determinant]["pdb_id"]

    def check_status(self, pdb_id: str) -> dict:
        file_path = os.path.join(self.cache_dir, f"{pdb_id}.pdb")
        if os.path.exists(file_path):
            return {"status": "ready", "path": f"/structures/{pdb_id}.pdb"}
        return {"status": "missing", "message": "Structure not cached"}

    def ensure_cached(self, pdb_id: str):
        file_path = os.path.join(self.cache_dir, f"{pdb_id}.pdb")
        if os.path.exists(file_path):
            return file_path
            
        # Download
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        try:
            print(f"Downloading PDB {pdb_id} from {url}...")
            res = requests.get(url)
            if res.status_code == 200:
                with open(file_path, "w") as f:
                    f.write(res.text)
                return file_path
            else:
                print(f"Failed to download PDB {pdb_id}: Status {res.status_code}")
                return None
        except Exception as e:
            print(f"Error downloading PDB: {e}")
            return None

if __name__ == "__main__":
    # Pre-cache seeds
    cache = PDBCache()
    for det, info in cache.structure_map.items():
        cache.ensure_cached(info["pdb_id"])
