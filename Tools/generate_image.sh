#!/usr/bin/env bash
#
# Generate a Jeopardy! Iranian Edition visual asset, locally and for free.
#
# Draw Things CLI runs FLUX.2 [klein] 4B (6-bit) on the machine itself. Nothing
# leaves it, nothing is billed, nothing needs a network once the model is down.
#
#   Tools/generate_image.sh "empty quiz-show stage, Tehran skyline behind glass"
#   Tools/generate_image.sh "..." --name stage-empty --variants 3
#   Tools/generate_image.sh "..." --width 1664 --height 960 --seed 42
#   Tools/generate_image.sh "..." --raw        # no house style, prompt verbatim
#   Tools/generate_image.sh "..." --people     # allow figures (hosts, players)
#
# The stage is empty by default -- people are excluded unless --people is given.
# Output lands in Assets/Generated/ as <name>-<seed>.png with a .txt sidecar
# carrying the exact prompt and seed, so any image can be reproduced.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/Assets/Generated"
MODEL="${DT_MODEL:-flux_2_klein_4b_q6p.ckpt}"

# --- the house look ---------------------------------------------------------
# The written contract is STYLE_SHEET.md; this is its translation into pixels.
# Charcoal ground, silver-grey structure, the flag's green and red used as stage
# lighting rather than as a flag, and restraint above all.
STYLE="cinematic production still of a television quiz-show stage, near-black charcoal environment, very low-key lighting, deep blacks, high contrast, restrained silver-grey surfaces, emerald green light grazing the left wall, crimson red light grazing the right wall, polished black floor with a thin reflection, architectural photography, minimal and severe"

# Things that read as cheap. The user's standing brief bans these outright:
# no flags, no gold, no generic "Persian" ornament, no cliched Middle Eastern
# imagery -- unless a prompt explicitly asks. Pass --negative "" to lift it.
NEGATIVE="national flag, tricolor banner, gold, gold leaf, gold typography, gilded ornament, arabesque, moroccan tile, mosque dome, minaret, dome, domes, minarets, onion dome, spire, spires, turban, camel, oil lamp, hookah, belly dancer, bazaar trinket, generic middle-eastern ornament, volcano, snow-capped peak, lone peak, mount fuji, kitschy, cluttered, busy wallpaper, watermark, signature, text, letters, words, logo, caption, low quality, blurry, jpeg artifacts, oversaturated, cartoon, anime, illustration, haze, fog, mist, smoke, hazy, washed out, pale, bright background, daylight, flat lighting"

# Most assets here are sets, backdrops and tiles, so the stage is empty unless
# asked otherwise. `--people` drops these terms -- use it for host and
# contestant artwork, where figures are the point.
NEG_PEOPLE="person, people, man, woman, men, women, human, figure, figures, face, faces, crowd, audience, presenter, host, contestant, contestants, portrait, businessman, suit"

PROMPT=""
NAME=""
WIDTH=1344
HEIGHT=768
STEPS=""
SEED=""
VARIANTS=1
RAW=0
PEOPLE=0
NEG_OVERRIDE="__unset__"

die() { printf 'generate_image: %s\n' "$1" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --name)     NAME="${2:?--name needs a value}"; shift 2 ;;
    --width)    WIDTH="${2:?}"; shift 2 ;;
    --height)   HEIGHT="${2:?}"; shift 2 ;;
    --steps)    STEPS="${2:?}"; shift 2 ;;
    --seed)     SEED="${2:?}"; shift 2 ;;
    --variants) VARIANTS="${2:?}"; shift 2 ;;
    --model)    MODEL="${2:?}"; shift 2 ;;
    --negative) NEG_OVERRIDE="$2"; shift 2 ;;
    --raw)      RAW=1; shift ;;
    --people)   PEOPLE=1; shift ;;
    # Named sizes. Every value must be a multiple of 64 -- the sampler's rule.
    --size)     case "${2:?}" in
                  16:9)   WIDTH=1024; HEIGHT=576 ;;   # exactly 16:9
                  wide)   WIDTH=1344; HEIGHT=768 ;;   # default; ~7:4
                  stage)  WIDTH=1664; HEIGHT=960 ;;   # the game stage, 1.73:1
                  square) WIDTH=1024; HEIGHT=1024 ;;
                  *) die "--size takes 16:9, wide, stage or square" ;;
                esac; shift 2 ;;
    -h|--help)  sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)         die "unknown flag $1 (try --help)" ;;
    *)          [ -n "$PROMPT" ] && die "prompt already given"
                PROMPT="$1"; shift ;;
  esac
done

[ -n "$PROMPT" ] || die "no prompt. try --help"

command -v draw-things-cli >/dev/null 2>&1 || \
  die "draw-things-cli is not on PATH. install it with: brew install draw-things-cli"

[ "$RAW" -eq 1 ] && FULL="$PROMPT" || FULL="$PROMPT, $STYLE"

if [ "$NEG_OVERRIDE" != "__unset__" ]; then
  NEG="$NEG_OVERRIDE"
elif [ "$PEOPLE" -eq 1 ]; then
  NEG="$NEGATIVE"
else
  NEG="$NEGATIVE, $NEG_PEOPLE"
fi

mkdir -p "$OUT"
slug="$(printf '%s' "${NAME:-asset}" | tr '[:upper:]' '[:lower:]' \
        | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' | cut -c1-60)"
stamp="$(date +%Y%m%d-%H%M%S)"

printf '\n\033[1mmodel\033[0m   %s\n' "$MODEL"
printf '\033[1msize\033[0m    %sx%s\n' "$WIDTH" "$HEIGHT"
printf '\033[1mprompt\033[0m  %s\n\n' "$FULL"

for i in $(seq 1 "$VARIANTS"); do
  if [ -n "$SEED" ]; then
    s=$(( SEED + i - 1 ))
  else
    s=$(( (RANDOM << 15 | RANDOM) % 4294967295 ))
  fi

  base="$slug-$stamp-s$s"
  [ "$VARIANTS" -gt 1 ] && base="$slug-$stamp-v$i-s$s"
  png="$OUT/$base.png"

  args=(generate
        --model "$MODEL"
        --prompt "$FULL"
        --width "$WIDTH" --height "$HEIGHT"
        --seed "$s" --output "$png"
        --disable-preview)
  [ -n "$NEG" ] && args+=(--negative-prompt "$NEG")
  [ -n "$STEPS" ] && args+=(--steps "$STEPS")

  printf '\033[1m[%s/%s]\033[0m %s\n' "$i" "$VARIANTS" "$base.png"
  if draw-things-cli "${args[@]}" >/dev/null 2>&1; then
    {
      printf 'prompt: %s\n' "$FULL"
      printf 'negative: %s\n' "$NEG"
      printf 'model: %s\n' "$MODEL"
      printf 'size: %sx%s\n' "$WIDTH" "$HEIGHT"
      printf 'seed: %s\n' "$s"
      printf 'generated: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    } > "$OUT/$base.txt"
    printf '         %s\n' "$(du -h "$png" | cut -f1)"
  else
    printf '         FAILED -- re-run without >/dev/null to see why\n'
  fi
done

printf '\nwrote to %s\n' "${OUT#$ROOT/}"
