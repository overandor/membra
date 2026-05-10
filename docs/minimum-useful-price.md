# Minimum Useful Price (MUP)

## Concept

MEMBRA does not ask what an item is worth. It asks what the smallest useful purchasable unit of access is.

A drill is not a $90 item; it is $7/hour.
A shelf is not unused space; it is $12/month.
A couch is not furniture; it is $8/hour seating capacity.
A delivery trip is not a favor; it is an $8 local drop-off SKU.

That is the economic innovation: household assets become fractional access units.

## MUP Calculation

### Factors
- **Base asset value**: Original purchase price or replacement cost
- **Depreciation**: Age, condition, wear
- **Utility frequency**: How often the asset is typically used
- **Setup overhead**: Time to prepare, hand off, verify return
- **Risk exposure**: Probability of damage, loss, or dispute
- **Market rate**: Comparable rental prices in area
- **Supply/demand**: Local inventory scarcity vs. demand

### Formula

```
MUP = (Hourly Depreciation + Setup Overhead + Risk Premium + Market Adjustment) × (1 + Platform Margin)
```

### Component Breakdown

#### Hourly Depreciation
```
Hourly Depreciation = (Asset Value × Annual Depreciation Rate) / 8760 hours
```

- Annual depreciation rate by asset type:
  - Tools: 15%
  - Appliances: 10%
  - Furniture: 8%
  - Storage space: 0%

#### Setup Overhead
```
Setup Overhead = (Preparation Time + Handoff Time + Verification Time) × Host Hourly Rate
```

- Preparation time: 5-15 minutes typical
- Handoff time: 2-10 minutes
- Verification time: 2-5 minutes
- Host hourly rate: $20-50 (estimated local labor rate)

#### Risk Premium
```
Risk Premium = Asset Value × Damage Probability × Risk Factor
```

- Damage probability by risk level:
  - Low risk: 0.1%
  - Medium risk: 1%
  - High risk: 5%

- Risk factor:
  - Low: 1.0
  - Medium: 2.0
  - High: 5.0

#### Market Adjustment
```
Market Adjustment = (Local Market Rate - Calculated Rate) × Market Sensitivity
```

- Market sensitivity: 0.3-0.7 (how much to weight local market vs. calculated rate)
- Local market rate from comparable listings

#### Platform Margin
```
Platform Margin = 15-25% (covers platform fees, insurance, processing)
```

## MUP Examples

### Drill ($90 value, good condition, low risk)
- Hourly depreciation: $90 × 15% / 8760 = $0.15/hour
- Setup overhead: 10 minutes × $30/hour = $5/hour
- Risk premium: $90 × 0.1% × 1.0 = $0.09/hour
- Market adjustment: $2/hour (local market rate $7/hour)
- Subtotal: $7.24/hour
- Platform margin (20%): $1.45/hour
- **MUP: $8.69/hour**

### Shelf space ($0 value, low risk)
- Hourly depreciation: $0
- Setup overhead: 5 minutes × $30/hour = $2.50/hour
- Risk premium: $0
- Market adjustment: $0.50/hour (local storage rates)
- Subtotal: $3.00/hour
- Platform margin (20%): $0.60/hour
- **MUP: $3.60/hour ($108/month)**

### Vacuum ($80 value, fair condition, low risk)
- Hourly depreciation: $80 × 15% / 8760 = $0.14/hour
- Setup overhead: 8 minutes × $30/hour = $4/hour
- Risk premium: $80 × 0.1% × 1.0 = $0.08/hour
- Market adjustment: $1.50/hour
- Subtotal: $5.72/hour
- Platform margin (20%): $1.14/hour
- **MUP: $6.86/hour**

### Couch ($300 value, good condition, medium risk)
- Hourly depreciation: $300 × 8% / 8760 = $0.27/hour
- Setup overhead: 5 minutes × $30/hour = $2.50/hour
- Risk premium: $300 × 1% × 2.0 = $6/hour
- Market adjustment: $0
- Subtotal: $8.77/hour
- Platform margin (20%): $1.75/hour
- **MUP: $10.52/hour**

## MUP by Category

### Storage Space
- Shelf space: $3-5/hour ($90-150/month)
- Closet space: $5-8/hour ($150-240/month)
- Garage space: $8-15/hour ($240-450/month)

### Tools
- Hand tools (drills, saws): $5-10/hour
- Power tools (vacuums, sanders): $6-12/hour
- Specialty tools (pressure washers): $10-20/hour

### Furniture
- Chairs: $5-15/hour
- Tables: $8-20/hour
- Sofas (seating capacity): $8-15/hour per seat

### Small Appliances
- Kitchen appliances: $3-8/hour
- Cleaning appliances: $6-12/hour
- Entertainment equipment: $8-15/hour

### Services
- Local delivery: $8-15/trip
- Pickup coordination: $5-10/trip
- On-site assistance: $20-50/hour

## Dynamic Pricing

MEMBRA can adjust MUP based on:
- **Demand spikes**: Increase price during peak periods
- **Supply glut**: Decrease price when inventory is abundant
- **Seasonal factors**: Adjust for seasonal demand (e.g., storage in winter)
- **Bulk discounts**: Lower per-unit price for longer bookings
- **Early bird discounts**: Lower price for advance bookings

## Price Floor

Every SKU has a minimum price floor below which it cannot be listed:
- Ensures host profitability
- Covers platform costs
- Maintains quality perception
- Prevents race-to-the-bottom pricing

Price floor = MUP × 0.7 (minimum 70% of calculated MUP)

## Host Override

Hosts can set custom prices within bounds:
- Minimum: 70% of MUP
- Maximum: 200% of MUP
- System suggests MUP as default
- Host can adjust based on personal preference
