#!/usr/bin/env bash
set -euo pipefail

# Source shared notification library
source ~/.claude/hooks/lib/notify.sh 2>/dev/null || true

# Exit if not in a git repo
if ! command -v git >/dev/null 2>&1 || ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

# Check if there are Python changes
if ! git status --porcelain | grep -qE '\.py$'; then
  exit 0
fi

echo "🔍 Running tests..."

# Run tests if pytest is available
if command -v pytest >/dev/null 2>&1; then
  if pytest tests/ -q 2>/dev/null; then
    echo "✅ Tests passed"
  else
    echo "⚠️  Some tests failed"
  fi
fi

notify "daily-trending-info" "Task completed" 2>/dev/null || true
exit 0
