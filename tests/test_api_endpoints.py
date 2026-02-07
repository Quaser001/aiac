from fastapi.testclient import TestClient
from src.api.main import app
import unittest
import unittest.mock
import io

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        # Patch the Supabase wrapper to avoid "MOCK mode" prints during test execution
        # and to verify calls
        self.supabase_patcher = unittest.mock.patch("src.api.main.supabase")
        self.mock_supabase = self.supabase_patcher.start()
        self.client = TestClient(app)

    def tearDown(self):
        self.supabase_patcher.stop()

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertEqual(response.json()["status"], "operational")

    def test_analyze_genome_endpoint(self):
        # Create a dummy BLAST-like output file content
        # qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore,qlen,slen
        # Example hit: exact match to NDM-1
        dummy_content = "contig1\tNDM-1\t100.0\t800\t0\t0\t1\t800\t1\t800\t0.0\t1000\t800\t800"
        
        file_obj = io.BytesIO(dummy_content.encode('utf-8'))
        files = {'file': ('test.tsv', file_obj, 'text/tab-separated-values')}
        
        response = self.client.post("/analyze/genome", files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["overall_risk_level"], "HIGH")
        self.assertEqual(len(data["high_risk_details"]), 1)
        self.assertEqual(data["high_risk_details"][0]["gene"], "NDM-1")
        
        # Verify Audit Log was called
        self.assertTrue(self.mock_supabase.log_request.called)

if __name__ == '__main__':
    unittest.main()
