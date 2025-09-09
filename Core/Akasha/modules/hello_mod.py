def initialize(memory):
    if "hello_count" not in memory:
        memory["hello_count"] = 0
        print("[hello_mod] Initialized.")

def run_cycle(memory):
    memory["hello_count"] += 1
    print(f"[hello_mod] Hello #{memory['hello_count']}")
