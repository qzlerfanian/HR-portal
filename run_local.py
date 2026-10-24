"""Start the Python API and the React/Vinext web UI for local PyCharm use."""

import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("Node.js 22.13+ was not found. Install Node.js and restart PyCharm.", file=sys.stderr)
        return 1

    commands = [
        ([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"], "Python API"),
        ([node, "scripts/run-framework.mjs", "dev"], "Web UI"),
    ]
    processes: list[tuple[subprocess.Popen, str]] = []
    try:
        for command, label in commands:
            process = subprocess.Popen(command, cwd=ROOT)
            processes.append((process, label))
            print(f"Started {label} (pid {process.pid})", flush=True)
        print("Open http://localhost:5173 — press Ctrl+C to stop both services.", flush=True)

        while True:
            for process, label in processes:
                code = process.poll()
                if code is not None:
                    print(f"{label} stopped with exit code {code}.", file=sys.stderr)
                    return code or 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping TalentFlow…", flush=True)
        return 0
    finally:
        for process, _ in reversed(processes):
            if process.poll() is None:
                process.terminate()
        for process, _ in reversed(processes):
            if process.poll() is None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
