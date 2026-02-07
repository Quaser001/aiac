
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.novelty_detector import NoveltyDetector

router = APIRouter(
    prefix="/novelty",
    tags=["novelty"],
    responses={404: {"description": "Not found"}},
)

detector = NoveltyDetector()

class NoveltyRequest(BaseModel):
    determinant: str

class NoveltyResponse(BaseModel):
    determinant: str
    novelty_score: float
    category: str
    explanation: str
    disclaimer: str

@router.post("/score", response_model=NoveltyResponse)
async def get_novelty_score(request: NoveltyRequest):
    """
    Computes a novelty score (Out-of-Distribution) for a resistance determinant.
    """
    result = detector.compute_novelty(request.determinant)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result
