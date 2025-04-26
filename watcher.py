import os
import time
import subprocess
import sys
import signal

def watch_and_reload(script_path):
    last_modified = os.path.getmtime(script_path)
    process = subprocess.Popen([sys.executable, script_path])

    try:
        while True:
            time.sleep(3)
            current_modified = os.path.getmtime(script_path)
            if current_modified != last_modified:
                print("Changes detected. Reloading...")
                # Kill the old process
                process.terminate()
                process.wait()
                # Restart the process
                process = subprocess.Popen([sys.executable, script_path])
                last_modified = current_modified
    except KeyboardInterrupt:
        print("Stopping watcher...")
        process.terminate()

if __name__ == "__main__":
    watch_and_reload("student_panal.py")                  ##  your file name
