"""AkashaOS Autopilot Agent"""
import json, os, shutil, subprocess, time

CONFIG_FILE = os.path.expanduser("~/.akasha_autopilot_config.json")
BACKUP_DIR = os.path.expanduser("~/.akasha_backups")
APPLY_SCRIPT = os.path.expanduser("~/AkashaOS/apply_update.sh")

def load_config():
    default = {
        "mode": "scout",  # scout, trial, apply
        "repo_path": os.path.expanduser("~/AkashaOS"),
        "personality": "adventurer"  # logs flavor
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        default.update(cfg)
    return default

def log(msg, personality="adventurer"):
    prefix = {"adventurer":"🗺️", "scientist":"⚗️", "navigator":"🧭"}.get(personality,">")
    print(f"{prefix} {msg}")

def backup_repo(path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = int(time.time())
    backup_path = os.path.join(BACKUP_DIR,f"backup_{timestamp}")
    shutil.copytree(path, backup_path)
    log(f"Backup created at {backup_path}")
    return backup_path

def dry_run(zipfile_path, repo_path):
    tmpdir = os.path.join("/tmp","akasha_autopilot_test")
    shutil.rmtree(tmpdir, ignore_errors=True)
    os.makedirs(tmpdir)
    subprocess.run(["unzip","-o",zipfile_path,"-d",tmpdir], check=True)
    modules_dir = os.path.join(tmpdir,"modules","aiguard")
    if not os.path.isdir(modules_dir):
        log("INVALID ZIP STRUCTURE", "scientist")
        return False
    log("Dry-run OK")
    return True

def apply_update(zipfile_path, repo_path):
    backup_repo(repo_path)
    subprocess.run([APPLY_SCRIPT, zipfile_path], check=True)
    log("Update applied successfully")

def main():
    import sys
    cfg = load_config()
    personality = cfg.get("personality","adventurer")
    if len(sys.argv)<2:
        log("Usage: python3 autopilot.py [scout|trial|apply] [zipfile]", personality)
        sys.exit(1)
    mode = sys.argv[1]
    zipfile_path = sys.argv[2] if len(sys.argv)>2 else None
    repo_path = cfg.get("repo_path")
    if mode=="scout":
        log("Scouting for updates... (not implemented: GitHub API)", personality)
    elif mode=="trial":
        if not zipfile_path:
            log("Specify a zipfile for trial", personality)
            sys.exit(1)
        ok = dry_run(zipfile_path, repo_path)
        log("Trial result: "+("PASS" if ok else "FAIL"), personality)
    elif mode=="apply":
        if not zipfile_path:
            log("Specify a zipfile to apply", personality)
            sys.exit(1)
        if dry_run(zipfile_path, repo_path):
            apply_update(zipfile_path, repo_path)
        else:
            log("Dry-run failed. Update aborted.", personality)
    else:
        log("Unknown mode", personality)

if __name__=="__main__":
    main()
