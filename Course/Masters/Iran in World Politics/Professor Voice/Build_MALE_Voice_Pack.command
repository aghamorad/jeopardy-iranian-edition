#!/bin/bash
set -euo pipefail

PACK_NAME="Iran_World_Politics_Professor_MALE_Voice_Pack"
OUT="$HOME/Desktop/$PACK_NAME"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"
rm -f "$OUT"/*.wav "$OUT"/transcripts.tsv 2>/dev/null || true

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is missing."
  exit 1
fi

cat > "$TMP/items.tsv" <<'ITEMS'
01_professor_welcome|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/34a74e84-8905-4ec9-830f-383724435950.mp3|Welcome to IR4595: Iran in World Politics. We’ll begin with revolution, move through war, factional politics, the Revolutionary Guards, sanctions, gender, minorities, foreign policy, and finally the rather inconvenient fact that history has refused to stop happening.
02_start_game|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/7f2a169d-0ef2-4663-aad4-0351e532abf5.mp3|Right. Let’s see what you actually know.
03_choose_topic|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/9b2a3056-ee52-4bfe-980e-91af9406ff68.mp3|Choose a topic. Preferably one you’ve read about.
04_correct_annoyingly_so|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/742e34a6-0376-4bec-9b1c-8d97137678fa.mp3|Correct. Annoyingly so.
05_correct_surprised|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/64faacbf-9a13-496a-9149-02424b33631a.mp3|Yes. That is, in fact, the answer. I’m as surprised as you are.
06_wrong_confident|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/8b3670b5-8ea8-42f1-9e1b-11a388e36b4e.mp3|No. Confident, certainly. Correct, unfortunately not.
07_wrong_reading|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/b604e217-c4e1-4628-8dcd-17d034b7dbcf.mp3|That’s wrong. The reading was not merely decorative, you know.
08_timeout|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/9f6eda56-6c27-4cd1-86dd-4ac20cf092bc.mp3|Time. History has moved on without you.
09_close_call|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/94a8aa10-453f-404f-8c12-7ff22f1b17dd.mp3|Very close. In academia, of course, that remains wrong.
10_three_in_a_row|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/4a2e8df1-203a-4210-b2d2-7e1b8d549e17.mp3|Three in a row. I may have underestimated you. Briefly.
11_comeback|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/f54cad71-70a0-413a-be63-1eea9035b58d.mp3|A comeback. How very post-revolutionary of you.
12_daily_double|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/fcb2f9fc-d0f6-4f1f-92e7-e647f9fc5343.mp3|You’ve found the Daily Double. At last, a decision with consequences.
13_final_jeopardy|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/e5ec904c-95b7-4af5-9a3e-68102b417d27.mp3|Final Jeopardy. One question, one wager, and considerably less room for bluffing.
14_topic_revolution|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/80a0638d-d363-4946-b65e-fbab5589212a.mp3|Revolution and the Islamic Republic. Ideology, institutions, and the small matter of who actually rules.
15_topic_iran_iraq_war|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/c0ca7de6-3fe5-447f-bd55-beb4ab00207d.mp3|The Iran–Iraq War. Eight years, several turning points, and no shortage of people explaining them badly.
16_topic_factional_politics|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/81525a57-6dd4-4918-ab16-ec883208fa91.mp3|Factional politics. Because calling the Islamic Republic a single actor is a very efficient way to lose marks.
17_topic_irgc_political_economy|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/3155a1c3-be82-4549-88c4-df0f2a44f671.mp3|The Revolutionary Guards and political economy. Guns, contracts, institutions, and the awkward business of deciding where the state actually ends.
18_topic_foreign_policy|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/27af304b-6533-4757-8764-6b0de0945094.mp3|Iranian foreign policy. Ideology, pragmatism, insecurity, status, recognition. Pick your explanation carefully. Preferably more than one.
19_topic_axis_of_resistance|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/d23c683d-013d-4ce5-8ea4-137661ba6c86.mp3|The Axis of Resistance. Transnational solidarity, regional strategy, deterrence — and, as ever, a lively argument over which label is doing the most work.
20_topic_sanctions|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/c68005a5-5338-499b-b342-35d78b1c2736.mp3|Sanctions and the resistance economy. An excellent opportunity to discover why saying “sanctions hurt the economy” is the beginning of an answer, not the end of one.
21_topic_gender_politics|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/7e8c4de3-a36b-48ad-a043-1c6ffd07369e.mp3|Gender politics. State power, social change, negotiation, resistance, and the usual danger of assuming the answer before examining the evidence.
22_topic_minorities|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/4c681a19-418e-41c8-affa-f4672f34c7ee.mp3|Ethnic and religious minorities. A subject on which sweeping generalisations will be punished with particular enthusiasm.
23_topic_iran_at_war|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/0bce32fc-0355-4598-9dd4-a365a2a84075.mp3|Iran at war, from 2023 to the present. Which is the syllabus politely acknowledging that the examination period may not be the most stressful event of the semester.
24_score_lead|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/76fd9895-ac97-4e8f-bee6-5c2b96b6d731.mp3|You’re in the lead. Try not to convert that into a theory of your own brilliance just yet.
25_game_win|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/72683d0f-e85d-4b4a-bb95-df27ceb11d53.mp3|And that is the game. You’ve won. I’ll try not to let it affect the marking.
26_game_loss|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/f019e6ab-5d1b-4d0a-aefa-ca80bb5f2d18.mp3|And that is the game. You’ve lost, but quite usefully. There was clearly a great deal left to learn.
27_class_dismissed|https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/0003f455-9422-47e3-a73b-b8be4015cb79.mp3|Class dismissed. Do read before the next one. It makes the conversation considerably less painful for all of us.
ITEMS

printf '\nBuilding 27 male professor WAV files...\n\n'
fail=0
while IFS='|' read -r name url transcript; do
  mp3="$TMP/$name.mp3"
  wav="$OUT/$name.wav"
  printf '%-44s' "$name.wav"
  if ! curl -L --fail --retry 5 --retry-all-errors --retry-delay 2 --connect-timeout 30 --max-time 180 -sS "$url" -o "$mp3"; then
    echo ' DOWNLOAD FAILED'
    fail=1
    continue
  fi
  bytes=$(wc -c < "$mp3" | tr -d ' ')
  if [ "$bytes" -lt 1000 ]; then
    echo " BAD DOWNLOAD ($bytes bytes)"
    fail=1
    continue
  fi
  if command -v afconvert >/dev/null 2>&1 && afconvert -f WAVE -d LEI16@48000 "$mp3" "$wav" >/dev/null 2>&1; then
    echo ' ✓'
  elif command -v ffmpeg >/dev/null 2>&1 && ffmpeg -loglevel error -y -i "$mp3" -ar 48000 -ac 1 -c:a pcm_s16le "$wav"; then
    echo ' ✓ (ffmpeg)'
  else
    echo ' CONVERSION FAILED'
    fail=1
  fi
done < "$TMP/items.tsv"

{
  printf 'filename\ttranscript\n'
  while IFS='|' read -r name url transcript; do
    printf '%s.wav\t%s\n' "$name" "$transcript"
  done < "$TMP/items.tsv"
} > "$OUT/transcripts.tsv"

count=$(find "$OUT" -maxdepth 1 -name '*.wav' -type f | wc -l | tr -d ' ')
printf '\nCreated %s of 27 WAV files.\n' "$count"

if [ "$count" -eq 27 ]; then
  ZIP="$HOME/Desktop/${PACK_NAME}.zip"
  rm -f "$ZIP"
  if command -v ditto >/dev/null 2>&1; then
    /usr/bin/ditto -c -k --sequesterRsrc --keepParent "$OUT" "$ZIP"
  else
    (cd "$HOME/Desktop" && zip -qr "$ZIP" "$PACK_NAME")
  fi
  echo
  echo "DONE — all 27 male clips verified."
  echo "Folder: $OUT"
  echo "ZIP:    $ZIP"
  open "$OUT" 2>/dev/null || true
else
  echo
  echo "INCOMPLETE: $count/27 files were created."
  echo "Leave this window open to see which download failed, then run the builder again."
  open "$OUT" 2>/dev/null || true
  exit 2
fi

echo
read -n 1 -s -r -p 'Press any key to close...'
echo
