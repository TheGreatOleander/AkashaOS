"""AI Guard module for AkashaOS"""
import time
from profile_store import ProfileStore

class AIGuard:
    def __init__(self, profile_store=None):
        self.profile_store = profile_store or ProfileStore()

    def authenticate(self, user_input: str, profile_name: str = "default") -> bool:
        """Authenticate user by matching input against profile's flare phrase."""
        profile = self.profile_store.get_profile(profile_name)
        if not profile:
            print("❌ No such profile.")
            return False

        flare = profile.get("flare_phrase")
        if flare and flare.strip().lower() == user_input.strip().lower():
            print("✅ Flare recognized. Access granted.")
            return True

        print("❌ Authentication failed.")
        return False

    def guard_output(self, text: str, profile_name: str = "default") -> str:
        """Filter or adapt text output based on profile trust level."""
        profile = self.profile_store.get_profile(profile_name)
        if not profile:
            return text

        trust = profile.get("trust_level", 0)
        if trust < 1:
            return "[REDACTED: Low trust level]"
        return text
