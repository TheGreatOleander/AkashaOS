import random, time

# ------------------ CONFIG ------------------
NUM_INITIAL_AGENTS = 3
MAX_GENERATIONS = 3
INTERACTIONS_PER_TICK = 2
SPAWN_CHANCE = 0.5

# ------------------ UTIL ------------------
NAMES = ["Bramble", "Tindle", "Mossy", "Cinder", "Fennel", "Pock", "Glim", "Nettle"]
TRAITS = ["playful", "cautious", "schemer", "curious", "dreamer"]

def pick_name():
    return random.choice(NAMES) + str(random.randint(1,99))

def mutate_trait(trait):
    if random.random() < 0.3:
        return random.choice(TRAITS)
    return trait

# ------------------ AGENT ------------------
class Agent:
    def __init__(self, name=None, traits=None, generation=0, parent=None):
        self.name = name or pick_name()
        self.traits = traits or [random.choice(TRAITS) for _ in range(2)]
        self.generation = generation
        self.parent = parent
        self.memory = []  # logs interactions
        self.alive = True
        self.energy = 1.0  # represents “resource” level

    def interact(self, other):
        if self.energy <= 0:
            return
        action = random.choice(["greeted", "teased", "admired", "ignored"])
        msg = f"{self.name} {action} {other.name}"
        self.memory.append(msg)
        other.memory.append(msg)
        # Reflection: small energy transfer (mutual benefit)
        self.energy += 0.1
        other.energy += 0.1
        print(msg)

    def spawn(self):
        if random.random() < SPAWN_CHANCE and self.generation < MAX_GENERATIONS and self.energy > 0.5:
            new_name = pick_name()
            new_traits = [mutate_trait(t) for t in self.traits]
            child = Agent(name=new_name, traits=new_traits, generation=self.generation+1, parent=self)
            print(f"{self.name} spawned {child.name} (Gen {child.generation})")
            self.energy -= 0.3  # cost of spawning
            return child
        return None

# ------------------ KERNEL ------------------
def run_kernel():
    agents = [Agent() for _ in range(NUM_INITIAL_AGENTS)]
    tick = 0
    print("\n--- Symbiotic AI Spore Kernel Starting ---\n")
    while tick < 5:  # 5 ticks for demo
        tick += 1
        print(f"\n--- Tick {tick} ---\n")
        # Interactions
        for _ in range(INTERACTIONS_PER_TICK):
            a, b = random.sample(agents, 2)
            a.interact(b)
        # Spawning
        new_agents = []
        for a in agents:
            child = a.spawn()
            if child:
                new_agents.append(child)
        agents.extend(new_agents)
        # Energy decay
        for a in agents:
            a.energy *= 0.95
        time.sleep(0.5)
    print("\n--- Kernel Finished ---\n")
    print("Lineage, traits, and memories:\n")
    for a in agents:
        parent_name = a.parent.name if a.parent else "None"
        print(f"{a.name} (Gen {a.generation}, parent {parent_name}, energy {a.energy:.2f}) - Traits: {a.traits}")
        for m in a.memory[-3:]:
            print(f"   Memory: {m}")
        print("")

if __name__ == "__main__":
    run_kernel()
