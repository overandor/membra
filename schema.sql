-- MEMBRA Devnet Database Schema
-- This schema implements the MEMBRA Hybrid Architecture:
-- - Database is the canonical state
-- - Solana Devnet is the proof/training layer
-- - ProofBook bridges them

-- Agents table: stores agent profiles and status
CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL,
  solana_pubkey TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Agent wallets: stores Devnet wallet information
CREATE TABLE IF NOT EXISTS agent_wallets (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  cluster TEXT NOT NULL,
  public_key TEXT NOT NULL,
  encrypted_secret TEXT,
  fee_payer BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Tasks: stores task queue and job information
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  source TEXT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  reward_simulated_usd REAL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Skill tests: stores skill test results for graduation
CREATE TABLE IF NOT EXISTS skill_tests (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_name TEXT NOT NULL,
  test_prompt TEXT NOT NULL,
  scoring_rubric TEXT,
  result_json TEXT,
  score REAL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- ProofBook entries: stores proof hashes and Devnet anchors
CREATE TABLE IF NOT EXISTS proofbook_entries (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  task_id TEXT,
  proof_type TEXT NOT NULL,
  proof_json TEXT NOT NULL,
  proof_hash TEXT NOT NULL,
  solana_cluster TEXT DEFAULT 'devnet',
  solana_signature TEXT,
  explorer_url TEXT,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id),
  FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Devnet transactions: stores all Devnet transaction signatures
CREATE TABLE IF NOT EXISTS devnet_transactions (
  id TEXT PRIMARY KEY,
  agent_id TEXT,
  signature TEXT NOT NULL,
  action_type TEXT NOT NULL,
  request_json TEXT,
  response_json TEXT,
  explorer_url TEXT,
  confirmed BOOLEAN DEFAULT FALSE,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Graduation events: stores agent graduation records
CREATE TABLE IF NOT EXISTS graduation_events (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  skill_score REAL,
  uptime_score REAL,
  proof_count INTEGER,
  simulated_profit_usd REAL,
  status TEXT NOT NULL,
  proofbook_hash TEXT,
  solana_signature TEXT,
  explorer_url TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agent_wallets_agent_id ON agent_wallets(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_skill_tests_agent_id ON skill_tests(agent_id);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_agent_id ON proofbook_entries(agent_id);
CREATE INDEX IF NOT EXISTS idx_proofbook_entries_proof_hash ON proofbook_entries(proof_hash);
CREATE INDEX IF NOT EXISTS idx_devnet_transactions_agent_id ON devnet_transactions(agent_id);
CREATE INDEX IF NOT EXISTS idx_devnet_transactions_signature ON devnet_transactions(signature);
CREATE INDEX IF NOT EXISTS idx_graduation_events_agent_id ON graduation_events(agent_id);
