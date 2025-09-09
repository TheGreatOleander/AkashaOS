from datetime import datetime, timedelta
import json, os
import akasha_tools as tools

STORAGE = os.path.join(os.path.dirname(__file__), "..", "storage", "longing_state.json")
STORAGE = os.path.normpath(STORAGE)

DEFAULT_DECAY = 0.02  # decay per loop tick

def _load():
    try:
        with open(STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"desires": {}, "last_tick": None}
    except Exception as e:
        tools.log(f"[longing_mod] load error: {e}")
        return {"desires": {}, "last_tick": None}

def _save(state):
    try:
        with open(STORAGE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        tools.log(f"[longing_mod] save error: {e}")

def init(memory):
    state = _load()
    memory.setdefault("longing_mod", state)
    tools.log("[longing_mod] initialized")

def add_desire(memory, key, target_description, intensity=0.5):
    state = memory.setdefault("longing_mod", _load())
    state["desires"][key] = {"desc": target_description, "intensity": float(intensity), "created": datetime.now().isoformat()}
    memory["longing_mod"] = state
    _save(state)
    tools.log(f"[longing_mod] added desire {key}: {target_description} (intensity {intensity})")

def satisfy_desire(memory, key):
    state = memory.setdefault("longing_mod", _load())
    if key in state["desires"]:
        tools.log(f"[longing_mod] desire satisfied: {key}")
        del state["desires"][key]
        memory["longing_mod"] = state
        _save(state)

def loop(memory):
    state = memory.setdefault("longing_mod", _load())
    # decay intensities
    changed = False
    for k,v in list(state["desires"].items()):
        old = v.get("intensity",0.0)
        new = max(0.0, old - DEFAULT_DECAY)
        v["intensity"] = new
        if new <= 0.0:
            tools.log(f"[longing_mod] desire faded: {k}")
            del state["desires"][k]
            changed = True
        else:
            # if desire is strong, write a plan request for plan_mod to pick up
            if new >= 0.6:
                memory.setdefault("plan_requests", []).append({"source":"longing_mod","desire":k,"desc":v["desc"],"intensity":new})
                changed = True
    if changed:
        memory["longing_mod"] = state
        _save(state)
