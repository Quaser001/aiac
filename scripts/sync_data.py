import os
import sys
from dotenv import load_dotenv

# Load env vars FIRST
load_dotenv()

from kaggle.api.kaggle_api_extended import KaggleApi

def sync_card_dataset():
    print("--- INITIATING KAGGLE SYNC ---")
    
    # 1. Auth Debug
    u = os.environ.get("KAGGLE_USERNAME")
    k = os.environ.get("KAGGLE_KEY")
    print(f"DEBUG: Username={'Found' if u else 'Missing'}, Key={'Found' if k else 'Missing'}")

    if not u or not k:
        print("Error: KAGGLE credentials missing from .env")
        sys.exit(1)
        
    try:
        api = KaggleApi()
        api.authenticate()
        print("✓ Authenticated with Kaggle")
    except Exception as e:
        print(f"Error during authentication: {e}")
        # Assuming warning about json file might print to stderr but not raise if env vars valid
        # If it raises, we exit.
        sys.exit(1)

    # 2. Search for CARD
    # We look for a dataset that looks authoritative. 
    # For this environment, we will search for 'card antimicrobial' and pick the most relevant one
    # or a specific known slug if available.
    datasets = api.dataset_list(search="card-antimicrobial-resistance")
    
    target_dataset = None
    for d in datasets:
        # Prefer one with clear naming
        if "card" in d.ref.lower():
            target_dataset = d.ref
            break
    
    if not target_dataset:
        # Fallback search
        datasets = api.dataset_list(search="antibiotic resistance card")
        if datasets:
            target_dataset = datasets[0].ref

    if not target_dataset:
        print("Error: Could not find a suitable CARD dataset on Kaggle.")
        sys.exit(1)

    print(f"✓ Found dataset: {target_dataset}")

    # 3. Download
    download_path = os.path.join(os.getcwd(), "data", "raw")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    print(f"Downloading to: {download_path} ...")
    api.dataset_download_files(target_dataset, path=download_path, unzip=True)
    
    # 4. Verify
    files = os.listdir(download_path)
    print(f"✓ Download complete. Files: {files}")
    
    # Create a manifest
    with open(os.path.join(download_path, "manifest.json"), "w") as f:
        f.write(f'{{"source": "{target_dataset}", "files": {str(files)}}}')

if __name__ == "__main__":
    sync_card_dataset()
