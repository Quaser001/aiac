from src.data.db_utils import get_db_connection

def verify_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    tables = ["resistance_genes", "resistance_mechanisms", "drug_classes", "gene_families"]
    print("--- Database Verification ---")
    
    total = 0
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            count = cur.fetchone()[0]
            print(f"{t}: {count}")
            total += count
        except Exception as e:
            print(f"{t}: Error {e}")
            conn.rollback()
            
    conn.close()
    return total

if __name__ == "__main__":
    verify_db()
