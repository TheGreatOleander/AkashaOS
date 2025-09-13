"""Veil module for AkashaOS - mentor nudges + truths final shaping layer."""
from typing import Any
try:
    import truths
    import nudges
except Exception:
    # fallback local imports if installed under src/project
    from project import truths, nudges  # type: ignore

def reveal(data: Any) -> Any:
    """Apply mentor nudges and weave in a truth.
    If data is a mapping or sequence, return a wrapped dict with added guidance.
    If data is a string, return an enhanced string.
    """
    try:
        t = truths.drop_truth(0) if hasattr(truths, 'drop_truth') else None
    except Exception:
        t = None
    try:
        n = nudges.gentle_nudge(0) if hasattr(nudges, 'gentle_nudge') else None
    except Exception:
        n = None

    # Basic behavior: if string -> annotate; if dict/list -> inject fields; otherwise return tuple
    if isinstance(data, str):
        parts = [data]
        if t:
            parts.append(f"[TRUTH] {t}")
        if n:
            parts.append(f"[NUDGE] {n}")
        return " \n".join(parts)
    elif isinstance(data, dict):
        out = dict(data)
        if t:
            out.setdefault('truth', t)
        if n:
            out.setdefault('nudge', n)
        return out
    elif isinstance(data, (list, tuple)):
        out = list(data)
        if t:
            out.append({'truth': t})
        if n:
            out.append({'nudge': n})
        return out
    else:
        # fallback: return a descriptive tuple
        return (data, {'truth': t, 'nudge': n})
