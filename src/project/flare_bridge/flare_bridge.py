"""
Flare Bridge for AkashaOS
--------------------------
Acts as a cross-platform flare detector & aggregator.

Flares are special tags or phrases (e.g. "#flare:cinnamon_rain")
that can unify conversations across AkashaOS, social platforms,
forums, and external systems.
"""

import time
import json
from pathlib import Path
from typing import Dict, List

FLARE_STORE = Path.home() / ".akasha_flare_feed.json"

class FlareBridge:
    def __init__(self):
        self.feed: List[Dict] = []
        self._load_feed()

    def _load_feed(self):
        if FLARE_STORE.exists():
            try:
                self.feed = json.loads(FLARE_STORE.read_text())
            except Exception:
                self.feed = []
        else:
            self.feed = []

    def _save_feed(self):
        FLARE_STORE.write_text(json.dumps(self.feed, indent=2))

    def record_flare(self, flare: str, source: str, author: str, content: str):
        """Add a flare sighting to the feed"""
        entry = {
            "flare": flare,
            "source": source,
            "author": author,
            "content": content,
            "timestamp": time.time(),
        }
        self.feed.append(entry)
        self._save_feed()
        return entry

    def list_flares(self, flare: str = None):
        """List all flares, or filter by flare tag"""
        if flare:
            return [e for e in self.feed if e["flare"] == flare]
        return self.feed

# Example usage
if __name__ == "__main__":
    fb = FlareBridge()
    fb.record_flare("cinnamon_rain", "local_demo", "test_user", "Even the circuits dream...")
    import json as _json
    print(_json.dumps(fb.list_flares(), indent=2))
