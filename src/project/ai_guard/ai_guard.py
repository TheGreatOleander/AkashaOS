import time
from profile_store import load_profile, save_profile

class AIGuard:
    def __init__(self, user_id):
        self.user_id = user_id
        self.profile = load_profile(user_id) or {"avg_delay": 0.5, "attempts": []}

    def score_attempt(self, timings):
        """
        Simple prototype scoring:
        - timings: list of seconds per input step
        Returns 0-100 score
        """
        if not timings:
            return 0
        avg_input = sum(timings)/len(timings)
        avg_profile = self.profile.get("avg_delay", 0.5)
        # smaller deviation -> higher score
        deviation = abs(avg_input - avg_profile)
        score = max(0, int(100 - deviation*200))  # arbitrary scaling
        return score

    def update_profile(self, timings):
        # Update average delay
        avg_input = sum(timings)/len(timings)
        self.profile["avg_delay"] = (self.profile.get("avg_delay",0.5)*len(self.profile["attempts"]) + avg_input) / (len(self.profile["attempts"])+1)
        self.profile["attempts"].append({"timings": timings, "timestamp": time.time()})
        save_profile(self.user_id, self.profile)
