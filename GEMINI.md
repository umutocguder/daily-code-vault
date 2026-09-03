# Workspace Guidelines: Autonomous Development & Auto-Push

## Core Principles
1. **Autonomous Execution**:
   - For all personal projects and code written in this workspace, do NOT block for manual approval/confirmation steps.
   - Proactively implement the required solution, run automated verification tests, and finalize changes directly.

2. **Quality Standards**:
   - Never write temporary/junk code.
   - Maintain clean modular architecture, full type hints, docstrings, and comprehensive unit tests.

3. **Continuous Auto-Push**:
   - Ensure all changes are automatically committed with clean Conventional Commit messages and synced with GitHub (`origin main`).
   - The background auto-sync watcher (`auto_sync.py`) handles continuous real-time synchronization, but the assistant should also ensure working directories are cleanly verified and pushed.
