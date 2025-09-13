import json
import os

PROFILE_DIR = os.path.expanduser("~/.aiguard_profiles")
os.makedirs(PROFILE_DIR, exist_ok=True)

def profile_path(user_id):
    return os.path.join(PROFILE_DIR, f"{user_id}.json")

def load_profile(user_id):
    path = profile_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_profile(user_id, profile):
    path = profile_path(user_id)
    with open(path, "w") as f:
        json.dump(profile, f, indent=2)
