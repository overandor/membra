# MEMBRA Liquid

The liquidity layer for real-world household utility.

MEMBRA Liquid converts idle household assets, space, access, errands, storage, skills, and availability into priced, verified, fractional, finance-ready inventory.

## MEMBRA Devnet Doctrine

MEMBRA operates under the **MEMBRA Devnet Doctrine** by default:

- **Solana Devnet only** - No mainnet by default
- **No real SOL** - Uses fake/test Devnet SOL from airdrops
- **No real customer funds** - No live trading by default
- **Database is source of truth** - Canonical state preserved in database
- **Devnet is proof layer** - Real transaction mechanics without real-money exposure
- **User-gasless mode** - Platform sponsors Devnet transaction fees

### Core Architecture

```
Database (Postgres/SQLite/Supabase) → Canonical State
ProofBook → Verification Bridge
Solana Devnet → Proof/Training Layer
SkillOS → Agent Lifecycle
WatchTower → Monitoring
LaunchPad → Mainnet Promotion
BlockEdge → Blockchain Workflow Simulator
```

### Guardrails

Every application must enforce:
```python
from devnet_guardrails import enforce_membra_devnet_doctrine

enforce_membra_devnet_doctrine()  # Call at startup
```

This ensures:
- `ALLOW_MAINNET=false`
- `ALLOW_REAL_FUNDS=false`
- `ALLOW_LIVE_TRADING=false`
- `DRY_RUN=true`

See [docs/devnet-doctrine.md](docs/devnet-doctrine.md) for complete doctrine.

## Vision

Every household is an underwritten balance sheet of idle utility. MEMBRA Liquid converts that utility into verified local SKUs, priced access contracts, trust-scored inventory nodes, and eventually collateralizable neighborhood cash flow.

## The Primitive: Household Utility Liquidity (HUL)

Household Utility Liquidity is the conversion of idle private-world capacity — objects, spaces, access, time windows, storage, errands, skills, and local availability — into verified, priced, permissioned, and settleable micro-assets.

## Core Economic Unit: Minimum Useful Unit

A vacuum is not a vacuum. It is 20 minutes of cleaning capacity.
A shelf is not a shelf. It is 15 cubic feet of monthly storage.
A couch is not furniture. It is hourly seating capacity.
A neighbor's availability is not labor. It is local fulfillment liquidity.

## Product Architecture

Intent → Inventory → Assetization → Fractionalization → Risk → Permission → Price → Transaction → Proof → Settlement → Reputation → Yield

## Core Primitives

- **Inventory Node**: Private household or space converted into structured commerce source
- **SKU Verification**: AI-assisted detection, matching, confidence scoring, and host approval
- **FractionOS**: Breaking household utility into rent/access/storage/service units
- **AccessOS**: Rules for who can access what, when, and under what proof conditions
- **TrustOS**: Risk, proof, insurance, reputation, and permissioning
- **OracleOS**: LLM/vision matching of intent to inventory
- **LedgerOS**: Payment, escrow, deposits, usage records, returns, disputes, and reputation
- **MUP**: Minimum Useful Price - smallest price at which a household unit becomes economically worth exposing to the market

## Fintech Layer

- **Host Yield Score**: Expected monthly earnings from approved household inventory
- **Inventory Credit File**: Verified inventory, utilization, proof history, and cash flow
- **Node Yield**: Income generated per household node
- **MUP Oracle**: Pricing engine for minimum useful household units
- **Trust-Adjusted Liquidity**: How much of a household's inventory can be safely exposed
- **Household Utility Index**: Aggregate market value of local household capacity

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

## MEMBRA Liquid Terminal

The MEMBRA Liquid Terminal is a Bloomberg terminal for household liquidity. It converts rooms into underwritten micro-commerce balance sheets.

**Core Dashboard Sections:**
- Inventory Node Value
- Approved SKUs
- Projected Monthly Yield
- Trust-Adjusted Liquidity
- Risk Ladder
- MUP Pricing
- Local Demand Match
- Proof & Settlement Log
- Liquidity Index

