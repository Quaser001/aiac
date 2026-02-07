from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/docking",
    tags=["Docking Feasibility (Layer 4)"],
    responses={404: {"description": "Not found"}},
)

class DockingRequest(BaseModel):
    determinant: str
    ligand: str

class DockingResponse(BaseModel):
    status: str
    score: float
    unit: str
    pose_file: Optional[str] = None
    disclaimer: str

from src.docking.run_vina import run_docking_job
from src.docking.setup_manager import check_docking_status, setup_component

@router.post("/run", response_model=DockingResponse)
async def run_docking(request: DockingRequest):
    """
    LAYER 4: Docking Feasibility (Research Mode).
    Orchestrates asset fetching, preparation, and execution (or simulation).
    """
    result = run_docking_job(request.determinant, request.ligand)
    
    if result.get("status") == "error":
         raise HTTPException(status_code=500, detail=result.get("message"))
         
    return {
        "status": result["status"],
        "score": result["score"],
        "unit": result["unit"],
        "pose_file": result["pose_file"],
        "disclaimer": result["disclaimer"]
    }

# DiffDock Integration
from src.docking.diffdock_runner import DiffDockRunner

class DiffDockRequest(BaseModel):
    determinant: str
    ligand: str # SMILES or Name

@router.post("/diffdock/run")
async def run_diffdock(request: DiffDockRequest, x_abrisk_mode: Optional[str] = Header(None)):
    """
    Run diffusion docking via DiffDock-L.
    Respects x-abrisk-mode: 'offline' | 'online'
    """
    runner = DiffDockRunner()
    mode = x_abrisk_mode if x_abrisk_mode in ["offline", "online"] else "auto"
    return runner.run_job(request.determinant, request.ligand, mode=mode)

# DynamicBind Integration
from src.docking.dynamicbind_runner import DynamicBindRunner

class RefineRequest(BaseModel):
    determinant: str
    pose_data: str = "pose_1.sdf" # Placeholder for pose identifier

@router.post("/dynamicbind/refine")
async def refine_dynamicbind(request: RefineRequest):
    """
    Refine a docking pose using DynamicBind (Induced Fit).
    """
    runner = DynamicBindRunner()
    return await runner.refine_pose(request.determinant, request.pose_data)

class SetupRequest(BaseModel):
    component: str # vina, ligand, receptor
    determinant: str = "NDM-1"

@router.get("/status")
async def get_docking_status(determinant: str = "NDM-1"):
    return check_docking_status(determinant)

@router.post("/setup")
async def setup_docking_asset(request: SetupRequest):
    success = setup_component(request.component, request.determinant)
    return {"status": "success" if success else "error"}
