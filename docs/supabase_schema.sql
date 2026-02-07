-- ABRISK Supabase Schema
-- Phase 7: Engineering Architecture

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Request Logs
-- Tracks every analysis request for auditability and lineage.
create table public.request_logs (
  id uuid primary key default uuid_generate_v4(),
  timestamp timestamptz default now(),
  user_id uuid references auth.users(id), -- Nullable if anonymous access allowed initially
  input_hash text not null, -- Short hash of the input file/sequence for deduplication logic
  risk_level text not null, -- HIGH, MODERATE, LOW
  model_version text not null, -- Captured from app version
  metadata jsonb -- Stores full Finding details if needed (careful with size)
);

-- 2. Audit Trails (Governance)
-- Logs system actions, errors, or critical overrides.
create table public.audit_trails (
  id uuid primary key default uuid_generate_v4(),
  timestamp timestamptz default now(),
  actor text not null, -- 'SYSTEM', 'USER', 'ADMIN'
  action text not null, -- 'ANALYZE', 'OVERRIDE', 'ERROR'
  details text,
  severity text default 'INFO' -- 'INFO', 'WARNING', 'CRITICAL'
);

-- 3. Row Level Security (RLS) policies would go here.
-- For now, we assume service role access for the backend.
alter table public.request_logs enable row level security;
alter table public.audit_trails enable row level security;
