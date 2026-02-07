import unittest
from src.scout.gene_parser import GeneParser
from src.intelligence.risk import RiskStratifier

class TestRiskLogic(unittest.TestCase):

    def setUp(self):
        self.parser = GeneParser()
        self.stratifier = RiskStratifier()

    def test_parser_filtering(self):
        # Mocking a DataFrame-like list of dicts for simplicity or testing the filter directly
        # Here we test the classify_variant logic
        high_id_hit = {"pident": 100.0, "coverage": 100.0, "sseqid": "NDM-1"}
        low_id_hit = {"pident": 80.0, "coverage": 100.0, "sseqid": "NDM-1"}
        
        self.assertEqual(self.parser.classify_variant(high_id_hit), "KNOWN_RESISTANCE")
        self.assertEqual(self.parser.classify_variant(low_id_hit), "BELOW_THRESHOLD")

    def test_risk_stratification_high_risk(self):
        # Simulator a hit that passed the parser
        hits = [
            {"sseqid": "blaNDM-1", "pident": 99.0, "coverage": 100.0}
        ]
        
        report = self.stratifier.stratify_risk(hits)
        
        self.assertEqual(report["overall_risk_level"], "HIGH")
        self.assertIn("Carbapenems", report["drug_classes_implicated"])
        self.assertTrue("NDM-1" in report["high_risk_details"][0]["gene"] or "blaNDM-1" in report["high_risk_details"][0]["gene"])

    def test_risk_stratification_clean_sample(self):
        hits = []
        report = self.stratifier.stratify_risk(hits)
        self.assertEqual(report["overall_risk_level"], "LOW")

if __name__ == '__main__':
    unittest.main()
