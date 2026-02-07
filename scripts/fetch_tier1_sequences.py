import json
import requests
import time

ACCESSION_FILE = "data/tier1_accessions.json"
OUT_FASTA = "data/tier1_sequences.fasta"

def fetch_fasta(uniprot_id: str) -> str:
    # Adding a small delay to be nice to the API if running in a loop
    time.sleep(0.5) 
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    print(f"  GET {url}")
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError(f"Failed UniProt fetch: {uniprot_id} (Status: {r.status_code})")
    return r.text.strip()

def main():
    print(f"Loading accessions from {ACCESSION_FILE}...")
    with open(ACCESSION_FILE) as f:
        accs = json.load(f)

    fasta_blocks = []
    print("Fetching sequences from UniProt...")
    
    for gene, uid in accs.items():
        print(f"Fetching {gene} -> {uid}")
        try:
            fasta = fetch_fasta(uid)
            
            # Rewrite header to be deterministic and match our gene name
            lines = fasta.splitlines()
            if lines:
                # Format: >GeneName|UniProt:ID OriginalHeader
                original_header = lines[0]
                lines[0] = f">{gene}|UniProt:{uid} {original_header[1:]}"
                fasta_blocks.append("\n".join(lines))
                print(f"  ✓ Success ({len(''.join(lines[1:]))} aa)")
        except Exception as e:
            print(f"  X Error: {e}")

    with open(OUT_FASTA, "w") as out:
        out.write("\n\n".join(fasta_blocks))

    print(f"Done. Wrote {len(fasta_blocks)} sequences to {OUT_FASTA}")

if __name__ == "__main__":
    main()
