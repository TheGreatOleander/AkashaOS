# AkashaOS Autopilot Technical Specs

## Overview
Autopilot manages updates for AkashaOS modules, focusing on AI Guard. It supports three modes:
- **scout**: detect available updates (GitHub API polling planned)
- **trial**: dry-run updates in sandbox
- **apply**: apply updates using `apply_update.sh` with backup/rollback

## Data Flow
1. Fetch/update zip (manual or future API)
2. Dry-run unzip to `/tmp/akasha_autopilot_test`
3. Run health checks (`tests/health_check.py`)
4. Backup current repo to `~/.akasha_backups/`
5. Call `apply_update.sh` to apply update
6. Log results with personality flavor

## Backup Strategy
- Every apply creates timestamped backup
- Rollback by copying last backup over repo

## Personality Engine
- `adventurer`, `scientist`, `navigator` personalities
- Affects log prefixes/emojis

## Integration Points
- Works alongside `ai_guard.py` and `profile_store.py`
- Optionally can run `demo_login.py` tests

## Expansion Roadmap
- GitHub API integration for auto scouting
- GPG-signed zip verification
- CI/CD release integration
- PR opening, automated merges
- Full AI co-pilot for adaptive module application
