"""Simple health check for AI Guard modules"""
import sys, os

modules_path = os.path.join(os.path.dirname(__file__), "..", "modules", "aiguard")
sys.path.insert(0, modules_path)

try:
    from ai_guard import AIGuard
    from profile_store import ProfileStore
except Exception as e:
    print("❌ Module import failed:", e)
    sys.exit(1)

demo_script = os.path.join(modules_path,"demo_login.py")
ret = os.system(f"python3 {demo_script} <<'EOF'\nq\nEOF")
if ret!=0:
    print("❌ demo_login.py failed")
    sys.exit(1)

print("✅ Health check passed")
