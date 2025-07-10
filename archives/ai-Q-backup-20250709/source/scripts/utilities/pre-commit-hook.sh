#!/bin/bash
# Pre-commit hook to enforce file size limits
# This script prevents commits with files that exceed 150 lines or 5K tokens

set -e

echo "🔍 Running file size compliance check..."

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel)"

# Run the file size enforcement script
python3 "$SCRIPT_DIR/enforce_file_size_limits.py" "$PROJECT_ROOT" --strict

if [ $? -eq 0 ]; then
    echo "✅ All files are compliant with size limits"
    exit 0
else
    echo "❌ File size limits violated! Commit blocked."
    echo ""
    echo "Please refactor any files that exceed:"
    echo "  - 300 lines (hard limit)"
    echo "  - 10K tokens (hard limit)"
    echo "  - Target range: 150-250 lines"
    echo ""
    echo "Run the following command to see details:"
    echo "  python3 scripts/enforce_file_size_limits.py"
    exit 1
fi 