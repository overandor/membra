# MEMBRA

AI-powered household inventory commerce OS for converting private assets, spaces, utilities, and errands into verified local SKUs.

MEMBRA is the inventory, access, trust, and fulfillment layer for household-to-market conversion. It turns homes into verified micro-warehouses and utility nodes for neighborhood commerce.

## Vision

Turn your home into a local inventory node. Scan your space, approve your assets, and earn from storage, tools, errands, and everyday household utility.

## Product Architecture

Intent → Inventory → Assetization → Fractionalization → Listing → Access → Fulfillment → Proof → Settlement → Reputation → Replenishment

## Core Primitives

- **Inventory Node**: Private household or space converted into structured commerce source
- **SKU Verification**: AI-assisted detection, matching, confidence scoring, and host approval
- **FractionOS**: Breaking household utility into rent/access/storage/service units
- **AccessOS**: Rules for who can access what, when, and under what proof conditions
- **TrustOS**: Risk, proof, insurance, reputation, and permissioning
- **OracleOS**: LLM/vision matching of intent to inventory
- **LedgerOS**: Payment, escrow, deposits, usage records, returns, disputes, and reputation
- **MUP**: Minimum Useful Price - smallest price at which a household unit becomes worth sharing

## MVP Focus

Low-risk, high-frequency SKUs:
- Storage shelf space
- Closet space
- Tool access
- Vacuum rental
- Folding chair rental
- Charging/workspace access
- Local drop-off errands
- Sealed household consumables
- Small appliance access

## User Roles

- **Host**: Owns assets, space, services, or local availability
- **Requester**: Needs access to an object, space, service, or errand
- **Hero**: Fulfills delivery, pickup, inspection, setup, or handoff
- **House**: Physical household node with inventory, trust score, availability, and access rules

## Initial Wedges

1. **Overflow Inventory Hosting** - Shelf, closet, garage, fridge, or storage space
2. **Micro-Utility Rentals** - Vacuum for 20 minutes, drill for one hour, ring light for one shoot
3. **Household Fulfillment Nodes** - Hosts earn by storing, handing off, delivering, or meeting halfway

## Monetization Stack

- Transaction fee on rentals/access
- Subscription for power hosts
- Verification fee for trusted inventory nodes
- Premium placement for local SKUs
- Insurance/protection margin
- Fulfillment margin on delivery or handoff
- B2B/API access for property managers, dorms, co-living operators

## Quick Start

### Prerequisites

- Python 3.8+
- HuggingFace token (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/overandor/membra.git
cd membra

# Install dependencies
pip install -r requirements.txt

# Run the Inventory Node Simulator
python app.py
```

### Deployment

Deploy to HuggingFace:

```bash
# Set your HF token
export HF_TOKEN=your_huggingface_token

# Deploy
python deploy_hf.py
```

## Documentation

- [MEMBRA Thesis](docs/membra-thesis.md)
- [Operations Schema](docs/operations-schema.md)
- [Minimum Useful Price](docs/minimum-useful-price.md)
- [Trust Risk Ladder](docs/trust-risk-ladder.md)
- [SKU Verification](docs/sku-verification.md)
- [Host Node Model](docs/host-node-model.md)

## License

MIT
