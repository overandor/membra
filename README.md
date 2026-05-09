# MEMBRA
**Author:** Joseph Skrobynets  
**Nicknames / Handles:** Dr.Profitosis, overandor, jskroby, carpathianwolfjoseph  
**Project Lineage:** Couchify → MEMBRA  
**Category:** Agentic local-commerce operating layer, household assetification, permissioned market supply  

## One-Line Thesis
**MEMBRA is a marketplace you talk to:** an agentic local-commerce operating layer that converts private household assets into permissioned, proof-backed, locally matched market supply.

## Core Flow
```txt
Ask MEMBRA
→ Assetify inventory
→ Approve listing
→ Match demand
→ Split / Relay / Book
→ Capture proof
→ Settle payment
```

## Product Modules

* Ask MEMBRA
* MEMBRA Inventory
* MEMBRA Marketplace
* MEMBRA Hero
* MEMBRA House
* MEMBRA Alpha Hub
* MEMBRA Relay
* MEMBRA SplitOrder
* MEMBRA SplitPulse
* MEMBRA Wallet
* MEMBRA Trust
* MEMBRA Pay

## MVP Screens

1. Client Home
2. Hero Dashboard
3. Inventory Assetification
4. SplitOrder
5. SplitPulse
6. Relay
7. Wallet
8. Trust / Proof Receipts

## Tech Stack

* Next.js
* React
* Tailwind CSS
* FastAPI
* OpenAPI
* PostgreSQL later
* AI/Vision assetification layer later

## Final Identity

MEMBRA = apartment capitalism with a chat box, a trust layer, and a tiny bodega hiding in every lease.

---

## Repository Structure

This is a monorepo with apps and packages:

```
membra/
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── docker-compose.yml
├── package.json
├── apps/
│   ├── web/
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tailwind.config.ts
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── ask/
│   │   │   │   └── page.tsx
│   │   │   ├── marketplace/
│   │   │   │   └── page.tsx
│   │   │   ├── hero/
│   │   │   │   └── page.tsx
│   │   │   ├── inventory/
│   │   │   │   └── page.tsx
│   │   │   ├── split-order/
│   │   │   │   └── page.tsx
│   │   │   ├── split-pulse/
│   │   │   │   └── page.tsx
│   │   │   ├── relay/
│   │   │   │   └── page.tsx
│   │   │   ├── wallet/
│   │   │   │   └── page.tsx
│   │   │   └── trust/
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── AppShell.tsx
│   │   │   ├── ChatBar.tsx
│   │   │   ├── ServiceGrid.tsx
│   │   │   ├── ListingCard.tsx
│   │   │   ├── HeroDashboard.tsx
│   │   │   ├── WalletCard.tsx
│   │   │   ├── RelayCard.tsx
│   │   │   ├── SplitOrderCard.tsx
│   │   │   ├── ProofReceipt.tsx
│   │   │   └── GoldCard.tsx
│   │   └── lib/
│   │       ├── api.ts
│   │       ├── types.ts
│   │       └── mock-data.ts
│   │
│   └── api/
│       ├── main.py
│       ├── requirements.txt
│       ├── app/
│       │   ├── routers/
│       │   │   ├── chat.py
│       │   │   ├── inventory.py
│       │   │   ├── marketplace.py
│       │   │   ├── hero.py
│       │   │   ├── relay.py
│       │   │   ├── split_order.py
│       │   │   ├── split_pulse.py
│       │   │   ├── wallet.py
│       │   │   └── trust.py
│       │   ├── models/
│       │   ├── services/
│       │   └── db/
│       └── openapi.json
│
├── packages/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Input.tsx
│   │   └── index.ts
│   └── config/
│       ├── eslint-config/
│       └── tailwind-config/
│
└── docs/
    ├── MEMBRA_SUPER_SUMMARY.md
    ├── API_OVERVIEW.md
    ├── UI_SCREENS.md
    ├── MVP_PLAN.md
    └── SAFETY_BOUNDARIES.md
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker

### Deployment

### Public API Documentation (Recommended)

To deploy the MEMBRA API with public documentation links:

**Option 1: Railway (Web Interface)**
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select `overandor/membra` repository
4. Railway auto-detects Python/FastAPI
5. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-random-secret-key-here
   DATABASE_URL=postgresql://user:password@host:5432/membra
   REDIS_URL=redis://host:6379/0
   ```
