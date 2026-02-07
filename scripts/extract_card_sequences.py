import re
import os

# Target determinants requested by the user
TARGETS = [
    "NDM-1", "KPC-2", "OXA-48", "mecA", "vanA", "vanB", 
    "MexB", "AcrB", "AAC(6')", "APH(3')", "CTX-M-15", 
    "TEM-1", "SHV-1", "mcr-1", "ermB", "tetA", "qnrS1"
]

# Mappings for specific edge cases based on common CARD naming
ALIASES = {
    "tetA": "tet(A)",
    "ermB": "ErmB", 
    "AAC(6')": "AAC(6')-Ib", # Common representative
    "APH(3')": "APH(3')-Ia", # Common representative
    "mcr-1": "MCR-1.1"
}

# Base dir is the project root, assuming script is in scripts/
BASE_DIR = r"c:/Users/asef6/OneDrive/Desktop/2026/AIAIC"
INPUT_FILES = [
    os.path.join(BASE_DIR, "data/raw/protein_fasta_protein_homolog_model_variants.fasta"),
    os.path.join(BASE_DIR, "data/raw/protein_fasta_protein_variant_model_variants.fasta")
]
OUTPUT_FILE = os.path.join(BASE_DIR, "data/sequences/reference_bank_20.fasta")

def parse_fasta(filepath):
    """Yields (header, sequence) tuples from a FASTA file."""
    header = None
    sequence = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    if header:
                        yield header, "".join(sequence)
                    header = line
                    sequence = []
                else:
                    sequence.append(line)
            if header:
                yield header, "".join(sequence)
    except FileNotFoundError:
        print(f"File not found: {filepath}")

def extract_sequences():
    found_sequences = {}
    
    # helper to normalize names for comparison
    def matches_target(header_dict, target):
        # Check ARO Name and CARD Short Name
        aro_name = header_dict.get('ARO_Name', '')
        short_name = header_dict.get('CARD_Short_Name', '')
        
        # Exact match
        if target.lower() == aro_name.lower() or target.lower() == short_name.lower():
            return True
        
        # Check aliases
        if target in ALIASES:
            alias = ALIASES[target]
            if alias.lower() == aro_name.lower() or alias.lower() == short_name.lower():
                return True
        
        # substring check for some (be careful)
        if target in ["AAC(6')", "APH(3')"]:
             if target.lower() in aro_name.lower():
                 return True
                 
        return False

    # First pass: try to find all targets
    print(f"Scanning files...")
    
    for filepath in INPUT_FILES:
        print(f"Reading {filepath}...")
        for header, sequence in parse_fasta(filepath):
            # Parse header
            # >Prevalence_Sequence_ID:1|ARO_Name:qacG|ARO:3007015|Detection_Model:Protein Homolog Model|CARD_Short_Name:qacG
            parts = header[1:].split('|')
            header_data = {}
            for part in parts:
                if ':' in part:
                    key, val = part.split(':', 1)
                    header_data[key.strip()] = val.strip()
            
            # Check against targets
            for target in TARGETS:
                if target not in found_sequences:
                    if matches_target(header_data, target):
                        found_sequences[target] = {
                            'header': header,
                            'original_header_data': header_data,
                            'sequence': sequence,
                            'target_name': target
                        }
    
    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    print(f"\nWriting sequences to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as out:
        for target in TARGETS:
            if target in found_sequences:
                data = found_sequences[target]
                aro_id = data['original_header_data'].get('ARO', 'Unknown')
                # Format: >Determinant_Name | CARD_ARO_ID
                new_header = f">{target} | {aro_id}"
                out.write(f"{new_header}\n{data['sequence']}\n")
                print(f"Exported: {target:<15} Length: {len(data['sequence'])}")
            else:
                print(f"MISSING: {target}")

if __name__ == "__main__":
    extract_sequences()
