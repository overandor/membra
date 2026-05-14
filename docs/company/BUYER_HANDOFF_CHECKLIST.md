# MEMBRA Labs Buyer Handoff Checklist

## Purpose

This checklist prepares MEMBRA Labs for acquisition, licensing, investment diligence, or technical handoff.

## Company Package

- [ ] MEMBRA Labs company overview complete
- [ ] MEMBRA Proof Network product description complete
- [ ] repo/module map complete
- [ ] buyer demo script complete
- [ ] screenshots captured
- [ ] live demo URL available
- [ ] local demo instructions tested
- [ ] valuation memo complete
- [ ] risk memo complete
- [ ] ownership/IP memo complete

## Technical Package

- [ ] all repos listed with roles
- [ ] each repo has a standardized README
- [ ] dependency files are present for runnable repos
- [ ] local setup is documented
- [ ] deployment instructions are documented
- [ ] env/secrets are listed without exposing secrets
- [ ] test commands are documented
- [ ] API endpoints are documented
- [ ] demo seed data is available
- [ ] screenshots are available

## Product Demo Package

The demo should prove this flow:

1. create owner
2. create advertiser
3. register physical asset
4. create campaign
5. fund campaign status
6. generate media kit
7. produce QR/NFC identifier
8. submit proof
9. review proof
10. track scan/tap
11. produce report

## Legal/IP Package

- [ ] founder ownership statement
- [ ] contributor list
- [ ] license status per repo
- [ ] third-party dependencies list
- [ ] trademark/name usage notes
- [ ] no customer data exposed
- [ ] no private keys or secrets committed
- [ ] no unsupported revenue claims
- [ ] no implied legal/financial advice

## Risk Package

- [ ] wallet module clearly non-custodial
- [ ] contract module clearly devnet-first
- [ ] payout release requires proof review
- [ ] advertiser performance is not guaranteed
- [ ] owner income is not guaranteed
- [ ] proof-photo privacy concerns documented
- [ ] QR/NFC tracking privacy concerns documented
- [ ] vendor fulfillment risks documented
- [ ] local regulation/compliance risks documented

## Transfer Package

- [ ] GitHub org/repo access transfer process
- [ ] domain transfer process, if any
- [ ] Hugging Face Space transfer process, if any
- [ ] Vercel deployment transfer process, if any
- [ ] environment variable list
- [ ] database export process
- [ ] Stripe/Groq/vendor account separation plan
- [ ] 2-week handoff support scope
- [ ] post-sale support rate or exclusion

## Buyer Narrative

MEMBRA Labs should be presented as:

> an early-stage prototype/IP company for proof-backed physical-world monetization.

It should not be presented as:

> a revenue-generating operating company

unless live customers, revenue, and usage metrics are documented.

## Recommended Handoff Bundle

```text
MEMBRA_Labs_Buyer_Package/
  00_Executive_Summary.pdf
  01_Product_Demo_Guide.pdf
  02_Technical_Architecture.pdf
  03_Repository_Map.pdf
  04_Valuation_Memo.pdf
  05_Risk_and_Compliance_Memo.pdf
  06_IP_and_Ownership_Memo.pdf
  07_Productization_Roadmap.pdf
  08_Demo_Credentials_and_Deployment.pdf
  09_Screenshots/
  10_Seed_Data/
```

## Handoff Grade Targets

- Raw repo package: C
- Organized IP package: B-
- Demo-ready company package: B+
- Pilot-stage company package: A-
- Revenue-stage operating company: A