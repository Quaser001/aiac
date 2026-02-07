
import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.db_utils import get_db_connection

SEED_FILE = 'data/bv_brc_seed.json'

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS phenotype_evidence (
    id SERIAL PRIMARY KEY,
    genome_id TEXT,
    genome_name TEXT,
    antibiotic TEXT,
    resistant_phenotype TEXT,
    measurement TEXT,
    measurement_sign TEXT,
    measurement_unit TEXT,
    laboratory_typing_method TEXT,
    testing_standard TEXT,
    source TEXT,
    accession TEXT,
    ingestion_date TIMESTAMP DEFAULT NOW()
);
"""

def seed_phenotypes():
    print(f"Reading seed data from {SEED_FILE}...")
    try:
        with open(SEED_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {SEED_FILE} not found.")
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Create table
            print("Ensuring table 'phenotype_evidence' exists...")
            cur.execute(CREATE_TABLE_SQL)
            
            # Optional: Clear table if you want a fresh seed every time
            # cur.execute("TRUNCATE TABLE phenotype_evidence;")

            print(f"Ingesting {len(data)} rows...")
            inserted_count = 0
            for entry in data:
                cur.execute("""
                    INSERT INTO phenotype_evidence (
                        genome_id, genome_name, antibiotic, resistant_phenotype,
                        measurement, measurement_sign, measurement_unit,
                        laboratory_typing_method, testing_standard, source, accession
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    entry.get('genome_id'),
                    entry.get('genome_name'),
                    entry.get('antibiotic'),
                    entry.get('resistant_phenotype'),
                    entry.get('measurement'),
                    entry.get('measurement_sign'),
                    entry.get('measurement_unit'),
                    entry.get('laboratory_typing_method'),
                    entry.get('testing_standard'),
                    entry.get('source'),
                    entry.get('accession')
                ))
                inserted_count += 1
            
            conn.commit()
            print(f"SUCCESS: Ingested {inserted_count} rows into phenotype_evidence.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    seed_phenotypes()
