# MEMBRA Liquid Inventorization and Indexing

## The Inventorization Claim

MEMBRA inventorizes the private world. It converts rooms, objects, spaces, skills, services, utilities, and time windows into indexed economic fields. Those fields become searchable inventory, priced utility units, permissioned SKUs, risk-scored transactions, proof-backed settlements, and trust-adjusted liquidity.

## Inventorization Layer

Inventorization is the process of turning unstructured household reality into structured, indexed, priced, and permissioned inventory fields.

### Canonical Inventorization Fields

- **field_id**: Unique identifier for the inventorized field
- **field_name**: Human-readable name of the field
- **field_type**: Type of field (object, space, utility, service, skill, consumable, storage, access)
- **source_object**: Original source object (e.g., room scan, manual entry)
- **entity_type**: Type of entity (inventory_item, utility_unit, sku, transaction)
- **entity_id**: Unique identifier for the entity
- **capture_method**: How the field was captured (ai_vision, manual, hybrid)
- **raw_value**: Raw unprocessed value from capture
- **normalized_value**: Canonical normalized value
- **confidence_score**: Confidence score for field detection/classification
- **owner_verified**: Whether the host has verified this field
- **system_verified**: Whether the system has verified this field
- **indexable_status**: Whether the field is ready for indexing
- **created_at**: Timestamp when record was created
- **updated_at**: Timestamp when record was last updated

### Example

```
field_name: "vacuum_cleaner"
field_type: "object"
source_object: "living_room_scan"
entity_type: "inventory_item"
raw_value: "black upright vacuum near boxes"
normalized_value: "Vacuum Cleaner"
confidence_score: 0.93
owner_verified: true
indexable_status: true
```

The critical move is that nothing stays descriptive. Everything becomes fielded.

"Vacuum in room" becomes:
- category = Appliance
- subcategory = Cleaning
- unit_type = 20-minute access
- risk_grade = Medium
- mup = $5.00
- suggested_price = $7.00
- availability = Host approved
- proof_required = Return photo
- liquidity_status = Indexable

## Field Classes

MEMBRA classifies every field into one of ten index families:

1. **Identity Fields** - Who controls this?
2. **Location Fields** - Where can it be accessed?
3. **Inventory Fields** - What exists?
4. **Utility Fields** - What useful unit can be sold?
5. **Pricing Fields** - What is the minimum viable price?
6. **Risk Fields** - What can go wrong?
7. **Trust Fields** - Who is allowed to transact?
8. **Access Fields** - How does the transaction happen?
9. **Transaction Fields** - What cleared?
10. **Liquidity Fields** - What value can safely enter the market?

## Index Dictionary

### Inventory Index

**Purpose**: Makes household assets searchable and classifiable.

**Indexed fields**: item_id, node_id, canonical_name, category, subcategory, condition, brand, model, detection_confidence, owner_approved, photo_hash

**Example query**: Find all approved cleaning appliances within 1 mile.

### Utility Index

**Purpose**: Converts inventory into useful access units.

**Indexed fields**: utility_unit_id, item_id, unit_type, unit_duration, unit_capacity, unit_quantity, unit_constraints, availability_window

**Examples**:
- Vacuum Cleaner → 20-minute cleaning access
- Shelf Space → cubic-foot/month storage access
- Ring Light → hourly lighting access

### SKU Index

**Purpose**: Makes approved utility units transactable.

**Indexed fields**: sku_id, node_id, item_id, utility_unit_id, sku_name, rent_mode, space_mode, access_mode, fulfillment_mode, price, deposit_required, listing_status

**Example query**: Show rentable tools under $10/hour with host-approved status.

### MUP Index

**Purpose**: Tracks the smallest economically useful price for each unit.

**Indexed fields**: sku_id, host_friction_cost, risk_cost, time_cost, depreciation_cost, cleaning_cost, handoff_cost, platform_margin, minimum_useful_price, suggested_price, price_confidence

**Core rule**: A SKU is liquid only when market price >= MUP.

### Risk Index

**Purpose**: Prevents unsafe liquidity.

**Indexed fields**: sku_id, risk_grade, damage_risk, theft_risk, privacy_risk, access_risk, regulatory_risk, hygiene_risk, insurance_required, prohibited_flag

**Risk decision**:
- Low Risk → listable
- Medium Risk → deposit/proof required
- High Risk → restricted
- Prohibited → blocked

### Trust Index

**Purpose**: Scores whether host, requester, hero, node, and SKU are reliable enough to transact.

**Indexed fields**: entity_type, entity_id, identity_score, transaction_score, proof_score, return_score, dispute_score, condition_score, response_score, final_trust_score

**Trust objects**: Host Trust, Requester Trust, Hero Trust, Node Trust, SKU Trust

### Access Index

**Purpose**: Defines how utility can be accessed safely.

**Indexed fields**: sku_id, access_mode, handoff_mode, pickup_allowed, delivery_allowed, meet_halfway_allowed, home_entry_required, access_window, proof_required, deposit_required, identity_required

**Access modes**: No Entry, Door Handoff, Meet Halfway, Hero Delivery, Host Delivery, Supervised Use, On-Premise Use, Restricted Access

### Demand Index

**Purpose**: Measures whether a SKU has likely buyer/requester demand.

**Indexed fields**: sku_id, local_search_count, intent_match_count, category_demand_score, radius_demand_score, urgency_score, seasonality_score, repeatability_score, demand_confidence

