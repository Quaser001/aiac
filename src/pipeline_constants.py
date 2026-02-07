# ABRISK Pipeline Constants
MW_VERSION = "0.1.0"

# --- Gene Detection Thresholds ---
# We prioritize specificity over sensitivity to avoid "hallucinating" resistance.
MIN_IDENTITY_PERCENT = 95.0
MIN_COVERAGE_PERCENT = 90.0

# --- e-value Cutoffs ---
# Diamond/BLAST e-value thresholds
STRICT_E_VALUE = 1e-50
LOOSE_E_VALUE = 1e-5

# --- Structural Analysis parameters (Future) ---
# Distance in Angstroms to consider an atom "in contact"
CONTACT_THRESHOLD_ANGSTROM = 5.0

# --- India Context ---
# Placeholder for regional weighting factors
DEFAULT_REGION = "INDIA_NATIONAL"
