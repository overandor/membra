# SP_Graduation_Check

## Purpose
Check if an agent meets graduation requirements.

## Context
Graduation means the agent is ready for more advanced controlled tasks.
Graduation does NOT mean mainnet. Mainnet promotion requires LaunchPad approval.

## Graduation Requirements
- Minimum skill tests: GRADUATION_MIN_SKILL_TESTS (default: 5)
- Minimum average score: GRADUATION_MIN_AVG_SCORE (default: 0.80)
- Minimum task simulations: GRADUATION_MIN_TASK_SIMULATIONS (default: 3)
- Minimum proof anchors: GRADUATION_MIN_PROOF_ANCHORS (default: 3)
- Minimum simulated profit: GRADUATION_MIN_SIMULATED_PROFIT_USD (default: 100)

## Actions
1. Query agent skill test results
2. Query agent task execution history
3. Query agent ProofBook entries
4. Calculate average skill score
5. Count proof anchors
6. Sum simulated profit
7. Check all graduation requirements
8. Generate graduation report
9. Create graduation event record in database
10. Anchor graduation proof hash to Devnet (if requirements met)

## Guardrails
- Simulated profit marked as simulated
- No automatic mainnet promotion
- LaunchPad approval required for mainnet
- Database is source of truth
- Proof hash anchored if graduated

## Output
- Agent ID
- Skill test count
- Average skill score
- Task simulation count
- Proof anchor count
- Simulated profit total
- Graduation status (PASSED/FAILED)
- Missing requirements (if any)
- Graduation event ID
- Proof hash (if graduated)
- Devnet signature (if graduated)
- Explorer URL (if graduated)
