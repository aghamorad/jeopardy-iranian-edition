#!/usr/bin/env bash
# The version of the show, read out of the one file that declares it.
#
# `Web/update.js` has to know this number. It is what the boot-time update check
# measures a GitHub release against, so a build stamped with anything else would
# either miss a real release or announce one the player already has. Every other
# place a version gets written — the Mac bundle's Info.plist, the iOS project,
# Android's manifest — reads it from here rather than keeping a second copy to
# drift out of step with the check.
#
# Prints the dotted version (`1.0.10`). `--build` prints the same number with the
# dots taken out (`1010`), which is the form Apple's CFBundleVersion and Android's
# versionCode want: a counter that moves forward, not a marketing string.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$PROJECT_DIR/Web/update.js"

VERSION="$(sed -n "s/^[[:space:]]*var VERSION = '\([0-9][0-9.]*\)'.*$/\1/p" "$SOURCE" | head -n 1)"

if [[ -z "$VERSION" ]]; then
  echo "No version declared in $SOURCE" >&2
  exit 1
fi

case "${1:-}" in
  "")       printf '%s\n' "$VERSION" ;;
  --build)  printf '%s\n' "${VERSION//./}" ;;
  *)        echo "usage: $0 [--build]" >&2; exit 2 ;;
esac
