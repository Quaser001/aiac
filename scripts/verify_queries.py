from src.data.db_utils import get_db_connection

def test_queries():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("--- Layer 1 Query: NDM-1 Profile ---")
    sql1 = """
        SELECT rg.gene_symbol, dc.class_name 
        FROM resistance_genes rg
        JOIN gene_drug_class_links l ON rg.aro_accession = l.aro_accession
        JOIN drug_classes dc ON l.drug_class_id = dc.id
        WHERE rg.gene_symbol LIKE 'NDM-1%'
        LIMIT 5;
    """
    cur.execute(sql1)
    rows = cur.fetchall()
    for r in rows:
        print(f"Gene: {r[0]} -> Resists: {r[1]}")

    print("\n--- Layer 2A Query: Mechanism Lookup (Metallo-beta-lactamase) ---")
    sql2 = """
        SELECT g.gene_symbol, m.mechanism_name
        FROM resistance_genes g
        JOIN resistance_mechanisms m ON g.mechanism_id = m.id
        WHERE m.mechanism_name ILIKE '%metallo-beta-lactamase%'
        LIMIT 3;
    """
    cur.execute(sql2)
    rows = cur.fetchall()
    for r in rows:
        print(f"Gene: {r[0]} -> Mech: {r[1]}")

    conn.close()

if __name__ == "__main__":
    test_queries()
