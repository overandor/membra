# MEMBRA Object Storage and Config

## Object storage

MEMBRA should move uploaded files, proof evidence, exports, QR artifacts, and generated investor packets into object storage.

Recommended providers:

- S3-compatible storage
- Cloudflare R2
- Google Cloud Storage
- Azure Blob Storage
- local filesystem for development only

## Object metadata

Suggested fields:

- object_id
- tenant_id
- bucket
- object_key
- sha256
- content_type
- byte_size
- purpose
- retention_policy
- created_by
- created_at

## Adapter interface

Suggested operations:

- put_object
- get_signed_url
- list_objects
- verify_object_hash

Proof evidence should use retention policies and audit logging.

## Centralized configuration

Use typed config loaded from environment variables and deployment-specific overrides.

Config groups:

- app
- auth
- database
- object_storage
- llm
- vision
- queue
- billing
- observability
- frontend

## Secret management

Never store secrets in repositories.

Recommended secret sources:

- GitHub Actions secrets
- Hugging Face Space secrets
- cloud secret managers

Expected secrets:

- DATABASE_URL
- GROQ_API_KEY
- STRIPE_SECRET_KEY
- OBJECT_STORAGE_ACCESS_KEY_ID
- OBJECT_STORAGE_SECRET_ACCESS_KEY
- OCR_PROVIDER_API_KEY
- SENTRY_DSN

## Runtime policy

The runtime should expose status visibility for:

- configured providers
- object storage connectivity
- queue health
- OCR/vision provider availability
- active LLM provider
- migration version
