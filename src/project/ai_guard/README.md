# AkashaOS AI Guard

This update adds a prototype AI-based guard system with flare phrase authentication.

## Files

- **ai_guard.py** → AI Guard logic for authentication and output filtering.
- **profile_store.py** → Local JSON-based profile storage (`~/.akasha_profiles.json`).
- **demo_login.py** → Simple CLI to test flare phrase authentication.
- **README.md** → This file.

## Default Flare Phrase

The default profile comes preloaded with the phrase:

```
even the circuits dream of cinnamon rain
```

You can change it by editing `~/.akasha_profiles.json` or calling `ProfileStore.update_profile()`.

## Usage

```bash
python3 demo_login.py
```

Enter the flare phrase to authenticate. If successful, you'll see:

```
✅ Flare recognized. Access granted.
Welcome back, dreamer.
```
