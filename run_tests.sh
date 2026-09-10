#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Keep SwiftPM caches inside the writable project sandbox.
export SWIFT_MODULECACHE_PATH="${SWIFT_MODULECACHE_PATH:-$PROJECT_DIR/.build/ModuleCache}"
export CLANG_MODULE_CACHE_PATH="${CLANG_MODULE_CACHE_PATH:-$PROJECT_DIR/.build/ClangModuleCache}"
mkdir -p "$SWIFT_MODULECACHE_PATH" "$CLANG_MODULE_CACHE_PATH"

echo "Building current test runner..."
swift build --disable-sandbox --product JeopardyTests
BIN_DIR="$(swift build --disable-sandbox --show-bin-path)"
TEST_BIN="$BIN_DIR/JeopardyTests"

echo "Running Jeopardy - Iranian Edition Automated Test Suite..."
exec "$TEST_BIN" "$@"
