# MEMBRA Inventorization Index Map

MEMBRA inventorizes household reality into canonical fields, then indexes those fields into searchable, priced, risk-scored, permissioned, and settleable economic units.

## The Flow

Household Reality → Inventorization Layer → Canonical Field Record → Index Families → MembraIndexRecord → Liquidity Outputs

## Household Reality

- Room Scan
- Host Input
- Item Detection
- Availability Capture
- Access Constraints

## Inventorization Layer

### Canonical Field Record

- field_id
- field_name
- field_type
- source_object
- entity_type
- entity_id
- capture_method
- raw_value
- normalized_value
- confidence_score
- owner_verified
- system_verified
- indexable_status
- created_at
- updated_at

## Index Families

### Inventory Index
**Purpose**: What exists?

### Utility Index
**Purpose**: What useful unit can be exposed?

### SKU Index
**Purpose**: What becomes transactable?

### MUP Index
**Purpose**: What is the minimum useful price?

### Risk Index
**Purpose**: What must be restricted, insured, proven, or blocked?

### Trust Index
**Purpose**: Who can safely transact?

### Access Index
**Purpose**: How can the unit be accessed?

### Demand Index
**Purpose**: Who wants it, where, and how urgently?

### Liquidity Index
**Purpose**: What portion can safely enter the market?

### Yield Index
**Purpose**: What does the node earn?

### Proof Index
**Purpose**: What evidence clears settlement?

### Settlement Index
**Purpose**: What paid, returned, cleared, or disputed?

## MembraIndexRecord

The compressed representation of one liquid household unit.

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

## Liquidity Outputs

- Trust-Adjusted Liquidity
- Node Yield
- Inventory Credit File
- Household Utility Index
- Finance-Ready SKU Ledger

## Example Flow

### Raw Reality
"Black upright vacuum near boxes"

### Inventorized Field
- field_name = vacuum_cleaner
- field_type = object
- raw_value = black upright vacuum near boxes
- normalized_value = Vacuum Cleaner
- confidence_score = 0.93
- owner_verified = true
- indexable_status = true

### Indexed Unit
- Inventory Index = Cleaning Appliance
- Utility Index = 20-minute cleaning access
- SKU Index = Vacuum access, door handoff
- MUP Index = $5.00 minimum useful price
- Risk Index = Medium
- Trust Index = Host verified
- Access Index = No home entry, door handoff
- Demand Index = High local repeat demand
- Liquidity Index = Listed and usable
- Yield Index = $42/month projected
- Proof Index = Return photo required
- Settlement Index = Escrow-ready

### Compressed MembraIndexRecord
- membra_index_id: MI-LIVINGROOM-0007
- canonical_name: Vacuum Cleaner
- unit_type: 20-minute use
- minimum_useful_price: $5
- suggested_price: $7
- risk_grade: Medium
- trust_score: 93.7
- demand_score: 81.4
- liquidity_score: 72.8
- finance_ready: false

## The Defensible Phrase

MEMBRA inventorizes household reality into canonical fields, then indexes those fields into searchable, priced, risk-scored, permissioned, and settleable economic units.
