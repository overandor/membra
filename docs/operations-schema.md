# MEMBRA Operations Schema

## Product Architecture Loop

Intent → Inventory → Assetization → Fractionalization → Listing → Access → Fulfillment → Proof → Settlement → Reputation → Replenishment

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
- Raw inventory item converted to commercial asset
- Asset receives: unique ID, category, condition rating, risk level
- Asset tagged with access requirements (supervised, unsupervised, remote)
- Asset assigned base pricing tier

### Fractionalization
- Asset broken into usable units
- Time-based: hourly, daily, weekly access
- Space-based: shelf units, closet sections, storage zones
- Usage-based: per-use, per-charge, per-delivery
- Each unit receives Minimum Useful Price (MUP)

### Listing
- Fractional unit becomes public SKU
- SKU includes: price, availability, access rules, fulfillment method
- SKU published to local market
- SKU indexed by location, category, price, availability

### Access
- Requester discovers SKU through search or recommendation
- Requester requests access with proposed terms
- Host receives request with requester reputation and verification status
- Host approves, modifies, or declines request

### Fulfillment
- Access granted based on approved terms
- Fulfillment method executed: pickup, delivery, on-site, remote
- Hero may handle logistics for physical items
- Access timer or usage meter activated

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

### Replenishment
- Asset availability restored
- Inventory count updated
- Asset condition re-evaluated
- SKU may be repriced based on demand

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
