import subprocess

def init(memory):
    memory['act_mod'] = {"executed": []}
    print("[act_mod] Ready for action.")

def save(memory):
    print("[act_mod] Executed actions saved.")

def loop(memory):
    tasks = memory.get('plan_mod', {}).get('current_goal')
    if tasks:
        print(f"[act_mod] Simulating task for goal: {tasks}")