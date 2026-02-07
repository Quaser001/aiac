from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.api.schemas import RiskReport, HealthCheck

load_dotenv()
from src.scout.gene_parser import GeneParser
from src.clinical.risk import RiskStratifier
from src.infra.supabase_client import SupabaseClientWrapper
from src.pipeline_constants import MW_VERSION
from src.api.routers import specialist, docking, structure, mutation, novelty, mechanism_predict, docking_demo
import shutil
import os
import tempfile
import hashlib
import json

app = FastAPI(
    title="ABRISK Decision Intelligence",
    description="Antibiotic Risk Stratification API",
    version=MW_VERSION
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(specialist.router)
app.include_router(docking.router)
app.include_router(structure.router)
app.include_router(mutation.router)
app.include_router(novelty.router)
app.include_router(mechanism_predict.router)
app.include_router(mechanism_predict.router)
app.include_router(docking_demo.router)  # Conference Demo Mode
from src.api.routers import system
app.include_router(system.router)

# Static Mounts
os.makedirs("data/docking_cache/results", exist_ok=True)
app.mount("/docking_results", StaticFiles(directory="data/docking_cache/results"), name="docking_results")
app.mount("/structures", StaticFiles(directory="data/structures"), name="structures")

# Initialize singletons
gene_parser = GeneParser()
risk_stratifier = RiskStratifier()
supabase = SupabaseClientWrapper()

@app.get("/health", response_model=HealthCheck)
def health_check():
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    return {"status": "operational", "version": MW_VERSION, "demo_mode": demo_mode}

@app.post("/analyze/genome", response_model=RiskReport)
async def analyze_genome(file: UploadFile = File(...)):
    """
    Analyzes an uploaded tabular BLAST/Diamond output file.
    Returns a Risk Report.
    """
    tmp_path = None
    input_hash = "unknown"
    
    try:
        # Create a wrapper to handle the file safely
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tsv") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        # Compute hash for audit
        try:
            with open(tmp_path, "rb") as f:
                file_bytes = f.read()
                input_hash = hashlib.sha256(file_bytes).hexdigest()[:16]
        except Exception:
            pass # Non-critical

        # Step 1: Parse
        hits = gene_parser.parse_tabular_output(tmp_path)
        
        # Step 2: Stratify
        report = risk_stratifier.stratify_risk(hits)
        
        # Step 3: Audit Log (Async in production, blocking here for simplicity)
        supabase.log_request(
            input_hash=input_hash,
            risk_level=report["overall_risk_level"],
            model_version=MW_VERSION,
            metadata={"file_name": file.filename, "hit_count": len(hits)}
        )
        
        return report

    except Exception as e:
        # Log error to audit trail
        supabase.log_audit(
            actor="SYSTEM",
            action="ERROR",
            details=f"Analysis failed: {str(e)}",
            severity="ERROR"
        )
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Cleanup
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
