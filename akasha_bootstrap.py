 # AkashaOS bootstrap - prints a stylish startup and runs heartbeat UI if Flask is installed.
 import os, time, subprocess, sys
 banner = r"""
  ___    _  __   _   _   _   _   ___   ___   ___
 / _ \  | |/ /  | | | | | | | | | _ \ / _ \ / __|
| (_) | | ' <   | |_| |_| |_| |_|  _/| (_) |\__ \
 \___/  |_|\_\   \___\___/\___/ |_|   \___/ |___/
 """
 print(banner)
 print('AkashaOS bootstrap — awakening the AetherBox...')
 # attempt to run heartbeat UI
 try:
     import flask  # type: ignore
     print('Starting heartbeat UI (Flask detected)')
     sys.stdout.flush()
     # run flask app module
     subprocess.run([sys.executable, '-m', 'tools.heartbeat.app'], check=False)
 except Exception as e:
     print('Flask not available or failed to start UI:', e)
     print('Falling back to heartbeat log...')
     for i in range(5):
         print(f'[{i+1}] Akasha heartbeat — {time.strftime("%Y-%m-%d %H:%M:%S") }')
         time.sleep(1)



# --- AI Guard Integration ---
import random
try:
    from ai_guard.ai_guard import AIGuard
    AI_GUARD_ENABLED = True
except ImportError:
    AI_GUARD_ENABLED = False

def run_ai_guard_check():
    if not AI_GUARD_ENABLED:
        return "AI Guard not available"
    try:
        guard = AIGuard(user_id="default")
        # For now, fake timings instead of real keystrokes
        timings = [random.uniform(0.3, 0.7) for _ in range(5)]
        score = guard.score_attempt(timings)
        if score >= 70:
            msg = f"✅ AI Guard: User verified (score {score})"
        else:
            msg = f"⚠️ AI Guard: Suspicious profile detected (score {score})"
        print(msg)
        return msg
    except Exception as e:
        return f"AI Guard error: {e}"
# --- End AI Guard Integration ---

# Run AI Guard check at startup
print(run_ai_guard_check())
