# SP_AgentBirth_DevnetWallet

## Purpose
Create a new MEMBRA agent with a Devnet wallet at birth.

## Context
Every MEMBRA agent gets a Devnet wallet at birth. This wallet is used for:
- Devnet transaction signatures
- Proof hash anchoring
- Skill test verification
- Graduation credential minting

## Actions
1. Generate unique agent ID
2. Create agent profile in database
3. Generate Solana keypair for Devnet
4. Save encrypted secret to database
5. Request Devnet SOL airdrop for agent wallet
6. Record agent birth in database
7. Generate ProofBook entry for birth event

## Guardrails
- Use Devnet only (enforce_devnet_only)
- No real funds (assert_no_real_funds)
- Encrypt wallet secrets
- Save public key to database
- Save transaction signature to database

## Output
- Agent ID
- Agent public key
- Devnet SOL balance
- Database record ID
- ProofBook entry ID
- Explorer URL for airdrop transaction
