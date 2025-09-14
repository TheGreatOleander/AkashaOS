# cognitive_bridge.py
import json, os, time, random, hashlib
from modules.utils.logger import log
from pathlib import Path

STATE_FILE = Path(__file__).parent / "evolution_state.json"

class Archetype:
    def __init__(self, name, description, traits=None):
        self.name = name
        self.description = description
        self.traits = traits or {}
        self.history = []

    def evolve(self, response):
        hash_digest = hashlib.sha256(response.encode()).hexdigest()[:8]
        self.traits["last_hash"] = hash_digest
        self.history.append({"response": response, "hash": hash_digest})
        log(f"Archetype {self.name} evolved: {hash_digest}")

def run():
    log("Cognitive Bridge running...")
    if not STATE_FILE.exists():
        with open(STATE_FILE, "w") as f:
            json.dump({"archetypes": []}, f, indent=2)
    while True:
        time.sleep(10)
        log("Cognitive Bridge heartbeat...")
