#!/usr/bin/env bash
#
# The whole verification sweep, in one command. Run it before a release cut.
#
# Every gate in the project, against MAIN, in the order they cost: the cheap
# consistency reads first, the Swift suite last. All of them run even when an
# early one fails, because a release is blocked on the whole list and finding
# out about the second failure should not mean a second run.
#
#   ./verify_all.sh
#
# Exit status is 1 if any step failed, 0 if every step passed.
#
# Two of these overlap on purpose and neither is redundant:
#
#   - the play files under `Web/data/` are what the browser loads, and they are
#     the only place the button rules can be checked;
#   - the archives under `QuestionBank/` are MAIN's canonical rows and carry
#     four fields the play file never sees — `distractor_rationales` above all —
#     so they are the only place the citation and rationale rules can be.
#
# A bank can pass one and fail the other. That is not a contradiction; it is two
# different questions about two different files, and both have to be answered
# before a release.
#
# Course editions are not swept here. They have their own banks with their own
# archives-less shape and are checked one at a time:
#
#   python3 Tools/check_bank.py Web/courses/<id>/data/bank-en.js \
#       --fa Web/courses/<id>/data/bank-fa.js \
#       --edition Web/courses/<id>/course.js

set -uo pipefail
cd "$(dirname "$0")"

# label :: command
STEPS=(
  "archive in step with play files :: python3 Tools/render_bank.py --check"
  "play bank, English and Persian :: python3 Tools/check_bank.py Web/data/clues.js --fa Web/data/clues_fa.js"
  "archive bank, English and Persian :: python3 Tools/check_bank.py QuestionBank/verified_clues.json --archive --fa QuestionBank/verified_clues_fa.json"
  "Persian calendar markers :: python3 Tools/normalize_fa_prose.py --check"
  "Persian bank integrity :: python3 Tools/validate_persian_bank.py"
  "exhaustive state audit :: python3 Tools/verify_flawless_state.py"
  "cross-clue repeats, both banks :: python3 Tools/check_repeats.py --bank"
  "engine and Swift suite :: ./run_tests.sh"
)

failed=()
for step in "${STEPS[@]}"; do
  label="${step%% :: *}"
  command="${step##* :: }"
  printf '\n\033[1m── %s\033[0m\n' "$label"
  if eval "$command"; then
    printf '   PASS  %s\n' "$label"
  else
    printf '   FAIL  %s\n' "$label"
    failed+=("$label")
  fi
done

echo
echo "=================================================="
if [ ${#failed[@]} -eq 0 ]; then
  echo "ALL ${#STEPS[@]} STEPS PASSED"
  exit 0
fi
echo "${#failed[@]} of ${#STEPS[@]} STEP(S) FAILED:"
for label in "${failed[@]}"; do
  echo "  X $label"
done
exit 1
