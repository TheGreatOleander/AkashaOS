# Tests Folder

## Overview
Validates AkashaOS modules and workflow integrity.

### `health_check.py`
- Confirms `ai_guard` and `profile_store` import
- Runs `demo_login.py` in a dry test
- Outputs pass/fail

## Usage
```bash
python3 tests/health_check.py
```

## Notes
- Local developer testing only
- No destructive operations
