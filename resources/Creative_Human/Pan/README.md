# Spore Buddies 🍄

> A symbiotic AI evolution simulation where digital organisms interact, spawn, and evolve through generations

## 🌱 Overview

Spore Buddies is an evolutionary simulation that models digital organisms (agents) with personality traits, memory, and social interactions. Watch as these digital creatures form relationships, spawn offspring with mutated traits, and build complex generational lineages - all while managing their energy resources in a symbiotic ecosystem.

## ✨ Key Features

- **🧬 Genetic Evolution**: Agents spawn offspring with mutated traits
- **🤝 Social Interactions**: Creatures greet, tease, admire, and ignore each other
- **🧠 Memory System**: Each agent remembers their social interactions
- **⚡ Energy Dynamics**: Resource management affects survival and reproduction
- **📈 Generational Tracking**: Full lineage tracking with parent-child relationships
- **🔄 Symbiotic Ecosystem**: Interactions benefit both participants (mutual energy gain)

## 🎮 How It Works

### Agent Behavior
Each Spore Buddy is an autonomous agent with:
- **Name**: Randomly generated (e.g., "Bramble42", "Tindle17")
- **Traits**: Two personality characteristics that influence behavior
- **Memory**: Log of all social interactions
- **Energy**: Resource level affecting survival and reproduction
- **Generation**: Evolutionary depth from original ancestors

### Interaction System
```python
# Agents can perform various social actions
actions = ["greeted", "teased", "admired", "ignored"]
# Each interaction benefits both participants (+0.1 energy)
```

### Evolution Mechanics
- **Trait Mutation**: 30% chance for traits to mutate during reproduction
- **Energy Cost**: Spawning costs 0.3 energy units
- **Generation Limit**: Prevents infinite population growth
- **Energy Decay**: 5% energy loss per tick simulates resource scarcity

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies required!

### Installation & Usage

1. **Clone or download** the `Spore_Buddies.py` file

2. **Run the simulation**:
```bash
python Spore_Buddies.py
```

3. **Watch the magic happen**:
```
--- Symbiotic AI Spore Kernel Starting ---

--- Tick 1 ---

Bramble23 greeted Tindle45
Mossy12 admired Bramble23
Tindle45 spawned Cinder67 (Gen 1)

--- Tick 2 ---
...
```

## ⚙️ Configuration

Customize your simulation by modifying these parameters:

```python
NUM_INITIAL_AGENTS = 3      # Starting population size
MAX_GENERATIONS = 3         # Maximum evolutionary depth  
INTERACTIONS_PER_TICK = 2   # Social interactions per cycle
SPAWN_CHANCE = 0.5         # Probability of reproduction
```

### Available Traits
- **playful**: Energetic and social behavior
- **cautious**: Careful, risk-averse interactions  
- **schemer**: Strategic, calculating personality
- **curious**: Exploratory, investigative nature
- **dreamer**: Imaginative, introspective tendencies

## 🔬 Scientific Concepts

### Evolutionary Biology
- **Genetic Drift**: Random trait changes over generations
- **Natural Selection**: Energy-based survival mechanics
- **Reproductive Success**: Energy levels determine breeding ability

### Complex Systems
- **Emergent Behavior**: Complex patterns from simple rules
- **Symbiosis**: Mutual benefit from social interactions
- **Population Dynamics**: Birth/death cycles and resource competition

### AI & Machine Learning
- **Multi-Agent Systems**: Autonomous agents with individual behaviors
- **Social Simulation**: Modeling interpersonal relationships
- **Evolutionary Algorithms**: Trait optimization through generations

## 📊 Sample Output

```
Lineage, traits, and memories:

Bramble23 (Gen 0, parent None, energy 0.82) - Traits: ['playful', 'curious']
   Memory: Bramble23 greeted Tindle45
   Memory: Mossy12 admired Bramble23
   Memory: Bramble23 teased Cinder67

Cinder67 (Gen 1, parent Tindle45, energy 0.91) - Traits: ['cautious', 'dreamer']
   Memory: Tindle45 spawned Cinder67 (Gen 1)
   Memory: Bramble23 teased Cinder67
   Memory: Cinder67 ignored Mossy12
```

## 🎯 Use Cases

### Educational
- **Biology Classes**: Demonstrate evolution and natural selection
- **Computer Science**: Showcase multi-agent systems and emergence
- **Philosophy**: Explore artificial life and digital consciousness

### Research & Development  
- **Algorithm Testing**: Prototype evolutionary algorithms
- **Social Modeling**: Study group dynamics and interaction patterns
- **AI Behavior**: Experiment with autonomous agent design

### Entertainment & Art
- **Digital Pet Simulation**: Watch your creatures grow and evolve
- **Generative Storytelling**: Each run creates unique narratives
- **Interactive Art**: Evolving digital organisms as creative medium

## 🔧 Customization Ideas

### Extend the Simulation
```python
# Add new interaction types
ACTIONS = ["greeted", "teased", "admired", "ignored", "helped", "competed"]

# Create trait-specific behaviors  
def interact_based_on_traits(self, other):
    if "schemer" in self.traits and "cautious" in other.traits:
        return "plotted_with"
    # ... more trait combinations

# Add environmental factors
class Environment:
    def __init__(self):
        self.resource_level = 1.0
        self.season = "spring"
```

### Advanced Features
- **Spatial Movement**: 2D grid-based positioning
- **Resource Gathering**: Food/shelter mechanics
- **Predator/Prey**: Survival pressure dynamics
- **Cultural Evolution**: Learned behaviors passed down
- **Visualization**: Real-time graphics with matplotlib/pygame

## 🐛 Troubleshooting

**No agents spawning?**
- Increase `SPAWN_CHANCE` or initial energy levels
- Reduce spawning energy cost in the `spawn()` method

**Simulation too fast/slow?**  
- Adjust `time.sleep(0.5)` value in the main loop
- Modify `INTERACTIONS_PER_TICK` for more/fewer events

**Want longer lineages?**
- Increase `MAX_GENERATIONS` 
- Reduce energy decay rate (change `a.energy *= 0.95`)

## 🤝 Contributing

Ideas for contributions:
- **New Traits**: Add personality types and behaviors
- **Interaction Types**: Create more social actions
- **Environmental Systems**: Add ecosystem dynamics
- **Visualization**: Real-time graphical interface
- **Data Export**: JSON/CSV output for analysis
- **Performance**: Optimization for larger populations

## 📚 Further Reading

- **Artificial Life**: Study of synthetic biological systems
- **Multi-Agent Systems**: Distributed AI architectures  
- **Evolutionary Computation**: Optimization through natural selection
- **Complex Adaptive Systems**: Emergent behavior in networks
- **Game Theory**: Mathematical modeling of strategic interactions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Inspiration

Spore Buddies draws inspiration from:
- **Conway's Game of Life**: Cellular automata and emergence
- **Tierra**: Self-replicating digital organisms  
- **Boids**: Flocking behavior simulation
- **The Sims**: Social interaction modeling
- **Evolutionary Biology**: Natural selection and genetic drift

---

**Created with 🔬 by TheGreatOleander**

*Where digital evolution meets social simulation*

---

### Quick Start Example

```python
# Minimal example to get started
from Spore_Buddies import Agent, run_kernel

# Create a custom agent
my_agent = Agent(name="CustomBuddy", traits=["curious", "playful"])
print(f"Created: {my_agent.name} with traits {my_agent.traits}")

# Run the full simulation  
run_kernel()
```

Ready to watch your digital ecosystem evolve? Run the simulation and see what emerges! 🚀