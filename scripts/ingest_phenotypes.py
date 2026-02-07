import os
import pandas as pd
import psycopg2
import urllib.parse
from kaggle.api.kaggle_api_extended import KaggleApi

# 1. Configuration
DATASET = 'meirnizri/antibiotic-resistance'
os.environ['KAGGLE_USERNAME'] = 'killergoat'
os.environ['KAGGLE_KEY'] = 'KGAT_99d9b9cd87a5a48ab9336427ffeb8605'

# CARD Mapping
DRUG_MAPPING = {
    'meropenem': 'Carbapenem',
    'imipenem': 'Carbapenem',
    'ertapenem': 'Carbapenem',
    'doripenem': 'Carbapenem',
    'ceftriaxone': 'Cephalosporin',
    'cefotaxime': 'Cephalosporin',
    'ceftazidime': 'Cephalosporin',
    'cefepime': 'Cephalosporin', 
    'ciprofloxacin': 'Fluoroquinolone',
    'levofloxacin': 'Fluoroquinolone',
    'gentamicin': 'Aminoglycoside',
    'amikacin': 'Aminoglycoside',
    'tobramycin': 'Aminoglycoside',
    'vancomycin': 'Glycopeptide'
}

# Standard Organisms
TARGET_ORGS = [
    "klebsiella pneumoniae", 
    "escherichia coli", 
    "staphylococcus aureus",
    "pseudomonas aeruginosa",
    "enterococcus faecium"
]

def get_db_url():
    url = os.getenv("DATABASE_URL")
    if not url: return None
    # Fix encoding
    if "WL$r2%8?TFeKT_N" in url:
        return url.replace("WL$r2%8?TFeKT_N", "WL$r2%258%3FTFeKT_N")
    return url

def ingest():
    global DATASET
    print("--- Starting Ingestion ---")
    
    candidate_datasets = [
        'meirnizri/antibiotic-resistance',
        'saurabhshahane/antibiotic-resistance-bacteria',
        'divyansh22/antibiotic-resistance'
    ]
    
    downloaded_dataset = None
    
    # Download
    api = KaggleApi()
    api.authenticate()
    
    for d in candidate_datasets:
        print(f"DTOI: Attempting download of {d}...")
        try:
            api.dataset_download_files(d, path='.', unzip=True)
            downloaded_dataset = d
            print(f"SUCCESS: Downloaded {d}")
            break
        except Exception as e:
            print(f"FAILED {d}: {e}")
            
    if not downloaded_dataset:
        print("All downloads failed.")
        return

    # Find CSV
    csv_file = None
    for f in os.listdir('.'):
        if f.endswith('.csv'):
            csv_file = f
            break
            
    if not csv_file:
        print("No CSV found.")
        return
        
    print(f"Processing {csv_file} from {downloaded_dataset}...")
    # Update global DATASET for DB insertion
    global DATASET
    DATASET = downloaded_dataset
    try:
        df = pd.read_csv(csv_file)
        
        # Identify columns - inspection showed likelihood of 'test_id', 'bacteria', 'antibiotic', 'exclude', 'year', 'result', etc.
        # But we need to be robust.
        # Let's clean headers
        df.columns = [c.lower() for c in df.columns]
        
        # Heuristic Mapping
        col_org = next((c for c in df.columns if 'bacteria' in c or 'species' in c), None)
        col_drug = next((c for c in df.columns if 'antibiotic' in c), None)
        col_res = next((c for c in df.columns if 'zone' not in c and ('res' in c or 'sens' in c or 'phenotype' in c)), None)
        
        if not (col_org and col_drug and col_res):
            print(f"Missing columns. Found: {df.columns}")
            return

        print(f"Mapped: Org={col_org}, Drug={col_drug}, Result={col_res}")

        # Filter & Transform
        data = []
        for _, row in df.iterrows():
            org = str(row[col_org]).lower().strip()
            drug = str(row[col_drug]).lower().strip()
            res_val = str(row[col_res]).lower().strip()
            
            # Filter Org
            matched_org = None
            for t in TARGET_ORGS:
                if t in org:
                    matched_org = t.capitalize()
                    break
            if not matched_org: continue
            
            # Filter Drug
            matched_class = None
            for d_name, d_class in DRUG_MAPPING.items():
                if d_name in drug:
                    matched_class = d_class
                    break
            if not matched_class: continue
            
            is_resistant = 'r' in res_val or 'resistant' in res_val
            
            data.append({
                'organism': matched_org,
                'drug_class': matched_class,
                'resistant': 1 if is_resistant else 0,
                'count': 1
            })
            
        if not data:
            print("No data matched filters.")
            return
            
        agg_df = pd.DataFrame(data).groupby(['organism', 'drug_class']).agg({
            'resistant': 'sum',
            'count': 'sum' 
        }).reset_index()
        
        agg_df['resistance_rate'] = (agg_df['resistant'] / agg_df['count']) * 100
        
        print(agg_df)
        
        # Insert to DB
        conn = psycopg2.connect(get_db_url())
        cur = conn.cursor()
        
        # Clear old stats from this source to avoid dupes
        cur.execute("DELETE FROM phenotype_resistance_stats WHERE source_dataset LIKE %s", (f'%{DATASET}%',))
        
        inserted = 0
        for _, row in agg_df.iterrows():
            # Ensure organism exists
            org_id = row['organism'].lower().replace(" ", "_")
            cur.execute("INSERT INTO organisms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (org_id, row['organism']))
            
            # Insert Stat
            cur.execute("""
                INSERT INTO phenotype_resistance_stats 
                (organism_id, drug_class, resistant_count, susceptible_count, sample_count, resistance_rate, source_dataset, year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                org_id,
                row['drug_class'],
                int(row['resistant']),
                int(row['count'] - row['resistant']),
                int(row['count']),
                float(row['resistance_rate']),
                f"Kaggle: {DATASET}",
                2026
            ))
            inserted += 1
            
        conn.commit()
        print(f"Successfully inserted {inserted} rows.")
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        if csv_file and os.path.exists(csv_file):
            os.remove(csv_file)

if __name__ == "__main__":
    ingest()
