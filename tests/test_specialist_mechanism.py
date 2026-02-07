import unittest
from fastapi.testclient import TestClient
from src.api.main import app
from src.specialist.mechanism_engine import MechanismEngine
from src.specialist.constraints import TherapeuticConstraints
from unittest.mock import patch

class TestLayer2AMechanism(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.mech_engine = MechanismEngine()
        self.constraint_logic = TherapeuticConstraints()
        
        # Patch Supabase for API tests
        self.supabase_patcher = patch("src.api.routers.specialist.supabase")
        self.mock_supabase = self.supabase_patcher.start()

    def tearDown(self):
        self.supabase_patcher.stop()

    def test_mechanism_logic_ndm(self):
        # Deterministic check for NDM-1
        ctx = self.mech_engine.analyze_mechanism("NDM-1", "Metallo-beta-lactamase")
        self.assertIn("Metallo-beta-lactamase", ctx["mechanism_class"])
        self.assertIn("Zinc-dependent", ctx["structural_impact"])

    def test_constraint_logic_ndm(self):
        # Check constraints for MBL
        ctx = {"mechanism_class": "Metallo-beta-lactamase"}
        constraints = self.constraint_logic.derive_constraints(ctx)
        
        self.assertTrue(any(c["rule"] == "MUST_BIND_ZINC" for c in constraints))
        self.assertTrue(any(c["rule"] == "NO_BETA_LACTAM_RING" for c in constraints))

    def test_api_mechanism_endpoint(self):
        # Test the API wrapper
        payload = {"gene_id": "NDM-1", "family": "Metallo-beta-lactamase"}
        response = self.client.post("/specialist/analyze/mechanism", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check structure
        self.assertIn("mechanism", data)
        self.assertIn("constraints", data)
        self.assertIn("disclaimer", data)
        
        # Check Disclaimer content
        self.assertIn("RESEARCH", data["disclaimer"])
        
        # Check Audit Log was called
        self.assertTrue(self.mock_supabase.log_audit.called)

if __name__ == '__main__':
    unittest.main()
