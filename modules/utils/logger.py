# logger.py
import time
from pathlib import Path

LOG_FILE = Path(__file__).parents[2] / "conjuror.log"

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")
