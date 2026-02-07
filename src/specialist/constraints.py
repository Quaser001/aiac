from typing import List, Dict, Any

class TherapeuticConstraints:
    """
    LAYER 2A: SPECIALIST ONLY
    Translates biological resistance mechanisms into chemical/physical constraints
    for drug discovery.
    """
    
    def derive_constraints(self, mechanism_ctx: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Returns a list of structured constraints based on mechanism.
        """
        constraints = []
        mech_class = mechanism_ctx.get("mechanism_class", "")
        
        if "Metallo-beta-lactamase" in mech_class:
            constraints.append({
                "type": "PHARMACOPHORE",
                "rule": "MUST_BIND_ZINC",
                "reason": "Active site requires zinc coordination for inhibition."
            })
            constraints.append({
                "type": "EXCLUSION",
                "rule": "NO_BETA_LACTAM_RING",
                "reason": "High hydrolysis rate by MBLs makes beta-lactams liable."
            })
            constraints.append({
                "type": "SCAFFOLD_SUGGESTION",
                "rule": "CONSIDER_SIDEROPHORE_CONJUGATE",
                "reason": "Trojan horse entry via iron transporters bypasses some resistance."
            })
        
        if "Serine-beta-lactamase" in mech_class:
            constraints.append({
                "type": "BINDING_MODE",
                "rule": "COVALENT_INHIBITOR",
                "reason": "Serine nucleophile allows for stable acyl-enzyme complex (e.g., Avibactam)."
            })

        if "Porin Loss" in mech_class:
            constraints.append({
                "type": "PHYSICOCHEMICAL",
                "rule": "MW_LIMIT_600",
                "reason": "Reduced pore size excludes large molecules."
            })
            constraints.append({
                "type": "PHYSICOCHEMICAL",
                "rule": "HIGH_POLARITY",
                "reason": "Remaining entry pathways often favor polar zwitterions."
            })
            
        return constraints
