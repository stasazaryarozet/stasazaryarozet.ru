import time
import shutil
from pathlib import Path
import build

# Configuration
WATCH_DIRS = [Path("."), Path("src")]
EXTENSIONS = {'.md', '.html', '.css', '.py'}
# Output dir for the separate "pegasus-sale" folder which presumably is being served
TARGET_DIR = Path("../pegasus-sale")

def get_mtimes():
    mtimes = {}
    for d in WATCH_DIRS:
        for p in d.rglob("*"):
            if p.suffix in EXTENSIONS:
                try:
                    mtimes[str(p)] = p.stat().st_mtime
                except FileNotFoundError:
                    pass
    return mtimes

def sync_artifacts():
    """Copies built artifacts from internal 'pegasus' dir to external 'pegasus-sale'"""
    source_dir = Path("pegasus")
    if not source_dir.exists():
        return

    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)
        
    # Sync files
    for file_path in source_dir.glob("*"):
        if file_path.is_file():
            shutil.copy2(file_path, TARGET_DIR / file_path.name)
            
    print(f"   -> Synced to {TARGET_DIR}")

def main():
    print("--- Pegasus Watcher & Auto-Builder Started ---")
    print(f"Monitoring in real-time: {', '.join([str(d) for d in WATCH_DIRS])}")
    
    # Initial build
    try:
        build.build()
        sync_artifacts()
    except Exception as e:
        print(f"Initial build failed: {e}")

    last_mtimes = get_mtimes()

    try:
        while True:
            time.sleep(0.5) # Fast check
            current_mtimes = get_mtimes()
            
            changed = False
            for p, mtime in current_mtimes.items():
                if p not in last_mtimes or last_mtimes[p] != mtime:
                    print(f"\n[Detected change] {p}")
                    changed = True
                    break
            
            if changed:
                try:
                    # Re-run build
                    build.build()
                    # Sync to serving dir
                    sync_artifacts()
                    print("[Done] Updated.")
                except Exception as e:
                    print(f"[Error] Build cycle failed: {e}")
                
                last_mtimes = current_mtimes
                
    except KeyboardInterrupt:
        print("\nWatcher stopped.")

if __name__ == "__main__":
    main()
