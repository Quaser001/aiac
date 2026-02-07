import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def audit(name, method, endpoint, payload=None):
    print(f"\n=== AUDIT: {name} ===")
    url = f"{BASE_URL}{endpoint}"
    print(f"Request: {method} {url}")
    try:
        if method == "GET":
            r = requests.get(url)
        else:
            r = requests.post(url, json=payload)
        
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:")
            print(json.dumps(r.json(), indent=2))
        else:
            print("Error Response:")
            print(r.text)
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    print("Starting Phase 20 Final Audit...")
    
    # 1. Search
    audit("Search Determinants", "GET", "/specialist/genes/search?query=ndm")
    
    # 2. Analyze
    audit("Analyze Mechanism", "POST", "/specialist/analyze/mechanism", {
        "gene_id": "NDM-1",
        "family": "Unknown",
        "organism_context": "Klebsiella pneumoniae"
    })
    
    # 3. Structure
    audit("Structure Cache", "GET", "/structure/NDM-1")
    
    # 4. Docking
    audit("Docking Run", "POST", "/docking/run", {
        "determinant": "NDM-1",
        "ligand": "meropenem"
    })
    
    print("\nAudit Complete.")
