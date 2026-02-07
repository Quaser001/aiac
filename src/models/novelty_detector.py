
import os
import json
import requests
import numpy as np
import hashlib
from typing import List, Dict, Optional, Any
from src.models.mutation_impact import MutationImpactScorer

class NoveltyDetector:
    def __init__(self, 
                 ref_bank_path: str = "data/embeddings/reference_bank.json",
                 cache_dir: str = "data/cache/embeddings"):
        self.ref_bank_path = ref_bank_path
        self.cache_dir = cache_dir
        self.reference_embeddings = self._load_reference_bank()
        
        # Reuse scorer for seq loading and API helpers
        self.scorer = MutationImpactScorer()
        
        # Ensure cache exists
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_reference_bank(self) -> List[Dict]:
        if not os.path.exists(self.ref_bank_path):
            return []
        try:
            with open(self.ref_bank_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load reference bank: {e}")
            return []

    def _save_embedding(self, determinant: str, embedding: List[float]):
        # HFClient handles caching now
        pass

    def get_embedding(self, sequence: str, determinant_name: str = None) -> List[float]:
        """
        Get embedding from ESM-2 API via HFClient.
        """
        # Call HF via Singleton Client (it handles NPY cache and Hash cache)
        from src.models.hf_client import HFClient
        client = HFClient()
        embedding = client.get_embedding(sequence, determinant_name=determinant_name)
        
        if embedding:
            return embedding
            
        print("Failed to get embedding for sequence.")
        return []

    def compute_distance(self, vec_a: List[float], vec_b: List[float]) -> float:
        """cosine distance = 1 - cosine_similarity"""
        a = np.array(vec_a)
        b = np.array(vec_b)
        
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 1.0
            
        cos_sim = np.dot(a, b) / (norm_a * norm_b)
        return 1.0 - cos_sim

    def compute_novelty(self, determinant: str) -> Dict:
        # Load sequence
        seq = self.scorer.load_sequence(determinant)
        if not seq:
             return {"error": f"Sequence for {determinant} not found."}
        
        # Pass determinant name to utilize specialized cache loader
        embedding = self.get_embedding(seq, determinant_name=determinant)
        
        if not embedding:
             return {"error": "Failed to generate embedding (HF API Error)."}

        # Compare against reference bank
        min_dist = 1.0
        nearest_ref = "None"
        
        for ref in self.reference_embeddings:
            dist = self.compute_distance(embedding, ref['embedding'])
            if dist < min_dist:
                min_dist = dist
                nearest_ref = ref['determinant']
        
        # Normalize/Scale score for UX (Cosine dist is 0..2 usually, but we want 0..1ish)
        # 0.0 distance = 0.0 score (Known)
        # 0.2 distance = 0.5 score
        # 0.5 distance = 1.0 score
        
        novelty_score = min(1.0, min_dist * 2.5) # Scaling factor for sensitivity
        
        # Categorize
        if novelty_score < 0.3:
            category = "Known-like"
            explanation = f"Sequence is very similar to known {nearest_ref} cluster."
        elif novelty_score < 0.7:
            category = "Moderately Unusual"
            explanation = f"Distinguishable from {nearest_ref}, potential variant."
        else:
            category = "High Novelty"
            explanation = "Out-of-distribution. Distinct from current reference bank."

        return {
            "determinant": determinant,
            "novelty_score": round(novelty_score, 3),
            "category": category,
            "explanation": explanation,
            "disclaimer": "Surveillance prioritization only. Genetic distance metric."
        }
