# modules/loader.py
# Auto-load all python modules in the modules/ directory (simple example).
import os, importlib.util, sys, traceback

MODULES_DIR = os.path.join(os.path.dirname(__file__), '..', 'modules')
MODULES_DIR = os.path.abspath(MODULES_DIR)

def discover_and_load():
    found = []
    if not os.path.exists(MODULES_DIR):
        return found
    for fname in os.listdir(MODULES_DIR):
        if not fname.endswith('.py') or fname == 'loader.py': continue
        path = os.path.join(MODULES_DIR, fname)
        try:
            spec = importlib.util.spec_from_file_location(fname[:-3], path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            found.append(fname)
        except Exception:
            traceback.print_exc()
    return found

if __name__ == '__main__':
    print('Discovered modules:', discover_and_load())
