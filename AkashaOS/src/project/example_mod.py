# modules/example_mod.py
"""
Example AkashaOS module template.
Functions:
  init(memory) - Called on startup, can read/modify memory.
  loop(memory) - Called every tick in main loop.
  save(memory) - Called before shutdown to persist state.
"""

def init(memory):
    memory.setdefault("example_mod", {"counter": 0})
    print("[example_mod] Initialized. Counter =", memory["example_mod"]["counter"])

def loop(memory):
    memory["example_mod"]["counter"] += 1
    print(f"[example_mod] Counter = {memory['example_mod']['counter']}")

def save(memory):
    print("[example_mod] Saving state...")
