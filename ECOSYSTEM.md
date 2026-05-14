# MEMBRA Ecosystem Manifest

MEMBRA is a proof-of-reality monetization network: physical utility becomes structured inventory, inventory becomes permissioned listings, listings become local matches, matches become proof events, and proof events become reporting and payout eligibility.

## Core Operating Flow

Detect -> Assetify -> List -> Match -> Fulfill -> Settle -> Report

## Repository Map

| Repository | Role | Production Responsibility |
|---|---|---|
| `membra` | Umbrella OS | Doctrine, shared runtime, top-level product surface, ecosystem manifest |
| `Membra_api` | API gateway | Canonical users, assets, listings, proofs, campaigns, relay jobs, wallet events |
| `Membra_mobile` | Mobile shell | Owner/agent/advertiser mobile command surface |
| `Membra_admin-` | Operator console | Proof review, fraud review, campaign approval, payout holds, operational decisions |
| `Membra_wallet` | Wallet/payout boundary | Ledger entries, escrow state, Stripe event intake, payout eligibility records |
| `Membra_proofbook` | Proof ledger | Hashes, evidence metadata, consent scope, immutable proof events |
| `Membra_contracts` | Legal/schema layer | Event schemas, proof policies, owner/campaign/relay agreements |
| `Membra_ads` | Demand wedge | Proof-based physical media campaigns and QR/NFC ad inventory |
| `Membra_wear` | Wearable media | QR/NFC apparel, badges, patches, and vendor-ready kit manifests |
| `membra-relay` | Local fulfillment | Neighborhood handoff, micro-delivery, return runs, hub transfer, route proof |
| `membra-qr-gateway` | Gateway/provenance | QR/NFC artifact registration, redirects, scan events, public hashes |
| `Membra_kpi` | Reporting engine | KPI generation, scorecards, investor reporting, owner/campaign analytics |
| `Membra_vendor_adapters` | Fulfillment rails | Printful/Printify/Gelato/NFC/local printer adapter interfaces |
| `Membra_demo_data` | Demo universe | Seed apartments, assets, campaigns, proofs, routes, wallet events |
| `Membra_investor_room-` | Fundraising room | Pitch memo, diligence checklist, metrics, architecture, rollout plan |

## Canonical Objects

- `user_id`
- `asset_id`
- `listing_id`
- `campaign_id`
- `kit_id`
- `relay_id`
- `artifact_id`
- `proof_id`
- `wallet_account_id`
- `ledger_event_id`
- `payout_event_id`

## Operating Doctrine

No consent -> no MEMBRA.

No verified owner -> no asset.

No approved creative or valid task -> no placement.

No proof package -> no payout eligibility.

Proof is not money. External settlement rails settle money.

Private keys and seed phrases are never collected, stored, rendered, or requested.

## MVP Wedge

Start with `Membra_ads` + `Membra_wear` + `membra-qr-gateway` + `Membra_proofbook` + `Membra_wallet` + `Membra_kpi`.

This creates a commercial path: campaign demand -> QR/NFC physical media kit -> proof review -> scan events -> reporting -> payout eligibility.

## Deployment Pattern

Each runtime repository is Hugging Face/FastAPI/Gradio compatible where appropriate. Shared production deployments should later converge behind `Membra_api` as the public API gateway and `Membra_admin-` as the operator console.
