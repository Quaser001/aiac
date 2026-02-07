from typing import Dict, Optional

class MechanismMapper:
    """
    Maps gene names to their biological resistance mechanism and functional category.
    Includes a 'Lite' in-memory database of high-priority pathogens/genes for the prototype.
    """

    # Prototype Database: WHO Priority Pathogens & Key Resistance Genes
    # Format: "GENE_ID": {"mechanism": "Mechanism", "class": "Drug Class", "tier": "Risk Tier"}
    LITE_DB = {
        "NDM-1": {
            "name": "New Delhi metallo-beta-lactamase 1",
            "mechanism": "Antibiotic inactivation (Hydrolysis)",
            "drug_class": "Carbapenems",
            "risk_tier": 1,
            "significance": "High conservation, global spread, confers resistance to all beta-lactams except monobactams."
        },
        "KPC-2": {
            "name": "Klebsiella pneumoniae carbapenemase 2",
            "mechanism": "Antibiotic inactivation (Hydrolysis)",
            "drug_class": "Carbapenems",
            "risk_tier": 1,
            "significance": "Class A carbapenemase, very common in Enterobacteriaceae."
        },
        "OXA-48": {
            "name": "Oxacillinase-48",
            "mechanism": "Antibiotic inactivation (Hydrolysis)",
            "drug_class": "Carbapenems",
            "risk_tier": 1,
            "significance": "Class D carbapenemase, difficult to detect phenotypically."
        },
        "mecA": {
            "name": "Methicillin resistance protein",
            "mechanism": "Target alteration (PBP2a)",
            "drug_class": "Methicillin/Beta-lactams",
            "risk_tier": 1,
            "significance": "Defines MRSA."
        },
        "vanA": {
            "name": "Vancomycin resistance protein A",
            "mechanism": "Target alteration (Cell wall precursor)",
            "drug_class": "Vancomycin",
            "risk_tier": 1,
            "significance": "High-level vancomycin resistance (VRE)."
        },
        "mcr-1": {
            "name": "Mobilized Colistin Resistance-1",
            "mechanism": "Target modification",
            "drug_class": "Colistin",
            "risk_tier": 1,
            "significance": "Plasmid-mediated colistin resistance, last-resort drug."
        }
    }

    def __init__(self, use_full_db: bool = False):
        """
        Initialize the MechanismMapper.
        
        Args:
            use_full_db: If True, attempts to load the full external database (e.g., from JSON).
                         If False, defaults to the internal LITE_DB.
        """
        self.use_full_db = use_full_db
        self.db = self.LITE_DB
        
        if self.use_full_db:
            self._load_external_db()

    def _load_external_db(self):
        """
        Placeholder for loading the full CARD/ARO ontology from disk.
        For Phase 5/6, this will parse the JSON files discovered in Phase 1.
        """
        # TODO: Implement JSON loading logic
        print("Warning: Full DB loading not yet implemented. Falling back to Lite DB.")
        pass

    def lookup_gene(self, gene_identifier: str) -> Optional[Dict]:
        """
        Looks up a gene by its identifier (e.g., Short name or Accession) in the Postgres DB.
        """
        from src.data.db_utils import get_db_connection
        
        # 1. Check LITE_DB first (for fallback/speed if needed, or remove completely)
        # For this phase, we prefer DB.
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        result = None
        
        try:
            # Fetch Gene + Mechanism
            cur.execute("""
                SELECT rg.aro_accession, rg.gene_name, m.mechanism_name, rg.card_short_name
                FROM resistance_genes rg
                JOIN resistance_mechanisms m ON rg.mechanism_id = m.id
                WHERE rg.gene_symbol ILIKE %s OR rg.card_short_name ILIKE %s OR rg.aro_accession = %s
                LIMIT 1
            """, (gene_identifier, gene_identifier, gene_identifier))
            
            row = cur.fetchone()
            if row:
                aro, name, mech, short_name = row
                
                # Fetch Drug Classes
                cur.execute("""
                    SELECT dc.class_name
                    FROM gene_drug_class_links l
                    JOIN drug_classes dc ON l.drug_class_id = dc.id
                    WHERE l.aro_accession = %s
                """, (aro,))
                
                classes = [r[0] for r in cur.fetchall()]
                
                # Determine Risk Tier (Simple logic for now: Carbapenems/Colistin = Tier 1)
                # In Layer 2A, this is more complex.
                tier = 2
                classes_str = ", ".join(classes)
                if "carbapenem" in classes_str.lower() or "colistin" in classes_str.lower() or "vancomycin" in classes_str.lower():
                    tier = 1
                
                result = {
                    "name": name,
                    "mechanism": mech,
                    "drug_class": classes_str if classes else "Unknown",
                    "risk_tier": tier,
                    "significance": f"Detected {mech} conferring resistance to {classes_str or 'multidrugs'}."
                }
                
        except Exception as e:
            print(f"DB Lookup Error: {e}")
        finally:
            conn.close()
            
        return result

    def get_mechanism(self, gene_identifier: str) -> str:
        data = self.lookup_gene(gene_identifier)
        return data["mechanism"] if data else "Unknown Mechanism"
