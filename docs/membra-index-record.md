# MembraIndexRecord

## Definition

The MembraIndexRecord is the central underwriting object for MEMBRA. It is the compressed representation of one liquid household unit, containing all fields required for inventory, pricing, risk assessment, trust scoring, access control, demand estimation, liquidity calculation, yield projection, proof requirements, and settlement readiness.

## Structure

```json
{
  "membra_index_id": "MI-LIVINGROOM-0007",
  "node_id": "NODE-LIVINGROOM-ALPHA",
  "host_id": "HOST-001",
  "item_id": "ITEM-0007",
  "utility_unit_id": "UU-0007",
  "sku_id": "SKU-0007",
  
  "canonical_name": "Vacuum Cleaner",
  "category": "Appliance / Cleaning",
  "unit_type": "20-minute use",
  "unit_duration": "20 minutes",
  "access_mode": "Door Handoff",
  "fulfillment_mode": "Host Handoff",
  
  "minimum_useful_price": 5.00,
  "suggested_price": 7.00,
  "deposit_required": 15.00,
  
  "risk_grade": "Medium",
  "trust_score": 93.7,
  "demand_score": 81.4,
  "liquidity_score": 72.8,
  "yield_score": 64.2,
  
  "owner_approved": true,
  "risk_approved": true,
  "listed_status": "Listed",
  "transaction_status": "None",
  
  "proof_required": "Return photo",
  "settlement_ready": true,
  "finance_ready": false
}
```

## Field Descriptions

### Identity Fields
- **membra_index_id**: Unique identifier for the MembraIndexRecord
- **node_id**: Identifier for the household node
- **host_id**: Identifier for the host who owns the asset
- **item_id**: Identifier for the physical item
- **utility_unit_id**: Identifier for the utility unit abstraction
- **sku_id**: Identifier for the transactable SKU

### Asset Fields
- **canonical_name**: Standardized name for the asset
- **category**: Hierarchical category classification
- **unit_type**: Type of utility unit (e.g., "20-minute use", "cubic-foot/month")
- **unit_duration**: Duration of the utility unit
- **access_mode**: How the unit can be accessed (Door Handoff, On-Premise Use, etc.)
- **fulfillment_mode**: How fulfillment occurs (Host Handoff, Self-Service, etc.)

### Pricing Fields
- **minimum_useful_price**: MUP - minimum economically viable price
- **suggested_price**: Market-adjusted suggested price
- **deposit_required**: Security deposit amount

### Index Scores
- **risk_grade**: Risk classification (Low, Medium, High, Prohibited)
- **trust_score**: Trust score (0-100)
- **demand_score**: Demand score (0-100)
- **liquidity_score**: Liquidity score (0-100)
- **yield_score**: Yield score (0-100)

### Approval Fields
- **owner_approved**: Owner has approved this unit for listing
- **risk_approved**: Risk system has approved this unit for listing
- **listed_status**: Current listing status (Listed, Unlisted, Pending)
- **transaction_status**: Current transaction status (None, Active, Completed, Disputed)

### Settlement Fields
- **proof_required**: Type of proof required for settlement
- **settlement_ready**: Whether the unit is ready for settlement
- **finance_ready**: Whether the unit is ready for financial settlement

## Index Sources

Each field in the MembraIndexRecord is populated from one or more index families:

- **Inventory Index**: Provides identity and asset fields
- **Utility Index**: Provides unit_type and unit_duration
- **SKU Index**: Provides canonical_name and category
- **MUP Index**: Provides minimum_useful_price
- **Risk Index**: Provides risk_grade
- **Trust Index**: Provides trust_score
- **Access Index**: Provides access_mode and fulfillment_mode
- **Demand Index**: Provides demand_score
- **Liquidity Index**: Provides liquidity_score
- **Yield Index**: Provides yield_score
- **Proof Index**: Provides proof_required
- **Settlement Index**: Provides settlement_ready and finance_ready

## Usage

The MembraIndexRecord is used throughout the MEMBRA system:

1. **Inventory Detection**: AI vision creates initial MembraIndexRecord candidates
2. **Owner Approval**: Host reviews and approves records
3. **Risk Assessment**: Risk system evaluates and approves records
4. **Listing**: Approved records become searchable SKUs
5. **Matching**: Requesters search and match against records
6. **Fulfillment**: Access mode and fulfillment mode guide execution
7. **Proof**: Proof required field guides settlement verification
8. **Settlement**: Settlement ready and finance ready enable payment

## Example

A vacuum cleaner detected in a living room:

```json
{
  "membra_index_id": "MI-LIVINGROOM-0007",
  "canonical_name": "Vacuum Cleaner",
  "category": "Appliance / Cleaning",
  "unit_type": "20-minute use",
  "access_mode": "Door Handoff",
  "fulfillment_mode": "Host Handoff",
  "minimum_useful_price": 5.00,
  "suggested_price": 7.00,
  "deposit_required": 15.00,
  "risk_grade": "Medium",
  "trust_score": 93.7,
  "demand_score": 81.4,
  "liquidity_score": 72.8,
  "yield_score": 64.2,
  "owner_approved": true,
  "risk_approved": true,
  "listed_status": "Listed",
  "proof_required": "Return photo",
  "settlement_ready": true,
  "finance_ready": false
}
```

This record represents a 20-minute vacuum access unit that can be accessed via door handoff, requires a $15 deposit, has medium risk, and is ready for settlement but not yet finance-ready (pending trust history or insurance).
