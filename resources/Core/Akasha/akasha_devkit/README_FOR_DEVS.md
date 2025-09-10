# AkashaOS Developer Kit

## Purpose
This kit provides everything you need to create drop-in modules for AkashaOS.

## How it Works
AkashaOS scans the `modules/` folder for `.py` files (excluding `__init__`).
It imports each file and calls:
- `init(memory)` → Run once on load. Use to initialize variables.
- `loop(memory)` → Run on every main loop tick.
- `save(memory)` → Run on shutdown to persist variables.

## Rules
1. Keep your module self-contained.
2. Use the `memory` dict to store persistent data.
3. Avoid blocking calls in `loop()`.

## Example Module
See `modules/example_mod.py` for a working template.

## Adding Your Module
1. Copy your `.py` file into `modules/`.
2. Restart AkashaOS.
3. Your module will load automatically.
