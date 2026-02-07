import os
import re
import psycopg2
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        raise ValueError("DATABASE_URL not set in .env")

    # Regex fix for special chars in password (e.g. Supabase passwords often have special chars)
    db_url = raw_url
    match = re.search(r"://([^:]+):([^@]+)@", raw_url)
    if match:
        user = match.group(1)
        password = match.group(2)
        encoded_pwd = quote_plus(password)
        if encoded_pwd != password:
            db_url = raw_url.replace(f":{password}@", f":{encoded_pwd}@")
            
    return psycopg2.connect(db_url)