**Example Output:**
```
Household Node: Living Room Alpha
Detected Utility Units: 14
Approved Liquid Units: 8
Gross Utility Value: $1,240/month
Trust-Adjusted Liquidity: $486/month
Node Yield Score: 87.2
Risk Grade: Low-Medium
Top Units: shelf storage, vacuum access, ring light rental, chair rental, local drop-off, charging workspace
```

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

# Run the MEMBRA Liquid Terminal
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

- [MEMBRA Devnet Doctrine](docs/devnet-doctrine.md) - Official operating doctrine for Solana Devnet
- [MEMBRA Thesis](docs/membra-thesis.md)
- [Operations Schema](docs/operations-schema.md)
- [Minimum Useful Price](docs/minimum-useful-price.md)
- [Trust Risk Ladder](docs/trust-risk-ladder.md)
- [SKU Verification](docs/sku-verification.md)
- [Host Node Model](docs/host-node-model.md)
- [Inventorization and Indexing](docs/inventorization-indexing.md) - Field-to-index mapping and index dictionary
- [Inventorization Index Map](docs/inventorization-index-map.md) - Visual flow from household reality to liquidity outputs
- [Index Dictionary](membra_index_dictionary.json) - Complete field definitions for household utility liquidity

## Devnet Infrastructure

### Core Modules

- **devnet_guardrails.py** - Enforces MEMBRA Devnet Doctrine guardrails
- **proof_utils.py** - Standard proof hashing and Devnet memo generation
- **schema.sql** - Database schema for hybrid architecture

### Prompt Pack

Located in `prompts/` directory:
- `SYSTEM_MembraDevnet_Operator.md` - Master system prompt for all MEMBRA agents
- `SP_MembraDevnet_Init.md` - Initialize Devnet environment
- `SP_AgentBirth_DevnetWallet.md` - Create agent with Devnet wallet
- `SP_SkillTest_Run.md` - Execute skill tests
- `SP_TaskHunter_Search.md` - Search for available tasks
- `SP_TaskExecution_Devnet.md` - Execute tasks on Devnet
- `SP_ProofBook_Anchor.md` - Anchor proof hashes to Devnet
- `SP_BlockEdge_OpportunityScan.md` - Scan blockchain opportunities
- `SP_WatchTower_Report.md` - Generate monitoring reports
- `SP_Graduation_Check.md` - Check agent graduation requirements
- `SP_MainnetPromotion_Request.md` - Request mainnet promotion

## License

MIT

---

## Valuation Narrative

MEMBRA Liquid is pre-user because it is manufacturing the market object first, not because it lacks a market.

### Asset Value Sources

- Category creation (Household Utility Liquidity)
- Named economic primitive (HUL)
- Product architecture (Protocol loop)
- UI/brand system (Liquid Terminal)
- Pricing doctrine (Minimum Useful Price)
- Risk/trust system (Trust-Adjusted Liquidity)
- Data model (Inventory Node, SKU, Transaction)
- Demo terminal (Artifact-complete app.py)
- Protocol documentation (Complete docs)
- Implementation pathway (Clear deployment path)

### Appraisal Ladder

- Concept + visuals + schema: $25k–$75k
- Artifact-complete demo with app.py, docs, pricing engine, SKU model, exportable reports: $75k–$200k
- Fintech-grade MVP with auth, payments, verification, node dashboards, and real host onboarding: $250k–$750k
- Pilot with transactions, retention, node yield, and repeat liquidity: $1M–$5M+ seed-stage valuation potential

### Investor Line

We are building the market structure for household utility before household utility becomes a market.

### Densest Pitch

MEMBRA Liquid converts idle household utility into verified, fractional, finance-ready local liquidity. Using AI inventory detection, Minimum Useful Price modeling, trust-adjusted access rules, proof-of-use settlement, and node-yield scoring, MEMBRA transforms rooms into underwritten micro-commerce balance sheets. The result is a new asset class: household utility liquidity.

### Sharpest Investor Line

MEMBRA turns every home into a liquid inventory node.

### Product Phrase

Pre-user. Post-thesis. Artifact-complete.
