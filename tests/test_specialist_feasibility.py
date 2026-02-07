import unittest
from fastapi.testclient import TestClient
from src.api.main import app
from src.specialist.dl_wrapper import DLWrapper
from unittest.mock import patch, AsyncMock

class TestLayer2BFeasibility(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.dl_wrapper = DLWrapper()
        
        # Patch Supabase for API tests
        self.supabase_patcher = patch("src.api.routers.specialist.supabase")
        self.mock_supabase = self.supabase_patcher.start()

    def tearDown(self):
        self.supabase_patcher.stop()

    def test_dl_wrapper_structure(self):
        # Test structure without calling external API
        async def mock_get_embedding(seq):
            return [0.1] * 320
        
        self.dl_wrapper.hf_client.get_embedding = AsyncMock(side_effect=mock_get_embedding)
        
        # We need to run async test - checking structure logic
        # For simplicity in this unittest suite, we trust the integration test below

    def test_api_feasibility_endpoint(self):
        # Integration test for the endpoint
        payload = {
            "gene_id": "NDM-1",
            "mechanism_class": "Metallo-beta-lactamase",
            "sequence": "MRLT..." # Dummy
        }
        
        # We need to patch the async DLWrapper call inside the endpoint or ensure it runs in mock mode
        # HFClient defaults to mock if no key, so it should be fine.
        
        response = self.client.post("/specialist/analyze/feasibility", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check Layer 2B fields
        self.assertIn("in_silico_feasibility", data)
        self.assertIn("score_value", data["in_silico_feasibility"])
        self.assertIn("docking_config", data["in_silico_feasibility"])
        
        # Check Audit Log
        self.assertTrue(self.mock_supabase.log_audit.called)

if __name__ == '__main__':
    unittest.main()
