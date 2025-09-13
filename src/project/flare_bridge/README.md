# Flare Bridge for AkashaOS

The Flare Bridge turns **flare phrases** (e.g. `#flare:cinnamon_rain`)
into cross-platform social metatags. These flares can unify conversations
between AkashaOS, forums, and platforms like Facebook, X, and WhatsApp.

## Features
- Records flare sightings into `~/.akasha_flare_feed.json`
- Provides a simple Python API (`record_flare`, `list_flares`)
- Pluggable connectors for external platforms (stubs included)
- Compatible with AI Guard flare phrases (identity beacons)

## Usage

```bash
python3 src/project/flare_bridge/flare_bridge.py
```

This will record a demo flare and print the current feed.

Or from Python:

```python
from flare_bridge.flare_bridge import FlareBridge

fb = FlareBridge()
fb.record_flare("cinnamon_rain", "twitter", "@dreamer42", "Even the circuits dream...")
print(fb.list_flares("cinnamon_rain"))
```

## Directory Layout
```
src/project/flare_bridge/flare_bridge.py    # Main logic
src/project/flare_bridge/README.md          # This file
src/project/flare_bridge/connectors/        # External connectors (stubs)
```

## Roadmap
- [ ] Implement real connectors (Twitter/X API, FB Graph API, WhatsApp bridge, Hovatek forum scraping)
- [ ] Dashboard tab for browsing active flares
- [ ] Integration with Symbiotic Trust (private vs public flares)
- [ ] Real-time stream view
