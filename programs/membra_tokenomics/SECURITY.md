# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to the MEMBRA core team directly.

**Do NOT open a public issue for security bugs.**

Email: security@membra.xyz

We will respond within 48 hours with an acknowledgment and a timeline for resolution.

## Program Specific Risks

### Financial Guardrails

The tokenomics program handles SOL transfers. Critical checks:

- All transfers use CPI through the System Program (no raw lamport manipulation).
- All math uses `checked_*` operations to prevent overflow.
- Rebate claims are capped at `max_rebate_per_buyer_lamports` and pool-limited.
- Early reward pool is capped at `early_reward_cap_lamports`.
- Hard cap prevents infinite fundraising.

### Admin Privileges

The `authority` on `TokenSale` can:
- Activate, finalize, cancel, pause, resume sales
- Migrate liquidity status

**Production recommendation**: Replace single-key authority with a multisig (e.g. Squads) before mainnet launch.

### Known Limitations (v0.1)

- Refunds for cancelled sales must be handled off-chain.
- No automatic DEX liquidity migration on-chain (status flag only).
- No SPL token minting in this version (allocation is recorded, tokens distributed off-chain).

## Audit Status

- [ ] Internal review complete
- [ ] External audit scheduled
- [ ] Bug bounty program active
