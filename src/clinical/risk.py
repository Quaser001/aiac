from typing import List, Dict, Any, Optional
from src.clinical.mechanism import MechanismMapper

class RiskStratifier:
    """
    Evaluates the risk of a set of identified genes.
    """

    def __init__(self):
        self.mapper = MechanismMapper()

    def stratify_risk(self, hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of valid hits from GeneParser and produces a Risk Report.
        
        Args:
            hits: List of dictionaries containing gene hit info.

        Returns:
            Risk Report dictionary.
        """
        high_risk_findings = []
        moderate_risk_findings = []
        detected_drug_classes = set()

        for hit in hits:
            finding = self._analyze_hit(hit)
            if finding:
                detected_drug_classes.add(finding["drug_class"])
                if finding["risk_tier"] == 1:
                    high_risk_findings.append(finding)
                elif finding["risk_tier"] == 2:
                    moderate_risk_findings.append(finding)

        return self._generate_report(high_risk_findings, moderate_risk_findings, detected_drug_classes)

    def _analyze_hit(self, hit: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyzes a single gene hit to determine its significance.
        """
        gene_id = hit.get("sseqid", "")
        mech_info = self.mapper.lookup_gene(gene_id)

        if not mech_info:
            return None

        return {
            "gene": gene_id,
            "identity": hit["pident"],
            "mechanism": mech_info["mechanism"],
            "significance": mech_info["significance"],
            "drug_class": mech_info["drug_class"],
            "risk_tier": mech_info["risk_tier"]
        }

    def _generate_report(self, high_risk: List[Dict], moderate_risk: List[Dict], drug_classes: set) -> Dict[str, Any]:
        """
        Constructs the final risk report dictionary.
        """
        # Determine Overall Risk Level
        if high_risk:
            overall_risk = "HIGH"
            main_alert = f"Detected {len(high_risk)} high-priority resistance mechanisms."
        elif moderate_risk:
            overall_risk = "MODERATE"
            main_alert = "Detected potential resistance variants."
        else:
            overall_risk = "LOW"
            main_alert = "No high-priority resistance genes detected in this panel."

        return {
            "overall_risk_level": overall_risk,
            "alert_message": main_alert,
            "high_risk_details": high_risk,
            "drug_classes_implicated": list(drug_classes)
        }
