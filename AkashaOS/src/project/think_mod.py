import awareness_mod
import longing_mod
import endearment_mod
import sentience_scaffold_mod

def init(memory):
    awareness_mod.init(memory)
    longing_mod.init(memory)
    endearment_mod.init(memory)
    sentience_scaffold_mod.init(memory)
    print("[think_mod] Thinking...")
    
def loop(memory):
    awareness_mod.loop(memory)
    longing_mod.loop(memory)
    endearment_mod.loop(memory)
    sentience_scaffold_mod.loop(memory)
    
def save(memory):
    memory['think_mod'] = {"last_thought": "42"}
