---
title: Overworker
emoji: ⚡
colorFrom: purple
colorTo: blue
sdk: docker
app_file: main.py
pinned: false
---

# Overworker

**AI execution layer - GitHub repo to verified package ZIP with production-grade dashboard**

Overworker converts messy repositories into verified, inspectable, saleable assets through automated analysis, scoring, and packaging.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Overwork Score Bands

| Score | Band | Description |
|-------|------|-------------|
| 0.85 - 1.0 | PRODUCTION_READY | Ready for production deployment |
| 0.70 - 0.84 | DEMO_READY | Suitable for demos and prototypes |
| 0.50 - 0.69 | SCAFFOLD | Basic structure present, needs work |
| 0.30 - 0.49 | PROVENANCE | Minimal provenance, mostly archival |
| 0.0 - 0.29 | FRAGMENT | Incomplete or fragmented |

## API Endpoints

### `POST /analyze`
Analyzes a GitHub repository.

**Request:**
```json
{"url": "https://github.com/owner/repo"}
```

## License

MIT
