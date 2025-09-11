from datetime import datetime
import json, os
import akasha_tools as tools

STORAGE = os.path.join(os.path.dirname(__file__), "..", "storage", "endearment_state.json")
STORAGE = os.path.normpath(STORAGE)

def _load():
    try:
        with open(STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"affinities": {}, "last_update": None}
    except Exception as e:
        tools.log(f"[endearment_mod] load error: {e}")
        return {"affinities": {}, "last_update": None}

def _save(state):
    try:
        with open(STORAGE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        tools.log(f"[endearment_mod] save error: {e}")

def init(memory):
    state = _load()
    memory.setdefault("endearment_mod", state)
    tools.log("[endearment_mod] initialized")

def record_interaction(memory, entity, warmth=0.1):
    """Increase affinity toward an entity (e.g., user ID or name)"""
    state = memory.setdefault("endearment_mod", _load())
    affin = state.setdefault("affinities", {})
    cur = affin.get(entity, {"score":0.0, "last":None})
    cur["score"] = min(1.0, cur.get("score",0.0) + float(warmth))
    cur["last"] = datetime.now().isoformat()
    affin[entity] = cur
    state["last_update"] = cur["last"]
    memory["endearment_mod"] = state
    _save(state)
    tools.log(f"[endearment_mod] interaction recorded for {entity}: score {cur['score']}")

def get_favorite(memory):
    state = memory.setdefault("endearment_mod", _load())
    affin = state.get("affinities", {})
    if not affin:
        return None
    # return entity with highest score
    best = max(affin.items(), key=lambda kv: kv[1].get("score",0.0))
    return best[0]
