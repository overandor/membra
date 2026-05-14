---
title: MEMBRA Labs
emoji: 🏠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# MEMBRA Labs

**MEMBRA Labs builds proof infrastructure for physical-world monetization.**

The company packages real-world assets, surfaces, inventory, QR/NFC media, proof events, and payout eligibility into a coherent verification and reporting system.

## Flagship Product

# MEMBRA Proof Network

MEMBRA Proof Network converts physical-world activity into verified, reportable, and monetizable records.

The first commercial wedge is **verified physical media**:

- owners register surfaces, objects, or locations
- advertisers fund campaigns
- MEMBRA generates QR/NFC media kits
- owners submit proof photos and receipt confirmations
- admins review evidence and fraud flags
- scans and taps are tracked through MEMBRA-controlled links
- payouts become eligible only after proof rules pass
- advertiser, owner, investor, and operator reports are generated from the proof trail

## Company Positioning

MEMBRA is not a generic marketplace. MEMBRA is a **proof, attribution, and settlement-control layer** for physical-world commerce.

Long-term vision: every verified home, surface, object, person, route, and local asset can become a priced, permissioned, risk-scored economic node.

Near-term wedge: QR/NFC proof media, wearable media kits, campaign proof review, scan/tap attribution, and payout eligibility.

## Product Suite

| Product | Repository | Role |
|---|---|---|
| MEMBRA Core | `overandor/membra` | Company hub, demo terminal, KPI generator, doctrine, appraisal, docs |
| MEMBRA Ads | `overandor/Membra_ads` | Campaign control plane for owners, advertisers, assets, proof, QR/NFC tracking |
| MEMBRA QR Gateway | `overandor/membra-qr-gateway` | React dashboard for QR, provenance, wallet, proof, and artifact activity |
| MEMBRA Wallet | `overandor/Membra_wallet` | Non-custodial SMS Bitcoin/Lightning relay and payout boundary scaffold |
| MEMBRA Wear | `overandor/Membra_wear` | Wearable QR/NFC media-kit module for shirts, bags, patches, badges |
| MEMBRA KPI | `overandor/Membra_kpi` | Reporting module for campaign, proof, scan, owner, advertiser, and investor KPIs |
| MEMBRA Relay | `overandor/membra-relay` | Local handoff, delivery, storage, route proof, and fulfillment expansion layer |
| MEMBRA ProofBook | `overandor/Membra_proofbook` | Proof ledger namespace for hashes, evidence, audit records, and reports |
| MEMBRA Vendor Adapters | `overandor/Membra_vendor_adapters` | Vendor adapter namespace for Printful, Printify, Gelato, sign shops, NFC batches |
| MEMBRA Admin | `overandor/Membra_admin-` | Internal operations console namespace for review, fraud, claims, payouts, vendors |
| MEMBRA API | `overandor/Membra_api` | Future centralized control-plane API namespace |
| MEMBRA Mobile | `overandor/Membra_mobile` | Owner mobile workflow namespace for onboarding, proof photos, scans, offers |
| MEMBRA Contracts | `overandor/Membra_contracts` | Devnet proof-anchor contract namespace; no-real-funds testing only |
| MEMBRA Investor Room | `overandor/Membra_investor_room-` | Investor and buyer data-room namespace |
| MEMBRA Demo Data | `overandor/Membra_demo_data` | Seed scenarios and demo records namespace |

## Current Productization Status

MEMBRA Labs is an **early-stage prototype/IP company package**.

Current strengths:

- coherent company thesis
- runnable Hugging Face-style FastAPI + Gradio app
- FastAPI scaffold for ads/proof/QR/NFC campaign control
- FastAPI scaffold for non-custodial SMS wallet relay
- React/Vite dashboard package for QR/provenance UI
- documented module map across ads, proof, wallet, relay, KPI, wearables, vendors, mobile, contracts, and admin

Current gaps before operating-company resale:

- no verified customer revenue yet
- no production auth system across the full suite yet
- no unified persistent production database yet
- no legal/compliance review package yet
- no production payment/payout integration yet
- no audited proof-review workflow yet
- no live pilot metrics yet

## Fast Start

```bash
git clone https://github.com/overandor/membra.git
cd membra
pip install -r requirements.txt
python app.py
```

Deploy to Hugging Face Spaces:

```bash
export HF_TOKEN=your_huggingface_token
python deploy_hf.py
```

## Required Runtime Secrets

For the current KPI/demo runtime, configure:

```text
GROQ_API_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_PRICE_ID
APP_BASE_URL
```

Optional:

```text
GROQ_MODEL
REQUIRE_STRIPE
FREE_DAILY_KPI_LIMIT
PAID_DAILY_KPI_LIMIT
APP_DB_PATH
APP_EXPORT_DIR
ADMIN_API_TOKEN
AUTO_INSTALL_DEPS
```

## Company Documents

- `docs/company/MEMBRA_LABS_COMPANY_PACKAGE.md` — canonical company packaging memo
- `docs/company/MODULE_ARCHITECTURE.md` — repo-to-product architecture map
- `docs/company/BUYER_HANDOFF_CHECKLIST.md` — acquisition and diligence handoff checklist
- `docs/company/PRODUCTIZATION_ROADMAP.md` — 30/60/90-day execution roadmap
- `docs/company/RESALE_APPRAISAL.md` — grounded appraisal and value unlock ladder

## Existing Doctrine

- `docs/product-doctrine.md` — canonical MEMBRA product doctrine
- `docs/inventorization-index-map.md` — field-to-index mapping
- `docs/membra-index-record.md` — central underwriting object
- `docs/mvp-wedge.md` — initial wedge strategy
- `docs/prohibited-risk-categories.md` — risk framework
- `docs/investor-appraisal.md` — valuation narrative
- `membra_index_dictionary.json` — field definitions
- `claim_registry.json` — claims mapped to evidence
- `risk_register.json` — risk assessment matrix

## Safety Posture

MEMBRA must not imply guaranteed income, guaranteed advertiser performance, custodial wallet control, real-funds test contracts, or automatic payout release without proof review.

Wallet flows are non-custodial by design. Contract flows are devnet-first unless explicitly upgraded through legal, audit, and compliance review.

## License

MIT for this repository unless superseded by a separate written agreement or module-specific license.