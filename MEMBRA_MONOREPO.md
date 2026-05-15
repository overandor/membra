# MEMBRA Unified Development System

MEMBRA is now organized as one operating system with specialized repos.

The root repo, `overandor/membra`, is the command center. The specialized repos remain independently deployable modules, but all development should map to the shared registry in `modules/registry.json`.

## Why not flatten everything blindly?

A forced file-level merge would destroy useful module boundaries. MEMBRA needs both:

1. one cohesive product system for Replit and users
2. specialized repos for API, KPI, ProofBook, wallet, admin, ads, wear, relay, QR, contracts, vendor adapters, demo data, and investor room

This repo acts as the monorepo control plane.

## Source of truth

```text
modules/registry.json
```

The registry defines:

- module id
- GitHub repo URL
- module role
- module type
- development priority
- intended local path
- default port
- health check path
- Replit development style

## Development model

### 1. Primary deployable wedge

`Membra_kpi` is the current main production wedge.

It contains the full Replit-style loop:

```text
real photo/data upload
→ inventory mapping
→ SKU creation
→ KPI cards
→ ProofBook hashes
→ private listing drafts
→ owner visibility request
→ owner confirmation
→ marketplace listing
→ wallet/payout eligibility
```

### 2. Services

The other repos remain service modules:

- `Membra_api` normalizes shared objects
- `Membra_proofbook` owns proof/audit ledger behavior
- `Membra_wallet` owns payout eligibility and settlement boundaries
- `Membra_admin-` owns review/risk decisions
- `membra-qr-gateway` owns QR/NFC and scan provenance
- `membra-relay` owns local handoff logic
- `Membra_ads` owns physical media campaign flows
- `Membra_wear` owns wearable ad kit flows
- `Membra_vendor_adapters` owns package/fulfillment registry

### 3. Policies and data

- `Membra_contracts` defines event schemas and policy boundaries
- `Membra_demo_data` seeds the demo universe
- `Membra_investor_room-` packages the diligence story

## Replit strategy

There are two supported Replit modes.

### Mode A — Single-product Replit deploy

Deploy only `Membra_kpi`.

This is the current fastest path to a working product.

### Mode B — MEMBRA OS workspace

Use `overandor/membra` as the workspace root and clone each module into `modules/<repo>` using `scripts/bootstrap_modules.py`.

This creates a local working directory like:

```text
modules/
  Membra_kpi/
  Membra_api/
  Membra_proofbook/
  Membra_wallet/
  Membra_admin-/
  Membra_mobile/
  Membra_ads/
  Membra_wear/
  membra-relay/
  membra-qr-gateway/
  Membra_vendor_adapters/
  Membra_contracts/
  Membra_demo_data/
  Membra_investor_room-/
```

## Required development rule

Every module must implement or document:

```text
/api/health
README.md
.env.example or documented environment variables
production boundaries
module contract
```

## Production boundary

MEMBRA records proof, consent, listings, analytics, and payout eligibility. MEMBRA does not custody funds. External rails settle money.

## Immediate next development priority

1. Finish route-level auth in `Membra_kpi`.
2. Add owner isolation to uploads, inventory, drafts, wallet records, and privacy requests.
3. Make `Membra_api` consume the same event schema as `Membra_contracts`.
4. Connect `Membra_kpi` ProofBook writes to `Membra_proofbook` contract shape.
5. Connect QR artifact creation to `membra-qr-gateway`.
6. Connect owner-confirmed listings to `Membra_ads`, `Membra_wear`, and `membra-relay` depending on asset type.
