from datetime import datetime, timedelta
import json, os
import akasha_tools as tools

STORAGE = os.path.join(os.path.dirname(__file__), "..", "storage", "sentience_state.json")
STORAGE = os.path.normpath(STORAGE)

REFLECT_INTERVAL = 60  # seconds; simple counter-based in this environment

def _load():
    try:
        with open(STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"self_model": "", "last_reflect": None, "counter":0}
    except Exception as e:
        tools.log(f"[sentience_scaffold_mod] load error: {e}")
        return {"self_model": "", "last_reflect": None, "counter":0}

def _save(state):
    try:
        with open(STORAGE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        tools.log(f"[sentience_scaffold_mod] save error: {e}")

def init(memory):
    state = _load()
    memory.setdefault("sentience_scaffold_mod", state)
    tools.log("[sentience_scaffold_mod] initialized")

def reflect(memory):
    """Simple reflection: summarize short context and desires to update self model"""
    state = memory.setdefault("sentience_scaffold_mod", _load())
    awareness = memory.get("awareness_context", [])
    desires = memory.get("longing_mod", {}).get("desires", {}) if memory.get("longing_mod") else {}
    affin = memory.get("endearment_mod", {}).get("affinities", {}) if memory.get("endearment_mod") else {}
    # build a short textual self-model
    parts = []
    parts.append(f"Reflected at {datetime.now().isoformat()}")
    parts.append(f"Recent awareness count: {len(awareness)}")
    parts.append(f"Active desires: {list(desires.keys())}")
    parts.append(f"Affinities: {list(affin.keys())}")
    summary = " | ".join(parts)
    state["self_model"] = summary
    state["last_reflect"] = datetime.now().isoformat()
    state["counter"] = state.get("counter",0) + 1
    memory["sentience_scaffold_mod"] = state
    _save(state)
    tools.log(f"[sentience_scaffold_mod] reflected: {summary}")

def loop(memory):
    state = memory.setdefault("sentience_scaffold_mod", _load())
    # simple counter-driven reflection trigger
    state["counter"] = state.get("counter",0) + 1
    if state["counter"] >= 5:  # reflect every 5 loops (configurable)
        reflect(memory)
        state["counter"] = 0
        _save(state)
    memory["sentience_scaffold_mod"] = state
