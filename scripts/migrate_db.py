import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

import re
from urllib.parse import quote_plus

def encode_password(db_url):
    # Regex to capture password between user: and @host
    match = re.search(r"://([^:]+):([^@]+)@", db_url)
    if match:
        user = match.group(1)
        password = match.group(2)
        # Check if already encoded (simple check: % followed by hex)
        # But safer to assume if it failed, it might need encoding.
        # However, if we double encode, it breaks. 
        # Given the error "invalid token", it is likely raw.
        
        # We perform a safe encode.
        encoded_pwd = quote_plus(password)
        if encoded_pwd != password:
            return db_url.replace(f":{password}@", f":{encoded_pwd}@")
    return db_url

def migrate():
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        print("Error: DATABASE_URL not found in .env")
        return

    db_url = encode_password(raw_url)
    
    schema_path = os.path.join("src", "data", "schema.sql")
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        return

    print(f"Applying schema from {schema_path}...")
    
    try:
        with open(schema_path, "r") as f:
            sql = f.read()

        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("✓ Schema applied successfully.")
        
    except Exception as e:
        print(f"Migration Failed: {e}")

if __name__ == "__main__":
    migrate()
