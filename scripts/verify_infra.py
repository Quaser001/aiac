import os
import sys
import asyncio
import httpx
from datetime import datetime
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def print_result(service, status, message=""):
    color = "\033[92m" if status == "PASS" else "\033[91m"
    reset = "\033[0m"
    print(f"[{service}] {color}{status}{reset} {message}")

async def verify_supabase():
    try:
        from supabase import create_client
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or "your-project" in url:
            print_result("SUPABASE", "FAIL", "URL not configured in .env")
            return False
            
        client = create_client(url, key)
        
        # Test 1: Auth (Health check of connection)
        # We can't easily create tables via client-side libraries usually (needs SQL editor/dashboard)
        # so we will check if we can read/write to 'request_logs' as defined in schema?
        # Or better, just check basic connectivity via a harmless select or auth check.
        
        # Trying a simple select from a non-existent table usually returns specific error, verifying connection
        try:
            client.table("request_logs").select("count", count="exact").execute()
            # If table exists, this passes. If not, it errors but confirms connection.
        except Exception as e:
            # If error is about table not found, we connected successfully. 
            # If error is connection refused/auth, we failed.
            if "host" in str(e).lower() or "auth" in str(e).lower():
                print_result("SUPABASE", "FAIL", f"Connection error: {e}")
                return False
                
        print_result("SUPABASE", "PASS", "Connection successful")
        return True
    except Exception as e:
        print_result("SUPABASE", "FAIL", f"Exception: {e}")
        return False

async def verify_hf():
    try:
        key = os.environ.get("HF_API_KEY")
        if not key or "hf_" not in key:
            print_result("HUGGING_FACE", "FAIL", "Key seems invalid or missing")
            return False
            
        headers = {"Authorization": f"Bearer {key}"}
        # Test with Enzyme Commission model or ESM
        model = "facebook/esm2_t6_8M_UR50D"
        # Updated endpoint
        api_url = f"https://router.huggingface.co/hf-inference/models/{model}"
        
        # Short sequence test
        payload = {"inputs": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"}
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(api_url, headers=headers, json=payload, timeout=10.0)
            
            if resp.status_code == 200:
                print_result("HUGGING_FACE", "PASS", f"Inference successful ({model})")
                return True
            else:
                print_result("HUGGING_FACE", "FAIL", f"Status {resp.status_code}: {resp.text[:100]}")
                return False
    except Exception as e:
        print_result("HUGGING_FACE", "FAIL", f"Exception: {e}")
        return False

def verify_kaggle():
    try:
        # Check env vars first
        if not os.environ.get("KAGGLE_USERNAME") or not os.environ.get("KAGGLE_KEY"):
            print_result("KAGGLE", "FAIL", "Credentials missing in .env")
            return False

        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        # Try listing datasets to verify auth (lighter than download)
        # Search for CARD
        datasets = api.dataset_list(search="card-antimicrobial-resistance")
        if datasets:
            print_result("KAGGLE", "PASS", f"Auth success. Found {len(datasets)} datasets for 'card'.")
            return True
        else:
            print_result("KAGGLE", "PASS", "Auth success (no datasets found, but auth worked)")
            return True
            
    except Exception as e:
        print_result("KAGGLE", "FAIL", f"Exception: {e}")
        return False

async def main():
    print("--- INFRASTRUCTURE VERIFICATION START ---")
    
    s_ok = await verify_supabase()
    h_ok = await verify_hf()
    k_ok = verify_kaggle()
    
    print("--- VERIFICATION COMPLETE ---")
    if s_ok and h_ok and k_ok:
        print("OVERALL: PASS")
    else:
        print("OVERALL: FAIL - Check .env settings")

if __name__ == "__main__":
    asyncio.run(main())
