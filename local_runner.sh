#!/bin/bash
set -e

# Change directory to project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=== Running Daily Code Generator ==="
python3 generator.py

echo "=== Running Unit Tests ==="
python3 -m unittest discover -s . -p "test_*.py"

echo "=== Checking Git Status ==="
if [ -f .last_commit_msg ]; then
  COMMIT_MSG=$(cat .last_commit_msg)
  rm -f .last_commit_msg
else
  COMMIT_MSG="chore(daily): automated daily code update [$(date +'%Y-%m-%d')]"
fi

git add .
if git diff --cached --quiet; then
  echo "No file changes detected. Creating empty commit as requested..."
  git commit --allow-empty -m "$COMMIT_MSG"
  git push origin main
  echo "Successfully pushed empty commit: $COMMIT_MSG"
else
  git commit -m "$COMMIT_MSG"
  git push origin main
  echo "Successfully committed and pushed changes: $COMMIT_MSG"
fi
