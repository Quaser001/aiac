from typing import Dict, Any, List

class MechanismEngine:
    """
    LAYER 2A: SPECIALIST MECHANISM INTELLIGENCE
    Deterministic mapping of gene/variant -> Biological Mechanism.
    """
    
    def analyze_mechanism(self, gene_id: str, family: str) -> Dict[str, Any]:
        """
        Returns structural and mechanistic context for a gene.
        """
        # Database-backed implementation
        from src.data.db_utils import get_db_connection
        
        ctx = {
            "gene_id": gene_id,
            "mechanism_class": "Unknown",
            "structural_impact": "Analysis requires further research",
            "catalytic_type": "Unknown"
        }
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Join genes to mechanisms
            cur.execute("""
                SELECT m.mechanism_name, rg.gene_name 
                FROM resistance_genes rg
                JOIN resistance_mechanisms m ON rg.mechanism_id = m.id
                WHERE rg.gene_symbol = %s OR rg.card_short_name = %s
                LIMIT 1
            """, (gene_id, gene_id))
            
            row = cur.fetchone()
            if row:
                ctx["mechanism_class"] = row[0]
                ctx["full_name"] = row[1]
                
                # Dynamic Logic for description based on mechanism keywords
                # In Layer 2A, we expand this mapping.
                if "beta-lactamase" in row[0].lower():
                    if "metallo" in row[0].lower():
                        ctx["structural_impact"] = "Zinc-dependent hydrolysis of beta-lactam ring"
                        ctx["catalytic_type"] = "Metallo-enzyme (Zn2+)"
                    else:
                        ctx["structural_impact"] = "Hydrolysis of beta-lactam ring"
                        ctx["catalytic_type"] = "Serine-hydrolase"
                elif "efflux" in row[0].lower():
                    ctx["structural_impact"] = "Active export of antibiotic"
                    ctx["catalytic_type"] = "Transmembrane Pump"
        except Exception as e:
            print(f"Error in mechanism analysis: {e}")
        finally:
            conn.close()
            
        return ctx
