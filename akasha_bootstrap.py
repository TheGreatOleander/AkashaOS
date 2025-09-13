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



# --- AkashaOS Dashboard Wiring (Update 017: Curiosity & Flow integration) ---
import threading, time, random
try:
    from akashaos import curiosity
except ImportError:
    curiosity = None
import nudges

def curiosity_flow_worker():
    while True:
        try:
            if curiosity:
                spark_val = curiosity.spark()
                explore_val = curiosity.explore()
                score = len(spark_val) + len(explore_val)
                STATE['curiosity'] = min(100, score)
            else:
                STATE['curiosity'] = random.randint(0, 100)
        except Exception as e:
            STATE['curiosity'] = random.randint(0, 100)
            STATE['logs'].append(f"Curiosity error: {e}")
            if len(STATE['logs']) > 10:
                STATE['logs'].pop(0)
        try:
            nudge_val = nudges.gentle_nudge(random.randint(0, len(nudges.NUDGES)-1))
            STATE['flow'] = min(100, len(nudge_val))
        except Exception as e:
            STATE['flow'] = random.randint(0, 100)
            STATE['logs'].append(f"Flow error: {e}")
            if len(STATE['logs']) > 10:
                STATE['logs'].pop(0)
        time.sleep(5)

# Launch background thread
threading.Thread(target=curiosity_flow_worker, daemon=True).start()
# --- End Update 017 ---
