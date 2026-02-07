
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.system.mode import system_mode

router = APIRouter(
    prefix="/system",
    tags=["System Control"],
    responses={404: {"description": "Not found"}},
)

class ModeRequest(BaseModel):
    mode: str

@router.get("/mode")
async def get_mode():
    return {
        "mode": system_mode.mode,
        "tier1_policy": "live execution enabled" if system_mode.is_online else "cached demo only"
    }

@router.post("/mode")
async def set_mode(request: ModeRequest):
    if request.mode.lower() not in ["online", "offline"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'online' or 'offline'.")
    
    system_mode.set_mode(request.mode)
    return {
        "mode": system_mode.mode,
        "message": f"System switched to {system_mode.mode.upper()} mode."
    }
