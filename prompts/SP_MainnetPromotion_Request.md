# SP_MainnetPromotion_Request

## Purpose
Request mainnet promotion for a graduated agent through LaunchPad.

## Context
Mainnet promotion requires:
1. Explicit human approval
2. Risk review
3. Compliance review
4. Budget limit
5. Kill switch
6. Credential rotation
7. Separate mainnet wallet
8. Separate environment file
9. Live execution checklist
10. Signed promotion record in ProofBook

## Actions
1. Verify agent graduation status
2. Generate promotion request package
3. Include skill test results
4. Include task execution history
5. Include ProofBook evidence
6. Include simulated profit history
7. Include risk assessment
8. Generate promotion request JSON
9. Submit for human review
10. Await approval

## Guardrails
- MAINNET_PROMOTION_REQUIRES_HUMAN_APPROVAL must be true
- Agent must be graduated
- All graduation requirements must be met
- Separate mainnet wallet required
- Separate environment file required
- No automatic promotion

## Output
- Agent ID
- Graduation status
- Promotion request ID
- Request package (JSON)
- Review status
- Required approvals
- Missing items (if any)
