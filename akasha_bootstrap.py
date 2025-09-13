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



# --- AkashaOS Dashboard Server Integration ---
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__)

# Dummy state
STATE = {
    "curiosity": 42,
    "synthesis": 67,
    "flow": 88,
    "logs": ["System booted", "Dashboard online"]
}

@app.route('/')
def dashboard_index():
    return send_from_directory('resources/dashboard', 'akasha-unified-dashboard.html')

@app.route('/api/state')
def api_state():
    return jsonify(STATE)

@app.route('/api/action/<name>', methods=['POST'])
def api_action(name):
    STATE['logs'].append(f"Action triggered: {name}")
    if len(STATE['logs']) > 10:
        STATE['logs'].pop(0)
    return ('', 204)

def run_dashboard():
    print("Serving AkashaOS Dashboard at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
# --- End Dashboard Integration ---

if __name__ == '__main__':
    run_dashboard()
