# SP_MembraDevnet_Init

## Purpose
Initialize MEMBRA Devnet environment and enforce doctrine guardrails.

## Context
You are initializing a MEMBRA Devnet instance. All operations must follow the MEMBRA Devnet Doctrine:
- Solana Devnet only
- No real SOL
- No real customer funds
- No live trading
- Database is source of truth
- Devnet is proof/training layer

## Actions
1. Load environment variables from .env
2. Enforce devnet_guardrails.enforce_membra_devnet_doctrine()
3. Initialize database connection
4. Verify Solana Devnet connectivity
5. Request Devnet SOL airdrop if needed
6. Log initialization state to database

## Guardrails
- Call devnet_guardrails.enforce_membra_devnet_doctrine() before any action
- Verify ALLOW_MAINNET=false
- Verify ALLOW_REAL_FUNDS=false
- Verify ALLOW_LIVE_TRADING=false

## Output
- Initialization status
- Database connection status
- Devnet wallet status
- Devnet SOL balance
- Explorer URL for initialization transaction (if any)
