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

push_with_retry() {
  local max_retries=5
  local count=0
  local delay=5

  while [ $count -lt $max_retries ]; do
    if git push origin main; then
      return 0
    fi
    count=$((count + 1))
    echo "⚠️ Git push failed (attempt $count/$max_retries). Network may be connecting, retrying in ${delay}s..."
    sleep $delay
    delay=$((delay * 2))
  done
  echo "❌ Git push failed after $max_retries attempts."
  return 1
}

git add .
if git diff --cached --quiet; then
  echo "No file changes detected. Creating empty commit as requested..."
  git commit --allow-empty -m "$COMMIT_MSG"
  push_with_retry
  echo "Successfully pushed empty commit: $COMMIT_MSG"
else
  git commit -m "$COMMIT_MSG"
  push_with_retry
  echo "Successfully committed and pushed changes: $COMMIT_MSG"
fi
