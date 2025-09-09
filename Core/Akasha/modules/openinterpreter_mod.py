import subprocess

def init(memory):
    print("[openinterpreter_mod] Ready to launch Open Interpreter.")

def loop(memory):
    # Only run once per boot if not already started
    if not memory.get('openinterpreter_mod', {}).get('started'):
        print("[openinterpreter_mod] Launching Open Interpreter...")
        subprocess.Popen(["interpreter", "-y"])
        memory['openinterpreter_mod'] = {'started': True}

def save(memory):
    # Optional: Nothing special to save right now
    pass
