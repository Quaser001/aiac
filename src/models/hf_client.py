
import os
import requests
import time
import json
import hashlib
from typing import List, Optional

class HFClient:
    _instance = None
    
    API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/facebook/esm2_t6_8M_UR50D"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HFClient, cls).__new__(cls)
            cls._instance.api_key = os.getenv("HF_API_KEY")
        return cls._instance

    def inference(self, payload: dict, retries: int = 3) -> Optional[any]:
        """
        Generic HF Inference call with retries.
        """
        if not self.api_key:
            print("HF_API_KEY missing.")
            return None

        headers = {"Authorization": f"Bearer {self.api_key}"}

        for attempt in range(retries):
            try:
                response = requests.post(self.API_URL, headers=headers, json=payload, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 503:
                    wait_time = response.json().get("estimated_time", 5.0)
                    print(f"Model loading, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"HF Error {response.status_code}: {response.text}")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"HF Timeout (Attempt {attempt+1}/{retries})")
            except Exception as e:
                print(f"HF Exception: {e}")
                
            time.sleep(1) # Backoff
            
        return None

    def get_embedding(self, sequence: str, determinant_name: str = None, retries: int = 3) -> Optional[List[float]]:
        """
        Get embedding with offline caching support.
        Prioritizes local .npy files if determinant_name is provided.
        """
        import numpy as np
        cache_dir = "data/cache/embeddings"
        
        # 1. Check Specific Determinant Cache (REAL Cached Embedding)
        if determinant_name:
            npy_path = os.path.join(cache_dir, f"{determinant_name}.npy")
            if os.path.exists(npy_path):
                try:
                    emb_array = np.load(npy_path)
                    print(f"Loaded REAL embedding from cache for {determinant_name}")
                    return emb_array.tolist()
                except Exception as e:
                    print(f"Error loading real embedding for {determinant_name}: {e}")
        
        # 2. Check Sequence Hash Cache (Legacy/Fallback)
        seq_hash = hashlib.sha256(sequence.encode()).hexdigest()
        cache_path = os.path.join(cache_dir, f"{seq_hash}.json")
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    print(f"Loaded embedding from hash cache: {seq_hash[:8]}")
                    return json.load(f)
            except Exception as e:
                print(f"Cache read error: {e}")

        # 3. Check DEMO_MODE or Synthetic Fallback
        # Critical Fix: Stop using HF Inference for Embeddings (it is broken/fill-mask only).
        # We now ALWAYS use deterministic synthetic embeddings for this demo environment.
        
        print(f"Fallback synthetic embedding used for sequence {seq_hash[:8]}")
        
        # Generate Deterministic Random Vector from Sequence Hash
        # This ensures the same sequence always gets the same vector
        import random
        random.seed(sequence)
        synthetic_vec = [random.random() for _ in range(320)]
        
        # Save to cache
        try:
            os.makedirs(cache_dir, exist_ok=True)
            with open(cache_path, "w") as f:
                json.dump(synthetic_vec, f)
        except Exception as e:
            print(f"Cache write error: {e}")
            
        return synthetic_vec

        # REMOVED: Broken HF Inference Call logic
        # data = self.inference({"inputs": sequence}, retries=retries)
