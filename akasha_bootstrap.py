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



# --- AkashaOS Dashboard Wiring (Update 015) ---
import threading, time
from core import loop

loop_running = False
loop_thread = None

def loop_worker():
    global loop_running
    while loop_running:
        try:
            result = loop.mirror_loop()
            STATE['logs'].append(f"Mirror loop result: {result}")
            if len(STATE['logs']) > 10:
                STATE['logs'].pop(0)
        except Exception as e:
            STATE['logs'].append(f"Loop error: {e}")
        time.sleep(2)

@app.route('/api/action/start_loop', methods=['POST'])
def api_start_loop():
    global loop_running, loop_thread
    if not loop_running:
        loop_running = True
        loop_thread = threading.Thread(target=loop_worker, daemon=True)
        loop_thread.start()
        STATE['logs'].append("Mirror loop started")
    return ('', 204)

@app.route('/api/action/step_loop', methods=['POST'])
def api_step_loop():
    try:
        result = loop.mirror_loop()
        STATE['logs'].append(f"Step result: {result}")
    except Exception as e:
        STATE['logs'].append(f"Step error: {e}")
    if len(STATE['logs']) > 10:
        STATE['logs'].pop(0)
    return ('', 204)

@app.route('/api/action/pause_loop', methods=['POST'])
def api_pause_loop():
    global loop_running
    loop_running = False
    STATE['logs'].append("Mirror loop paused")
    if len(STATE['logs']) > 10:
        STATE['logs'].pop(0)
    return ('', 204)

@app.route('/api/action/synthesize', methods=['POST'])
def api_synthesize():
    # Placeholder for truths/nudges integration
    STATE['logs'].append("Synthesis action triggered (stub)")
    if len(STATE['logs']) > 10:
        STATE['logs'].pop(0)
    return ('', 204)
# --- End Dashboard Wiring ---
