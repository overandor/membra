# MEMBRA Protocol v0.1

MEMBRA is a proof-of-placement protocol for turning real-world surfaces into verified, trackable, payout-ready media inventory.

## Protocol thesis

A physical ad placement is valid only when campaign identity, physical surface identity, media-kit identity, proof evidence, tracking events, and reward state can be reconciled.

## Core actors

- Owner: controls a physical surface.
- Advertiser: funds a campaign.
- Operator: reviews proof and manages exceptions.
- Vendor: produces or fulfills media kits.
- Viewer: scans a QR code or taps NFC.
- Protocol: records state, proof, analytics, and reward eligibility.

## Core objects

- owner
- advertiser
- asset
- campaign
- creative
- placement
- media kit
- QR tag
- NFC tag
- proof event
- tracking event
- reward state
- payout record
- audit event
- ProofBook entry

## Protocol lifecycle

```text
owner_registered
asset_registered
asset_verified
advertiser_registered
campaign_created
creative_submitted
creative_approved
campaign_funded
placement_accepted
media_kit_created
qr_identity_assigned
nfc_identity_assigned
vendor_order_created
kit_shipped
kit_received
proof_submitted
proof_reviewed
placement_activated
scan_recorded
tap_recorded
reward_eligible
reward_released
campaign_completed
```

## Valid placement rule

A placement is protocol-valid only if:

1. Campaign exists.
2. Campaign creative is approved.
3. Owner asset is verified.
4. Placement is accepted.
5. Media kit has MEMBRA QR or NFC identity.
6. Proof is submitted.
7. Proof is approved.
8. Tracking events route through MEMBRA.
9. Reward state references approved proof.

## Proof rule

Proof must be canonicalized before hashing.

```text
canonical JSON -> SHA-256 hash -> ProofBook record -> optional Devnet anchor
```

The database is the source of truth. ProofBook hashes make records reproducible. Devnet anchors are optional proof references, not a database replacement.

## Tracking rule

Every QR or NFC destination must route through MEMBRA first.

Direct advertiser URLs break attribution, fraud checks, analytics, and reward eligibility.

## Reward rule

No reward can be eligible unless:

- campaign is funded
- placement is active
- proof is approved
- no unresolved claim blocks the placement
- reward state is audit logged

## Vendor rule

Vendor shipment alone does not create reward eligibility.

Shipment proves kit movement. Install proof proves placement.

## Fraud flags

- reused proof media
- missing campaign creative
- hidden or unreadable QR/NFC identity
- mismatched asset type
- location mismatch where location is required
- scan clustering anomaly
- self-scan abuse pattern
- proof outside campaign window
- vendor delivery without owner receipt

## Protocol modules

- Membra API: source-of-truth backend.
- Membra Ads: campaign and media-kit engine.
- Membra ProofBook: proof hashing and verification ledger.
- Membra QR Gateway: scan/tap attribution and dashboards.
- Membra Admin: review console.
- Membra Wallet: reward and payout boundary.
- Membra Relay: physical handoff and kit movement.
- Membra Wear: wearable surface module.
- Membra Vendor Adapters: fulfillment rails.
- Membra KPI: analytics and reporting.
- Membra Demo Data: live demo state.
- Membra Contracts: Devnet proof-anchor experiments.

## Safety posture

MEMBRA does not guarantee advertiser results.

MEMBRA does not guarantee owner income.

MEMBRA does not release rewards without proof and policy checks.

MEMBRA does not require blockchain for core operation. Chain anchoring is optional.

## Protocol goal

Make physical advertising measurable, auditable, and payout-ready by giving every placement a lifecycle, identity, proof record, and analytics trail.
