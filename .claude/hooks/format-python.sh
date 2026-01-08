#!/usr/bin/env bash
set -euo pipefail

# Exit if not in a git repo
if ! command -v git >/dev/null 2>&1 || ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

# Only format if Edit or Write tool was used
if [[ ! "${TOOL_NAME:-}" =~ ^(Edit|Write)$ ]]; then
  exit 0
fi

# Only format Python files
if [[ ! "${FILE_PATH:-}" =~ \.py$ ]]; then
  exit 0
fi

# Check if file exists
if [[ ! -f "${FILE_PATH}" ]]; then
  exit 0
fi

# Format using black if available
if command -v black >/dev/null 2>&1; then
  black "${FILE_PATH}" 2>/dev/null || true
fi

exit 0
