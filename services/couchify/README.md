# Booking Concierge API

Production-ready booking agent API. Turns plain-language requests into completed seat bookings with minimal friction.

## What It Does

- **Chat-based booking**: User types natural language → system extracts details → completes booking
- **Minimal registration**: Only asks for name + phone at the last moment
- **Smart ranking**: Scores listings by availability, price, location, privacy, rating
- **Fast execution**: Complete booking flow in 3-4 messages

## API Endpoints

### 1. Start Session
```bash
POST /chat/session

Response:
{
  "session_id": "uuid",
  "user_detected": false,
  "message": "Hi! I'm your booking concierge..."
}
```

### 2. Send Message
```bash
POST /chat/message
{
  "session_id": "uuid",
  "message": "I need 2 seats in SoHo today at 3pm for an hour"
}

Response:
{
  "reply": "I found 5 options...",
  "state": {"area": "Soho", "seat_count": 2, ...},
  "missing_fields": [],
  "next_action": "select_listing",
  "options": [...]
}
```

### 3. Quick Register
```bash
POST /users/quick-register
{
  "session_id": "uuid",
  "first_name": "Alex",
  "phone": "+1234567890"
}
```

### 4. Direct Search
```bash
POST /booking/search
{
  "session_id": "uuid",
  "area": "SoHo",
  "seat_count": 2,
  "start_time": "2026-04-25T15:00:00",
  "duration_minutes": 60
}
```

### 5. Create Quote
```bash
POST /booking/quote
{
  "session_id": "uuid",
  "listing_id": "space_1"
}
```

### 6. Confirm Booking
```bash
POST /booking/confirm
{
  "session_id": "uuid",
  "quote_id": "quote_xxx",
  "payment_token": "tok_xxx"  // optional for now
}
```

## Running Locally

```bash
pip3 install -r requirements.txt
python3 main.py
```

Server runs on `http://localhost:8000`

## Deployment

### Render (Recommended)
1. Push to GitHub
2. Connect repo at https://dashboard.render.com
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
