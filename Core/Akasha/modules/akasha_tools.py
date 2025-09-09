# modules/akasha_tools.py
import datetime

# Keep logs in memory
_log_buffer = []

def log(message):
    """Log a message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    _log_buffer.append(entry)

def load_logs(memory):
    """Load logs from memory if present."""
    global _log_buffer
    _log_buffer = memory.get("_logs", [])

def save_logs(memory):
    """Save current logs to memory."""
    memory["_logs"] = _log_buffer

