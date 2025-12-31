#!/usr/bin/env python3
import time
import os
import subprocess
from pathlib import Path

BASE = Path(__file__).parent.absolute()
CONTENT = BASE / 'content.md'
TEMPLATE = BASE / 'template.html'
BUILD_SCRIPT = BASE / 'build.py'
PEGASUS_SALE = BASE.parent / 'pegasus-sale'

def run_build():
    print(f"[{time.strftime('%H:%M:%S')}] Change detected. Building...")
    try:
        # Run build script
        subprocess.run(['python3', str(BUILD_SCRIPT)], check=True, cwd=str(BASE))
        
        # Sync to pegasus-sale for local preview
        if PEGASUS_SALE.exists():
            dest = PEGASUS_SALE / 'index.html'
            src = BASE / 'pegasus' / 'index.html'
            if src.exists():
                subprocess.run(['cp', str(src), str(dest)], check=True)
                print(f"Synced to {dest}")
        
        # Git auto-deploy (optional but helps "deploy" part)
        subprocess.run(['git', 'add', '.'], cwd=str(BASE))
        subprocess.run(['git', 'commit', '-m', 'Auto-sync from content.md'], cwd=str(BASE))
        subprocess.run(['git', 'push'], cwd=str(BASE))
        print("Pushed to GitHub.")
        
    except Exception as e:
        print(f"Error during build/deploy: {e}")

def watch():
    print(f"Watching {CONTENT} and {TEMPLATE}...")
    last_mtime = {
        CONTENT: CONTENT.stat().st_mtime if CONTENT.exists() else 0,
        TEMPLATE: TEMPLATE.stat().st_mtime if TEMPLATE.exists() else 0
    }
    
    while True:
        time.sleep(1)
        for path in last_mtime:
            if path.exists():
                current_mtime = path.stat().st_mtime
                if current_mtime > last_mtime[path]:
                    last_mtime[path] = current_mtime
                    run_build()

if __name__ == '__main__':
    run_build() # Initial build
    watch()
