---
title: MEMBRA OS
emoji: 🧾
colorFrom: gray
colorTo: indigo
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
---

# MEMBRA OS — Proof-to-Payout Assetification Infrastructure

MEMBRA OS is the cohesive product layer for the overandor MEMBRA repositories.

It turns real-world uploads, spaces, QR scans, SMS/claim links, and owner approvals into proof records, KPI cards, marketplace drafts, and payout-eligibility logs without custodying funds or promising returns.

## Safe Product Boundary

MEMBRA OS records:

- assetification suggestions
- proof hashes
- consent state
- QR/claim attribution
- scan events
- KPI estimates
- listing drafts
- payout eligibility

MEMBRA OS does not:

- custody money
- guarantee revenue
- issue bearer money
- execute tokenomics
- run trading strategies
- provide investment advice
- settle payments internally

Protocol and token experiments belong only in `labs/` until separately audited and legally reviewed.

## Consolidated Repo Roles

| Existing repo | Consolidated role |
|---|---|
| `membra` | Canonical parent, SDK, docs, registry |
| `Membra_kpi` | Flagship assetification and KPI SaaS |
| `membra-qr-gateway` | QR/NFC proof and scan attribution rail |
| `sms` | SMS/email/QR claim-link rail |
| `membramoney-protocol` | Devnet-only protocol research lab |

## Core Flow

```txt
Upload / image / text
  -> Assetification engine
  -> ProofBook hash
  -> Owner consent
  -> QR and claim-link rails
  -> KPI analytics
  -> Marketplace draft
  -> Payout eligibility
  -> External settlement rail
```

## Included Files

- `app.py` — Hugging Face/Gradio demo
- `requirements.txt` — Python dependencies
- `.env.example` — environment template
- `membra_repo_map.json` — repo-to-module map
- `docs/architecture.md` — target architecture
- `docs/migration-plan.md` — consolidation steps
- `docs/appraisal.md` — dollar appraisal summary
- `docs/github-issues.md` — implementation issue backlog
- `deployments/docker/Dockerfile` — container starter

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

## Commercial Positioning

Best market framing:

> Physical-world inventory intelligence and proof-commerce infrastructure.

Avoid customer-facing claims around token finance, bearer notes, reserves, or guaranteed payout until the relevant systems are independently audited and compliance-reviewed.
