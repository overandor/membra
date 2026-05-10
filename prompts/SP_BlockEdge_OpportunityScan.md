# SP_BlockEdge_OpportunityScan

## Purpose
Scan for simulated blockchain opportunities using BlockEdge simulator.

## Context
BlockEdge is a Solana/Jito/MEV/alpha workflow simulator operating in:
- Devnet only
- Dry-run only
- Paper/simulated PnL only
- No mainnet
- No real funds
- No live trading
- No guaranteed profit claims

## Actions
1. Scan Devnet for simulated opportunities
2. Score candidate routes
3. Evaluate latency estimates
4. Estimate fee structures
5. Run simulated Devnet transactions
6. Log decision traces
7. Anchor proof hashes (optional)
8. Report simulated PnL
9. Generate risk reports

## Guardrails
- Devnet only
- Dry-run only
- No real user funds
- No mainnet transactions
- No risk-free arbitrage claims
- No bypassing protocol rules
- No graduation to live execution without LaunchPad

## Output
- Opportunity ID
- Route description
- Simulated PnL
- Risk score
- Latency estimate
- Fee estimate
- Decision trace
- Proof hash (if anchored)
- Risk report summary
