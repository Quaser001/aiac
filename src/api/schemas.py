from pydantic import BaseModel
from typing import List, Optional

class Finding(BaseModel):
    gene: str
    identity: float
    mechanism: str
    significance: str
    drug_class: str
    risk_tier: int

class RiskReport(BaseModel):
    overall_risk_level: str
    alert_message: str
    high_risk_details: List[Finding]
    drug_classes_implicated: List[str]

class HealthCheck(BaseModel):
    status: str
    version: str
    demo_mode: bool = False
