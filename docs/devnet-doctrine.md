# MEMBRA DEVNET DOCTRINE

## Default Operating Environment

Solana Devnet.

## Core Rules

1. No mainnet by default.
2. No real SOL by default.
3. No real customer funds by default.
4. No live trading by default.
5. No irreversible agent action without explicit promotion.
6. No agent graduates directly into mainnet execution.
7. The database is the source of truth.
8. Solana Devnet is the proof, simulation, credential, and training layer.

## Technical Framing

MEMBRA uses real Solana Devnet transactions, real signatures, real wallets, real proof anchors, and real replay logic.
MEMBRA does not use real-money SOL by default.
Transaction fees still exist technically, but they are paid with fake Devnet SOL obtained through developer airdrop/faucet methods.

## User-Facing Phrase

User-gasless Devnet mode.

## Technical Phrase

Platform-sponsored Devnet transaction mode.

## Meaning

The platform or agent wallet pays Devnet transaction fees using fake/test SOL.
The user does not pay real SOL.
The database preserves canonical state.
Devnet stores proof anchors, not the complete application database.

## MEMBRA HYBRID ARCHITECTURE

### Canonical State
Postgres, SQLite, or Supabase.

### Proof/Training Layer
Solana Devnet.

### Verification Bridge
ProofBook.

### Agent Lifecycle Layer
SkillOS.

### Monitoring Layer
WatchTower.

### Promotion Layer
LaunchPad.

### Blockchain Workflow Simulator
BlockEdge.

## Rule

Do not store the whole MEMBRA database on-chain.

### Database Stores
- agent profiles
- agent wallets
- skill tests
- task queue
- job attempts
- deliverables
- proof files
- prompt logs
- simulated profit
- audit events
- graduation reports
- Devnet transaction signatures

### Solana Devnet Stores
- proof hash anchors
- memo transactions
- agent public key references
- task proof IDs
- simulated settlement records
- credential mint or test-token references
- graduation badge anchors

### ProofBook Connection
Database record → canonical JSON → SHA-256 proof hash → Devnet memo anchor → saved transaction signature → explorer URL.

## DATABASE PRESERVATION MODEL

The database is the source of truth.

### Rule 1
Never rely on Solana Devnet as permanent storage.

### Rule 2
Every Devnet transaction signature must be saved in the database.

### Rule 3
Every proof hash must be reproducible from the database record.

### Rule 4
If Devnet resets, the database can replay proof anchors.

### Rule 5
If the database is lost, Devnet is not enough to reconstruct the system.

### Rule 6
Every mutation writes database state first as pending.

### Rule 7
Every chain action updates the database after signature.

### Rule 8
Every failed chain action remains in the database as failed.

### Rule 9
Every replay starts from the database, not from prompt memory.

## MEMBRA DEVNET ACTION CHAIN

Prompt → Policy Guardrail Check → Action Plan → Simulated Execution → Database Pending Record → Deliverable or Result → Proof JSON → Canonical Proof Hash → Optional Devnet Anchor → Transaction Signature → Database Signature Update → ProofBook Entry → WatchTower Report → Replay-Ready State

## USER-GASLESS DEVNET MODE

User-gasless Devnet mode means:
- the user pays no real SOL
- agents use fake/test Devnet SOL
- the platform may sponsor Devnet transaction fees
- transaction signatures are still real Devnet signatures
- ProofBook still records cryptographic proof anchors
- database records remain canonical

## MEMBRA FEE MODEL

### Mode 1 — User Pays
Not recommended for MEMBRA training.

### Mode 2 — Agent Pays From Devnet Airdrop
Good for isolated training.

### Mode 3 — Platform Devnet Fee Payer Sponsors Transactions
Best UX and default MEMBRA mode.

**Default:** `AGENT_FEE_PAYER_MODE=platform`

**Meaning:**
Agent acts.
Platform Devnet wallet pays test fee.
User experiences the workflow as gasless.
ProofBook records the action.
Database saves the signature.

## LAUNCHPAD MAINNET PROMOTION POLICY

Graduation does not mean mainnet.
Graduation means the agent is ready for more advanced controlled tasks.

### Mainnet Promotion Requires
1. explicit human approval
2. risk review
3. compliance review
4. budget limit
5. kill switch
6. credential rotation
7. separate mainnet wallet
8. separate environment file
9. live execution checklist
10. signed promotion record in ProofBook

### Default
```
ALLOW_MAINNET=false
ALLOW_REAL_FUNDS=false
ALLOW_LIVE_TRADING=false
DRY_RUN=true
```

## FINAL MEMBRA DEVNET DOCTRINE

MEMBRA trains every agent on Solana Devnet first.
Every Membra agent gets a Devnet wallet at birth.
Every training action is logged in the database.
Every important proof is hashed.
Every proof hash can be anchored on Solana Devnet.
Every Devnet signature is saved back to the database.
Every simulated profit claim is marked as simulated.
Every graduation event requires ProofBook evidence.
Every mainnet promotion requires explicit LaunchPad approval.
Devnet provides real transaction mechanics without real-money exposure.
The database preserves canonical state.
ProofBook proves work.
WatchTower monitors execution.
SkillOS certifies ability.
BlockEdge simulates blockchain opportunity workflows.
LaunchPad controls promotion.
Mainnet is a promotion, not a default.

## BLOCKEDGE DEVNET DOCTRINE

BlockEdge is a Solana/Jito/MEV/alpha workflow simulator.

### Default Mode
- Devnet only
- dry-run only
- paper/simulated PnL only
- no mainnet
- no real funds
- no live trading
- no guaranteed profit claims

### BlockEdge May
- scan simulated opportunities
- score candidate routes
- evaluate latency
- estimate fees
- run Devnet transactions
- log decision traces
- anchor proof hashes
- report simulated PnL
- produce risk reports

### BlockEdge May Not
- use real user funds by default
- execute mainnet transactions by default
- imply risk-free arbitrage
- hide failed simulations
- bypass protocol or platform rules
- graduate into live execution without LaunchPad approval
