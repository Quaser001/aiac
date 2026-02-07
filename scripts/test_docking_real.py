import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from src.docking.run_vina import run_docking_job

def test():
    print("Testing Real Docking Pipeline...")
    # NDM-1 -> 4RL2 (Real PDB should be in cache from previous step? If not, it might fail PDB check too)
    # Ensure PDB is there first (we can use pdb_cache)
    from src.structural.pdb_cache import get_or_download_pdb
    get_or_download_pdb("4RL2")
    
    result = run_docking_job("NDM-1", "meropenem")
    print("\nResult:")
    print(result)
    
    with open("vina_debug_error.txt", "w") as f:
        f.write(str(result))
        if result.get("status") == "error":
             # Try to read the job log if it exists
             try:
                 with open("data/docking_cache/results/NDM-1_meropenem.log", "r") as log:
                     f.write("\n\nVina Log:\n")
                     f.write(log.read())
             except:
                 f.write("\nNo Vina log found.")
                 
        if "stderr" in result:
             f.write("\n\nSTDERR:\n")
             f.write(result["stderr"])

if __name__ == "__main__":
    test()
