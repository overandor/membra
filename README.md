---
title: MEMBRA OS
emoji: 🏠
colorFrom: yellow
colorTo: black
sdk: docker
pinned: false
---

# MEMBRA OS

MEMBRA is organized as **one operating system with specialized repos**.

The root repo, `overandor/membra`, is now the command center for the MEMBRA ecosystem. It reads `modules/registry.json`, displays every module, exposes registry APIs, gives Replit-friendly bootstrap instructions, and can run the root OS plus the primary KPI product in one workspace command.

## Product thesis

**MEMBRA turns idle physical reality into measurable opportunity.**

Users can chat with AI, upload real photos or KPI data, and convert eligible apartment space, storage, car ad space, first-floor windows, wearables, local handoff capacity, QR/NFC artifacts, proof records, and payout eligibility into structured software workflows.

## Current primary deployable

The primary product wedge is:

```text
https://github.com/overandor/Membra_kpi
```

`Membra_kpi` owns the full production-style loop:

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

## Root command center only

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open:

```text
/
/workspace
/docs
/api/health
/api/registry
/api/modules
/api/replit-plan
/api/health-check-modules
```

## Full Replit workspace mode

In Replit, press Run. `.replit` now runs:

```bash
python scripts/run_workspace.py
```

That starts:

```text
MEMBRA OS root dashboard: http://localhost:8000
MEMBRA KPI product:       http://localhost:8001   # after modules are bootstrapped
```

First-time setup:

```bash
python scripts/bootstrap_modules.py
python scripts/status_modules.py
python scripts/run_workspace.py
```

If `modules/Membra_kpi` is not present, the workspace runner still starts the root OS and tells you to run the bootstrap command.

## Bootstrap all modules locally

```bash
python scripts/bootstrap_modules.py
python scripts/status_modules.py
```

This clones registered repos into:

```text
modules/Membra_kpi
modules/Membra_api
modules/Membra_proofbook
modules/Membra_wallet
modules/Membra_admin-
modules/Membra_mobile
modules/Membra_ads
modules/Membra_wear
modules/membra-relay
modules/membra-qr-gateway
modules/Membra_vendor_adapters
modules/Membra_contracts
modules/Membra_demo_data
modules/Membra_investor_room-
```

## Module registry

The source of truth is:

```text
modules/registry.json
```

Each module declares:

- module ID
- GitHub repo
- role
- type
- priority
- local path
- default port
- health path
- Replit development style

## Module contracts

Every specialized repo has a `MEMBRA_MODULE.md` contract explaining its role, inputs, outputs, health route, Replit role, and production boundary.

## Root APIs

```text
GET /api/health
GET /api/registry
GET /api/modules
GET /api/modules/{module_id}
GET /api/replit-plan
GET /api/health-check-modules
```

## Production boundary

MEMBRA records proof, consent, listings, reports, and payout eligibility. MEMBRA does not custody funds. External rails settle money.

AI may draft inventory. Owner confirmation is required before marketplace visibility. Estimates are not guaranteed.

## Recommended development sequence

1. Run `Membra_kpi` as the first live product.
2. Use `overandor/membra` as the OS dashboard and registry.
3. Wire `Membra_kpi` auth/session primitives into routes.
4. Connect QR artifacts to `membra-qr-gateway`.
5. Connect ProofBook writes to `Membra_proofbook`.
6. Connect payout eligibility to `Membra_wallet`.
7. Connect ads/wear/relay listings to their specialized modules.
8. Keep module contracts updated before new integrations.
