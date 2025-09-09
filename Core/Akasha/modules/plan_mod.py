import akasha_tools as tools

def init(memory):
    goal = "optimize system"
    memory['plan_mod'] = {"current_goal": goal}
    print(f"[plan_mod] Goal set: {goal}")

def save(memory):
    print("[plan_mod] Saving current goal.")

def loop(memory):
    goal = memory.get('plan_mod', {}).get("current_goal", "none")
    print(f"[plan_mod] Working toward: {goal}")
    requests = memory.pop("plan_requests", [])
    for req in requests:
        plan = f"Act on desire '{req['desire']}' ({req['desc']})"
        memory.setdefault("plans", []).append(plan)
        tools.log(f"[plan_mod] created plan from longing_mod: {plan}")
