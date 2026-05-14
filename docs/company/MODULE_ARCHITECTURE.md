# MEMBRA Labs Module Architecture

## Canonical Company Structure

MEMBRA Labs should be presented as one company with a modular product suite.

## System Layers

### 1. Company Hub

**Repo:** `overandor/membra`

Purpose:

- company narrative
- Hugging Face-style demo runtime
- KPI generator
- doctrine
- index dictionary
- appraisal and productization docs
- risk and claim registries

### 2. Commercial Control Plane

**Repo:** `overandor/Membra_ads`

Purpose:

- owner registration
- advertiser registration
- surface/asset registration
- campaign creation
- campaign funding status
- QR/NFC media kit generation
- proof submission
- proof review
- scan/tap tracking
- audit events

### 3. QR and Provenance Interface

**Repo:** `overandor/membra-qr-gateway`

Purpose:

- dashboard UI
- public support wallet display
- artifact and proof panels
- provenance layer
- QR gateway view
- mobile preview
- KPI cards

### 4. Wallet and Payout Boundary

**Repo:** `overandor/Membra_wallet`

Purpose:

- non-custodial wallet relay
- SMS command parsing
- phone alias registry
- payment intent creation
- watch-only balance records
- audit logs
- explicit user wallet authorization

Rule:

MEMBRA must not hold private keys, seed phrases, or custodial balances.

### 5. Proof Ledger

**Repo:** `overandor/Membra_proofbook`

Purpose:

- hash records
- proof photos
- scan/tap logs
- payout eligibility states
- Devnet anchors
- audit reports

### 6. Wearable Media

**Repo:** `overandor/Membra_wear`

Purpose:

- campaign apparel
- QR/NFC patches
- badges
- delivery bags
- event kits
- proof requirements
- vendor output specs

### 7. Local Fulfillment Expansion

**Repo:** `overandor/membra-relay`

Purpose:

- Hero House fulfillment
- Alpha Hub storage
- relay agent routes
- meet-halfway flows
- return runs
- route proof
- local transfer records

### 8. Analytics and Reporting

**Repo:** `overandor/Membra_kpi`

Purpose:

- campaign KPIs
- owner reports
- advertiser reports
- investor summaries
- proof audit reports
- CSV/JSON exports

### 9. Vendor Layer

**Repo:** `overandor/Membra_vendor_adapters`

Purpose:

- Printful adapter
- Printify adapter
- Gelato adapter
- sticker vendor adapter
- NFC batch supplier adapter
- manual local print shop workflow

### 10. Admin Operations

**Repo:** `overandor/Membra_admin-`

Purpose:

- proof review
- creative approval
- fraud flags
- campaign status
- vendor oversight
- payout hold reasons
- claims and disputes

### 11. Central API Namespace

**Repo:** `overandor/Membra_api`

Purpose:

- eventual consolidated API surface
- shared schemas
- shared auth
- shared audit middleware
- module integration

### 12. Mobile Owner App

**Repo:** `overandor/Membra_mobile`

Purpose:

- owner onboarding
- asset registration
- proof photo capture
- campaign offer acceptance
- kit receipt confirmation
- reward status

### 13. Devnet Contracts

**Repo:** `overandor/Membra_contracts`

Purpose:

- proof-anchor contracts
- simulated credentials
- audit hashes
- no-real-funds testing
- Devnet-only workflows until legal/audit review

### 14. Investor Room

**Repo:** `overandor/Membra_investor_room-`

Purpose:

- pitch narrative
- demo script
- valuation map
- pricing model
- roadmap
- screenshots
- traction model
- claims registry

### 15. Demo Data

**Repo:** `overandor/Membra_demo_data`

Purpose:

- seed owners
- seed advertisers
- sample campaigns
- sample proof events
- sample scans/taps
- sample payout states
- demo reports

## Priority Integration Path

1. `membra` becomes company hub.
2. `Membra_ads` becomes the first runnable product backend.
3. `membra-qr-gateway` becomes the first product dashboard.
4. `Membra_demo_data` supplies seed records.
5. `Membra_kpi` absorbs KPI/reporting runtime from `membra/app.py` or exposes it as a reusable package.
6. `Membra_admin-` receives the proof-review UI.
7. `Membra_vendor_adapters` receives vendor interfaces.
8. `Membra_wallet` remains optional and non-custodial.
9. `Membra_contracts` remains devnet-only until reviewed.
10. `membra-relay` becomes phase-two fulfillment expansion.

## Naming Standard

Use these public names:

- Company: **MEMBRA Labs**
- Flagship: **MEMBRA Proof Network**
- Commercial wedge: **Membra Ads**
- Ledger: **ProofBook**
- Dashboard: **QR Gateway**
- Wallet module: **Membra Wallet Relay**
- Wearable module: **Membra Wear**
- Fulfillment module: **Membra Relay**

## Buyer Narrative

The repos should be described as a modular company system, not isolated experiments.

The core asset is the full-stack proof-commerce workflow:

> Register asset → generate QR/NFC kit → capture proof → review proof → track scans/taps → calculate payout eligibility → generate reports.