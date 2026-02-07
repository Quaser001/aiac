from src.specialist.mechanism_engine import MechanismEngine

def test_engine():
    engine = MechanismEngine()
    print("--- Testing NDM-1 Lookup ---")
    result = engine.analyze_mechanism("NDM-1", "Metallo-beta-lactamase")
    print(result)

if __name__ == "__main__":
    test_engine()
