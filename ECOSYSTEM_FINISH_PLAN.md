# MEMBRA Ecosystem Finish Plan

This document defines the practical done-state for every MEMBRA repository. The goal is not to pretend every module is production today; the goal is to turn each repo into a clear, testable, deployable, or intentionally documented module in the MEMBRA Proof Network.

## Global definition of done

Every MEMBRA repo should have:

- `README.md` explaining product role, current status, and run path
- `MEMBRA_MODULE.md` defining inputs, outputs, health route, boundaries, and integration points
- `.env.example` with safe placeholders only
- `SECURITY.md` or root-linked security boundary
- tests or a documented reason why the repo is docs/data-only
- clear production boundary: demo, scaffold, service, library, or deployable product
- no secrets, private keys, seed phrases, or unsupported revenue claims

## Priority 1 — deployable core

### overandor/Membra_kpi
Done-state: primary deployable FastAPI product.

Finish items:
- keep CI green
- deploy staging
- add Postgres migration path
- add auth/session model
- add S3/R2 upload adapter
- add structured logging
- add rate limit and security tests
- add production smoke-test script

### overandor/membra
Done-state: ecosystem command center and module registry.

Finish items:
- show registry health for all modules
- document bootstrap workflow
- add module status badges
- add ecosystem finish plan
- add release checklist

### overandor/Membra_ads
Done-state: first commercial backend wedge for proof-backed physical media campaigns.

Finish items:
- upgrade scaffold into canonical campaign service or explicitly hand off to Membra_api
- add auth boundary
- add Postgres/Supabase option
- add proof upload flow
- add demo loader
- add tests for campaign, checkout fallback, scan tracking, and webhook validation

### overandor/membra-qr-gateway
Done-state: buyer-visible dashboard for proof, QR/NFC, scans, wallet state, and KPI cards.

Finish items:
- connect to demo data and/or Membra_ads API
- add environment config for API base URL
- add static build CI
- add screenshot-ready demo route
- add dashboard panels for campaign, proof, scan, wallet, KPI

## Priority 2 — trust and money boundary

### overandor/Membra_proofbook
Done-state: proof ledger service/library.

Finish items:
- implement canonical JSON hashing utility
- implement proof event create/list/verify endpoints
- define proof schema
- add tests for reproducible hashes
- add export format

### overandor/Membra_wallet
Done-state: non-custodial payout eligibility and payment-state boundary.

Finish items:
- keep strictly non-custodial
- implement reward state machine
- add audit log for every mutation
- add Stripe/Connect placeholder integration only after auth
- add tests for state transitions

### overandor/Membra_contracts
Done-state: Devnet-only proof-anchor library and policy docs.

Finish items:
- add explicit `NO_MAINNET.md`
- add sample ProofAnchor contract or schema-only boundary
- add devnet-only tests if contracts are added
- prohibit real-funds deployment by default

## Priority 3 — operations and UX

### overandor/Membra_admin-
Done-state: operator review console.

Finish items:
- build minimal admin UI or API
- add proof review queue
- add payout hold queue
- add fraud/dispute states
- require audit event for every action

### overandor/Membra_mobile
Done-state: owner proof-capture mobile shell.

Finish items:
- create Expo shell or declare docs-only roadmap
- add screens for asset registration, proof capture, QR scanner, reward status
- connect to demo API when stable

### overandor/Membra_demo_data
Done-state: canonical demo seed pack.

Finish items:
- add `data/demo_bundle.json`
- add owners, advertisers, campaigns, assets, kits, proof events, tracking events, reward states
- add loader scripts for Membra_ads and dashboard mock adapter
- label all demo records clearly

## Priority 4 — expansion modules

### overandor/Membra_wear
Done-state: wearable media-kit module specification plus optional catalog service.

Finish items:
- define wearable catalog schema
- define media-kit request schema
- connect to vendor-adapter contract

### overandor/membra-relay
Done-state: phase-two local fulfillment roadmap and relay schema.

Finish items:
- define relay object schema
- define pickup/dropoff proof events
- block restricted goods by policy

### overandor/Membra_vendor_adapters
Done-state: vendor adapter interface and mock/manual adapter.

Finish items:
- define adapter interface
- add mock/manual adapter
- document Printful/Printify/Gelato as future rails only

### overandor/Membra_api
Done-state: canonical backend API contract or actual service.

Finish items:
- either absorb Membra_ads backend or remain OpenAPI/schema contract
- define source-of-truth resources
- add OpenAPI spec

### overandor/Membra_investor_room-
Done-state: buyer/investor package.

Finish items:
- add executive summary
- add architecture map
- add repo map
- add valuation memo
- add risk memo
- add demo script and screenshot placeholders

## Immediate execution order

1. Finish root `membra` documentation and registry status.
2. Keep `Membra_kpi` as primary deployable and move it to staging.
3. Make `Membra_ads` + `membra-qr-gateway` demo-connected.
4. Implement `Membra_demo_data` bundle.
5. Implement ProofBook hash service.
6. Add Wallet state machine.
7. Add Admin review queue.
8. Convert all remaining modules from loose charters into explicit schema/library/service packages.

## Appraisal impact

Current value is mostly productized IP and scaffolding. Value increases materially only when:

- the KPI app is live in staging
- the Ads backend can create a campaign
- QR Gateway displays campaign/proof/scan states
- Demo Data seeds a complete buyer walkthrough
- ProofBook verifies hashes reproducibly
- Wallet tracks eligibility without custody
- Investor Room packages evidence without unsupported claims
