from src.data.db_utils import get_db_connection

def seed_data():
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    print("--- Seeding Test Data ---")
    
    # 1. Mechanisms
    mechs = [
        "antibiotic inactivation", 
        "antibiotic efflux", 
        "antibiotic target alteration",
        "antibiotic target protection"
    ]
    mech_map = {}
    for m in mechs:
        cur.execute("INSERT INTO resistance_mechanisms (mechanism_name) VALUES (%s) ON CONFLICT (mechanism_name) DO UPDATE SET mechanism_name=EXCLUDED.mechanism_name RETURNING id", (m,))
        mech_map[m] = cur.fetchone()[0]

    # 2. Drug Classes
    classes = [
        "carbapenem", "cephalosporin", "penicillin", "monobactam", # Beta-lactams
        "glycopeptide antibiotic", # Vancomycin
        "tetracycline", "fluoroquinolone", "macrolide"
    ]
    class_map = {}
    for c in classes:
        cur.execute("INSERT INTO drug_classes (class_name) VALUES (%s) ON CONFLICT (class_name) DO UPDATE SET class_name=EXCLUDED.class_name RETURNING id", (c,))
        class_map[c] = cur.fetchone()[0]

    # 3. Genes
    # (ARO, Symbol, Name, Mech_Key, [Class_Keys])
    genes = [
        ("3000589", "NDM-1", "NDM-1 beta-lactamase", "antibiotic inactivation", 
         ["carbapenem", "cephalosporin", "penicillin", "monobactam"]),
         
        ("3000410", "KPC-2", "KPC-2 beta-lactamase", "antibiotic inactivation", 
         ["carbapenem", "cephalosporin", "penicillin"]),
         
        ("3000168", "MexB", "MexB efflux pump", "antibiotic efflux", 
         ["fluoroquinolone", "tetracycline"]),
         
        ("3000698", "mecA", "mecA PBP2a", "antibiotic target alteration", 
         ["penicillin", "cephalosporin"]),
         
        ("3000568", "vanA", "vanA ligase", "antibiotic target alteration", 
         ["glycopeptide antibiotic"])
    ]

    for aro, sym, name, m_key, c_keys in genes:
        m_id = mech_map[m_key]
        cur.execute("""
            INSERT INTO resistance_genes (aro_accession, gene_symbol, gene_name, mechanism_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (aro_accession) DO UPDATE SET 
                gene_symbol = EXCLUDED.gene_symbol,
                mechanism_id = EXCLUDED.mechanism_id
        """, (aro, sym, name, m_id))
        
        # Links
        for ck in c_keys:
            if ck in class_map:
                cid = class_map[ck]
                cur.execute("INSERT INTO gene_drug_class_links (aro_accession, drug_class_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (aro, cid))

    conn.commit()
    print("✓ Seeded NDM-1, KPC-2, MexB, mecA, vanA")
    conn.close()

if __name__ == "__main__":
    seed_data()
