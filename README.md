# AkashaOS

[![CI](https://github.com/TheGreatOleander/AkashaOS/actions/workflows/ci.yml/badge.svg)](https://github.com/TheGreatOleander/AkashaOS/actions)

## Overview
AkashaOS is a modular Python-based system designed to explore emergent behaviors,
mirrored processes, and distributed intelligence.

### Core Features
- **Bridges** (`project.bridges`) — bridges between modules and external systems  
- **Core** (`project.core`) — mirror loops, daemon, memory, UI handling  
- **Resources** (`resources/`) — assets and reference materials  
- **Tests** (`tests/`) — automated checks via CI  

---

## Usage Example

```python
from project.core import loop

# Start a mirror loop
loop.start()

# Or run a single iteration
loop.step()
```

This demonstrates how to import and run the mirror loops provided in `project.core.loop`.
