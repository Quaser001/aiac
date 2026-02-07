import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

import urllib.parse

def get_safe_db_url():
    url = os.getenv("DATABASE_URL")
    if not url: return None
    # Very basic hack to fix specific password issue if needed
    # Ideally we parse the URL properly
    if "WL$r2%8?TFeKT_N" in url:
        return url.replace("WL$r2%8?TFeKT_N", "WL$r2%258%3FTFeKT_N")
    return url

DB_URL = get_safe_db_url()

def init_db():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("Creating table: organisms...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organisms (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        
        print("Creating table: phenotype_resistance_stats...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phenotype_resistance_stats (
                id SERIAL PRIMARY KEY,
                organism_id TEXT REFERENCES organisms(id),
                drug_class TEXT NOT NULL,
                resistant_count INTEGER,
                susceptible_count INTEGER,
                sample_count INTEGER,
                resistance_rate REAL,
                source_dataset TEXT,
                year INTEGER,
                region TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing DB: {e}")

if __name__ == "__main__":
    init_db()
