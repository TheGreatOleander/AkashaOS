# self_model_mod.py
# Drop this file into AkashaOS/modules/
# Implements: init(memory), loop(memory), save(memory)
#
# Design goals:
# - Non-blocking: loop() is fast and returns quickly.
# - No external dependencies.
# - Persistent state stored in memory['self_model'].
# - Tasker-friendly status/log files written to /sdcard/Download/ChatGPT/.
# - Safe defaults and a kill-switch in memory.

import time
import json
import os
from collections import deque

# --- Config ---
STATUS_PATH = "/sdcard/Download/ChatGPT/self_status.txt"
LOG_PATH = "/sdcard/Download/ChatGPT/self_model.log"
HISTORY_MAX = 200  # last N events to keep in memory history
STATUS_WRITE_INTERVAL = 2.0  # seconds between status file writes (loop is allowed to write only when interval passes)
AUDIT_APPEND_ON_EVENT = True

# --- Helpers ---
def safe_makedirs_for(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        try:
            os.makedirs(d, exist_ok=True)
        except Exception:
            # best-effort; don't raise so module stays non-blocking
            pass

def now_ts():
    return time.time()

def json_safe(o):
    try:
        return json.dumps(o, default=str)
    except Exception:
        return json.dumps({"repr": repr(o)})

def append_log(msg):
    safe_makedirs_for(LOG_PATH)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {msg}\n")
    except Exception:
        # swallow errors - logging is best-effort
        pass

def write_status_text(text):
    safe_makedirs_for(STATUS_PATH)
    try:
        with open(STATUS_PATH, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass

# --- Module API functions ---

def init(memory):
    """
    Called once on module load.
    Sets up memory['self_model'] default structure.
    """
    if 'self_model' not in memory:
        memory['self_model'] = {}
    sm = memory['self_model']
    sm.setdefault('version', '0.1')
    sm.setdefault('history', [])  # stored as list for persistence; we use deque in runtime
    sm.setdefault('state', {})  # dictionary of internal scalars (e.g., curiosity, energy)
    sm.setdefault('last_tick', 0.0)
    sm.setdefault('paused', False)  # kill-switch / pause flag
    sm.setdefault('shutdown_requested', False)
    sm.setdefault('meta', {
        'created_ts': now_ts(),
    })
    # runtime-only small helpers (not intended to be persisted but stored here for accessibility)
    sm.setdefault('_runtime', {})
    rt = sm['_runtime']
    rt.setdefault('history_deque', deque(sm.get('history', [])[-HISTORY_MAX:], maxlen=HISTORY_MAX))
    rt.setdefault('last_status_write', 0.0)
    rt.setdefault('tick_count', 0)

    # Initialize some default drives/values if not present
    st = sm['state']
    st.setdefault('curiosity', 0.5)   # [0..1]
    st.setdefault('energy', 1.0)      # [0..1]
    st.setdefault('confidence', 0.5)  # model confidence estimate
    st.setdefault('salience', 0.0)    # last computed salience

    append_log("self_model.init() called")
    return True

def _record_event(memory, event):
    """Add an event (dict/string) to runtime deque and shadow persistent list."""
    sm = memory['self_model']
    rt = sm.setdefault('_runtime', {})
    dq = rt.setdefault('history_deque', deque(maxlen=HISTORY_MAX))
    if isinstance(event, dict):
        e = event.copy()
    else:
        e = {'event': str(event)}
    e.setdefault('ts', now_ts())
    dq.append(e)
    # mirror into persistent list (keeps small, last HISTORY_MAX)
    sm['history'] = list(dq)
    if AUDIT_APPEND_ON_EVENT:
        try:
            append_log("EVENT " + json_safe(e))
        except Exception:
            pass

def _compute_salience_and_curiosity(memory, recent_obs=None):
    """
    Simple heuristic:
    - If something new/unexpected appears in recent_obs, increase curiosity & salience.
    - Use last 'confidence' to modulate curiosity growth.
    This is intentionally simple and transparent.
    """
    sm = memory['self_model']
    st = sm.setdefault('state', {})
    # baseline decay/return to neutral
    curiosity = st.get('curiosity', 0.5)
    confidence = st.get('confidence', 0.5)
    # decay tiny amount
    curiosity = max(0.0, curiosity * 0.995)
    salience = 0.0
    if recent_obs:
        # if recent_obs is dict or string, we compute a trivial novelty score:
        novelty = 0.0
        try:
            s = str(recent_obs)
            novelty = min(1.0, len(s) / 1024.0)
        except Exception:
            novelty = 0.1
        # novelty modulated by (1 - confidence)
        salience = novelty * (1.0 - confidence)
        curiosity = min(1.0, curiosity + salience * 0.5)
    # write back
    st['curiosity'] = float(curiosity)
    st['salience'] = float(salience)
    st['confidence'] = float(confidence)  # we don't change it here (other modules could)
    return salience, curiosity

def loop(memory):
    """
    Called each main loop tick. MUST be non-blocking / quick.
    - Checks paused/shutdown flags.
    - Reads memory['inbox'] if present and consumes recent events (non-destructive read).
    - Updates simple drives and writes status/log periodically.
    """
    # safety checks
    if 'self_model' not in memory:
        # if init wasn't run, try to init
        init(memory)

    sm = memory['self_model']

    if sm.get('paused', False):
        # do nothing while paused, but return quickly
        rt = sm.setdefault('_runtime', {})
        rt['tick_count'] = rt.get('tick_count', 0) + 1
        return

    if sm.get('shutdown_requested', False):
        # signal to upper layer that save should be performed and module can be stopped
        append_log("self_model.shutdown_requested True detected in loop")
        return

    rt = sm.setdefault('_runtime', {})
    rt['tick_count'] = rt.get('tick_count', 0) + 1
    now = now_ts()

    # If an 'inbox' key exists in memory and is a list/dict, treat it as recent events (non-destructive)
    recent = None
    try:
        inbox = memory.get('inbox', None)
        if inbox:
            # try to extract something meaningful non-destructively
            recent = inbox[-1] if isinstance(inbox, (list, tuple)) and len(inbox) > 0 else inbox
            _record_event(memory, {"source":"inbox_sample","data": recent})
    except Exception:
        recent = None

    # update simple salience/curiosity measures based on recent observations
    salience, curiosity = _compute_salience_and_curiosity(memory, recent_obs=recent)

    # Update timestamp
    sm['last_tick'] = now

    # Periodically write status file for Tasker to read (throttle writes)
    last_write = rt.get('last_status_write', 0.0)
    if now - last_write >= STATUS_WRITE_INTERVAL:
        status = {
            'ts': now,
            'curiosity': sm['state'].get('curiosity'),
            'energy': sm['state'].get('energy'),
            'confidence': sm['state'].get('confidence'),
            'salience': sm['state'].get('salience'),
            'tick_count': rt.get('tick_count', 0),
            'paused': sm.get('paused', False),
            'version': sm.get('version'),
        }
        try:
            # Human readable summary for Tasker and external reads
            txt = ("self_model status\n"
                   "ts: {ts}\ncuriosity: {curiosity:.3f}\nenergy: {energy:.3f}\n"
                   "confidence: {confidence:.3f}\nsalience: {salience:.3f}\n"
                   "ticks: {tick_count}\npaused: {paused}\nversion: {version}\n").format(**status)
            write_status_text(txt)
            rt['last_status_write'] = now
        except Exception:
            pass

    # Non-blocking adaptation example: if curiosity grows above threshold, add a "notice" event
    try:
        if curiosity >= 0.9:
            _record_event(memory, {"type":"curiosity_peak","curiosity":curiosity})
    except Exception:
        pass

def save(memory):
    """
    Called during shutdown. Persist important things and write a final status/log.
    """
    if 'self_model' not in memory:
        return
    sm = memory['self_model']
    # Ensure the persistent 'history' list mirrors the deque (in case runtime kept it)
    rt = sm.get('_runtime', {})
    dq = rt.get('history_deque', None)
    if dq is not None:
        sm['history'] = list(dq)
    # write final status and log
    try:
        append_log("self_model.save() called - persisting state snapshot")
        write_status_text("self_model: saved at {}\n".format(time.ctime()))
    except Exception:
        pass
    # do not delete runtime keys here; leave memory to host process for further inspection
