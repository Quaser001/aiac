
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.models.mutation_impact import MutationImpactScorer

def test_ndm1_h122y():
    print("Testing NDM-1 H122Y Impact Score...")
    scorer = MutationImpactScorer()
    
    # Ensure env var is set or warn
    if not os.getenv("HF_API_KEY"):
        print("WARNING: HF_API_KEY not set. Using mock/fallback logic.")
        
    result = scorer.calculate_score("NDM-1", "H122Y")
    print(f"Result: {result}")
    
    if "error" in result:
        print("FAILED: Error returned.")
        sys.exit(1)
        
    if result["impact_score"] < 0 or result["impact_score"] > 1:
        print("FAILED: Score out of range.")
        sys.exit(1)
        
    print("SUCCESS: Scoring module operational.")

if __name__ == "__main__":
    test_ndm1_h122y()
