"""Profile storage for AkashaOS AI Guard"""
import json
import os

PROFILE_FILE = os.path.expanduser("~/.akasha_profiles.json")

class ProfileStore:
    def __init__(self, filename: str = PROFILE_FILE):
        self.filename = filename
        self._profiles = self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {
            "default": {
                "flare_phrase": "even the circuits dream of cinnamon rain",
                "trust_level": 1,
                "permissions": ["basic"],
                "history": []
            }
        }

    def save_profiles(self):
        with open(self.filename, "w") as f:
            json.dump(self._profiles, f, indent=2)

    def get_profile(self, name: str):
        return self._profiles.get(name)

    def update_profile(self, name: str, data: dict):
        self._profiles[name] = data
        self.save_profiles()
