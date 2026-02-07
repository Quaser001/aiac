import sys
import os

# Add src to path
sys.path.append(os.getcwd())

from src.data.db_utils import get_db_connection

def inspect_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("\n--- Columns in resistance_genes ---")
        try:
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'resistance_genes'")
            cols = cur.fetchall()
            for c in cols:
                print(c[0])
        except Exception as e:
            print(f"Error checking cols: {e}")

        print("\n--- Count ---")
        try:
            cur.execute("SELECT COUNT(*) FROM resistance_genes")
            print(cur.fetchone()[0])
        except Exception as e:
            print(f"Error checking count: {e}")
            
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    inspect_db()
