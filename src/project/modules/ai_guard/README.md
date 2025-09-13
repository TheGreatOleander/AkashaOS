# AI Guard Module

## Overview
`ai_guard.py` implements the adaptive AI-based security layer for AkashaOS. It monitors user authentication, input patterns, and context to determine risk and adjust access dynamically.

This module can be used for:
- Adaptive login/authentication
- Monitoring command access
- Filtering output or enforcing permissions

## Key Classes & Functions

### `AI_Guard`
The main class for the AI Guard agent.

**Methods:**
- `check_guardrails(user_input, profile)` → `bool`
- `update_profile(profile, metrics)` → `Profile`
- `risk_score(user_input, context)` → `int` (0–100)

### `check_guardrails()`
Standalone function for simple checks.

## Usage
```python
from ai_guard import AI_Guard
from profile_store import ProfileStore

guard = AI_Guard()
profile = ProfileStore.load_profile("user123")

if guard.check_guardrails("some input", profile):
    print("Access granted")
else:
    print("Access denied")
```

## Integration
- Runs at login or before sensitive actions.
- Interacts with `profile_store.py` for metrics.
