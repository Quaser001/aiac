from typing import List, Dict, Any
import json
import os

class PhenotypeService:
    """
    Manages organism-level phenotype evidence stats.
    Source: BV-BRC (Patric) Aggregate Data 2025.
    
    In a full production environment, this would query the `phenotype_resistance_stats` 
    relational table. For v1.5 prototype, we serve verified seed slices.
    """
    
    def __init__(self):
        # Use direct DB connection
        pass

    def get_evidence(self, organism_name: str) -> Dict[str, Any]:
        """
        Retrieves raw phenotype evidence for a given organism from Supabase (via direct DB).
        Queries the 'phenotype_evidence' table for isolate-level MIC observations.
        """
        if not organism_name:
            return None
            
        from src.data.db_utils import get_db_connection
        conn = get_db_connection()
        
        try:
            with conn.cursor() as cur:
                # Flexible matching for organism name
                # using ILIKE to find rows where genome_name contains the organism_name
                cur.execute("""
                    SELECT 
                        genome_name, antibiotic, resistant_phenotype, 
                        measurement_sign, measurement, measurement_unit,
                        laboratory_typing_method, testing_standard, source
                    FROM phenotype_evidence 
                    WHERE genome_name ILIKE %s 
                    LIMIT 20
                """, (f"%{organism_name}%",))
                
                rows = cur.fetchall()
                if not rows:
                    return None

                # Transform for frontend
                evidence_list = []
                source = "Unknown"
                
                for row in rows:
                    # Unpack tuple
                    (genome_name, antibiotic, phenotype, sign, meas, unit, method, standard, src) = row
                    
                    # Format MIC nicely
                    mic_value = f"{sign or ''}{meas or ''} {unit or ''}".strip()
                    
                    evidence_list.append({
                        "antibiotic": antibiotic,
                        "phenotype": phenotype,
                        "mic": mic_value,
                        "method": method,
                        "standard": standard,
                        "isolate": genome_name
                    })
                    if src: source = src

                return {
                    "organism_name": organism_name,
                    "source": source,
                    "evidence": evidence_list
                }
            
        except Exception as e:
            print(f"Error fetching phenotype evidence: {e}")
            return None
        finally:
            conn.close()
