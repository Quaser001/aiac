from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from src.structural.pdb_cache import PDBCache

router = APIRouter(
    prefix="/structure",
    tags=["Structural Context (Layer 3)"],
    responses={404: {"description": "Not found"}},
)

# Initialize Cache
pdb_cache = PDBCache()

class DownloadRequest(BaseModel):
    determinant: str

@router.get("/{determinant}")
async def get_structure(determinant: str):
    """
    LAYER 3: Structural Context.
    Checks PDB availability for a determinant.
    Returns {status: 'ready'|'missing'|'unavailable'}.
    """
    # 1. Get PDB ID
    pdb_id = pdb_cache.get_pdb_id(determinant)
    
    if not pdb_id:
        return {"status": "unavailable", "message": "No PDB mapped"}
        
    # 2. Check Cache Status
    result = pdb_cache.check_status(pdb_id)
    return result

@router.post("/download")
async def download_structure(request: DownloadRequest):
    """
    Triggers download of PDB asset from RCSB.
    """
    pdb_id = pdb_cache.get_pdb_id(request.determinant)
    
    if not pdb_id:
        raise HTTPException(status_code=404, detail="No PDB ID found")
        
    path = pdb_cache.ensure_cached(pdb_id)
    if path:
        return {"status": "ready", "path": f"/structures/{pdb_id}.pdb"}
    
    raise HTTPException(status_code=500, detail="Failed to download PDB")