6. Click "Deploy"
7. Wait ~2 minutes for deployment
8. Your public links:
   - API: `https://your-project-name.railway.app`
   - Swagger UI: `https://your-project-name.railway.app/docs`
   - ReDoc: `https://your-project-name.railway.app/redoc`
   - Custom UI: `https://your-project-name.railway.app/docs-ui`
   - OpenAPI Spec: `https://your-project-name.railway.app/openapi.json`

**Option 2: Render (Web Interface)**
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository `overandor/membra`
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as above)
6. Click "Create Web Service"
7. Your public links appear after deployment

### Local Development

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Python directly
pip install -r requirements.txt
python -m uvicorn api.main:app --reload
```

### Environment Variables

```bash
DEBUG=False
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/membra
REDIS_URL=redis://host:6379/0
OPENAI_API_KEY=your-openai-key
STRIPE_SECRET_KEY=your-stripe-key
JWT_SECRET=your-jwt-secret
```

## GitHub Description

MEMBRA is an agentic local-commerce operating layer that converts private household assets into permissioned, proof-backed, locally matched market supply.

Created by Joseph Skrobynets (Dr.Profitosis, overandor, jskroby, carpathianwolfjoseph), MEMBRA turns household objects, online purchases, private spaces, storage capacity, human services, delivery routes, and local demand into fractional neighborhood inventory.

## Core Thesis

MEMBRA fractionalizes household utility through AI agents.

A vacuum becomes 15 minutes of access.
A pack of cups becomes single-unit local inventory.
A shelf becomes storage.
A couch becomes bookable space.
A fridge slot becomes cold storage.
A van becomes route capacity.
An Amazon order becomes neighborhood supply.

## Investor Version

MEMBRA is an agentic local-commerce operating layer that converts private household assets into permissioned, proof-backed, locally matched market supply.

## Simple Version

Take a picture of what you own. Ask for what you need. MEMBRA turns household assets into local supply.

## Sharp Version

MEMBRA converts private household reality into permissioned, proof-backed, locally matched market supply.

## Radical Version

MEMBRA makes every apartment the nearest warehouse, every useful object a potential SKU, and every chat a path from need into income.

---

## Core Thesis

Most homes contain underused economic infrastructure.

Inside a normal apartment there are:
- Tools
- Seats
- Storage
- Delivery capacity
- Service capacity
- Receipts
- Amazon orders
- Skills
- Time

Most of this is latent. It exists but is not monetized.

MEMBRA is the agentic operating layer that makes this latent infrastructure visible, priceable, bookable, and locally fulfillable.

---

## Main MEMBRA One-Liners

Use these depending on the audience:

- MEMBRA is an agentic local-commerce operating layer.
- Need nearby. Earn locally.
- Turn household assets into local supply.
- Every apartment is the nearest warehouse.
- Users need. Heroes earn. Hero Houses become Alpha Hubs.
- MEMBRA turns homes into local business nodes.
- MEMBRA turns every lease signer into a micro-entrepreneur.
- MEMBRA turns household utility into programmable local commerce.
- MEMBRA is Entrepreneurship-as-a-Service for renters.
- MEMBRA is HouseOS-as-a-Service.
- LLMs create the inventory. Blockchain proves the transaction. MEMBRA monetizes the intent.

---

## What MEMBRA Actually Does

A user can say:
- "What do I need nearby?"
- "What can I earn from my apartment?"
- "I need a drill and someone to install curtain rods."
- "I have unused Amazon items. Can I monetize them?"
- "I have a van after 6 PM."
- "I can store packages."
- "What should I stock in my area?"
- "What else in my house can make money?"

MEMBRA turns those prompts into structured actions:
- Detects assets
- Creates listings
- Estimates prices
- Checks risk
- Matches demand
- Routes fulfillment
- Enables communication
- Captures proof
- Splits payments
- Rewards users
- Builds reputation

So MEMBRA is not just browsing. It is chat → transaction.

---

## Core Roles

### User
Someone who needs something nearby.

### Hero
Someone who earns by fulfilling local needs. A Hero can offer:
- Items
- Tools
- Space
- Skills
- Time
- Food/supplies where compliant
- Storage
- Delivery
- Utilities
- Services

### Hero House
A home that becomes a local business node. It can function as:
- Pickup point
- Storage node
- Service node
- Inventory node
- Fulfillment node
- Package holding point
- Local bodega

### Alpha Hub
A high-trust, high-volume Hero House. Alpha Hubs can:
- Store inventory for other Heroes
- Fulfill orders
- Handle pickups and returns
- Stock high-demand goods
- Earn hub fees
- Support local liquidity

**Role ladder:** User → Hero → Hero House → Alpha Hub

---

## Marketplace Categories

MEMBRA supports categories that are permissioned, legal, safe, priceable, and governable.

**Rent:** Tools, vacuums, ring lights, tripods, appliances, couch seats, workspaces, equipment

**Buy:** Sealed supplies, chargers, household extras, unused goods, Amazon/Temu items, unopened products

**Split:** One egg, one cup of milk, detergent pods, pantry quantities, bulk supplies (with food-safety controls)

**Store:** Closet shelf, fridge shelf later, garage corner, package holding, luggage storage, temporary storage

**Access:** Wi-Fi, charging, printer, TV, desk, kitchen tools, laundry-adjacent access, restricted utilities where compliant

**Move:** Vans, pickups, furniture moving, hauling, delivery, marketplace pickup, return drop-off

**Book:** Cleaning, setup, repair, organizing, errands, installation, tech help

**Supply:** USB-C cables, batteries, laundry pods, trash bags, paper towels, pet supplies, household essentials

**Food / Catering:** Sealed goods, pantry bundles, licensed catering, cold storage, regulated food services where legal

---

## Core MEMBRA Brand Stack

Ask MEMBRA — The chat layer. Users ask what they need. Heroes ask what they can earn.

MEMBRA Inventory — The assetification layer. Photos, receipts, Amazon orders, CSVs, and product links become structured local inventory.

MEMBRA Marketplace — The commerce layer. Approved offers become rentable, buyable, splittable, storable, accessible, movable, or bookable.

MEMBRA Hero — The earning profile. A Hero manages listings, pricing, availability, trust, orders, and payouts.

MEMBRA House — The home-as-business layer. A home becomes a pickup point, storage node, service node, or fulfillment point.

MEMBRA Alpha Hub — The high-trust fulfillment layer. Alpha Hubs store inventory for other Heroes, fulfill orders, handle pickups and returns, and stock high-demand goods.

MEMBRA Supply — The demand intelligence and inventory investment layer. MEMBRA tells Heroes what to stock next based on local demand.

MEMBRA Opportunity — The supply-creation layer. It converts passive users into Heroes by showing what people nearby already want.

MEMBRA Wallet — The rewards and settlement layer. It holds earnings, credits, cashback, deposits, refunds, proof receipts, loyalty, and referral rewards.

MEMBRA Trust — The safety layer. Identity, reviews, deposits, proof, risk checks, category approvals, compliance, and disputes.

MEMBRA Pay — The transparent money layer. It splits payment between Owner Hero, Skill Hero, Hub Hero, Delivery Hero, Referral Hero, User cashback, and MEMBRA.

---

## Simplified Technical OS Stack

1. **InventoryOS** — The master inventory graph. Stores everything reusable, monetizable, matchable, permissionable, or executable. Key idea: Intent is inventory.

2. **RoomOS** — Organizes monetization by apartment zone (BedroomOS, KitchenOS, BathroomOS, CommonOS, ClosetOS, EntrywayOS, WorkspaceOS, UtilityOS)

3. **MarketOS** — Turns inventory into commerce (listings, SKU creation, pricing, matching, bundles, bodega flows, subscriptions)

4. **ProfileOS** — The human layer. Turns each resident into a personal commerce profile: part storefront, part trust passport, part communication hub, part operating manual

5. **AccessOS** — Controls who can use what (time windows, deposits, host approval, verified-only rules, pickup-only rules)

6. **TrustOS** — Handles safety and governance (identity verification, risk classification, compliance checks, reputation, reviews, disputes)

7. **TransactionOS** — Executes the commerce (bookings, rentals, purchases, errands, fulfillment, contracts, escrow, proof, returns, settlement, payouts, refunds)

8. **LedgerOS** — The blockchain-backed proof and provenance layer. Records consent, access events, proof of pickup/return/condition, settlement events, reputation credentials

9. **CommsOS** — Permissioned communication tied to intent, listings, bookings, transactions, disputes, or approved relationships

---

## AI Assetification

MEMBRA's strongest technical feature is AI Assetification.

A Hero can take photos of:
- A room
- Shelf
- Closet
- Fridge
- Garage
- Kitchen
- Vehicle
- Amazon package pile
- Receipt
- CSV
- Product link
- Amazon order history

MEMBRA detects monetizable assets.

**Flow:** Photo / Amazon import / receipt / CSV / voice note / pasted link → Detect → Assetify → Price → Risk-check → Suggest listing → Hero approves → Marketplace publishes → MEMBRA matches demand → Fulfillment happens → Proof is captured → Payment settles

**Critical rule:** The owner approves what goes public. Nothing is listed without consent.

---

## Amazon Layer 2

MEMBRA can become an Amazon Layer 2.

**Best phrase:** Amazon delivers ownership. MEMBRA activates utilization.

Amazon creates post-purchase inventory. MEMBRA turns that inventory into local liquidity (missed returns, duplicate items, expired return-window products, unused household supplies, bulk Temu inventory, extra chargers, wrong-size items, unopened products, pantry goods, tools, appliances).

---

## Intent-as-Inventory

This is one of MEMBRA's most original ideas. Intent itself becomes inventory.

A user's wants, needs, recurring requests, permissions, boundaries, and willingness are stored as reusable entities.

**Owner intent examples:**
- "I am willing to rent my vacuum."
- "I am willing to sell sealed pantry items."
- "I can offer delivery after 6 PM."
- "I rent couch seating only to verified users."
- "I do not allow bathroom access."

**Demand intent examples:**
- "I need a vacuum for 20 minutes."
- "I need a cup of milk now."
- "I need storage for a package until 8 PM."
- "I need a tripod tonight."
- "I need someone to deliver something two blocks away."

MEMBRA inventories both. This creates a live graph of what exists, who owns it, who may access it, what people need, what people are willing to provide, when it is available, what risk class it belongs to, and what price clears the transaction.

---

## Apartment-as-Bodega

Apartments become bodegas when resident inventory and reusable intent are connected by an LLM.

A user says: "I need eggs, paper towels, and someone to hold my package until 8."

MEMBRA extracts the need, location, urgency, trust need, price preference, access preference, and fulfillment type. Then it matches with neighbors who have eggs, paper towels, can hold packages, can deliver from local store, or Alpha Hub fulfillment.

**Best line:** Not one store downstairs. A thousand tiny storefronts inside the building.

---

## Demand Intelligence and Inventory Investment

MEMBRA is not only a marketplace of existing supply. It creates supply.

A user can ask: "What should I sell or offer near me?"

MEMBRA answers based on local demand signals (recent requests, failed matches, repeat searches, time of day, weather, events, building-level demand clusters, nearby inventory shortages, opt-in purchase behavior, aggregated anonymous trends).

A user can ask: "I have $200. What should I buy to earn locally?"

MEMBRA replies with stock recommendations based on local demand, buy cost, sale/rent price, estimated earnings, risk level, and fulfillment option.

**Important safety rule:** Do not target by race, ethnicity, religion, health, or protected traits. Use aggregate demand behavior instead.

---

## Wallet, Rewards, and Payment Splits

**Example payment split:**
User pays: $40
- Tool Hero earns $6
- Skill Hero earns $22
- Alpha Hub earns $3
- Delivery Hero earns $4
- User receives $1 MEMBRA credit
- MEMBRA earns $4

MEMBRA Wallet can hold:
- Hero earnings
- User cashback
- MEMBRA credits
- Refunds
- Deposits
- Rewards
- Proof receipts
- Access passes
- Referral rewards
- Loyalty status
- Reputation badges

---

## Blockchain Layer

Blockchain acts as the trust, proof, settlement, and provenance rail underneath the marketplace. Use it for:
- Proof of listing
- Proof of consent
- Proof of access
- Proof of deposit
- Proof of return
- Proof of condition
- Proof of transaction
- Reputation portability
- Escrow settlement
- Dispute evidence
- Asset history

The user experience remains simple: Scan → approve → match → rent → return → earn

Under the hood: consent hash, listing record, deposit escrow, access event, return proof, settlement event, review credential.

**Best phrase:** Tokenized access, not speculative assets.

---

## Entrepreneurship-as-a-Service

MEMBRA is Entrepreneurship-as-a-Service for the home. Not everyone wants to start a business. MEMBRA creates the business stack automatically (inventory creation, intent capture, listing generation, pricing, contracts, trust, proof, settlement, reputation).

**Best investor phrase:** MEMBRA is Entrepreneurship-as-a-Service for the home: an AI and blockchain-powered stack that turns household assets, human intent, and local availability into verified income streams.

**Best consumer phrase:** MEMBRA helps you make money from what you already own, what you can do, and what you are willing to share.

**Big distinction:** Gig apps make people the labor. MEMBRA makes people the operator.

---

## HouseOS-as-a-Service

MEMBRA can also be framed as HouseOS-as-a-Service. The core prompt: What else in my house can make money?

MEMBRA scans the home and identifies monetization categories:
- **ObjectOS** — Things you own (vacuum, drill, ladder, toolkit, ring light, tripod, projector, speaker, printer, scanner, etc.)
- **SpaceOS** — Unused space (closet shelf, cabinet shelf, garage corner, basement area, balcony space, fridge shelf, freezer space, pantry shelf, package holding spot, bike storage, luggage storage, parking spot if allowed)
- **UtilityOS** — Household access (charging station, Wi-Fi access, desk hour, printer use, scanner use, cold storage, ice, filtered water where allowed)
- **SkillOS** — What the user can do (furniture assembly, local delivery, dog walking, tutoring, tech setup, cleaning help, sewing, translation, content creation help)
- **TimeOS** — Availability as inventory (run errands after 6 PM, accept package deliveries, hold items until pickup, wait for maintenance, carry groceries upstairs)

**Best thesis:** MEMBRA turns the home into an income-generating operating system by inventorying objects, spaces, utilities, skills, time, permissions, and reusable intent.

**Sharpest line:** Your house is not just where you live. It is under-inventoried economic infrastructure.

---

## Safety and Risk Boundaries

MEMBRA must stay governable.

**Safe early categories:**
- Tools, tripods, ring lights, sealed supplies
- Couch seats, desk seats, charging access, Wi-Fi
- Closet shelf, storage, package holding
- Local errands, delivery help

**Medium-risk:**
- Fridge shelf, pantry splits, cleaning supplies
- Small appliance lending, workspace access
- Ingredient splitting

**High-risk later:**
- Shower access, bathroom access
- Food handling, hygiene infrastructure
- Home entry, cooked food
- Transportation of people

**Avoid early or prohibit:**
- Medicine, alcohol, open food
- Sleep/bed access, intimacy, companionship
- Bodily services, regulated goods
- Anything ambiguous around consent or legality

**Rule:** MEMBRA is not "anything of any nature." MEMBRA is anything permissioned, legal, safe, priceable, and governable.

---

## Defensible Novelty

MEMBRA's defensible novelty is not "local marketplace" — that category exists everywhere (Facebook Marketplace, Nextdoor, OfferUp, TaskRabbit, Neighbor, Turo-style asset rental, local services marketplaces).

The stronger claim is:

**MEMBRA is an agentic local-commerce operating layer that converts private household assets into permissioned, proof-backed, locally matched market supply.**

This distinction is much cleaner than "AI marketplace" because AI marketplace is already crowded (AI commerce/chat shopping assistants help users shop conversationally, but usually against existing merchant catalogs, not household-level supply creation).

MEMBRA does not compete with:
- **Membrane** (getmembrane.com) — AI-generated software integrations, unified APIs, MCP/tooling, SaaS app connectors (different category entirely)

MEMBRA's uniqueness lies in:
- **AI assetification of private household reality** — photos, receipts, Amazon orders, CSVs, and voice prompts become structured local inventory
- **Intent-as-inventory** — wants, needs, permissions, boundaries, and willingness become reusable entities
- **Apartment-as-bodega** — homes become local business nodes through permissioned inventory and fulfillment
- **Demand intelligence** — MEMBRA shows what the neighborhood already wants and recommends what to stock, rent, store, deliver, or service
- **Proof-backed transactions** — blockchain records consent, access events, pickup/return proof, settlement events, reputation credentials

The result: Every apartment becomes the nearest warehouse, every useful object becomes a potential SKU, every Hero becomes a local operator, and every chat becomes a pathway from need into income.

---

## Full Final Pitch

MEMBRA is a marketplace you talk to.

It turns homes into local business nodes by converting household inventory, post-purchase goods, rooms, spaces, skills, storage, utilities, delivery capacity, reusable intent, and local demand into permissioned marketplace transactions.

Users ask for what they need. Heroes earn by offering what they own, what they can do, or what their home can provide. Hero Houses become local pickup, storage, service, and inventory nodes. Alpha Hubs become trusted fulfillment infrastructure for the neighborhood.

MEMBRA uses AI to assetify household reality: photos, receipts, Amazon orders, CSVs, and voice prompts become structured listings with pricing, risk controls, trust rules, demand estimates, and fulfillment options.

It also turns demand into work. If a person does not know what to sell or offer, MEMBRA shows what the neighborhood already wants and recommends what to stock, rent, cook, store, deliver, or service.

The result is a new local commerce layer:
- Every apartment becomes the nearest warehouse
- Every useful object becomes a potential SKU
- Every Hero becomes a local operator
- Every chat becomes a pathway from need into income
- Every purchase can return value through MEMBRA Wallet

**Final tagline stack:**
- A marketplace you talk to
- Need nearby. Earn locally
- Turn assets into access
- Every apartment is the nearest warehouse
- Users need. Heroes earn. Hero Houses become Alpha Hubs

---

## Combined Repositories

This repo combines and references earlier work from GitHub submodules. See `/submodules/` for linked projects.

## Documentation

- [MEMBRA Master Summary](docs/MEMBRA_MASTER_SUMMARY.md) — Complete overview of MEMBRA as a chat-first, LLM-operated local sharing marketplace
- [Submodule Components](docs/SUBMODULE_COMPONENTS.md) — Which parts from each submodule can be used for MEMBRA

## Technical Structure

```
MEMBRA/
├── models/
│   └── membra.py          # Core data models (Item, Space, Skill, Request, Listing, Transaction, Credit, Assessment, AdAgentCampaign)
├── api/
│   └── membra_endpoints.py # API endpoints for MEMBRA modules
├── docs/
│   ├── MEMBRA_MASTER_SUMMARY.md
│   └── SUBMODULE_COMPONENTS.md
├── requirements.txt
├── .gitignore
├── .gitmodules
└── README.md
```

## Public Deployment Links

**Quick Deploy to Railway (Easiest):**
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select this repository
4. Railway will auto-detect Python/FastAPI
5. Add environment variables (see below)
6. Click Deploy
7. **Your public links will appear after ~2 minutes:**
   - API: `https://your-project.railway.app`
   - Swagger UI: `https://your-project.railway.app/docs`
   - ReDoc: `https://your-project.railway.app/redoc`
   - Custom UI: `https://your-project.railway.app/docs-ui`

**Quick Deploy to Render:**
1. Go to https://render.com
2. Click "New +"
3. Select "Web Service"
4. Connect GitHub repository
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
7. **Your public links will appear after deployment:**
   - API: `https://your-project.onrender.com`
   - Swagger UI: `https://your-project.onrender.com/docs`
   - ReDoc: `https://your-project.onrender.com/redoc`
   - Custom UI: `https://your-project.onrender.com/docs-ui`

**Required Environment Variables:**
```env
DEBUG=False
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/membra
REDIS_URL=redis://host:6379/0
# Optional for full features:
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_...
```

**Current Local Links (for development):**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Custom UI: http://localhost:8000/docs-ui
- OpenAPI Spec: http://localhost:8000/openapi.json

## Getting Started

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Run with Docker Compose (includes PostgreSQL and Redis)
docker-compose up -d

# Or run directly
./run.sh
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation
- Local: http://localhost:8000/docs
- Local ReDoc: http://localhost:8000/redoc

---

**MEMBRA — A marketplace you talk to.**
