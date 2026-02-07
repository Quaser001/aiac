from src.data.db_utils import get_db_connection
import sys

def kill_lock(pid):
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    
    print(f"Terminating PID {pid}...")
    try:
        cur.execute("SELECT pg_terminate_backend(%s)", (pid,))
        print(f"Result: {cur.fetchone()[0]}")
    except Exception as e:
        print(f"Error: {e}")
        
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        kill_lock(sys.argv[1])
    else:
        print("Usage: python -m scripts.kill_locks <PID>")
