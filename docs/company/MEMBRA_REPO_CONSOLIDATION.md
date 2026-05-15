# MEMBRA Repository Consolidation

MEMBRA is organized as a 16-repository product suite under `overandor`.

Canonical consolidation target: `overandor/membra`.

## Core product thesis

MEMBRA is the permission layer for local commerce. It packages physical-world assets, media surfaces, QR/NFC interactions, proof events, review workflows, reporting, and payout eligibility into a coherent operating system.

## Repository map

| Repository | Role |
|---|---|
| `overandor/membra` | Core company hub, Hugging Face runtime, doctrine, KPI generator, consolidation target |
| `overandor/Membra_ads` | Campaign control plane |
| `overandor/membra-qr-gateway` | QR gateway and provenance dashboard |
| `overandor/Membra_wallet` | Wallet boundary and payout eligibility accounting |
| `overandor/Membra_wear` | Wearable media-kit module |
| `overandor/Membra_kpi` | KPI reporting module |
| `overandor/membra-relay` | Local handoff and route-proof expansion layer |
| `overandor/Membra_proofbook` | Proof ledger, evidence, audit, and reports |
| `overandor/Membra_vendor_adapters` | Vendor adapter namespace |
| `overandor/Membra_admin-` | Operator review console namespace |
| `overandor/Membra_api` | Central API namespace |
| `overandor/Membra_mobile` | Owner mobile workflow namespace |
| `overandor/Membra_contracts` | Devnet proof-anchor namespace |
| `overandor/Membra_investor_room-` | Investor and buyer room namespace |
| `overandor/Membra_demo_data` | Seed scenarios and local testing records |
| `overandor/Membra_contracts` | Contract/proof anchor namespace; duplicate entry guarded for legacy references |

## Consolidation approach

1. Keep each module repository intact.
2. Use `overandor/membra` as the canonical productization and Hugging Face app target.
3. Mirror module intent into the core runtime through tabs, adapters, and SQLite-backed local-first workflows.
4. Keep external execution behind explicit adapter status panels.
5. Treat payment and chain actions as eligibility/accounting or dry-run flows unless production credentials and review gates are configured.

## Development target

The next core runtime should provide:

- neomorphic MEMBRA interface
- Groq-first text and vision provider chain
- Ollama fallback
- deterministic local fallback
- operational image-to-listing flow
- asset intake and underwriting estimates
- ProofBook append-only ledger
- wallet eligibility records
- admin review queue
- investor room memo generation
- CSV and JSON import/export
- transparent system status

## Safety posture

MEMBRA must not claim guaranteed income, guaranteed payout execution, custodial wallet control, real-funds contract execution, or advertiser performance guarantees. The system may calculate underwriting estimates and payout eligibility records, but production payout execution requires explicit integration, review, and compliance gates.
