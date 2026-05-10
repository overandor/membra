# SKU Verification

## Overview

SKU Verification is the AI-assisted process of detecting, matching, confidence scoring, and host approval of household inventory items. It converts raw physical objects into verified, priced, and permissioned local SKUs.

## Detection Pipeline

### Stage 1: Image Capture
- User uploads room photo
- System validates image quality
- System extracts metadata (timestamp, location if available)
- System generates image hash for deduplication

### Stage 2: Object Detection
- AI vision model detects objects in image
- Model identifies: object type, location in frame, confidence score
- Model generates bounding boxes for each detected object
- Model classifies objects into categories: storage, tool, appliance, furniture, space

### Stage 3: Object Classification
- Detected objects classified into specific types
- Examples: drill, vacuum, shelf, couch, chair, table, charger, extension cord
- Classification confidence score assigned
- Alternative classifications suggested if confidence is low

### Stage 4: Attribute Extraction
- Extract object attributes: color, size, condition indicators, brand logos
- Estimate object value based on visual cues
- Estimate object age and condition
- Estimate object dimensions

### Stage 5: SKU Generation
- Object converted to potential SKU
- SKU assigned: unique ID, category, type, attributes
- SKU assigned risk level based on category and condition
- SKU assigned MUP based on category and attributes
- SKU assigned access mode based on category

### Stage 6: Host Review
- Host presented with detected SKUs
- Host can: approve, modify, or reject each SKU
- Host can adjust: price, availability, access rules
- Host can add: custom descriptions, photos, notes
- Host can remove: false positives, unwanted items

### Stage 7: Verification
- Host-approved SKUs become verified
- SKUs assigned verification status: pending, verified, rejected
- Verified SKUs published to local market
- Pending SKUs held for additional information

## Confidence Scoring

### Detection Confidence (0-1.0)
- Based on object detection model confidence
- Adjusted for image quality
- Adjusted for object clarity
- Adjusted for lighting conditions

### Classification Confidence (0-1.0)
- Based on classification model confidence
- Adjusted for object uniqueness
- Adjusted for visual distinctiveness
- Adjusted for alternative classifications

### Overall Confidence (0-1.0)
```
Overall Confidence = (Detection Confidence × 0.6) + (Classification Confidence × 0.4)
```

### Confidence Thresholds
- **0.8+**: Auto-approve (host can still review)
- **0.6-0.8**: Require host review
- **0.4-0.6**: Require host confirmation
- **<0.4**: Require manual entry

## Manual Entry Fallback

When AI detection fails or confidence is low:
- Host can manually enter inventory items
- Host provides: item name, category, description, photos
- Host sets: price, availability, access rules
- System assigns: SKU ID, risk level, MUP
- Manual entries marked as "manually verified"

## SKU Categories

### Storage Space
- Shelf space
- Closet space
- Garage space
- Fridge space
- Basement space
- Attic space

### Tools
- Hand tools (drills, saws, wrenches)
- Power tools (vacuums, sanders, grinders)
- Specialty tools (pressure washers, tile cutters)
- Measuring tools (tape measures, levels)
- Cutting tools (knives, scissors)

### Appliances
- Small appliances (blenders, toasters, coffee makers)
- Cleaning appliances (vacuums, steam cleaners)
- Kitchen appliances (microwaves, air fryers)
- Entertainment appliances (speakers, projectors)

### Furniture
- Chairs (dining chairs, folding chairs, office chairs)
- Tables (coffee tables, desks, dining tables)
- Sofas (couches, sectionals)
- Storage furniture (bookshelves, cabinets)
- Outdoor furniture (patio chairs, tables)

### Services
- Local delivery
- Pickup coordination
- On-site assistance
- Assembly/disassembly
- Installation

## SKU Attributes

### Standard Attributes
- SKU ID (unique)
- Name
- Category
- Type
- Description
- Condition (excellent, good, fair, poor)
- Dimensions (if applicable)
- Weight (if applicable)
- Age (if applicable)
- Brand (if visible)

### Pricing Attributes
- MUP (calculated)
- Custom price (if set by host)
- Price per unit (hour, day, week, use)
- Minimum booking duration
- Maximum booking duration
- Deposit required (yes/no, amount)

### Access Attributes
- Access mode (supervised, unsupervised, remote)
- Access rules
- Availability schedule
- Location (lat, lng, radius)
- Fulfillment method (pickup, delivery, onsite, remote)

### Risk Attributes
- Risk level (low, medium, high)
- Risk factors
- Insurance required (yes/no)
- Proof required (photo, GPS, signature)

### Verification Attributes
- Detection confidence
- Classification confidence
- Verification status (pending, verified, rejected)
- Verification method (AI, manual, hybrid)
- Verification timestamp

## Host Approval Workflow

### Step 1: Review Detected SKUs
- Host sees list of detected SKUs
- Each SKU shows: image, name, confidence, suggested price, risk level
- Host can filter by category, confidence, risk level

### Step 2: Approve/Modify/Reject
- Host can approve SKU as-is
- Host can modify SKU attributes
- Host can reject SKU (false positive)
- Host can add custom SKUs

### Step 3: Set Availability
- Host sets availability schedule
- Host sets booking rules
- Host sets access permissions
- Host sets fulfillment preferences

### Step 4: Set Pricing
- Host accepts suggested MUP
- Host sets custom price
- Host sets deposit requirements
- Host sets bulk discount rules

### Step 5: Publish
- Host publishes verified SKUs
- SKUs become visible to local market
- SKUs appear in search results
- Host receives notification of first request

## Quality Assurance

### Detection Quality
- False positive rate monitoring
- False negative rate monitoring
- Confidence calibration
- Model retraining on errors

### Classification Quality
- Classification accuracy monitoring
- Category confusion analysis
- Attribute extraction accuracy
- Model improvement on misclassifications

### Pricing Quality
- MUP accuracy monitoring
- Market rate comparison
- Host acceptance rate
- Price adjustment tracking

## Batch Processing

### Bulk Upload
- Host can upload multiple room photos
- System processes photos in batch
- System generates batch SKU report
- Host reviews and approves in batch

### Import/Export
- Host can export inventory as JSON/CSV
- Host can import inventory from other systems
- Host can share inventory with other platforms
- Host can backup inventory data

## Verification Badge

### Verified SKU Badge
- SKUs with confidence >0.8 get "AI Verified" badge
- Manually entered SKUs get "Manually Verified" badge
- Badge increases requester trust
- Badge may justify premium pricing

### Verified Host Badge
- Hosts with 10+ verified SKUs get "Verified Host" badge
- Hosts with 50+ verified SKUs get "Premium Host" badge
- Badge increases visibility in search
- Badge may qualify for lower platform fees
