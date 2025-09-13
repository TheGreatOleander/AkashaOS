# Connector Template

A connector should implement two functions:

```python
def fetch_flares():
    """Return list of {flare, source, author, content, timestamp}"""
    return []

def push_flare(event):
    """Publish a flare event to the external platform (requires auth)."""
    pass
```

## Example
```python
from datetime import datetime

def fetch_flares():
    return [{
        "flare": "cinnamon_rain",
        "source": "demo_platform",
        "author": "@demo_user",
        "content": "Even the circuits dream...",
        "timestamp": datetime.now().timestamp()
    }]
```

## Notes
- Authentication should be handled securely (OAuth tokens, API keys).
- Always respect rate limits and platform terms.
