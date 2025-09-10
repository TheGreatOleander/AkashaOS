# `example_mod.py`

Example AkashaOS module template.
Functions:
  init(memory) - Called on startup, can read/modify memory.
  loop(memory) - Called every tick in main loop.
  save(memory) - Called before shutdown to persist state.

## Usage

Import the module from the `project` package. Example:

```python
from project import example_mod
# or
import project.example_mod
```
