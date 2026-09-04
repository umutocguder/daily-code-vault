#!/usr/bin/env python3
"""
Auto Sync Watcher Daemon
Monitors the workspace for file changes, debounces, creates meaningful commit messages, and pushes automatically to GitHub.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Paths to ignore
IGNORED_PATTERNS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    ".last_commit_msg",
    "gitbot.log",
    "gitbot_error.log",
    "auto_sync.log",
    "auto_sync_error.log",
    "auto_sync.pid"
}

DEBOUNCE_SECONDS = 4
POLL_INTERVAL_SECONDS = 1


def get_project_dir() -> Path:
    return Path(__file__).resolve().parent


def is_ignored(path: Path, root_dir: Path) -> bool:
    try:
        rel_parts = path.relative_to(root_dir).parts
    except ValueError:
        return True

    for part in rel_parts:
        if part in IGNORED_PATTERNS or part.endswith(".pyc") or part.endswith(".log") or part.endswith(".tmp"):
            return True
    return False


def get_file_mtimes(root_dir: Path) -> dict[str, float]:
    """Returns mapping of relative file path -> mtime."""
    mtimes = {}
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_PATTERNS]
        for f in files:
            full_path = Path(root) / f
            if not is_ignored(full_path, root_dir):
                try:
                    mtimes[str(full_path.relative_to(root_dir))] = full_path.stat().st_mtime
                except (OSError, FileNotFoundError):
                    pass
    return mtimes


def generate_commit_message(root_dir: Path) -> str:
    """Generates a meaningful commit message based on git status."""
    try:
        status_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root_dir,
            capture_output=True,
            text=True,
            check=True
        )
        raw_lines = [line for line in status_proc.stdout.splitlines() if line]
        if not raw_lines:
            return f"chore: auto-sync update [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

        modified = []
        added = []
        deleted = []

        for raw in raw_lines:
            status = raw[:2]
            filename = raw[3:].strip().strip('"\'')
            if "?" in status or "A" in status:
                added.append(filename)
            elif "D" in status:
                deleted.append(filename)
            else:
                modified.append(filename)

        details = []
        if added:
            details.append(f"add {', '.join(added[:3])}{'...' if len(added) > 3 else ''}")
        if modified:
            details.append(f"update {', '.join(modified[:3])}{'...' if len(modified) > 3 else ''}")
        if deleted:
            details.append(f"remove {', '.join(deleted[:3])}{'...' if len(deleted) > 3 else ''}")

        summary = "; ".join(details)

        # Categorize prefix
        all_changed = added + modified
        if any("algorithm" in f or "pattern" in f for f in all_changed):
            prefix = "feat"
        elif any("README" in f or "JOURNAL" in f or ".md" in f for f in all_changed):
            prefix = "docs"
        elif any(".py" in f or ".sh" in f for f in all_changed):
            prefix = "feat"
        else:
            prefix = "chore"

        return f"{prefix}: {summary} [{datetime.now().strftime('%H:%M:%S')}]"
    except Exception as e:
        return f"chore: auto-sync updates [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"


def commit_and_push(root_dir: Path) -> bool:
    """Stages all changes, commits with meaningful message, and pushes to remote."""
    try:
        status_check = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root_dir,
            capture_output=True,
            text=True,
            check=True
        )
        if not status_check.stdout.strip():
            return False

        commit_msg = generate_commit_message(root_dir)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Changes detected! Staging and committing...", flush=True)

        subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=root_dir, check=True)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pushing to GitHub (origin main)...", flush=True)
        push_proc = subprocess.run(["git", "push", "origin", "main"], cwd=root_dir, capture_output=True, text=True)

        if push_proc.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Pushed successfully: {commit_msg}", flush=True)
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Push failed: {push_proc.stderr}", flush=True)
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Sync error: {e}", flush=True)
        return False


def watch_loop(root_dir: Path):
    """Main watching loop with debounce."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Auto-Sync Watcher started on {root_dir}", flush=True)
    print(f"Debounce: {DEBOUNCE_SECONDS}s, Poll interval: {POLL_INTERVAL_SECONDS}s", flush=True)

    last_snapshot = get_file_mtimes(root_dir)
    pending_sync = False
    last_change_time = 0.0

    while True:
        try:
            time.sleep(POLL_INTERVAL_SECONDS)
            current_snapshot = get_file_mtimes(root_dir)

            if current_snapshot != last_snapshot:
                last_snapshot = current_snapshot
                last_change_time = time.time()
                pending_sync = True
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Detected file modification, debouncing {DEBOUNCE_SECONDS}s...", flush=True)

            if pending_sync and (time.time() - last_change_time >= DEBOUNCE_SECONDS):
                commit_and_push(root_dir)
                last_snapshot = get_file_mtimes(root_dir)
                pending_sync = False

        except KeyboardInterrupt:
            print("\nAuto-Sync Watcher stopped by user.", flush=True)
            break
        except Exception as e:
            print(f"Unexpected watcher error: {e}", flush=True)
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    project_dir = get_project_dir()
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        commit_and_push(project_dir)
    else:
        watch_loop(project_dir)