**Examples**:
- Vacuum: high local demand, repeatable, short-duration
- Closet storage: medium demand, long-duration
- Couch seat: uncertain demand, higher access risk

### Liquidity Index

**Purpose**: Converts approved inventory into finance-readable safe value.

**Indexed fields**: node_id, gross_utility_value, approved_sku_value, risk_adjusted_value, trust_adjusted_value, demand_adjusted_value, availability_adjusted_value, trust_adjusted_liquidity, liquidity_band

**Liquidity bands**: Dormant, Detected, Approved, Listed, Matched, Transacted, Yielding, Finance-Ready

This is one of the most important MEMBRA primitives.

### Yield Index

**Purpose**: Tracks earning capacity per node, SKU, host, and category.

**Indexed fields**: node_id, sku_id, gross_projected_yield, net_projected_yield, actual_yield, utilization_rate, yield_per_sku, yield_per_square_foot, yield_per_available_hour, repeat_rate

This makes MEMBRA look like fintech, not classifieds.

### Proof Index

**Purpose**: Makes physical-world transactions auditable.

**Indexed fields**: proof_id, transaction_id, proof_type, photo_before_hash, photo_after_hash, timestamp, geo_hash, condition_delta, attestation_score, proof_score

### Settlement Index

**Purpose**: Records completed financial movement.

**Indexed fields**: transaction_id, sku_id, node_id, host_id, requester_id, hero_id, gross_amount, platform_fee, hero_fee, insurance_fee, payout_amount, escrow_status, settlement_status, refund_status, dispute_status

This is what later supports inventory credit files and underwriting.

## Master Index Object

**MembraIndexRecord** is the compressed representation of one liquid household unit.

**Fields**:
- membra_index_id
- node_id
- host_id
- item_id
- utility_unit_id
- sku_id
- canonical_name
- category
- unit_type
- unit_duration
- access_mode
- fulfillment_mode
- minimum_useful_price
- suggested_price
- deposit_required
- risk_grade
- trust_score
- demand_score
- liquidity_score
- yield_score
- owner_approved
- risk_approved
- listed_status
- transaction_status
- proof_required
- settlement_ready
- finance_ready
- created_at
- updated_at

**Example**:
```
membra_index_id: MI-LIVINGROOM-0007
canonical_name: Vacuum Cleaner
category: Appliance / Cleaning
unit_type: 20-minute use
access_mode: Door Handoff
fulfillment_mode: Host Handoff
minimum_useful_price: $5.00
suggested_price: $7.00
risk_grade: Medium
trust_score: 93.7
demand_score: 81.4
liquidity_score: 72.8
yield_score: 64.2
owner_approved: true
risk_approved: true
listed_status: Listed
finance_ready: false
```

## Indexing Pipeline

The defensible process:

1. **Capture** - Room image, host input, object list, availability, location zone
2. **Normalize** - Convert raw labels into canonical MEMBRA categories
3. **Classify** - Assign object, space, utility, service, skill, consumable, storage, or access category
4. **Fractionalize** - Convert item into minimum useful units
5. **Price** - Calculate MUP and suggested market price
6. **Risk-score** - Apply category, access, hygiene, theft, privacy, and regulatory risk
7. **Trust-score** - Apply host, requester, node, SKU, and proof confidence
8. **Permission** - Determine access mode, deposit, proof, and identity requirements
9. **Index** - Write the object into Inventory, SKU, Risk, Trust, Liquidity, and Yield indexes
10. **Activate** - Allow search, match, quote, booking, proof, settlement, and yield tracking

## Field-to-Index Mapping

The data dictionary becoming an index system:

- **canonical_name** → Inventory Index, SKU Index, Search Index
- **category** → Inventory Index, Risk Index, Demand Index
- **unit_type** → Utility Index, Pricing Index, Yield Index
- **minimum_useful_price** → MUP Index, Liquidity Index
- **risk_grade** → Risk Index, Access Index, Liquidity Index
- **trust_score** → Trust Index, Match Index, Liquidity Index
- **availability_window** → Access Index, Demand Index, Match Index
- **proof_required** → Proof Index, Risk Index, Settlement Index
- **transaction_count** → Yield Index, Trust Index, Demand Index
- **settlement_status** → Settlement Index, Ledger Index, Finance-Ready Index
- **actual_yield** → Yield Index, Node Index, Underwriting Index

## Defensible Fintech Index Stack

The final finance-grade index hierarchy:

```
Household Utility Index
│
├── Inventory Index
│   └── What exists?
│
├── Utility Index
│   └── What useful unit can be exposed?
│
├── MUP Index
│   └── What is the minimum viable price?
│
├── Risk Index
│   └── What must be blocked, restricted, insured, or proven?
│
├── Trust Index
│   └── Who can safely transact?
│
├── Demand Index
│   └── Who wants this unit, where, and how urgently?
│
├── Liquidity Index
│   └── What portion of household utility can safely enter the market?
│
├── Yield Index
│   └── What does the node earn?
│
└── Settlement Index
    └── What cleared, paid, returned, and settled?
```

## Hypercompressed Version

Inventorization turns household reality into fields.
Indexing turns those fields into market structure.
MEMBRA's moat is the field grammar: every private object, space, service, utility, and time window becomes a searchable, priced, risk-scored, permissioned, and settleable economic unit.
