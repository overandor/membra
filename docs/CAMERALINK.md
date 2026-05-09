# MEMBRA CameraLink

A cross-account camera bridge that allows any phone to become a live MEMBRA camera for inventory scanning, fridge scans, closet scans, proof capture, and LLM assetification — without Apple ID, iCloud, AirDrop, or device sync.

## Product Sentence

Open a QR code on any machine, scan it with any phone, and the phone becomes a live MEMBRA camera for inventory scanning.

## Flow

1. Host machine opens MEMBRA
2. MEMBRA displays QR code
3. Phone scans QR
4. Phone browser opens secure camera session
5. User grants camera permission
6. Video/photos stream to MEMBRA session
7. LLM detects objects
8. Listings are generated
9. Owner approves

## Compatibility

- iPhone → Mac
- Android → Mac
- iPhone → Windows
- Android → Chromebook
- Old phone → host laptop
- Guest phone → host machine
- Hero phone → Alpha Hub tablet

## Modes

### Snapshot Mode
Easiest and safest. The phone captures photos and uploads them to the session. Perfect for:
- Closets
- Shelves
- Receipts
- Amazon piles
- Fridge scans
- Proof photos
- Package drop-off proof

### Live Scan Mode
The phone streams video using WebRTC, and MEMBRA takes frames for object detection. Better for:
- Walking through a room
- Scanning a closet continuously
- LLM-guided scanning ("move closer," "open the shelf," "show the barcode")

## API Endpoints

### POST /api/v1/camera-sessions/create
Creates a new camera scan session.

### GET /api/v1/camera-sessions/{id}/qr
Returns QR code data for pairing.

### POST /api/v1/camera-sessions/{id}/join
Phone joins the session via QR code.

### POST /api/v1/camera-sessions/{id}/photo
Upload photo (Snapshot Mode).

### POST /api/v1/camera-sessions/{id}/frame
Upload video frame (Live Scan Mode).

### GET /api/v1/camera-sessions/{id}/detections
Get AI-detected objects from session.

### POST /api/v1/camera-sessions/{id}/approve-listings
Approve or reject detected listings.

### POST /api/v1/camera-sessions/{id}/end
End the camera session.

## Session Object

```json
{
  "scan_session_id": "scan_123",
  "desktop_user_id": "hero_456",
  "phone_device_id": "temp_device_789",
  "mode": "live_scan",
  "pairing_method": "qr_code",
  "expires_in_minutes": 10,
  "camera_permission": true,
  "owner_approval_required": true,
  "status": "connected"
}
```

## Security Rules

- QR session expires quickly (10 minutes)
- Phone only accesses specific scan session
- Phone does not get access to whole account
- Desktop user must approve publishing
- Photos are private by default
- No background camera
- No hidden recording
- No automatic public listing

## Use Cases

CameraLink powers:
- Closet scan
- Fridge scan
- Room scan
- Garage scan
- Receipt scan
- Barcode scan
- Package proof
- Drop-off proof
- Pickup proof
- Condition proof
- Before/after proof

## Technical Stack

- **Frontend**: Next.js / PWA
- **Phone camera**: Browser getUserMedia API
- **Pairing**: QR code with short-lived token
- **Streaming**: WebRTC for live mode
- **Snapshots**: HTTPS upload for simple mode
- **Realtime events**: WebSocket
- **Storage**: Temporary object storage
- **AI**: Vision model + LLM listing generator
- **Approval**: Desktop Hero Dashboard

## Why CameraLink vs Apple Continuity

Apple Continuity is for personal devices. MEMBRA CameraLink is for commerce sessions across strangers, hosts, phones, laptops, Hero Houses, and Alpha Hubs. It is marketplace-native and device-independent.
