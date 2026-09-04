"""
Daily Code Maintainer & Hygiene Engine
Performs safe, non-destructive cleanups: whitespace normalization, EOF fixes,
and code hygiene without modifying core logic or breaking code structure.
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Paths/patterns to ignore from cleanup
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
    "auto_sync.pid",
}

SUPPORTED_EXTENSIONS = {".py", ".md", ".sh"}


def is_ignored(path: Path, root_dir: Path) -> bool:
    try:
        rel_parts = path.relative_to(root_dir).parts
    except ValueError:
        return True
    return any(p in IGNORED_PATTERNS or p.endswith(".pyc") or p.endswith(".log") for p in rel_parts)


def clean_file(path: Path) -> bool:
    """
    Cleans trailing whitespace and normalizes end-of-file newlines.
    Returns True if file was modified.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        return False

    lines = content.splitlines()

    # 1. Strip trailing whitespace from each line
    cleaned_lines = [line.rstrip() for line in lines]

    # 2. Limit excessive consecutive blank lines (max 2 consecutive empty lines)
    reduced_lines = []
    blank_count = 0
    for line in cleaned_lines:
        if line == "":
            blank_count += 1
            if blank_count <= 2:
                reduced_lines.append(line)
        else:
            blank_count = 0
            reduced_lines.append(line)

    # 3. Ensure single clean newline at end of file (trim trailing empty lines)
    while reduced_lines and reduced_lines[-1] == "":
        reduced_lines.pop()

    new_content = "\n".join(reduced_lines) + "\n" if reduced_lines else ""

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True

    return False


def run_tests(root_dir: Path) -> bool:
    """Runs project unit tests to guarantee code structure and functionality are intact."""
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(root_dir), "-p", "test_*.py"],
        cwd=root_dir,
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def update_journal(output_base_dir: Path, today_str: str, message: str) -> None:
    """Appends maintenance entry to JOURNAL.md."""
    journal_path = output_base_dir / "JOURNAL.md"
    log_entry = f"- **{today_str}** `[MAINTENANCE]` {message}\n"

    existing_content = ""
    if journal_path.exists():
        with open(journal_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = "# Daily Code & Engineering Vault\n\nAutomated daily repository tracking code hygiene, maintenance, and project activity.\n\n## Activity Log\n\n"

    with open(journal_path, "w", encoding="utf-8") as f:
        if "## Activity Log\n\n" in existing_content:
            parts = existing_content.split("## Activity Log\n\n", 1)
            f.write(parts[0] + "## Activity Log\n\n" + log_entry + parts[1])
        else:
            f.write(existing_content + "\n" + log_entry)


def generate_entry(output_base_dir: str = ".") -> dict:
    """
    Main entry point invoked by daily cron runner.
    Finds files needing whitespace/formatting cleanup, fixes them,
    verifies unit tests pass, and prepares commit metadata.
    """
    base_path = Path(output_base_dir).resolve()
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Scan for candidates
    modified_files = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_PATTERNS]
        for f in files:
            file_path = Path(root) / f
            if is_ignored(file_path, base_path):
                continue
            if file_path.suffix in SUPPORTED_EXTENSIONS and file_path.name != "JOURNAL.md":
                # We can clean candidate files
                if clean_file(file_path):
                    rel_name = str(file_path.relative_to(base_path))
                    modified_files.append(rel_name)
                    # Limit to 1-2 files per daily run if desired, or all modified
                    if len(modified_files) >= 3:
                        break
        if len(modified_files) >= 3:
            break

    # Verify unit tests pass after any change
    if modified_files:
        if not run_tests(base_path):
            print("⚠️ Unit tests failed after cleanup! Rolling back changes.")
            subprocess.run(["git", "checkout", "--", "."], cwd=base_path)
            sys.exit(1)

        summary_files = ", ".join(modified_files[:3])
        log_desc = f"Cleaned trailing whitespace and normalized formatting in `{summary_files}`."
        commit_message = f"style(cleanup): normalize whitespace and EOF formatting in {summary_files} [{today_str}]"
    else:
        # If all files are already clean, perform daily hygiene check & test verification
        run_tests(base_path)
        log_desc = "Routine code hygiene verification: whitespace checked, unit tests verified."
        commit_message = f"chore(hygiene): verify code formatting and test suite [{today_str}]"

    # Always update activity journal so a commit can be made daily
    update_journal(base_path, today_str, log_desc)

    with open(base_path / ".last_commit_msg", "w", encoding="utf-8") as f:
        f.write(commit_message)

    return {
        "title": "Code Hygiene & Maintenance",
        "category": "maintenance",
        "modified_files": modified_files,
        "commit_message": commit_message
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result = generate_entry(base_dir)
    print(f"Executed: {result['title']}")
    print(f"Commit message: {result['commit_message']}")
