#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

export SWIFT_MODULECACHE_PATH="${SWIFT_MODULECACHE_PATH:-$PROJECT_DIR/.build/ModuleCache}"
export CLANG_MODULE_CACHE_PATH="${CLANG_MODULE_CACHE_PATH:-$PROJECT_DIR/.build/ClangModuleCache}"
mkdir -p "$SWIFT_MODULECACHE_PATH" "$CLANG_MODULE_CACHE_PATH"

"$PROJECT_DIR/build_release.sh"
APP_BUNDLE="$PROJECT_DIR/dist/Jeopardy Iranian Edition.app"
echo "Launching Jeopardy - Iranian Edition (Apple Silicon Native)..."

# Quit any previous instance
killall JeopardyApp >/dev/null 2>&1 || true
sleep 0.4

if open -n "$APP_BUNDLE" --args "$@" 2>/dev/null; then
    echo "Launched via LaunchServices."
else
    echo "Launching binary directly..."
    exec "$APP_BUNDLE/Contents/MacOS/JeopardyApp" "$@"
fi
