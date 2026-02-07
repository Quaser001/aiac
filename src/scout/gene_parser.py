import pandas as pd
from typing import List, Dict, Any
from src.pipeline_constants import MIN_IDENTITY_PERCENT, MIN_COVERAGE_PERCENT

class GeneParser:
    """
    Parses and filters raw alignment results (e.g., from Diamond or BLAST).
    Enforces strict identity and coverage thresholds to prevent 'hallucinations'.
    """

    def __init__(self):
        self.min_identity = MIN_IDENTITY_PERCENT
        self.min_coverage = MIN_COVERAGE_PERCENT

    def parse_tabular_output(self, file_path: str, columns: List[str] = None) -> List[Dict[str, Any]]:
        """
        Parses a tabular BLAST-like output file.
        Assumes standard columns if not provided: qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore, qlen, slen
        
        Args:
            file_path: Path to the tabular output file.
            columns: List of column names.

        Returns:
            List of dictionaries representing valid hits.
        """
        if columns is None:
            # Standard blast fmt6 + qlen + slen recommended
            columns = [
                "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", 
                "qstart", "qend", "sstart", "send", "evalue", "bitscore", "qlen", "slen"
            ]

        try:
            df = pd.read_csv(file_path, sep='\t', names=columns)
        except FileNotFoundError:
            return []
        except pd.errors.EmptyDataError:
            return []

        # Calculate coverage if qlen/slen are present
        # Coverage = Alignment Length / Reference Length (slen)
        if "length" in df.columns and "slen" in df.columns:
            df["coverage"] = (df["length"] / df["slen"]) * 100
        else:
            # If coverage cannot be calculated, assume 0 for safety (strict mode)
            df["coverage"] = 0.0

        return self.filter_hits(df)

    def filter_hits(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Filters hits based on strict identity and coverage thresholds.
        """
        valid_hits = df[
            (df["pident"] >= self.min_identity) & 
            (df["coverage"] >= self.min_coverage)
        ]
        
        return valid_hits.to_dict(orient="records")

    def classify_variant(self, hit: Dict[str, Any]) -> str:
        """
        Classifies a hit as KNOWN_RESISTANCE or PUTATIVE_VARIANT
        """
        # Redundant check, but good for explicit logic
        if hit["pident"] >= self.min_identity and hit.get("coverage", 0) >= self.min_coverage:
            return "KNOWN_RESISTANCE"
        return "BELOW_THRESHOLD"
