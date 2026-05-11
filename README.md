# MEMBRA

MEMBRA turns every home into a verified inventory node.

MEMBRA is an AI inventory graph for private household assets, converting physical utility into verified, priced, permissioned, and settleable local SKUs.

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
