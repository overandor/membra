# MEMBRA Labs Productization Roadmap

## Objective

Convert MEMBRA from a prototype/IP portfolio into a cohesive, demo-ready company package.

## 30-Day Target

Produce a single buyer/investor demo that proves the MEMBRA Proof Network workflow:

> Register owner → register asset → create advertiser campaign → generate QR/NFC kit → submit proof → review proof → track scan/tap → produce KPI report.

## Phase 1: Company Consolidation

### Deliverables

- company hub README
- company package memo
- repo/module architecture map
- resale appraisal memo
- buyer handoff checklist
- standardized module READMEs
- consistent naming across repos

### Success Criteria

A buyer can understand the company, product, module suite, demo path, and current gaps in under 20 minutes.

## Phase 2: Demo Product Hardening

### Deliverables

- one-command local demo
- seeded demo data
- stable FastAPI backend path
- stable React dashboard path
- sample campaign flow
- sample proof events
- sample scan/tap events
- sample KPI report

### Success Criteria

A buyer can run a demo without guessing architecture.

## Phase 3: Data Room

### Deliverables

- executive summary
- product overview
- architecture map
- repository map
- API map
- risk and compliance memo
- valuation memo
- demo script
- screenshots
- owner/campaign/proof sample data
- acquisition handoff checklist

### Success Criteria

A buyer can perform first-pass technical and business diligence from the repo package.

## Phase 4: Pilot Readiness

### Deliverables

- production database decision
- auth layer
- admin review layer
- file upload/proof-photo storage
- scan/tap event telemetry
- payout hold/release state machine
- vendor adapter interfaces
- compliance checklist

### Success Criteria

MEMBRA can support a controlled pilot with fake or limited payment flows and real proof events.

## Phase 5: Operating Company Upgrade

### Deliverables

- signed pilot LOIs or test users
- live deployment
- completed proof events
- basic revenue or committed pilot budget
- retention/usage dashboard
- legal review
- payment/payout partner decision
- insurance/risk policy notes

### Success Criteria

MEMBRA becomes saleable as a pilot-stage operating company, not only as prototype/IP.

## Priority Build Order

1. `Membra_ads`: make this the first backend system of record.
2. `membra-qr-gateway`: make this the first buyer-visible dashboard.
3. `Membra_demo_data`: provide seed owners, advertisers, campaigns, proof events, scans, payouts.
4. `Membra_admin-`: add proof review and payout hold/release operator screen.
5. `Membra_kpi`: move or mirror KPI generator from `membra/app.py` into a dedicated analytics module.
6. `Membra_vendor_adapters`: define adapter contracts before integrating vendors.
7. `Membra_mobile`: implement proof-photo owner workflow after backend stabilizes.
8. `Membra_wallet`: keep non-custodial and optional until compliance review.
9. `Membra_contracts`: keep devnet-only until audit/legal review.
10. `membra-relay`: phase-two local fulfillment expansion.

## Non-Negotiable Safety Rules

- no guaranteed income claims
- no fake revenue claims
- no custodial wallet claims
- no real-funds contract testing without audit/legal review
- no payout release without proof status and audit trail
- no advertiser performance guarantees
- no hidden claims not mapped to evidence

## Resale Upgrade Checklist

The package becomes materially more valuable when it has:

- live URL
- demo video
- screenshots
- seed data
- one-command deploy
- test suite
- API docs
- admin dashboard
- proof-review state machine
- clean legal ownership notes
- buyer handoff checklist
- pilot-ready deployment path