from src.data.db_utils import get_db_connection
import sys

def verify_reasoning(genes_to_test):
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("\n=== SYSTEM VERIFICATION: END-TO-END REASONING ===\n")

    for gene in genes_to_test:
        print(f"--- CASE: {gene} ---")
        
        # 1. Layer 2A: Mechanism Identification
        # "Identify the mechanism associated with this genetic marker."
        cur.execute("""
            SELECT rg.gene_symbol, rg.gene_name, m.mechanism_name, rg.aro_accession
            FROM resistance_genes rg
            LEFT JOIN resistance_mechanisms m ON rg.mechanism_id = m.id
            WHERE rg.gene_symbol = %s OR rg.card_short_name = %s
            LIMIT 1;
        """, (gene, gene))
        
        gene_row = cur.fetchone()
        
        if not gene_row:
            print(f"[FAIL] RESULT: Gene '{gene}' not found in Knowledge Base.")
            print("   (Check spelling or CARD version coverage)")
            continue

        symbol, full_name, mechanism, aro = gene_row
        print(f"[PASS] IDENTIFICATION (Layer 2A):")
        print(f"   - Gene: {symbol} ({full_name})")
        print(f"   - ARO ID: {aro}")
        print(f"   - Mechanism: {mechanism}")

        # 2. Layer 1: Antibiotic Risk Stratification
        # "Determine which drug classes are compromised."
        cur.execute("""
            SELECT dc.class_name
            FROM gene_drug_class_links l
            JOIN drug_classes dc ON l.drug_class_id = dc.id
            WHERE l.aro_accession = %s;
        """, (aro,))
        
        drugs = [r[0] for r in cur.fetchall()]
        
        print(f"[PASS] RISK STRATIFICATION (Layer 1):")
        if drugs:
            print(f"   - Compromised Classes ({len(drugs)}):")
            for d in sorted(drugs):
                print(f"     - {d}")
            
            # Simple Heuristic Explanation
            print("   - Clinical reasoning: Pathogen likely resistant to above classes due to")
            print(f"     production of {mechanism} ({full_name}).")
        else:
            print("   - No specific drug class links found (Check dataset completeness).")
            
        print("\n")

    conn.close()

if __name__ == "__main__":
    # Test cases representing different mechanisms
    candidates = ["NDM-1", "MexB", "mecA", "vanA", "KPC-2"]
    verify_reasoning(candidates)
