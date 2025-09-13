# AkashaOS Autopilot

This package provides an Autopilot system for AkashaOS to automatically scout, trial, and apply updates. It integrates with the AI Guard module.

## Files

- **autopilot.py** → Main Autopilot agent. Modes: scout, trial, apply.
- **tests/health_check.py** → Simple sanity checks for AI Guard modules.
- **autopilot_config.json** → User config for modes, paths, and personality.
- **TECH_SPECS.md** → Detailed technical overview.

## Usage

```bash
python3 src/project/autopilot/autopilot.py scout
python3 src/project/autopilot/autopilot.py trial ai_guard_update.zip
python3 src/project/autopilot/autopilot.py apply ai_guard_update.zip
```

Backups are automatically created in `~/.akasha_backups/`.
