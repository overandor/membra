# MEMBRA Module Registry

Canonical runtime target: `overandor/membra`.

The MEMBRA suite should use a central module registry so every repo has a known role, integration boundary, status, and deployment target.

## Registry goals

- make all MEMBRA modules discoverable
- prevent duplicate responsibilities
- define service ownership
- support health checks
- support future deploy orchestration
- map events across modules

## Module fields

Each module should expose:

- module_name
- repository
- description
- service_type
- runtime_language
- default_branch
- health_check_path
- api_schema_path
- event_topics_published
- event_topics_consumed
- data_owned
- dependencies
- deployment_target
- status

## Service types

- core_runtime
- api_service
- frontend
- mobile_client
- proof_ledger
- wallet_boundary
- campaign_service
- reporting_service
- vendor_adapter
- seed_data
- contract_devnet

## Current module map

| Module | Repository | Service type |
|---|---|---|
| Core Runtime | `overandor/membra` | core_runtime |
| Ads | `overandor/Membra_ads` | campaign_service |
| QR Gateway | `overandor/membra-qr-gateway` | frontend |
| Wallet | `overandor/Membra_wallet` | wallet_boundary |
| Wear | `overandor/Membra_wear` | vendor_adapter |
| KPI | `overandor/Membra_kpi` | reporting_service |
| Relay | `overandor/membra-relay` | api_service |
| ProofBook | `overandor/Membra_proofbook` | proof_ledger |
| Vendor Adapters | `overandor/Membra_vendor_adapters` | vendor_adapter |
| Admin | `overandor/Membra_admin-` | api_service |
| API | `overandor/Membra_api` | api_service |
| Mobile | `overandor/Membra_mobile` | mobile_client |
| Contracts | `overandor/Membra_contracts` | contract_devnet |
| Investor Room | `overandor/Membra_investor_room-` | reporting_service |
| Demo Data | `overandor/Membra_demo_data` | seed_data |

## Integration pattern

Phase 1: registry only.

Phase 2: each repo adds `membra.module.json`.

Phase 3: core runtime reads the registry and renders module health/status.

Phase 4: deploy orchestration reads the same registry.

Phase 5: events and shared schemas become the integration contract.
