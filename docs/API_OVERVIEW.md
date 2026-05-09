# API Overview

MEMBRA API is a FastAPI-based backend that powers the chat-first local commerce platform.

## Endpoints

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check

### Chat
- `POST /chat` - Send message to MEMBRA LLM

### Inventory
- `GET /inventory` - Get user's inventory
- `POST /inventory` - Create inventory item

### Marketplace
- `GET /marketplace` - Get marketplace listings
- `POST /marketplace` - Create listing

### Hero
- `GET /hero` - Get hero dashboard data

### Relay
- `POST /relay` - Create relay delivery
- `GET /relay/{relay_id}` - Get relay details

### SplitOrder
- `POST /split-order` - Create split order
- `GET /split-order/{order_id}` - Get split order details

### SplitPulse
- `GET /split-pulse` - Get demand pulses
- `POST /split-pulse` - Create demand pulse

### Wallet
- `GET /wallet` - Get wallet balance
- `POST /wallet/withdraw` - Withdraw funds

### Trust
- `GET /trust` - Get trust score
- `POST /trust/verify` - Verify identity
