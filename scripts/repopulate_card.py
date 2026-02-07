import os
import sys
import psycopg2
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.getcwd())
from src.data.db_utils import get_db_connection

BASE_DIR = os.getcwd()
CARD_FASTA = os.path.join(BASE_DIR, "data/raw/protein_fasta_protein_homolog_model_variants.fasta")

def parse_fasta_headers(filepath):
    """
    Yields parsed header dictionaries from CARD fasta.
    Header format: >Prevalence_Sequence_ID:1|ARO_Name:qacG|ARO:3007015|Detection_Model:Protein Homolog Model|CARD_Short_Name:qacG
    """
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith(">"):
                # Remove > and split by |
                content = line[1:].strip()
                parts = content.split('|')
                data = {}
                for part in parts:
                    if ':' in part:
                        key, val = part.split(':', 1)
                        data[key.strip()] = val.strip()
                yield data

def repopulate_card():
    conn = None
    try:
        print("Connecting to DB...")
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Clear existing 5 rows
        print("Truncating resistance_genes...")
        cur.execute("TRUNCATE TABLE resistance_genes CASCADE")
        
        # 2. Parse CARD FASTA
        print(f"Parsing {CARD_FASTA}...")
        
        unique_genes = {} # Key by ARO Accession to avoid duplicates (variants of same gene)
        
        for data in parse_fasta_headers(CARD_FASTA):
            aro = data.get('ARO')
            if not aro: continue
            
            # We want one entry per gene model, not every sequence variant
            # But the user asked for "2772 genes". CARD has ~3000 models.
            # Using ARO as unique key seems correct.
            
            if aro not in unique_genes:
                unique_genes[aro] = {
                    'aro_accession': aro,
                    'gene_name': data.get('ARO_Name', 'Unknown'),
                    'gene_symbol': data.get('CARD_Short_Name', data.get('ARO_Name')),
                    'model_type': data.get('Detection_Model', 'Protein Homolog Model')
                }
        
        print(f"Found {len(unique_genes)} unique resistance genes.")
        
        # 3. Insert
        print("Inserting into DB...")
        insert_query = """
            INSERT INTO resistance_genes (aro_accession, gene_name, gene_symbol, model_type)
            VALUES (%s, %s, %s, %s)
        """
        
        batch = []
        for gene in unique_genes.values():
            batch.append((
                gene['aro_accession'],
                gene['gene_name'],
                gene['gene_symbol'],
                gene['model_type']
            ))
            
        cur.executemany(insert_query, batch)
        conn.commit()
        
        print(f"Successfully inserted {len(batch)} rows.")
        
        # 4. Verify
        cur.execute("SELECT COUNT(*) FROM resistance_genes")
        final_count = cur.fetchone()[0]
        print(f"Final Table Count: {final_count}")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    repopulate_card()
