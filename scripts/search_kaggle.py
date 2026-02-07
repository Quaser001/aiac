import os
import sys

# Set Credentials from Task Context
os.environ['KAGGLE_USERNAME'] = 'killergoat'
os.environ['KAGGLE_KEY'] = 'KGAT_99d9b9cd87a5a48ab9336427ffeb8605'

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except ImportError:
    print("Kaggle not installed. Please pip install kaggle")
    sys.exit(1)

def search():
    api = KaggleApi()
    api.authenticate()
    
    print("Searching for datasets...")
    datasets = api.dataset_list(search="antibiotic resistance", sort_by="votes", page=1)
    
    print(f"Found {len(datasets)} datasets.")
    
    results = []
    for d in datasets[:10]:
        print(f"Ref: {d.ref}")
        print(f"Title: {d.title}")
        print("-" * 30)
        results.append({"ref": d.ref, "title": d.title})
        
    import json
    with open('kaggle_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    search()
