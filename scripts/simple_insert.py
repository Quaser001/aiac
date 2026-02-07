from src.data.db_utils import get_db_connection
import sys

def simple_test():
    try:
        print("Connecting...")
        conn = get_db_connection()
        cur = conn.cursor()
        print("Inserting...")
        cur.execute("INSERT INTO drug_classes (class_name) VALUES ('TEST_DEBUG_CLASS') ON CONFLICT DO NOTHING")
        print("Committing...")
        conn.commit()
        print("DONE.")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_test()
