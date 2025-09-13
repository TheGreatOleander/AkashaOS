# Profile Store Module

## Overview
Manages user profiles: behavioral data, permissions, trust levels. Works with `ai_guard.py`.

## Profile Structure
Profiles as Python dicts/JSON. Example fields:
- `user_id`
- `trust_level` (0–100)
- `permissions` (list)
- `history` (list)
- `last_seen` (timestamp)

## Default Profile
```python
{
  "user_id": "new_user",
  "trust_level": 50,
  "permissions": [],
  "history": [],
  "last_seen": None
}
```

## Key Functions
- `load_profile(user_id)` → `dict`
- `save_profile(profile)`
- `update_profile(profile, updates)` → `dict`
- `delete_profile(user_id)`

## Usage
```python
from profile_store import ProfileStore

profile = ProfileStore.load_profile("user123")
profile["trust_level"] += 10
ProfileStore.save_profile(profile)
```
