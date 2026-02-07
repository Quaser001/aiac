
"""
Script for Generating REAL ESM-2 Embeddings (For Colab/GPU Machine)
Run this offline to populate data/cache/embeddings/ with real biological vectors if needed.
"""
import torch
import esm
import os
import json
import hashlib

# Install: pip install fair-esm torch

DEMO_SEQUENCES = {
    "NDM-1": "MELPNIMHPVAKLSTALAAALMLSGCMPGEIRPTIGQQMETGDQRFGDLVFRQLAPNVWQHTSYLDMPGFGAVASNGLIVRDGGRVLVVDTAWTDDQTAQILNWIKQEINLPVALAVVTHAHQDKMGGMDALHAAGIATYANALSNQLAPQEGMVAAQHSLTFAANGWVEPATAPNFGPLKVFYPGPGHTSDNITVGIDGTDIAFGGCLIKDSKAKSLGNLGDADTEHYAASARAFGAAFPKASMIVMSHSAPDSRAAITHTARMADKLR",
    "KPC-2": "MSLYRRLVLLSCLSWPLAGFSATALTNLVAEPFAKLEQDFGGSIGVYAMDTGSGATVSYRAEERFPLCSSFKGFLAAAVLERSQQAGVDVAYLEKKATGVNAERIGASRPTDTPFGWKTGRRGMAAVRQASVTVYPPEAPTGRTVVLTDDMGDQQVDFLRENSNVVLAVAGGIDGKRLSIAQALWCPPYIGLATGGGSSAKDEEELASIQKRGLLDLALPGCPRRPTEEVKIEIVPAAEKQAAVAIGGLIAQGLKAGPLGLWVDGTPTGQG"
}

# 10 Demo Mutations (Determinant, Mutation Code)
DEMO_VARIANTS = [
    ("NDM-1", "H122Y"), # Active site
    ("NDM-1", "K211R"), # Distal
    ("NDM-1", "C208S"), # Zinc binding
    ("NDM-1", "D124N"), # Active site
    ("KPC-2", "C69Y"),  # Disulfide bridge
    ("KPC-2", "R220K"), # Loops
    ("mecA", "P108L"),  # PBP2a
    ("mecA", "E150K"),  # Surface
    ("vanA", "H244A"),  # Ligand binding
    ("MexB", "G45A")  # Transmembrane
]

def mutate_sequence(seq, mutation_str):
    try:
        wt = mutation_str[0]
        mut = mutation_str[-1]
        pos = int(mutation_str[1:-1])
        if seq[pos-1] != wt:
            print(f"Values mismatch for {mutation_str}: Expected {wt} found {seq[pos-1]}")
            return None
        return seq[:pos-1] + mut + seq[pos:]
    except Exception as e:
        print(f"Mutation error {mutation_str}: {e}")
        return None

def generate_real_embeddings():
    print("Loading ESM-2 Model (esm2_t6_8M_UR50D)...")
    # Using small model for colab free tier speed
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()

    output_dir = "data/cache/embeddings"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Process Reference Sequences
    tasks = []
    for name, seq in DEMO_SEQUENCES.items():
        tasks.append((name, seq))
        
    # 2. Process Mutants
    # Note: Need sequences for others not in DEMO_SEQUENCES if requested?
    # For this script we rely on DEMO_SEQUENCES strings.
    # If user wants mecA/vanA/etc, they should add them to DEMO_SEQUENCES map first.
    # We will assume user populates DEMO_SEQUENCES fully.
    
    for det, mut_code in DEMO_VARIANTS:
        if det in DEMO_SEQUENCES:
            wt_seq = DEMO_SEQUENCES[det]
            mut_seq = mutate_sequence(wt_seq, mut_code)
            if mut_seq:
                tasks.append((f"{det}_{mut_code}", mut_seq)) # E.g. NDM-1_H122Y.npy

    print(f"Processing {len(tasks)} sequences...")

    for name, seq in tasks:
        data = [(name, seq)]
        batch_labels, batch_strs, batch_tokens = batch_converter(data)

        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[6], return_contacts=False)
        
        # Extract per-residue representations (on layer 6)
        token_representations = results["representations"][6]

        # Generate per-sequence representation via averaging
        sequence_representation = token_representations[0, 1 : len(seq) + 1].mean(0)
        
        vec = sequence_representation.tolist()
        
        # Save by NAME (npy) - Improved for Real Integration
        import numpy as np
        np.save(os.path.join(output_dir, f"{name}.npy"), np.array(vec))
        
        # Also Save by Hash (Legacy fallback)
        seq_hash = hashlib.sha256(seq.encode()).hexdigest()
        with open(os.path.join(output_dir, f"{seq_hash}.json"), "w") as f:
            json.dump(vec, f)
            
        print(f"Saved {name} (.npy) and {seq_hash[:8]} (.json)")

if __name__ == "__main__":
    generate_real_embeddings()
