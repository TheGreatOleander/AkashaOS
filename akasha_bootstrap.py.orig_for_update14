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
