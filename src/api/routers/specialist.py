from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.specialist.mechanism_engine import MechanismEngine
from src.specialist.constraints import TherapeuticConstraints
from src.specialist.hypothesis_engine import HypothesisEngine
from src.specialist.phenotype import PhenotypeService
from src.infra.supabase_client import SupabaseClientWrapper

router = APIRouter(
    prefix="/specialist",
    tags=["Specialist Layer (Layer 2)"],
    responses={404: {"description": "Not found"}},
)

@router.on_event("startup")
async def startup_event():
    try:
        from src.data.db_utils import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM resistance_genes")
        count = cur.fetchone()[0]
        print(f"ONLINE CARD MODE: Using Supabase resistance_genes (N={count})")
        conn.close()
    except Exception as e:
        print(f"OFFLINE FALLBACK: Activated due to {e}")
    
    # Load Tier-1 Sequences
    load_tier1_sequences()


# Shared Logic
mech_engine = MechanismEngine()
constraint_logic = TherapeuticConstraints()
phenotype_service = PhenotypeService()
supabase = SupabaseClientWrapper()

class MechanismRequest(BaseModel):
    gene_id: str
    family: str = "Unknown"
    organism_context: Optional[str] = None

class MechanismResponse(BaseModel):
    gene_id: str
    mechanism: Dict[str, Any]
    constraints: List[Dict[str, str]]
    phenotype_evidence: Optional[Dict[str, Any]] = None
    disclaimer: str

@router.get("/genes/search", response_model=List[str])
async def search_genes(query: Optional[str] = None):
    """
    Search for resistance genes by symbol (Typeahead).
    If query is empty, returns top 20 genes from DB.
    """
    # Use direct DB connection
    from src.data.db_utils import get_db_connection
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            if query and len(query) >= 1:
                cur.execute("SELECT DISTINCT gene_name FROM resistance_genes WHERE gene_name ILIKE %s ORDER BY gene_name LIMIT 50", (f"%{query}%",))
            else:
                # Return top 50 if no query (On Focus behavior)
                cur.execute("SELECT DISTINCT gene_name FROM resistance_genes ORDER BY gene_name LIMIT 50")
            
            rows = cur.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        print(f"Gene search error: {e}")
        # NO FALLBACK allowed for gene search - strict database source
        return []
    finally:
        if conn:
            conn.close()

@router.get("/phenotype/organisms/search", response_model=List[str])
async def search_organisms(query: Optional[str] = None):
    """
    Search for organisms with phenotype evidence.
    """
    from src.data.db_utils import get_db_connection
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = "SELECT DISTINCT genome_name FROM phenotype_evidence"
            params = []
            
            if query and len(query) >= 1:
                sql += " WHERE genome_name ILIKE %s"
                params.append(f"%{query}%")
                
            sql += " ORDER BY genome_name LIMIT 20"
            
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            results = [row[0] for row in rows]
            
            if not results:
                seeds = ["Klebsiella pneumoniae", "Escherichia coli", "Pseudomonas aeruginosa", "Acinetobacter baumannii"]
                if query:
                    return [s for s in seeds if query.lower() in s.lower()]
                return seeds
                
            return results
    except Exception as e:
        print(f"Organism search error: {e}")
        return ["Klebsiella pneumoniae", "Escherichia coli", "Pseudomonas aeruginosa"]
    finally:
        if conn:
            conn.close()

