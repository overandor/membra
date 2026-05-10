# Host Node Model

## Overview

The Host Node Model defines how households become verified micro-warehouses and utility nodes for neighborhood commerce. A "House" is a physical household node with inventory, trust score, availability, and access rules.

## House Node

### Definition
A House is a physical household or space converted into a structured commerce source. It contains inventory items, has a trust score, availability schedule, and access rules.

### House Attributes

#### Identity
- House ID (unique)
- Host ID (owner)
- Address (or approximate location)
- Geolocation (lat, lng, radius)
- House type (apartment, house, condo, townhouse)

#### Capacity
- Total inventory count
- Active SKU count
- Storage capacity (sq ft)
- Maximum concurrent bookings

#### Availability
- General availability schedule
- Blackout dates
- Response time SLA
- Fulfillment methods offered

#### Trust & Reputation
- Trust score (0-1.0)
- Verification level (basic, enhanced, full)
- Transaction count
- Success rate
- Average rating
- Dispute rate

#### Economics
- Total revenue
- Average monthly revenue
- Node yield (revenue per sq ft per month)
- Platform fees paid
- Insurance premiums

#### Access Rules
- Access modes allowed (supervised, unsupervised, remote)
- Maximum risk level allowed
- Deposit requirements
- Hero requirements

### House Status
- **Active**: Accepting bookings
- **Inactive**: Not accepting bookings
- **Maintenance**: Temporary pause
- **Suspended**: Platform suspension

## Host Role

### Definition
A Host owns assets, space, services, or local availability. They monetize their household inventory through MEMBRA.

### Host Responsibilities

#### Inventory Management
- Scan and approve inventory items
- Set availability schedule
- Set pricing (accept MUP or custom)
- Set access rules
- Maintain inventory condition
- Update inventory as items change

#### Booking Management
- Respond to booking requests
- Approve, modify, or decline requests
- Coordinate with heroes for fulfillment
- Provide access to approved requesters
- Verify return condition
- Report issues promptly

#### Communication
- Respond to inquiries within SLA
- Provide clear instructions
- Confirm bookings
- Coordinate pickup/delivery
- Handle disputes professionally

#### Reputation Management
- Maintain high response rate
- Maintain high success rate
- Provide accurate item descriptions
- Honor bookings
- Resolve issues fairly

### Host Benefits

#### Revenue
- Transaction revenue from rentals/access
- Subscription benefits for power hosts
- Premium placement for high-quality inventory
- B2B/API access for property managers

#### Flexibility
- Set own schedule
- Choose what to share
- Set own prices
- Choose access rules
- Pause anytime

#### Risk Mitigation
- Platform insurance
- Deposit protection
- Hero fulfillment option
- Dispute resolution
- Fraud prevention

## Hero Role

### Definition
A Hero fulfills delivery, pickup, inspection, setup, or handoff. They enable hosts to monetize without handling all logistics.

### Hero Types

#### Pickup Hero
- Picks up items from host
- Delivers to requester
- Handles logistics
- Provides proof of delivery

#### On-Site Hero
- Meets requester at host location
- Supervises access
- Handles setup/teardown
- Verifies condition

#### Inspection Hero
- Inspects items before/after use
- Documents condition
- Reports issues
- Facilitates disputes

#### Setup Hero
- Sets up equipment for requester
- Provides instruction
- Ensures proper use
- Handles teardown

### Hero Attributes

#### Identity
- Hero ID (unique)
- Name
- Photo
- Verification level
- Background check (optional)

#### Service Area
- Service radius (miles)
- Service zones
- Availability schedule
- Response time SLA

#### Capabilities
- Services offered (pickup, delivery, on-site, inspection, setup)
- Vehicle type (for pickup/delivery)
- Equipment (for setup)
- Skills (specialized services)

#### Trust & Reputation
- Trust score (0-1.0)
- Transaction count
- Success rate
- Average rating
- Cancellation rate
- On-time rate

