import os
import json
import psycopg2
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

SOURCE_FILE = 'src/data/phenotypes_bvbrc_2025.json'

def get_db_url():
    url = os.getenv("DATABASE_URL")
    if not url: return None
    if "WL$r2%8?TFeKT_N" in url:
        return url.replace("WL$r2%8?TFeKT_N", "WL$r2%258%3FTFeKT_N")
    return url

def seed_db():
    print(f"--- Seeding Database from {SOURCE_FILE} ---")
    
    if not os.path.exists(SOURCE_FILE):
        print(f"Source file not found: {SOURCE_FILE}")
        return

    with open(SOURCE_FILE, 'r') as f:
        data = json.load(f)
        
    db_url = get_db_url()
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Clean existing
    cur.execute("DELETE FROM phenotype_resistance_stats WHERE source_dataset LIKE '%BV-BRC%'")
    
    inserted = 0
    for item in data:
        org_name = item['organism_name']
        org_id = org_name.lower().replace(" ", "_")
        
        # Ensure organism
        cur.execute("INSERT INTO organisms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (org_id, org_name))
        
        # Calculate stats if needed (the json already has counts)
        resistance_rate = (item['resistant_count'] / item['sample_count']) * 100
        
        # Insert
        cur.execute("""
            INSERT INTO phenotype_resistance_stats 
            (organism_id, drug_class, resistant_count, susceptible_count, sample_count, resistance_rate, source_dataset, year, region)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            org_id,
            item['drug_class'],
            item['resistant_count'],
            item['sample_count'] - item['resistant_count'],
            item['sample_count'],
            resistance_rate,
            item['source_dataset'],
            item['year'],
            item.get('region', 'Global')
        ))
        inserted += 1
        
    conn.commit()
    print(f"Successfully seeded {inserted} rows from BV-BRC.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_db()
