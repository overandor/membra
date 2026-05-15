# MEMBRA Auth, RBAC, and Tenancy

Canonical target: `overandor/membra`.

## Central authentication

MEMBRA should use one identity layer across operators, asset owners, advertisers, investors, reviewers, admins, and internal service accounts.

Recommended interface:

- OIDC-compatible identity provider
- short-lived access tokens
- service tokens for workers
- FastAPI dependency that resolves current user
- tenant-aware session context

Identity fields:

- user_id
- tenant_id
- email
- display_name
- role
- auth_provider
- provider_subject
- status
- created_at
- last_login_at

## RBAC

Roles:

- platform_admin
- tenant_admin
- operator
- reviewer
- advertiser
- asset_owner
- investor_viewer
- service_account

Permission groups:

- assets.read
- assets.write
- campaigns.read
- campaigns.write
- proofbook.read
- proofbook.append
- proofbook.verify
- wallet.read
- wallet.review
- payouts.prepare
- billing.read
- billing.reconcile
- admin.review
- tenant.manage
- config.manage

Safety rule: payout or chain-adapter execution requires explicit role permission, tenant permission, configured adapter, and audit event.

## Tenant isolation

Every durable object should carry `tenant_id`.

Tables requiring tenant scope:

- users
- assets
- campaigns
- proof_events
- wallets
- billing_accounts
- invoices
- object_files
- audit_logs
- rate_limit_events
- config_values

Isolation modes:

1. Shared database with tenant_id filters.
2. Postgres row-level security.
3. Separate schema or database per tenant for enterprise deployments.

For the current SQLite app, add `tenant_id` now to avoid future migration friction.
