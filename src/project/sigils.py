
import hashlib
RUNES = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊ"
def sigil(word: str) -> str:
    if not word: return ""
    h = hashlib.sha256(word.encode("utf-8")).hexdigest()[:24]
    return "".join(RUNES[int(c,16) % len(RUNES)] for c in h)
