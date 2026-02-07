import os
import sys
import pandas as pd
import shutil

# Set Credentials
os.environ['KAGGLE_USERNAME'] = 'killergoat'
os.environ['KAGGLE_KEY'] = 'KGAT_99d9b9cd87a5a48ab9336427ffeb8605'

from kaggle.api.kaggle_api_extended import KaggleApi

CANDIDATES = [
    'adilimadeddinehosni/multi-resistance-antibiotic-susceptibility',
]

DOWNLOAD_DIR = 'data/phenotypes_raw'

def inspect_data():
    api = KaggleApi()
    api.authenticate()
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    for dataset in CANDIDATES:
        print(f"DTOI: Trying {dataset}...")
        try:
            # Clean dir first
            for filename in os.listdir(DOWNLOAD_DIR):
                file_path = os.path.join(DOWNLOAD_DIR, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

            api.dataset_download_files(dataset, path=DOWNLOAD_DIR, unzip=True)
            print(f"SUCCESS: Downloaded {dataset} to {DOWNLOAD_DIR}")
            
            # Find CSVs
            csv_files = []
            for root, dirs, files in os.walk(DOWNLOAD_DIR):
                for f in files:
                    if f.endswith('.csv') or f.endswith('.txt'): # Check txt too just in case
                        csv_files.append(os.path.join(root, f))
            
            if not csv_files:
                print("No CSV or TXT files found.")
                continue

            for csv_file in csv_files:
                print(f"\n--- Inspecting: {csv_file} ---")
                try:
                    df = pd.read_csv(csv_file)
                    print(f"Columns: {df.columns.tolist()}")
                    print(f"Shape: {df.shape}")
                    print(f"Head: \n{df.head()}")
                except Exception as e:
                     print(f"Could not read with pandas: {e}")
                
            return # Stop after first success
            
        except Exception as e:
            print(f"FAILED {dataset}: {e}")

if __name__ == "__main__":
    inspect_data()
