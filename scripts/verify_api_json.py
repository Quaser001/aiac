import requests
import json

base_url = "http://localhost:8000"

def test_search():
    print("--- 1. Search Endpoint (/specialist/genes/search?query=MDM) ---")
    try:
        # User asked for 'ndm' case insensitive
        r = requests.get(f"{base_url}/specialist/genes/search", params={"query": "ndm"})
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

def test_analyze():
    print("\n--- 2. Analysis Endpoint (/specialist/analyze/mechanism) ---")
    payload = {
        "gene_id": "NDM-1",
        "organism_context": "Klebsiella pneumoniae"
    }
    try:
        r = requests.post(f"{base_url}/specialist/analyze/mechanism", json=payload)
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
    test_analyze()
