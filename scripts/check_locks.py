from src.data.db_utils import get_db_connection

def check_locks():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("--- Active Queries ---")
    try:
        cur.execute("SELECT pid, state, query_start, query FROM pg_stat_activity WHERE state != 'idle'")
        rows = cur.fetchall()
        for r in rows:
            print(f"PID: {r[0]}, State: {r[1]}, Query: {r[3]}")
    except Exception as e:
        print(f"Error: {e}")
        
    conn.close()

if __name__ == "__main__":
    check_locks()
