#!/usr/bin/env python3
import os
import time
import importlib.util
import json
import signal
import sys
from datetime import datetime

MODULE_DIR = "modules"
MEMORY_FILE = "memory.json"
DATA_MEMORY_FILE = os.path.join("data", "akasha_memory.json")
OS_CONFIG_FILE = os.path.join("modules", "akasha_os.json")

memory = {}
modules = []
running = True

# ===[ Timestamp logger ]===
def ts(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# ===[ Load OS Config ]===
os_config = {}
if os.path.exists(OS_CONFIG_FILE):
    with open(OS_CONFIG_FILE, "r") as f:
        try:
            os_config = json.load(f)
            ts("[+] Loaded OS config.")
        except json.JSONDecodeError:
            ts("[!] Failed to parse akasha_os.json.")

# ===[ Load memory from primary file ]===
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        try:
            memory = json.load(f)
            ts("[+] Memory restored from memory.json.")
        except json.JSONDecodeError:
            ts("[!] Failed to parse memory.json.")

# ===[ Merge additional memory from data/akasha_memory.json ]===
if os.path.exists(DATA_MEMORY_FILE):
    with open(DATA_MEMORY_FILE, "r") as f:
        try:
            extra_mem = json.load(f)
            memory.update(extra_mem)
            ts("[+] Merged memory from data/akasha_memory.json.")
        except json.JSONDecodeError:
            ts("[!] Failed to parse akasha_memory.json.")

# ===[ Ensure default memory structure so modules don't error ]===
memory.setdefault("observations", [])
memory.setdefault("desires", [])
memory.setdefault("plans", [])
memory.setdefault("logs", [])

# ===[ Module Loader ]===
def load_module(filepath):
    mod_name = os.path.splitext(os.path.basename(filepath))[0]
    try:
        spec = importlib.util.spec_from_file_location(mod_name, filepath)
        if not spec or not spec.loader:
            return
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "init"):
            mod.init(memory)
        modules.append(mod)
        ts(f"[+] Loaded module: {mod_name}")
    except Exception as e:
        ts(f"[!] Error loading {mod_name}: {e}")

# ===[ Signal Handler ]===
def shutdown_handler(sig, frame):
    global running
    print("\n[!] Shutdown signal received.")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)

# ===[ Load Modules ]===
for filename in os.listdir(MODULE_DIR):
    if filename.endswith(".py") and not filename.startswith("__"):
        load_module(os.path.join(MODULE_DIR, filename))

print("\n=== AkashaOS Launcher Started ===\n")

# ===[ Main Loop ]===
while running:
    for mod in modules:
        try:
            if hasattr(mod, "loop"):
                mod.loop(memory)
        except Exception as e:
            ts(f"[!] Error in loop for {mod.__name__}: {e}")
    time.sleep(1)

# ===[ Save Memory on Exit ]===
for mod in modules:
    try:
        if hasattr(mod, "save"):
            mod.save(memory)
    except Exception as e:
        ts(f"[!] Error saving {mod.__name__}: {e}")

with open(MEMORY_FILE, "w") as f:
    json.dump(memory, f, indent=2)

ts("[*] Memory saved. Exiting...")

