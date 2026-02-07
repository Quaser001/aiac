import requests
import json

def test_api():
    url = "http://localhost:8000/specialist/analyze/mechanism"
    payload = {"gene_id": "NDM-1", "family": "Metallo-beta-lactamase"}
    
    print(f"POST {url}")
    print(f"Payload: {payload}")
    
    try:
        resp = requests.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print("\n--- API RESPONSE ---")
            print(json.dumps(data, indent=2))
            
            # Validation
            mech = data["mechanism"]["mechanism_class"]
            if "inactivation" in mech or "lactamase" in mech:
                print(f"\n[PASS] Mechanism correctly identified as: {mech}")
            else:
                print(f"\n[FAIL] Unexpected mechanism: {mech}")
        else:
            print(f"Error: {resp.text}")
            
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Ensure server is running (python -m uvicorn ...)")

if __name__ == "__main__":
    test_api()
