
import requests
import sys

BASE_URL = "http://localhost:8000"

def check_endpoint(name, method, endpoint, payload=None):
    print(f"Checking {name} ({endpoint})...", end=" ")
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            res = requests.post(url, json=payload)
        else:
            res = requests.get(url)
            
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            return True, res.json()
        else:
            print(f"  Error: {res.text}")
            return False, res.text
    except Exception as e:
        print(f"  Exception: {e}")
        return False, str(e)

def run_health_check():
    print("=== ABRISK Final API Health Check ===")
    
    # 1. Health/Root
    check_endpoint("Root", "GET", "/")
    
    # 2. Mutation Impact (Requires HF Key usually, expect 200 or 500 with explicit error)
    # If the user has a key in .env, this might work. If not, it should fail GRACEFULLY with "Live mode required"
    success, data = check_endpoint("Mutation Impact", "POST", "/mutation/impact", {
        "determinant": "NDM-1",
        "mutation": "H122Y"
    })
    
    # 3. Novelty (Requires embedding)
    check_endpoint("Novelty", "POST", "/novelty/score", {
        "determinant": "NDM-1"
    })
    
    # 4. Mechanism Prediction
    check_endpoint("Mechanism Predict", "POST", "/mechanism/predict", {
        "sequence": "MKKLL...FAKE..." # Short seq might fail logic but endpoint reachable
    })
    
    # 5. Docking Demo
    check_endpoint("Docking Demo", "POST", "/docking/research-demo", {
        "determinant": "NDM-1",
        "ligand": "Meropenem"
    })
    
    print("\nCheck Complete.")

if __name__ == "__main__":
    run_health_check()
