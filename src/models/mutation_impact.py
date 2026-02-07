
import os
import requests
import json
from enum import Enum
from Bio import SeqIO
from typing import Optional, Dict, Tuple, List

class ImpactLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class MutationImpactScorer:
    def __init__(self, model_id: str = "facebook/esm2_t6_8M_UR50D"):
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
        self.api_key = os.getenv("HF_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def load_sequence(self, determinant: str) -> Optional[str]:
        """
        Loads the protein sequence for a given determinant.
        Uses Tier-1 sequence cache for Big 6 determinants.
        """
        # Tier-1 Determinants - use new structured cache
        tier1_determinants = ["NDM-1", "KPC-2", "CTX-M-15", "OXA-48", "mecA", "vanA"]
        
        if determinant in tier1_determinants:
            tier1_path = f"data/tier1/sequences/{determinant}.fasta"
            if os.path.exists(tier1_path):
                try:
                    record = SeqIO.read(tier1_path, "fasta")
                    return str(record.seq)
                except Exception as e:
                    print(f"Error loading Tier-1 sequence: {e}")
        
        # Fallback: Legacy mapping
        mapping = {
            "NDM-1": "data/sequences/ndm1.fasta",
        }
        
        file_path = mapping.get(determinant.upper())
        if not file_path or not os.path.exists(file_path):
            # Fallback for demo: if file not found, try to look in data/sequences directly
            potential_path = f"data/sequences/{determinant.lower()}.fasta"
            if os.path.exists(potential_path):
                file_path = potential_path
            else:
                return None

        try:
            record = SeqIO.read(file_path, "fasta")
            return str(record.seq)
        except Exception as e:
            print(f"Error loading sequence: {e}")
            return None

    def parse_mutation(self, mutation_str: str) -> Optional[Tuple[str, int, str]]:
        """
        Parses a mutation string like 'H122Y' into (wt, pos, mut).
        Returns None if invalid format.
        """
        try:
            wt = mutation_str[0]
            mut = mutation_str[-1]
            pos = int(mutation_str[1:-1])
            return wt, pos, mut
        except (ValueError, IndexError):
            return None

    # Removed call_hf_esm2 (Converted to Embedding Distance Logic)

    def list_available_mutations(self, determinant: str) -> List[str]:
        """
        Lists available mutation variants for a determinant by checking the cache.
        Returns sorted list of mutation codes (e.g. ['H122Y', 'K211R']).
        """
        cache_dir = "data/cache/embeddings"
        variants = []
        
        if not os.path.exists(cache_dir):
            return []
            
        prefix = f"{determinant}_"
        
        try:
            for filename in os.listdir(cache_dir):
                if filename.startswith(prefix) and filename.endswith(".npy"):
                    # Extract mutation: NDM-1_H122Y.npy -> H122Y
                    # filename[len(prefix):-4]
                    mutation = filename[len(prefix):-4]
                    if mutation:
                        variants.append(mutation)
        except Exception as e:
            print(f"Error listing mutations: {e}")
            
        return sorted(variants)

    def calculate_score(self, determinant: str, mutation_str: str) -> Dict:
        """
        Main entry point to get the impact score.
        Uses offline embedding distance (WT vs Mutant).
        """
        import numpy as np
        
        # 1. Load Wildtype Sequence
        sequence = self.load_sequence(determinant)
        if not sequence:
            return {"error": "Sequence not found"}

        # 2. Parse Mutation
        parsed = self.parse_mutation(mutation_str)
        if not parsed:
            return {"error": "Invalid mutation format"}
        
        wt, pos, mut = parsed
        
        # Validate position (1-indexed)
        if pos < 1 or pos > len(sequence):
             return {"error": f"Position {pos} out of range (1-{len(sequence)})"}

        # Validate wild-type
        actual_wt = sequence[pos-1]
        if actual_wt != wt:
            return {"error": f"Sequence mismatch: Expected {wt} at {pos}, found {actual_wt}"}

        # 3. Generate Mutant Sequence
        # Strings are immutable, so use slicing
        mutant_seq = sequence[:pos-1] + mut + sequence[pos:]

        # 4. Get Embeddings (Offline/Cached via HFClient)
        from src.models.hf_client import HFClient
        client = HFClient()

        # Get WT Embedding (pass determinant name to check .npy cache)
        wt_emb_list = client.get_embedding(sequence, determinant_name=determinant)
        
        # Get Mutant Embedding
        # Strict Mode: Require precomputed cache for mutants
        mutant_key = f"{determinant}_{mutation_str}"
        cache_path = f"data/cache/embeddings/{mutant_key}.npy"
        
        if not os.path.exists(cache_path):
             # Return specific error for UI to display warning
             return {"error": "Mutant embedding not precomputed"}
             
        mut_emb_list = client.get_embedding(mutant_seq, determinant_name=mutant_key)
        
        if not wt_emb_list or not mut_emb_list:
             return {"error": "Failed to generate embeddings"}

        # 5. Compute Cosine Distance
        a = np.array(wt_emb_list)
        b = np.array(mut_emb_list)
        
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            dist = 0.0
        else:
            cos_sim = np.dot(a, b) / (norm_a * norm_b)
            dist = 1.0 - cos_sim
            
        # 6. Interpret Distance as Impact
        # Distance 0.0 = Identical
        # Distance > 0.0 = Functional Shift
        # For synthetic random vectors, distance is ~0.2-0.3 usually.
        # We scale it to be visible.
        
        impact_score = min(1.0, dist * 3.0) 
        
        return self._format_result(determinant, mutation_str, impact_score)

    def _format_result(self, determinant: str, mutation: str, score: float) -> Dict:
        if score < 0.3:
            risk = ImpactLevel.LOW
            interpretation = "Likely tolerated."
        elif score < 0.7:
            risk = ImpactLevel.MEDIUM
            interpretation = "Potential functional change."
        else:
            risk = ImpactLevel.HIGH
            interpretation = "Likely functional disruption."
            
        return {
            "determinant": determinant,
            "mutation": mutation,
            "impact_score": round(score, 3),
            "risk_level": risk.value,
            "interpretation": interpretation,
            "disclaimer": "Research support only. Not for clinical use."
        }
