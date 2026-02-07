"""Debug script to verify NDM-1 exists in the database."""
from src.data.db_utils import get_db_connection

def check_database():
    conn = get_db_connection()
    cur = conn.cursor()

    print("=== TABLE COUNTS ===")
    cur.execute("SELECT COUNT(*) FROM resistance_genes")
    print(f"resistance_genes: {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM resistance_mechanisms")  
    print(f"resistance_mechanisms: {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM gene_drug_class_links")
    print(f"gene_drug_class_links: {cur.fetchone()[0]}")

    print("")
    print("=== ALL GENES IN DB ===")
    cur.execute("SELECT aro_accession, gene_symbol, gene_name, mechanism_id FROM resistance_genes")
    rows = cur.fetchall()
    print(f"Total genes: {len(rows)}")
    for r in rows:
        print(f"  ARO: {r[0]}, Symbol: {r[1]}, Name: {r[2]}, MechID: {r[3]}")

    print("")
    print("=== SEARCHING FOR NDM-1 ===")
    cur.execute("SELECT * FROM resistance_genes WHERE gene_symbol ILIKE '%NDM%' OR card_short_name ILIKE '%NDM%'")
    rows = cur.fetchall()
    print(f"Matching rows for NDM: {len(rows)}")
    for r in rows:
        print(f"  {r}")

    print("")
    print("=== TESTING MECHANISM LOOKUP QUERY ===")
    # This is the exact query used in mechanism_engine.py
    cur.execute("""
        SELECT m.mechanism_name, rg.gene_name 
        FROM resistance_genes rg
        JOIN resistance_mechanisms m ON rg.mechanism_id = m.id
        WHERE rg.gene_symbol = %s OR rg.card_short_name = %s
        LIMIT 1
    """, ("NDM-1", "NDM-1"))
    row = cur.fetchone()
    if row:
        print(f"SUCCESS: Mechanism={row[0]}, Name={row[1]}")
    else:
        print("FAIL: Query returned no rows")

    conn.close()

if __name__ == "__main__":
    check_database()
