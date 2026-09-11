#!/usr/bin/env bash
# Freeze the current web build under Versions/<name>, so a working show can
# always be got back to. Never overwrites: pick a new name instead.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

NAME="${1:-beta-1}"
DEST="$PROJECT_DIR/Versions/$NAME"

if [[ -e "$DEST" ]]; then
  echo "Versions/$NAME already exists. Names are for going forward — pick the next one." >&2
  ls -1 "$PROJECT_DIR/Versions" 2>/dev/null | sed 's/^/  existing: /' >&2
  exit 1
fi

mkdir -p "$DEST"
rsync -a --exclude='.DS_Store' "$PROJECT_DIR/Web/" "$DEST/"

echo "Froze Web/ as Versions/$NAME"
echo "  • $(find "$DEST" -type f | wc -l | tr -d ' ') files, $(du -sh "$DEST" | cut -f1)"
