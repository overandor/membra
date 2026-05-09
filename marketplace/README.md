# MEMBRA Super Mono Repo - Marketplace Architecture

## Overview

MEMBRA is organized as a **self-referencing marketplace** where the repo itself functions as a marketplace of functions. This is a revolutionary architecture where:

- **The repo is a marketplace** - Code functions are tradable assets
- **External repos are service providers** - Functions from other repos are callable as API endpoints
- **LLM auto-updates every 15 minutes** - GitHub Actions with LLM maintain and improve the codebase
- **Self-referencing structure** - The repo structure mirrors the MEMBRA product itself

## Architecture

```
MEMBRA/
├── marketplace/                    # Marketplace core
│   ├── functions/                 # Local function implementations
│   ├── services/                  # Service implementations
│   ├── api/                       # API gateway layer
│   │   └── gateway.py            # Unified gateway for external repo calls
│   ├── gateway/                   # External repo integration
│   ├── registry/                  # Function registry and marketplace data
│   │   ├── functions.json        # Registered functions and external endpoints
│   │   └── sync-external-repos.py # Script to sync external functions
│   ├── external/                  # Synced functions from external repos
│   │   ├── couchify/             # Functions from couchify repo
│   │   ├── membra-relay/         # Functions from membra-relay repo
│   │   └── language-fi/          # Functions from language-fi repo
│   └── llm/                       # LLM auto-update scripts
│       └── update-backend.py     # LLM backend update orchestrator
├── .github/workflows/
│   └── llm-auto-update.yml        # GitHub Actions for LLM auto-updates
├── api/                           # FastAPI application (backend layer)
├── models/                        # Pydantic models
└── docs/                          # Documentation
```

## Key Concepts

### 1. Self-Referencing Marketplace

The repo structure mirrors the MEMBRA product itself:

- **marketplace/functions/** = MEMBRA Inventory (what the platform offers)
- **marketplace/registry/** = MEMBRA Trust (verified functions)
- **marketplace/api/gateway/** = MEMBRA Relay (movement between repos)
- **marketplace/external/** = MEMBRA Alpha Hub (external fulfillment)

### 2. External Repo References

Functions from external repos are referenced as API endpoints:

```python
# Call a function from external repo
from marketplace.api.gateway import call_external

result = call_external('membra-relay', 'relay', {
    'pickup': 'hero_house_123',
    'dropoff': 'user_456',
    'mode': 'local_delivery'
})
```

### 3. LLM Auto-Updates

GitHub Actions run every 15 minutes to:
- Analyze backend code and suggest improvements
- Sync functions from external repos
- Update marketplace registry
- Create pull requests for approved changes

### External Repos

- **couchify** - Rent, host, verify, llm-host
- **membra-relay** - Relay, delivery, route, batch, dispatch
- **language-fi** - Translate, localize, detect, semantic
- **llm-autonomous-agent** - Agent, task, planning, execution
- **groq-supervisor-ai** - Supervise, monitor, optimize

## Usage

### Calling External Functions

```python
from marketplace.api.gateway import gateway

# Call external function
result = gateway.call_function(
    repo='membra-relay',
    function='relay',
    params={
        'pickup': 'hero_house_123',
        'dropoff': 'user_456'
    }
)
```

### Listing Available Functions

```python
from marketplace.api.gateway import list_functions

functions = list_functions()
# Returns: ['membra-relay:relay', 'couchify:host', 'local:ask-membra', ...]
```

### Syncing External Functions

```python
from marketplace.api.gateway import gateway

# Sync a function from external repo
gateway.sync_function('membra-relay', 'relay')
```

## Auto-Update Process

Every 15 minutes, GitHub Actions:

1. Scan the codebase for components and functions
2. Analyze each component using LLM
3. Generate improvement suggestions
4. Apply high-priority updates
5. Sync functions from external repos
6. Update marketplace registry
7. Create pull requests for review

## Marketplace Functions

### Local Functions

- `ask-membra` - LLM chat interface for routing
- `assetify` - AI detection and assetification
- `fraction` - Fractional pricing calculation
- `room-os` - Room-based monetization
- `split-order` - Bulk order splitting
- `dispatch` - AI dispatch for fulfillment

### External Functions

- `couchify:rent` - Rent logic from couchify
- `couchify:host` - Host logic from couchify
- `membra-relay:relay` - Relay delivery
- `membra-relay:dispatch` - AI dispatch
- `language-fi:translate` - Translation
- `language-fi:detect` - Language detection

## Development

### Adding a New Function

1. Implement the function in `marketplace/functions/`
2. Register it in `marketplace/registry/functions.json`
3. Add external references if needed
4. Set `auto_update: true` to enable LLM improvements

### Adding an External Repo

1. Add repo to `marketplace/external/repos.json`
2. Configure API endpoints
3. Enable sync in registry
4. Functions will auto-sync every 15 minutes

### Customizing LLM Updates

Edit `marketplace/llm/update-backend.py` to customize:
- Update strategies
- Priority thresholds
- Analysis criteria
- Update application logic

## Benefits

1. **Self-Improving Codebase** - LLM maintains and improves code automatically
2. **External Function Integration** - Leverage code from other repos seamlessly
3. **Marketplace Architecture** - Repo structure mirrors product philosophy
4. **Auto-Synchronization** - External functions stay in sync automatically
5. **Unified Gateway** - Single interface for all function calls
6. **Registry-Based Discovery** - Easy to find and use available functions

## Future Enhancements

- Function marketplace UI for browsing available functions
- Function rating and reputation system
- Automated testing of external functions
- Function versioning and rollback
- Function marketplace for trading/selling functions
- Real-time function performance monitoring
- A/B testing of function implementations
