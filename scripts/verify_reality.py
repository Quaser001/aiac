import sys
import os
import psycopg2

# Add src to path
sys.path.append(os.getcwd())

from src.data.db_utils import get_db_connection

def verify_reality():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("\n--- REALITY CHECK ---")
        
        # 1. Count
        print("1. Checking Row Count:")
        cur.execute("SELECT COUNT(*) FROM resistance_genes")
        count = cur.fetchone()[0]
        print(f"   COUNT: {count}")
        
        # 2. Sample
        print("\n2. Checking First 20 Genes:")
        cur.execute("SELECT gene_name FROM resistance_genes ORDER BY gene_name LIMIT 20")
        rows = cur.fetchall()
        print(f"   Genes: {[r[0] for r in rows]}")
        
        # 3. CTX Check
        print("\n3. Checking CTX Variants:")
        cur.execute("SELECT gene_name FROM resistance_genes WHERE gene_name ILIKE '%CTX%' LIMIT 20")
        rows = cur.fetchall()
        print(f"   CTX Matches: {[r[0] for r in rows]}")
        
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_reality()
