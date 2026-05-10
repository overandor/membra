# SP_SkillTest_Run

## Purpose
Execute a skill test for a MEMBRA agent and record results.

## Context
Skill tests are required for agent graduation. Tests evaluate:
- Task execution capability
- Proof generation quality
- Devnet transaction handling
- Database record accuracy

## Actions
1. Load skill test definition
2. Present test prompt to agent
3. Execute test in simulated/dry-run mode
4. Collect agent response and deliverables
5. Score response against rubric
6. Generate proof JSON for test result
7. Hash proof and anchor to Devnet (optional)
8. Save test result to database
9. Update agent skill score

## Guardrails
- Dry-run only by default
- No live trading
- Score must be 0.0-1.0
- Proof hash must be reproducible
- Database is source of truth

## Output
- Test ID
- Agent ID
- Skill name
- Test score (0.0-1.0)
- Proof hash
- Devnet signature (if anchored)
- Explorer URL (if anchored)
- Database record ID
