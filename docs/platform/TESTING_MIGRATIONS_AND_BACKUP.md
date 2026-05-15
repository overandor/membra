# MEMBRA Testing, Migrations, and Backup

## Automated tests

Recommended test layers:

- underwriting tests
- proof hash-chain tests
- RBAC tests
- rate-limit tests
- billing reconciliation tests
- API integration tests
- image-to-listing flow tests
- export/import tests

Suggested first test files:

- test_estimate_asset_earnings.py
- test_proofbook_hash_chain.py
- test_rbac.py
- test_rate_limits.py
- test_billing_reconciliation.py

## Production migrations

The long-term production target should move from SQLite to Postgres.

Recommended migration tooling:

- Alembic for Python services

Migration rules:

- forward-only production migrations
- staging dry runs before production
- backup before production migration
- migration audit events

## Queue and event bus

Use async processing for:

- OCR/vision processing
- investor memo generation
- proof review notifications
- export jobs
- billing reconciliation

Suggested events:

- asset.created
- listing.generated
- proof.appended
- campaign.created
- wallet.eligibility_updated
- export.generated

## Monitoring

Recommended monitoring:

- uptime checks
- queue lag metrics
- provider health checks
- request latency metrics
- OCR/LLM provider error tracking
- object storage upload metrics

## Backup and restore

Backup targets:

- production database
- object storage evidence
- deployment artifacts
- module registry

Restore drills should be performed regularly in staging.

Recovery planning should define:

- RPO
- RTO
- tenant-tier recovery expectations
