
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, Dict, Any
from pydantic import BaseModel
from src.models.mutation_impact import MutationImpactScorer

router = APIRouter(
    prefix="/mutation",
    tags=["mutation"],
    responses={404: {"description": "Not found"}},
)

scorer = MutationImpactScorer()

class MutationRequest(BaseModel):
    determinant: str
    mutation: str

class MutationResponse(BaseModel):
    determinant: str
    mutation: str
    impact_score: float
    risk_level: str
    interpretation: str
    saprot: Optional[Dict[str, Any]] = None
    disclaimer: str

@router.get("/variants")
async def list_variants(determinant: str):
    """
    Lists precomputed mutation variants for a given determinant.
    """
    variants = scorer.list_available_mutations(determinant)
    return {
        "determinant": determinant,
        "variants": variants
    }

@router.post("/impact", response_model=MutationResponse)
async def get_mutation_impact(request: MutationRequest):
    """
    Calculates the functional impact of a point mutation using ESM-2 (Sequence) + SaProt (Structure).
    """
    # 1. Check System Mode / Tier-1
    from src.system.mode import system_mode
    from src.ai.esm1v_scorer import Esm1vScorer
    
    tier1_determinants = ["NDM-1", "KPC-2", "OXA-48", "CTX-M-15", "mecA", "vanA"]
    
    if request.determinant in tier1_determinants:
        # Tier-1 Path: Use ESM-1v (Live or Cached)
        esm_scorer = Esm1vScorer()
        
        # Load real Tier-1 sequence from cache
        import os
        from Bio import SeqIO
        tier1_seq_path = f"data/tier1/sequences/{request.determinant}.fasta"
        tier1_sequence = ""
        if os.path.exists(tier1_seq_path):
            try:
                record = SeqIO.read(tier1_seq_path, "fasta")
                tier1_sequence = str(record.seq)
            except Exception as e:
                print(f"[Tier-1] Failed to load sequence: {e}")
        
        if not tier1_sequence:
            # Fallback to legacy path
            tier1_sequence = "MOCK_FALLBACK"  # Will trigger cache lookup in scorer
        
        esm_result = esm_scorer.get_score(request.determinant, request.mutation, sequence=tier1_sequence)
        
        if esm_result.get("status") == "success":
             # Use ESM output as primary
             result = {
                 "determinant": request.determinant,
                 "mutation": request.mutation,
                 "impact_score": esm_result.get("esm1v_delta_loglik", 0),
                 "risk_level": esm_result.get("risk_level", "Unknown"),
                 "interpretation": esm_result.get("interpretation", ""),
                 "saprot": {"provenance": esm_result.get("provenance")}, # Re-using slot for badge
                 "disclaimer": "Tier-1 High Confidence Analysis"
             }
             return result
        elif esm_result.get("provenance") == "OFFLINE":
             # Conference Demo Fallback: Return simulated data instead of error
             demo_fallback = {
                 "determinant": request.determinant,
                 "mutation": request.mutation,
                 "impact_score": -2.3,  # Neutral simulated value
                 "risk_level": "Medium",
                 "interpretation": f"Simulated impact for {request.mutation}. Real-time ESM-1v inference available in online mode.",
                 "saprot": {"provenance": "DEMO_FALLBACK"},
                 "disclaimer": "Tier-1 Demo Mode (Offline) - Simulated Score"
             }
             return demo_fallback

    # 2. Legacy/Non-Tier-1 Path (ESM-2 Embedding)
    result = scorer.calculate_score(request.determinant, request.mutation)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # 3. SaProt Score (Only if not Tier-1 override)
    from src.ai.saprot_scorer import SaProtScorer
    saprot = SaProtScorer()
    saprot_data = saprot.get_score(request.determinant, request.mutation)
    
    # Merge results
    result["saprot"] = saprot_data
        
    return result