#### Economics
- Hourly rate
- Per-service fees
- Distance fees
- Tips received
- Total revenue

### Hero Benefits

#### Revenue
- Service fees from hosts
- Tips from requesters
- Bonuses for high performance
- Priority matching for top heroes

#### Flexibility
- Set own schedule
- Choose services to offer
- Set service area
- Accept/reject jobs
- Work on-demand

#### Growth
- Build reputation
- Expand service area
- Add new services
- Become Alpha Hub hero

## Alpha Hub

### Definition
An Alpha Hub is a high-volume household node with dedicated inventory, may employ heroes, has premium verification, and has priority in matching.

### Alpha Hub Requirements
- 50+ verified SKUs
- Trust score >0.85
- 100+ successful transactions
- Full verification
- Professional operation

### Alpha Hub Benefits
- Priority in search results
- Lower platform fees
- Premium placement
- API access
- White-label options
- B2B partnerships

### Alpha Hub Operations
- Dedicated inventory management
- Professional fulfillment team
- Customer service
- Marketing support
- Analytics dashboard

## Hero/House/Alpha Hub Model

### Separation of Concerns
- **Host**: Owns inventory, sets rules, earns revenue
- **Hero**: Handles logistics, provides service, earns fees
- **House**: Physical node with inventory and trust score
- **Alpha Hub**: Professional operation with dedicated resources

### Benefits of Separation
- Host doesn't need to handle all logistics
- Host can monetize without being present
- Heroes can specialize in fulfillment
- Scales better than "host does everything"
- Enables professional operations

### Interaction Patterns

#### Host + Hero
- Host lists inventory
- Requester books
- Hero fulfills pickup/delivery
- Host earns revenue
- Hero earns service fee

#### Host Only
- Host lists inventory
- Requester books
- Host fulfills directly
- Host earns full revenue
- No hero fee

#### Alpha Hub + Heroes
- Alpha Hub lists inventory
- Requester books
- Alpha Hub heroes fulfill
- Alpha Hub earns revenue
- Heroes earn wages

#### Requester + Hero
- Requester needs service (no inventory)
- Hero provides service
- Requester pays hero directly
- Platform takes small fee

## Trust Scoring by Role

### Host Trust Score
- Inventory quality accuracy
- Response rate
- Cancellation rate
- Success rate
- Dispute rate
- Review rating

### Hero Trust Score
- On-time rate
- Completion rate
- Item handling
- Communication
- Dispute rate
- Review rating

### Requester Trust Score
- On-time pickup
- On-time return
- Item care
- Payment reliability
- Dispute rate
- Review rating

## Access Control

### Supervised Access
- Host present during entire access
- Hero present if host unavailable
- Recommended for Level 2+ items
- Lower insurance premium

### Unsupervised Access
- Host not present
- Hero may supervise
- Requires higher trust score
- Requires deposit
- Higher insurance premium

### Remote Access
- No physical access required
- Examples: storage space, pickup/dropoff
- Lowest risk
- Lowest insurance premium
- No deposit required

## Node Yield

### Definition
Node yield is revenue per square foot per month. It measures how efficiently a household node monetizes its space.

### Calculation
```
Node Yield = (Monthly Revenue / Total Square Feet)
```

### Benchmarks
- **Low yield**: <$0.50/sq ft/month
- **Medium yield**: $0.50-$2.00/sq ft/month
- **High yield**: >$2.00/sq ft/month

### Optimization
- Focus on high-frequency SKUs
- Optimize pricing
- Improve availability
- Add complementary services
- Use heroes for fulfillment

## Growth Path

### New Host
- Start with low-risk SKUs
- Build trust score
- Learn platform
- Optimize inventory

### Power Host
- Expand inventory
- Add heroes
- Improve yield
- Consider Alpha Hub

### Alpha Hub
- Professional operation
- Multiple locations
- B2B partnerships
- Platform partnership
