# MEMBRA

MEMBRA turns every home into a verified inventory node.

## The Pitch

MEMBRA is the AI operating system that turns private household utility into verified, fractional, permissioned local commerce.

It starts with low-risk household utility: storage, tools, appliances, charging/workspace access, and local fulfillment.

Its moat is not listings. Its moat is the field grammar: every private object, space, service, utility, and time window becomes a searchable, priced, risk-scored, permissioned, and settleable economic unit.

## Quick Start

```bash
git clone https://github.com/overandor/membra.git
cd membra
pip install -r requirements.txt
python app.py
```

Deploy to HuggingFace:
```bash
export HF_TOKEN=your_huggingface_token
python deploy_hf.py
```

## Documentation

- [Product Doctrine](docs/product-doctrine.md) - Canonical MEMBRA product doctrine
- [Inventorization Index Map](docs/inventorization-index-map.md) - Field-to-index mapping
- [MembraIndexRecord](docs/membra-index-record.md) - Central underwriting object
- [MVP Wedge](docs/mvp-wedge.md) - Initial wedge strategy
- [Prohibited Risk Categories](docs/prohibited-risk-categories.md) - Risk framework
- [Investor Appraisal](docs/investor-appraisal.md) - Valuation narrative
- [Index Dictionary](membra_index_dictionary.json) - Complete field definitions
- [Claim Registry](claim_registry.json) - Claims mapped to evidence
- [Risk Register](risk_register.json) - Risk assessment matrix

## Core Primitives

- Inventory Node - Private household converted into commerce source
- MembraIndexRecord - Canonical liquid household unit
- MUP (Minimum Useful Price) - Smallest economically viable price
- Trust-Adjusted Liquidity - Safe market exposure calculation
- Household Utility Index - Aggregate local capacity value

## Current Stage

Pre-user. Post-thesis. Artifact-complete.

## License

MIT
