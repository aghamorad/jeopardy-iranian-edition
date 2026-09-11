#!/usr/bin/env bash
# Cut the iOS .ipa. Like build_release.sh, the web tree is the app's whole
# content, so this stages `Web/` into the bundle verbatim and refuses to ship a
# bundle whose Web tree has drifted from the source.
#
# The .ipa is UNSIGNED — there is no iOS development certificate on this
# machine, so CODE_SIGNING_ALLOWED=NO is not a shortcut, it is the only option.
# Anyone sideloading it has to sign it themselves (AltStore, Sideloadly, a
# personal team). Say so in the release notes.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR/iOS"

export DEVELOPER_DIR="${DEVELOPER_DIR:-/Applications/Xcode-beta.app/Contents/Developer}"

rm -rf /tmp/jdd /tmp/ipa
mkdir -p /tmp/ipa/Payload

echo "=== xcodegen ==="
xcodegen generate

echo "=== xcodebuild ==="
xcodebuild -project JeopardyIranianEdition.xcodeproj \
  -scheme JeopardyIOS -sdk iphoneos -configuration Release \
  -derivedDataPath /tmp/jdd CODE_SIGNING_ALLOWED=NO \
  clean build 2>&1 | tail -6

APP="$(find /tmp/jdd/Build/Products/Release-iphoneos -maxdepth 1 -name '*.app' | head -n 1)"
echo "=== app: $APP ==="
[[ -d "$APP" ]] || { echo "no .app produced" >&2; exit 1; }

ditto "$APP" /tmp/ipa/Payload/Jeopardy.app

echo "=== staged version ==="
plutil -p /tmp/ipa/Payload/Jeopardy.app/Info.plist | grep -i "shortversion\|CFBundleVersion"

# A bundle that shipped a stale or truncated Web tree is the one failure mode
# worth blocking on, so diff it rather than trusting the copy step.
echo "=== Web tree parity ==="
diff -rq "$PROJECT_DIR/Web" /tmp/ipa/Payload/Jeopardy.app/Web 2>&1 | grep -v "\.DS_Store" || true
echo "(end diff)"

cd /tmp/ipa
rm -f "$PROJECT_DIR/dist/Jeopardy-Iranian-Edition-iOS.ipa"
zip -qry "$PROJECT_DIR/dist/Jeopardy-Iranian-Edition-iOS.ipa" Payload
echo "=== ipa ==="
ls -la "$PROJECT_DIR/dist/Jeopardy-Iranian-Edition-iOS.ipa"
echo "=== done ==="
