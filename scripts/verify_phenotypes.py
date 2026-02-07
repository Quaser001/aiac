
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.db_utils import get_db_connection

def verify():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM phenotype_evidence;")
            count = cur.fetchone()[0]
            print(f"Total rows in phenotype_evidence: {count}")
            
            cur.execute("SELECT genome_name, antibiotic, resistant_phenotype, source FROM phenotype_evidence LIMIT 3;")
            rows = cur.fetchall()
            print("\nSample Data:")
            for row in rows:
                print(row)
    finally:
        conn.close()

if __name__ == '__main__':
    verify()
