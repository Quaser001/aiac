import os
import pandas as pd
from src.data.db_utils import get_db_connection

# Path to the specific index file with metadata
CARD_INDEX_PATH = os.path.join("data", "raw", "index-for-model-sequences.txt")

def clean_split(text):
    if not isinstance(text, str) or pd.isna(text):
        return []
    # Split by semicolon as seen in CARD docs (header says semi-colon-separated list)
    # Also handle commas just in case
    return [x.strip() for x in text.replace(",", ";").split(";") if x.strip()]

def ingest_card():
    if not os.path.exists(CARD_INDEX_PATH):
        print(f"Error: File not found {CARD_INDEX_PATH}")
        return

    print(f"Reading {CARD_INDEX_PATH}...")
    # It's a TSV. We only need metadata columns to build the gene catalog.
    cols = ["aro_accession", "aro_term", "detection_model", "resistance_mechanism", "drug_class", "amr_gene_family", "card_short_name"]
    
    # Chunking or optimization could be done, but let's try reading required cols first.
    # We drop duplicates based on ARO to get the unique gene definitions.
    df = pd.read_csv(CARD_INDEX_PATH, sep="\t", usecols=cols)
    print(f"Raw rows: {len(df)}")
    
    df_unique = df.drop_duplicates(subset=["aro_accession"])
    print(f"Unique AROs (Genes) to ingest: {len(df_unique)}")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # BATCHING STRATEGY
        
        # 1. Collect all unique dimensions
        all_mechanisms = set()
        all_families = set()
        all_classes = set()

        for _, row in df_unique.iterrows():
            mechs = clean_split(row.get("resistance_mechanism", ""))
            classes = clean_split(row.get("drug_class", ""))
            family = row.get("amr_gene_family", None)
            
            if mechs: all_mechanisms.add(mechs[0]) # Primary mechanism
            if classes: all_classes.update(classes)
            if isinstance(family, str): all_families.add(family)

        print(f"Dimensions to sync: {len(all_mechanisms)} mechs, {len(all_families)} fams, {len(all_classes)} classes.")

        # 2. Batch Insert Dimensions
        # Psycopg2 extras.execute_values is faster but we stick to standard for simplicity unless needed
        
        # Mechanisms
        if all_mechanisms:
            args_str = ",".join(cur.mogrify("(%s)", (m,)).decode('utf-8') for m in all_mechanisms)
            cur.execute("INSERT INTO resistance_mechanisms (mechanism_name) VALUES " + args_str + " ON CONFLICT DO NOTHING")
        
        # Families
        if all_families:
            args_str = ",".join(cur.mogrify("(%s)", (f,)).decode('utf-8') for f in all_families)
            cur.execute("INSERT INTO gene_families (family_name) VALUES " + args_str + " ON CONFLICT DO NOTHING")

        # Drug Classes
        if all_classes:
            args_str = ",".join(cur.mogrify("(%s)", (c,)).decode('utf-8') for c in all_classes)
            cur.execute("INSERT INTO drug_classes (class_name) VALUES " + args_str + " ON CONFLICT DO NOTHING")
            
        conn.commit() # Commit dims to resolve IDs

        # 3. Fetch IDs map
        cur.execute("SELECT mechanism_name, id FROM resistance_mechanisms")
        mech_map = dict(cur.fetchall())
        print(f"DEBUG: mech_map size: {len(mech_map)}")
        
        cur.execute("SELECT family_name, id FROM gene_families")
        fam_map = dict(cur.fetchall())
        print(f"DEBUG: fam_map size: {len(fam_map)}")
        
        cur.execute("SELECT class_name, id FROM drug_classes")
        class_map = dict(cur.fetchall())
        print(f"DEBUG: class_map size: {len(class_map)}")

        # 4. Prepare Batch Data
        gene_rows = []
        link_rows = []
        
        for _, row in df_unique.iterrows():
            aro_acc = str(row.get("aro_accession", "")).replace("ARO:", "")
            gene_name = row.get("aro_term", "Unknown")
            model_type = row.get("detection_model", "protein homolog")
            card_short = row.get("card_short_name", None)
            
            # IDs
            mechs = clean_split(row.get("resistance_mechanism", ""))
            m_id = mech_map.get(mechs[0]) if mechs and mechs[0] in mech_map else None
            
            fam = row.get("amr_gene_family", None)
            f_id = fam_map.get(fam) if isinstance(fam, str) else None
            
            gene_rows.append((aro_acc, gene_name, gene_name, f_id, m_id, model_type, card_short))
            
            # Links
            classes = clean_split(row.get("drug_class", ""))
            for c in classes:
                if c in class_map:
                    link_rows.append((aro_acc, class_map[c]))

        # 5. Insert Genes
        print(f"Inserting {len(gene_rows)} genes...")
        # Using executemany with optimization via mogrify manually if needed, or just fast_executemany pattern
        # For 3000 rows, standard executemany is fine.
        
        insert_gene_sql = """
            INSERT INTO resistance_genes 
            (aro_accession, gene_symbol, gene_name, family_id, mechanism_id, model_type, card_short_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (aro_accession) DO UPDATE SET 
                gene_symbol = EXCLUDED.gene_symbol,
                family_id = EXCLUDED.family_id,
                mechanism_id = EXCLUDED.mechanism_id,
                card_short_name = EXCLUDED.card_short_name
        """
        cur.executemany(insert_gene_sql, gene_rows)

        # 6. Insert Links
        print(f"Inserting {len(link_rows)} gene-drug links...")
        insert_link_sql = """
            INSERT INTO gene_drug_class_links (aro_accession, drug_class_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """
        cur.executemany(insert_link_sql, link_rows)

        # Metadata
        cur.execute("INSERT INTO card_metadata (dataset_version, source_url) VALUES (%s, %s)", ("v3.x", "card.mcmaster.ca"))

        conn.commit()
        print("✓ Ingestion Complete.")
        print(f"Stats: Genes={len(gene_rows)}, Links={len(link_rows)}")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    ingest_card()
