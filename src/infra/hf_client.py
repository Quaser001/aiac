import os
import httpx
import json
import hashlib
from typing import Dict, Any, Optional
from pathlib import Path

# Global in-memory flag for runtime toggling
LIVE_INFERENCE_ENABLED = os.getenv("ABRISK_LIVE_INFERENCE", "false").lower() == "true"

class HFClient:
    """
    Client for interacting with Hugging Face Inference API.
    Used for frozen protein language model embedding/inference.
    Supports OFFLINE CACHING for deterministic demos.
    """
    def __init__(self):
        self.api_key = os.environ.get("HF_API_KEY")
        self.api_url = "https://router.huggingface.co/hf-inference/models"
        self.cache_dir = Path("data/cache/embeddings")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            print("Warning: HF_API_KEY not set. Running in MOCK/CACHE-ONLY mode.")

    def _get_cache_path(self, sequence: str, model: str) -> Path:
        """Generate a deterministic cache key."""
        seq_hash = hashlib.md5(f"{model}:{sequence}".encode()).hexdigest()
        return self.cache_dir / f"{seq_hash}.json"

    async def get_embedding(self, sequence: str, model: str = "facebook/esm2_t6_8M_UR50D") -> Optional[Dict[str, Any]]:
        """
        Get embeddings for a protein sequence.
        Logic:
        1. Check Cache (Always preferred for speed/stability)
        2. If Missing:
           - If LIVE_INFERENCE_ENABLED: Call HF API and Cache result
           - If DISABLED: Return None or Mock (Conference Safety)
        """
        # 1. Check Cache
        cache_path = self._get_cache_path(sequence, model)
        if cache_path.exists():
            print(f"[HF Cache] Hit for {sequence[:10]}...")
            try:
                with open(cache_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[HF Cache] Read error: {e}")

        # 2. Check Mode
        if not LIVE_INFERENCE_ENABLED:
            print(f"[HF Offline] Cache miss for {sequence[:10]}... and Live Inference is DISABLED.")
            # Conference Safety: Do not return random mocks for specific sequences (Tier-1 usually cached)
            return {"mock": True, "error": "Offline Mode: Variant not cached", "embedding": []}

        # 3. Live Inference
        if not self.api_key:
            print(f"[HF Mock] Missing API Key. Returning explicit error.")
            return {"mock": True, "error": "Live inference unavailable (No API Key)", "embedding": []}

        print(f"[HF Live] Calling API for {sequence[:10]}...")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": sequence}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_url}/{model}", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Cache success
                with open(cache_path, "w") as f:
                    json.dump(data, f)
                    
                return data
        except Exception as e:
            print(f"Error calling HF API: {e}")
            return None

def set_live_inference(enabled: bool):
    global LIVE_INFERENCE_ENABLED
    LIVE_INFERENCE_ENABLED = enabled
    print(f"SYSTEM MODE UPDATE: Live Inference set to {LIVE_INFERENCE_ENABLED}")

