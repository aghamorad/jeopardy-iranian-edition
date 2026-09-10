#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
pkill -x JeopardyApp 2>/dev/null || true
./build_release.sh
APP_BUNDLE="$ROOT_DIR/Jeopardy Iranian Edition.app"
open -n "$APP_BUNDLE"
case "${1:-run}" in
  --verify) sleep 2; pgrep -x JeopardyApp ;;
  --logs|--telemetry) /usr/bin/log stream --info --style compact --predicate 'process == "JeopardyApp"' ;;
esac
