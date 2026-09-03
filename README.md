# 🚀 Daily Code & Engineering Vault

An automated code and engineering vault that curates clean, well-tested algorithms, architectural patterns, and software design insights with instant real-time and scheduled Git syncing.

---

## 📌 Features

- **⚡ Real-Time Auto-Push Watcher**: Automatically detects when you or the AI write/modify code, debounces briefly, generates meaningful Conventional Commits, and pushes instantly to GitHub.
- **⏰ Scheduled Daily Push**: Runs via macOS `launchd` service daily at 12:00 PM.
- **💎 High-Quality Code**: Includes full type annotations, docstrings, and comprehensive unit tests. Zero temporary or junk files.
  - `algorithms/`: Data structures & algorithmic problems.
  - `patterns/`: System design, resiliency, and architectural patterns.
  - `notes/`: Technical breakdowns and engineering principles.
- **📜 Activity Log**: Automatically tracked in [`JOURNAL.md`](./JOURNAL.md).

---

## 🛠️ Auto-Sync Controller (`auto_sync_ctl.sh`)

You can run the auto-sync daemon in the background so that any code written is pushed immediately without typing manual git commands:

```bash
# Start background watcher (pushes on every edit)
./auto_sync_ctl.sh start

# Check status and recent sync logs
./auto_sync_ctl.sh status

# Push all current changes immediately
./auto_sync_ctl.sh sync-now

# Stop the background watcher
./auto_sync_ctl.sh stop
```

---

## 🚀 Running Tests
```bash
python3 -m unittest discover -s . -p "test_*.py"
```
