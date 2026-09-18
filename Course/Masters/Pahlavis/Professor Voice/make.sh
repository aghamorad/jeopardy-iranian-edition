#!/bin/zsh
# Generate Stephanie's Pahlavi lines by cloning the reference clip.
# Serial by design: two mlx-speech runners OOM this 16 GB machine.
set -u
cd "$(dirname "$0")"

REF="reference/stephanie-cronin-ref.wav"
REFTXT="$(cat reference/stephanie-cronin-ref.txt)"
OUT="1.0x source"
RAW="raw"
MLX="$HOME/.local/bin/mlx-speech"

mkdir -p "$OUT" "$RAW"

while IFS=$'\t' read -r name text; do
  [ -z "$name" ] && continue
  if [ -f "$OUT/$name.m4a" ]; then
    echo "skip  $name"
    continue
  fi
  echo "---   $name"
  if ! "$MLX" tts --model fish-s2-pro --text "$text" \
        --reference-audio "$REF" --reference-text "$REFTXT" \
        --output "$RAW/$name.wav" >> batch.log 2>&1; then
    echo "FAIL  $name (tts)"
    continue
  fi
  if ! ffmpeg -y -loglevel error -i "$RAW/$name.wav" \
        -ac 1 -ar 48000 -c:a aac -b:a 96k "$OUT/$name.m4a"; then
    echo "FAIL  $name (encode)"
    continue
  fi
  echo "ok    $name"
done < <(tail -n +2 transcripts.tsv)

echo BATCH_DONE
