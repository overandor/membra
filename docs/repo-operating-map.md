# MEMBRA Repo Operating Map

This document assigns a clear role to each MEMBRA repository so the ecosystem can be built without fragmentation.

## Core repos

## membra

Umbrella doctrine, shared schema, Devnet safety, ProofBook doctrine, product thesis, risk rules, and coordination index.

This repo should not hold every product forever. It should define shared standards and point to the correct product modules.

## Membra_api

Future central control-plane API for owners, advertisers, assets, campaigns, media kits, proof records, QR/NFC tracking, and payment state.

## Membra_ads

Revenue wedge. Physical proof media network for cars, windows, wearables, bags, stickers, tags, and real-world ad surfaces.

## membra-qr-gateway

Dashboard and visual command center for QR/NFC activity, proof events, campaign reporting, wallet status, owner dashboards, advertiser dashboards, and trust signals.

## membra-relay

Physical fulfillment and proof-route layer for pickup, delivery, kit movement, route status, receipt confirmation, and handoff proof.

## Membra_wear

Wearable media kit layer for shirts, hoodies, hats, bags, event badges, and QR/NFC campaign apparel.

## Membra_wallet

Payment boundary for campaign funding, owner reward state, payout review, audit logs, and external payment rail coordination.

## Membra_kpi

Analytics and reporting layer for owner reports, advertiser reports, campaign metrics, proof metrics, and operational scorecards.

## Membra_proofbook

Future proof ledger repo for canonical hashes, audit records, report exports, proof bundles, and optional Devnet anchors.

## Membra_admin

Future internal operations console for campaign approval, proof review, claims, flags, vendor status, and release checks.

## Membra_mobile

Future owner mobile workflow for asset onboarding, proof media capture, kit receipt, campaign offers, and status checks.

## Membra_vendor_adapters

Future vendor adapter layer for print, kit, tag, and fulfillment providers.

## Build rule

Every repo must answer four questions:

1. What business capability does it own?
2. What API or user workflow does it expose?
3. What proof does it generate?
4. What monetization path does it support?
