# EnMaTeS System Overview

This directory contains the system overview for the EnMaTeS Overworker/49 AgentOps architecture.

## Architecture

The EnMaTeS system operates with four layers:

1. **Entrepreneurial Layer** - Defines market opportunity, product direction, and strategic value
2. **Managerial Layer** - Transforms intent into milestones, task queues, and verification loops
3. **Technological Layer** - Builds actual software: repo, code, database, APIs, UI, tests, deployment
4. **Profit Layer** - Turns working software into monetizable asset through pricing, packaging, and revenue-path design

## Components

- System Instruction (SI): SMF + FPM + FPS + PIC
- Initiation Package (IP): SG + SDA + SP + UM
- ChatConfig: Declares which SI + IP components compose each agent
- Running Agent: Loads ChatConfig → assembles SI → loads IP → retrieves SG nodes → fetches SDA evidence → acts boundedly → updates graph and ledgers

## Operating Loop

20-Hour / Day Operating Loop: 10 × 2-Hour Cycles

1. State refresh + graph sync
2. Code patch / app.py / UI
3. Tests + validation
4. Claim verification
5. Risk/security review
6. EnMaTeS artifact generation
7. Documentation / user manual
8. Deployment checks
9. Package ZIP export
10. Daily report + next plan

## Quality Gates

- app.py launches
- tests pass
- ZIP export works
- claims source-supported
- secrets redacted
- repo input validated
- clone timeout + size caps active
- README claims match code behavior

## Security Warning

Rotate any pasted Twilio, Telegram, Hugging Face, or API credentials before deployment.
