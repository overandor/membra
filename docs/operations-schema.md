# MEMBRA Liquid Operations Schema

## Product Architecture Loop

Intent → Inventory → Assetization → Fractionalization → Risk → Permission → Price → Transaction → Proof → Settlement → Reputation → Yield

## Stage Definitions

### Intent
- User expresses need through natural language, search, or category browse
- LLM translates casual intent into structured request
- Request includes: item type, duration, location, budget, urgency

### Inventory
- Household assets detected via AI vision or manual entry
- Each asset evaluated for commercial potential
- Confidence score assigned to detection
- Asset categorized by type, risk, and utility

### Assetization
- Raw inventory item converted to liquid asset
- Asset receives: unique ID, category, condition rating, risk level
- Asset tagged with access requirements (supervised, unsupervised, remote)
- Asset assigned base pricing tier using MUP

### Fractionalization
- Asset broken into Minimum Useful Units
- Time-based: hourly, daily, weekly access
- Space-based: shelf units, closet sections, storage zones
- Usage-based: per-use, per-charge, per-delivery
- Each unit receives Minimum Useful Price (MUP)

### Risk
- Risk assessment based on asset type, condition, access mode
- Risk score assigned: Low, Medium, High
- Risk determines insurance requirements and deposit amounts
- Risk affects trust-adjusted liquidity calculation

### Permission
- Access rules defined for each fractional unit
- Permission based on: trust score, verification level, risk tolerance
- Access modes: supervised, unsupervised, remote
- Permission granted or denied based on criteria

### Price
- MUP calculated for each fractional unit
- Price quoted based on MUP, market conditions, demand
- Dynamic pricing based on supply/demand
- Price floor enforced (70% of MUP)

### Transaction
- Requester requests access to fractional unit
- Host approves, modifies, or declines request
- Transaction created with terms
- Escrow holds payment

### Proof
- Fulfillment confirmed through: photo, GPS, digital signature, time-stamp
- Return condition verified
- Usage duration recorded
- Any disputes logged with evidence

### Settlement
- Payment released from escrow
- Fees deducted: platform fee, hero fee, insurance fee
- Net amount transferred to host
- Transaction recorded in ledger

### Reputation
- Both parties rate each other
- Trust scores updated
- Verification status may increase
- Risk profile adjusted based on transaction history

### Yield
- Node yield calculated based on approved inventory
- Monthly revenue projected
- Trust-adjusted liquidity computed
- Household Utility Index contribution calculated

## Data Model

### Inventory Item
```json
{
  "id": "string",
  "type": "storage|tool|appliance|furniture|space|service",
  "name": "string",
  "description": "string",
  "condition": "excellent|good|fair|poor",
  "confidence_score": 0.0-1.0,
  "risk_level": "low|medium|high",
  "access_mode": "supervised|unsupervised|remote",
  "base_price_usd": number,
  "image_url": "string"
}
```

### SKU
```json
{
  "id": "string",
  "inventory_item_id": "string",
  "fractional_unit": "hourly|daily|weekly|per_use|per_unit",
  "price_usd": number,
  "availability": "available|booked|maintenance",
  "access_rules": {},
  "fulfillment_method": "pickup|delivery|onsite|remote",
  "location": {
    "lat": number,
    "lng": number,
    "radius_meters": number
  },
  "min_booking_duration": number,
  "max_booking_duration": number
}
```

### Transaction
```json
{
  "id": "string",
  "sku_id": "string",
  "requester_id": "string",
  "host_id": "string",
  "hero_id": "string|null",
  "start_time": "ISO8601",
  "end_time": "ISO8601",
  "total_price_usd": number,
  "platform_fee_usd": number,
  "hero_fee_usd": number,
  "insurance_fee_usd": number,
  "net_payout_usd": number,
  "status": "pending|approved|active|completed|disputed|cancelled",
  "proof_url": "string|null",
  "proof_type": "photo|gps|signature|null"
}
```

## Hero/House/Alpha Hub Model

### House
- Physical household node
- Contains inventory items
- Has trust score
- Has availability schedule
- Has access rules

### Hero
- Local fulfillment agent
- Can handle pickup, delivery, inspection
- Has reputation score
- Has service radius
- Has availability schedule

### Alpha Hub
- High-volume household node
- Has dedicated inventory
- May employ heroes
- Has premium verification
- Has priority in matching

## Risk Mitigation

### Low Risk Categories
- Storage space (shelf, closet, garage)
- Tools (drills, vacuums, chargers)
- Furniture (chairs, tables)
- Small appliances (blenders, toasters)
- Sealed consumables

### High Risk Categories (Avoid in MVP)
- Bedrooms
- Unattended home access
- Hygiene-sensitive goods
- Medical items
- Weapons
- Controlled substances
- Adult access
- Financial services
- Childcare

### Risk Mitigation Measures
- Photo proof required for returns
- GPS verification for pickup/delivery
- Time-stamped access logs
- Deposit for high-value items
- Insurance coverage
- Hero supervision for unsupervised access
- Reputation gating
