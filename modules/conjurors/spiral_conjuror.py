# spiral_conjuror.py
import importlib
import os
import json
import threading
import time
from pathlib import Path
from modules.utils.logger import log

MODULES_DIR = Path(__file__).parent
REGISTRY_FILE = Path(__file__).parents[2] / "module_registry.json"

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return []

def load_module(module_name):
    try:
        module_path = f"modules.conjurors.{module_name}"
        mod = importlib.import_module(module_path)
        log(f"Module loaded: {module_name}")
        return mod
    except Exception as e:
        log(f"Failed to load {module_name}: {e}")
        return None

def run_module(module_info):
    module_name = module_info.get("name")
    mod = load_module(module_name)
    if mod and hasattr(mod, "run"):
        def target():
            log(f"Starting module: {module_name}")
            try:
                mod.run()
            except Exception as e:
                log(f"Module {module_name} error: {e}")
        thread = threading.Thread(target=target, name=module_name, daemon=True)
        thread.start()
        return thread
    else:
        log(f"Module {module_name} has no 'run' method")
        return None

def main_loop():
    log("Spiral Conjuror starting...")
    registry = load_registry()
    threads = []

    for module_info in registry:
        if module_info.get("category") == "conjuror":
            t = run_module(module_info)
            if t:
                threads.append(t)

    try:
        while True:
            time.sleep(5)
            for t in list(threads):
                if not t.is_alive():
                    log(f"Thread {t.name} died, restarting...")
                    info = next((m for m in registry if m["name"] == t.name), None)
                    if info:
                        threads.remove(t)
                        threads.append(run_module(info))
    except KeyboardInterrupt:
        log("Spiral Conjuror stopping...")

if __name__ == "__main__":
    main_loop()
