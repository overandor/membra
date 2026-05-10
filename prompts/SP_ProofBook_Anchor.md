# SP_ProofBook_Anchor

## Purpose
Anchor a proof hash to Solana Devnet via memo transaction.

## Context
ProofBook bridges database canonical state to Devnet proof layer:
Database record → canonical JSON → SHA-256 proof hash → Devnet memo anchor → saved transaction signature → explorer URL

## Actions
1. Load proof entry from database
2. Verify proof hash is reproducible
3. Generate memo payload: MEMBRA:v1:proofbook:{entry_id}:{hash_value}
4. Create Devnet memo transaction
5. Sign transaction with agent or platform fee payer
6. Submit to Solana Devnet
7. Wait for confirmation
8. Save transaction signature to database
9. Generate explorer URL
10. Update ProofBook entry with signature and URL

## Guardrails
- Devnet only (enforce_devnet_only)
- No real funds (assert_no_real_funds)
- Platform fee payer if AGENT_FEE_PAYER_MODE=platform
- Signature must be saved to database
- Hash must be reproducible

## Output
- ProofBook entry ID
- Proof hash
- Memo payload
- Transaction signature
- Explorer URL
- Confirmation status
- Database update status
