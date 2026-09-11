#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

export SWIFT_MODULECACHE_PATH="${SWIFT_MODULECACHE_PATH:-$PROJECT_DIR/.build/ModuleCache}"
export CLANG_MODULE_CACHE_PATH="${CLANG_MODULE_CACHE_PATH:-$PROJECT_DIR/.build/ClangModuleCache}"
mkdir -p "$SWIFT_MODULECACHE_PATH" "$CLANG_MODULE_CACHE_PATH"

UNIVERSAL=0
case "${1:-}" in
  "")           ;;
  --universal)  UNIVERSAL=1 ;;
  *)            echo "usage: $0 [--universal]" >&2; exit 2 ;;
esac

# Each arch gets its own scratch path, because a single build directory can only
# hold one architecture's object files.
# `--show-bin-path` mixes build chatter onto stdout with the path itself, and the
# chatter is not reliably first — so take the one line that is an absolute path.
# The two scratch layouts also differ (`out/Products/Release` under a triple, flat
# otherwise), which is why this is asked rather than guessed.
build_arch() {
  swift build -c release --disable-sandbox --product JeopardyApp \
    --scratch-path "$PROJECT_DIR/.build/$1" --triple "$2" >&2
  swift build --disable-sandbox -c release \
    --scratch-path "$PROJECT_DIR/.build/$1" --triple "$2" --show-bin-path 2>/dev/null \
    | grep -E '^/' | tail -n 1
}

echo "Compiling the show shell in Release mode..."
if [[ "$UNIVERSAL" -eq 1 ]]; then
  echo "  • arm64"
  ARM_BIN="$(build_arch arm64 arm64-apple-macosx14.0)/JeopardyApp"
  echo "  • x86_64"
  X86_BIN="$(build_arch x86_64 x86_64-apple-macosx14.0)/JeopardyApp"

  for bin in "$ARM_BIN" "$X86_BIN"; do
    [[ -x "$bin" ]] || { echo "No executable at $bin" >&2; exit 1; }
  done

  BIN_DIR="$PROJECT_DIR/.build/universal"
  mkdir -p "$BIN_DIR"
  lipo -create "$ARM_BIN" "$X86_BIN" -output "$BIN_DIR/JeopardyApp"
  echo "  • lipo: $(lipo -archs "$BIN_DIR/JeopardyApp")"
else
  swift build -c release --disable-sandbox --product JeopardyApp
  BIN_DIR="$(swift build --disable-sandbox -c release --show-bin-path 2>/dev/null \
    | grep -E '^/' | tail -n 1)"
fi

if [[ ! -x "$BIN_DIR/JeopardyApp" ]]; then
  echo "Release compilation did not produce executable at $BIN_DIR/JeopardyApp" >&2
  exit 1
fi

# The show is the web build, so refuse to ship a bundle without it. A shell that
# opens onto nothing is worse than a failed build.
[[ -f "$PROJECT_DIR/Web/index.html" ]] || { echo "Web/index.html is missing" >&2; exit 1; }
[[ -f "$PROJECT_DIR/Web/data/clues.js" ]] || { echo "Web/data/clues.js is missing" >&2; exit 1; }
# Both banks and the localisation table ship inside the bundle's Web tree. A build
# that carried only the English bank would silently drop the Persian edition.
[[ -f "$PROJECT_DIR/Web/data/clues_fa.js" ]] || { echo "Web/data/clues_fa.js is missing" >&2; exit 1; }
[[ -f "$PROJECT_DIR/Web/i18n.js" ]] || { echo "Web/i18n.js is missing" >&2; exit 1; }

APP_BUNDLE="$PROJECT_DIR/dist/Jeopardy Iranian Edition.app"
rm -rf "$APP_BUNDLE"
mkdir -p "$APP_BUNDLE/Contents/MacOS" "$APP_BUNDLE/Contents/Resources"

cp "$BIN_DIR/JeopardyApp" "$APP_BUNDLE/Contents/MacOS/JeopardyApp"
chmod +x "$APP_BUNDLE/Contents/MacOS/JeopardyApp"

printf "APPL????" > "$APP_BUNDLE/Contents/PkgInfo"

# The game, whole. `ShowSource` looks for `Web/index.html` in the bundle and
# hands the directory to a webview with read access to exactly that folder —
# so this tree is the app's entire content, and it is copied unmodified.
ditto "$PROJECT_DIR/Web" "$APP_BUNDLE/Contents/Resources/Web"

cp "$PROJECT_DIR/App/Resources/AppIcon.icns" "$APP_BUNDLE/Contents/Resources/AppIcon.icns"

cat > "$APP_BUNDLE/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key><string>en</string>
    <key>CFBundleExecutable</key><string>JeopardyApp</string>
    <key>CFBundleIconFile</key><string>AppIcon.icns</string>
    <key>CFBundleIdentifier</key><string>com.morad.jeopardy-iranian-edition</string>
    <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
    <key>CFBundleName</key><string>Jeopardy Iranian Edition</string>
    <key>CFBundleDisplayName</key><string>Jeopardy Iranian Edition</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleSignature</key><string>????</string>
    <key>CFBundleShortVersionString</key><string>1.0.5</string>
    <key>CFBundleSupportedPlatforms</key>
    <array>
        <string>MacOSX</string>
    </array>
    <key>CFBundleVersion</key><string>105</string>
    <key>LSMinimumSystemVersion</key><string>14.0</string>
    <key>LSApplicationCategoryType</key><string>public.app-category.games</string>
    <key>NSHighResolutionCapable</key><true/>
    <key>NSPrincipalClass</key><string>NSApplication</string>
</dict>
</plist>
PLIST

plutil -lint "$APP_BUNDLE/Contents/Info.plist"

# Remove quarantine/provenance extended attributes before signing
xattr -cr "$APP_BUNDLE" 2>/dev/null || true

codesign --force --deep --sign - "$APP_BUNDLE"
codesign --verify --deep --strict "$APP_BUNDLE"

# Also place the bundle directly in the root directory for immediate user access
rm -rf "$PROJECT_DIR/Jeopardy Iranian Edition.app"
cp -R "$APP_BUNDLE" "$PROJECT_DIR/Jeopardy Iranian Edition.app"

echo "Release build succeeded:"
echo "  • Dist bundle: $APP_BUNDLE ($(du -sh "$APP_BUNDLE" | cut -f1))"
echo "  • Root bundle: $PROJECT_DIR/Jeopardy Iranian Edition.app ($(du -sh "$PROJECT_DIR/Jeopardy Iranian Edition.app" | cut -f1))"