@router.post("/analyze/mechanism", response_model=MechanismResponse)
async def analyze_mechanism_constraints(request: MechanismRequest):
    """
    LAYER 2A: Deterministic Mechanism & Constraint Analysis.
    Now includes Layer 1.5 Observational Phenotype Evidence (optional).
    For Researcher Use Only.
    """
    try:
        # 1. Analyze Mechanism (Deterministic)
        mech_ctx = mech_engine.analyze_mechanism(request.gene_id, request.family)
        
        # 2. Derive Constraints
        constraints = constraint_logic.derive_constraints(mech_ctx)
        
        # 3. Fetch Phenotype Evidence (Observational)
        phenotype_evidence = None
        if request.organism_context:
            # Renamed method from get_stats to get_evidence to reflect raw data
            phenotype_evidence = phenotype_service.get_evidence(request.organism_context)
        
        # Audit Log (Specialist Access)
        log_details = f"Analyzed {request.gene_id}"
        if request.organism_context:
            log_details += f" in context of {request.organism_context}"
            
        try:
            supabase.log_audit(
                actor="SPECIALIST_USER",
                action="LAYER_2A_ANALYSIS",
                details=log_details,
                severity="INFO"
            )
        except Exception:
            pass # Non-critical audit failure

        return {
            "gene_id": request.gene_id,
            "mechanism": mech_ctx,
            "constraints": constraints,
            "phenotype_evidence": phenotype_evidence,
            "disclaimer": "RESEARCH USE ONLY. Not for clinical decision making."
        }
    except Exception as e:
        print(f"Mechanism Analysis Error (Using Fallback): {e}")
        # ROBUST FALLBACK FOR DEMO STABILITY
        return {
            "gene_id": request.gene_id,
            "mechanism": {
                "gene_id": request.gene_id,
                "mechanism_class": "Metallo-beta-lactamase" if "NDM" in request.gene_id else "Serine-beta-lactamase",
                "structural_impact": "Zinc-dependent hydrolysis" if "NDM" in request.gene_id else "Active site acylation",
                "catalytic_type": "Zinc Hydrolase" if "NDM" in request.gene_id else "Serine Hydrolase",
                "full_name": f"{request.gene_id} (Fallback Mode)" 
            },
            "constraints": [
                {"type": "System Warning", "description": "Backend database connection failed. Using fallback simulation data."}
            ],
            "phenotype_evidence": {
                "organism_name": request.organism_context or "Unknown",
                "source": "Fallback Cache",
                "evidence": [
                    {"antibiotic": "Meropenem", "phenotype": "Resistant", "mic": ">32", "method": "Vitek 2", "standard": "CLSI", "isolate": "DEMO-01"}
                ]
            },
            "disclaimer": "SYSTEM RECOVERY DATA. Non-clinical."
        }


# -----------------------------------------------------------------------------
# TIER-1 SEQUENCE LOADER (Conference Patch)
# -----------------------------------------------------------------------------
TIER1_SEQ_CACHE = {}

def load_tier1_sequences():
    """Parses data/tier1_sequences.fasta into a dict."""
    global TIER1_SEQ_CACHE
    try:
        if TIER1_SEQ_CACHE: return TIER1_SEQ_CACHE
        
        seqs = {}
        import os
        if not os.path.exists("data/tier1_sequences.fasta"):
            print("Tier-1 FASTA not found, skipping pre-load.")
            return {}
            
        with open("data/tier1_sequences.fasta", "r") as f:
            current = None
            buf = []
            for line in f:
                line = line.strip()
                if not line or line.startswith(";"): continue
                if line.startswith(">"):
                    if current:
                        seqs[current] = "".join(buf)
                    # Extract gene name: >NDM-1|UniProt:C7C422 -> NDM-1
                    header_safe = line[1:].split("|")[0].strip() 
                    current = header_safe
                    buf = []
                else:
                    buf.append(line)
            if current:
                seqs[current] = "".join(buf)
        
        TIER1_SEQ_CACHE = seqs
        print(f"Loaded {len(seqs)} Tier-1 sequences: {list(seqs.keys())}")
        return seqs
    except Exception as e:
        print(f"Error loading Tier-1 sequences: {e}")
        return {}

class FeasibilityRequest(BaseModel):
    gene_id: str
    mechanism_class: str
    sequence: Optional[str] = None # made optional to allow overrides

@router.post("/analyze/feasibility")
async def analyze_feasibility(request: FeasibilityRequest):
    """
    LAYER 2B: DL-Guided In-Silico Feasibility.
    """
    # PATCH: Auto-inject Tier-1 Sequence if missing or to ensure validity
    if not request.sequence or request.gene_id in TIER1_SEQ_CACHE:
        load_tier1_sequences() # Ensure loaded
        if request.gene_id in TIER1_SEQ_CACHE:
            print(f"[Tier-1] Auto-injecting canonical sequence for {request.gene_id}")
            request.sequence = TIER1_SEQ_CACHE[request.gene_id]

    hypothesis_engine = HypothesisEngine() # In real app, inject singleton
    
    result = await hypothesis_engine.generate_hypotheses(
        request.gene_id, 
        request.mechanism_class,
        request.sequence or ""
    )
    
    # Audit Log
    try:
        supabase.log_audit(
            actor="SPECIALIST_USER",
            action="LAYER_2B_DL_SCORE",
            details=f"Feasibility for {request.gene_id}",
            severity="INFO"
        )
    except Exception:
        pass
    
    return result
