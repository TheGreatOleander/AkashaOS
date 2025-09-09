from datetime import datetime
import json, os
import akasha_tools as tools

STORAGE = os.path.join(os.path.dirname(__file__), "..", "storage", "awareness_state.json")
STORAGE = os.path.normpath(STORAGE)

def _load():
    try:
        with open(STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"observations": [], "last_update": None}
    except Exception as e:
        tools.log(f"[awareness_mod] load error: {e}")
        return {"observations": [], "last_update": None}

def _save(state):
    try:
        with open(STORAGE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        tools.log(f"[awareness_mod] save error: {e}")

def init(memory):
    state = _load()
    memory.setdefault("awareness_mod", state)
    tools.log("[awareness_mod] initialized")

def observe(memory, source, note):
    """Record an observation. source: str, note: str"""
    state = memory.setdefault("awareness_mod", _load())
    obs = {"time": datetime.now().isoformat(), "source": source, "note": str(note)}
    state["observations"].append(obs)
    state["last_update"] = obs["time"]
    memory["awareness_mod"] = state
    _save(state)
    tools.log(f"[awareness_mod] observed from {source}: {note}")

def loop(memory):
    # lightweight housekeeping: trim history to last 500 entries
    state = memory.setdefault("awareness_mod", _load())
    if len(state["observations"]) > 500:
        state["observations"] = state["observations"][-500:]
        _save(state)
    # expose a short context summary for others
    summary = state["observations"][-5:]
    memory["awareness_context"] = summary
