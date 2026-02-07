-- CARD Schema Design
-- Goal: Normalize flat CARD data into relational structure for Layer 1/2 reasoning.

-- 1. Source Metadata (Provenance)
CREATE TABLE IF NOT EXISTS card_metadata (
    id SERIAL PRIMARY KEY,
    dataset_version TEXT NOT NULL,
    ingestion_date TIMESTAMP DEFAULT NOW(),
    source_url TEXT
);

-- 2. Resistance Mechanisms (Normalized)
-- E.g. "antibiotic efflux", "antibiotic inactivation"
CREATE TABLE IF NOT EXISTS resistance_mechanisms (
    id SERIAL PRIMARY KEY,
    mechanism_name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 3. Drug Classes (Normalized)
-- E.g. "aminoglycoside", "carbapenem"
CREATE TABLE IF NOT EXISTS drug_classes (
    id SERIAL PRIMARY KEY,
    class_name TEXT UNIQUE NOT NULL
);

-- 4. Gene Families (Normalized)
-- E.g. "NDM beta-lactamase", "KPC beta-lactamase"
CREATE TABLE IF NOT EXISTS gene_families (
    id SERIAL PRIMARY KEY,
    family_name TEXT UNIQUE NOT NULL
);

-- 5. Resistance Genes (Core Table)
-- Stores the specific ARO terms and mapped sequences.
CREATE TABLE IF NOT EXISTS resistance_genes (
    aro_accession TEXT PRIMARY KEY, -- e.g. "3003550"
    gene_symbol TEXT NOT NULL,      -- e.g. "NDM-1"
    gene_name TEXT,                 -- Full name
    family_id INTEGER REFERENCES gene_families(id),
    mechanism_id INTEGER REFERENCES resistance_mechanisms(id),
    
    -- Embeddings / Sequence Info (for Layer 2B later)
    -- sequence TEXT, -- Reserved for future
    
    -- Metadata
    card_short_name TEXT,
    model_type TEXT, -- "protein homolog", "protein variant", etc.
    deprecated BOOLEAN DEFAULT FALSE
);

-- 6. Many-to-Many: Genes form Multi-Drug Resistance
-- A single gene can confer resistance to multiple drug classes.
CREATE TABLE IF NOT EXISTS gene_drug_class_links (
    aro_accession TEXT REFERENCES resistance_genes(aro_accession),
    drug_class_id INTEGER REFERENCES drug_classes(id),
    PRIMARY KEY (aro_accession, drug_class_id)
);

-- Indexes for Performance (Layer 1 Queries)
CREATE INDEX IF NOT EXISTS idx_genes_symbol ON resistance_genes(gene_symbol);
CREATE INDEX IF NOT EXISTS idx_genes_mechanism ON resistance_genes(mechanism_id);
