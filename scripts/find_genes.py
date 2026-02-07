import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.db_utils import get_db_connection

def find_genes():
    conn = get_db_connection()
    cur = conn.cursor()
    
    queries = ["NDM-1", "MexB", "mecA", "vanA", "KPC-2"]
    
    print("--- Searching for Gene Symbols ---")
    for q in queries:
        # Search distinct symbols matching the query
        cur.execute("SELECT DISTINCT gene_symbol FROM resistance_genes WHERE gene_symbol ILIKE %s LIMIT 3", (f"%{q}%",))
        rows = cur.fetchall()
        print(f"Query '{q}': {[r[0] for r in rows]}")
        
    conn.close()

if __name__ == "__main__":
    find_genes()
