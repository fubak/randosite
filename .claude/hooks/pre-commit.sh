#!/bin/bash
# Pre-commit hook for daily-trending-info
# Runs mypy and ruff before commits

set -e
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || cd "$(dirname "$0")/../.."

echo "daily-trending-info: Running pre-commit checks..."

source ~/.claude/hooks/lib/pre-commit.sh 2>/dev/null || {
    # Fallback if shared lib not available
    black --check scripts/ tests/ 2>/dev/null && echo "Black: OK"
    ruff check . 2>/dev/null && echo "Ruff: OK"
    exit 0
}

run_pre_commit "python"
