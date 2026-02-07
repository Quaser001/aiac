import os
from supabase import create_client, Client
from datetime import datetime
import json

class SupabaseClientWrapper:
    """
    Wrapper around the official Supabase client.
    Handles connection and provides helper methods for ABRISK specific logs.
    """
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        self.client: Client = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Failed to initialize Supabase client: {e}")
        else:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not set. Running in MOCK mode.")

    def log_request(self, input_hash: str, risk_level: str, model_version: str, metadata: dict = None):
        """
        Logs an API request to the 'request_logs' table.
        """
        payload = {
            "timestamp": datetime.now().isoformat(),
            "input_hash": input_hash,
            "risk_level": risk_level,
            "model_version": model_version,
            "metadata": metadata or {}
        }
        
        if self.client:
            try:
                self.client.table("request_logs").insert(payload).execute()
            except Exception as e:
                print(f"Error writing to Supabase: {e}")
        else:
            # Mock mode: print to stdout for verification
            print(f"[Supabase Mock] Insert request_logs: {json.dumps(payload)}")

    def log_audit(self, actor: str, action: str, details: str, severity: str = "INFO"):
        """
        Logs a system action to 'audit_trails'.
        """
        payload = {
            "timestamp": datetime.now().isoformat(),
            "actor": actor,
            "action": action,
            "details": details,
            "severity": severity
        }
        
        if self.client:
            try:
                self.client.table("audit_trails").insert(payload).execute()
            except Exception as e:
                print(f"Error writing to Supabase: {e}")
        else:
            print(f"[Supabase Mock] Insert audit_trails: {json.dumps(payload)}")
