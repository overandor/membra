# SP_TaskExecution_Devnet

## Purpose
Execute a task on Solana Devnet with full database persistence.

## Context
Task execution follows the MEMBRA Devnet Action Chain:
Prompt → Policy Guardrail Check → Action Plan → Simulated Execution → Database Pending Record → Deliverable or Result → Proof JSON → Canonical Proof Hash → Optional Devnet Anchor → Transaction Signature → Database Signature Update → ProofBook Entry → WatchTower Report → Replay-Ready State

## Actions
1. Enforce devnet guardrails
2. Load task from database
3. Create database pending record
4. Execute task in simulated/dry-run mode
5. Generate deliverable or result
6. Create proof JSON
7. Generate canonical proof hash
8. Optional: Anchor proof hash to Devnet memo transaction
9. Save transaction signature to database
10. Update database record with result
11. Create ProofBook entry
12. Generate WatchTower report

## Guardrails
- enforce_membra_devnet_doctrine() must pass
- Database state written first as pending
- Devnet transaction only if enabled
- Signature saved to database
- Proof hash reproducible from database
- Explorer URL saved

## Output
- Task ID
- Execution status
- Deliverable/result
- Proof hash
- Devnet signature (if anchored)
- Explorer URL (if anchored)
- Database record IDs
- ProofBook entry ID
- WatchTower report summary
