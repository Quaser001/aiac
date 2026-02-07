import requests
import json

try:
    # Test Health
    print("Testing Health...")
    r = requests.get("http://localhost:8000/health")
    print(f"Health: {r.status_code} {r.text}")

    # Test Specialist Analysis
    print("\nTesting Specialist Analysis...")
    payload = {
        "gene_id": "NDM-1",
        "family": "Unknown",
        "organism_context": "Klebsiella pneumoniae"
    }
    r = requests.post("http://localhost:8000/specialist/analyze/mechanism", json=payload)
    print(f"Analysis: {r.status_code}")
    print(r.text[:500]) # Print first 500 chars

except Exception as e:
    print(f"FAILED: {e}")
