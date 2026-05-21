# MEMBRA OS Target Architecture

## Thesis

MEMBRA OS is a proof-to-payout assetification platform. It converts real-world assets, physical surfaces, user uploads, QR scans, SMS claim flows, and owner approvals into structured proof records and KPI reports.

## Product Modules

1. Assetification Engine — converts image/text/KPI uploads into inventory opportunities.
2. ProofBook — hashes source inputs, metadata, timestamps, and consent state.
3. QR Gateway — generates redirectable proof URLs and scan attribution.
4. Claim Links — SMS/email/QR claim and redemption event layer.
5. KPI Console — value estimates, event counts, conversion records, exportable reports.
6. Owner Approval — prevents public listing until explicit owner consent.
7. Marketplace Drafts — generates listing records without revenue guarantees.
8. Payout Eligibility — records eligibility; external rails settle payments.
9. Admin Review — fraud flags, approvals, exports, audit trails.
10. Labs Protocol — devnet-only Solana/protocol experiments.

## Target Repository Layout

```txt
membra/
  apps/
    console-web/
    api/
    qr-gateway/
    claim-links/
    admin/
  packages/
    assetification/
    proofbook/
    qr-engine/
    sms-engine/
    payout-ledger/
    sdk-python/
    sdk-ts/
    shared-types/
  services/
    postgres/
    redis/
    worker/
    embeddings/
    analytics/
  labs/
    membramoney-protocol/
  docs/
  deployments/
```

## Production Stack

| Layer | Recommended |
|---|---|
| Frontend | Next.js |
| API | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Queue | Celery or RQ |
| Object storage | S3/R2 |
| Auth | Clerk/Auth.js |
| Payments | Stripe Connect |
| SMS | Twilio |
| Analytics | ClickHouse or Postgres initially |
| Demo | Hugging Face Gradio |

## Non-Negotiable Boundary

Production-facing MEMBRA OS must not claim custody, bearer money issuance, treasury backing, token execution, guaranteed yield, or investment return. Those claims are isolated to labs until audit and legal review.
