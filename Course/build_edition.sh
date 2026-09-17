#!/usr/bin/env bash
#
# Gate one course edition before it goes on air.
#
#     ./build_edition.sh iran-in-world-politics
#
# There is no build step any more, and this script no longer copies anything. The
# web tree is the product: the engine ships under Web/, and every course lives
# inside it at Web/courses/<course-id>/, so the app that gets compiled already
# carries MAIN and every course. Nothing has to be merged and nothing is written
# here -- the one thing left to do before a course is announced is prove its
# banks are fit to play.
#
# So this is the gate, in the order that fails fastest:
#
#   check_edition.py   can the banks fill a board at all -- six categories a
#                      round, every rung present, ids unique, both languages
#                      saying the same thing
#   check_bank.py      what the clues actually say -- a leak, an options[correct]
#                      pointing at the wrong option, an empty alias list, an
#                      `_a`/`_b` pair that is one question twice, Persian script
#                      in the English bank
#   check_repeats.py   one fact asked at two rungs of two categories, which
#                      check_bank.py cannot see because it checks slot by slot
#   promote_course_bank.py --check
#                      whether MAIN carries this course. MAIN absorbs a course's
#                      whole bank, so a course that was never promoted is not
#                      finished -- and a course edited after promotion has left
#                      MAIN holding a question the course no longer asks
#
# The first is a board that will not deal; the second is a board that deals
# wrong. A bank has to pass all four. See BANK_SPEC.md for the shapes.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

# The project root. Override with JEOPARDY_ENGINE if the lab is ever moved.
ENGINE="${JEOPARDY_ENGINE:-$HERE/..}"

# The argument is a course id, or a path to the course's folder. An id is the
# folder name under Web/courses/, which is also the edition id and the `?ed=`
# value -- one string in three places, and the banks are named from it.
NAME="${1:-}"

if [[ -z "$NAME" ]]; then
  echo "usage: $0 <course-id | path>" >&2
  echo "   eg: $0 iran-in-world-politics" >&2
  echo
  echo "Courses in $ENGINE/Web/courses:"
  for d in "$ENGINE"/Web/courses/*/; do
    [[ -d "$d" ]] || continue
    echo "   $(basename "$d")"
  done
  echo
  echo "(a new course starts as a copy of $HERE/course-template)"
  exit 2
fi

if [[ -d "$NAME" ]]; then
  COURSE="$(cd "$NAME" && pwd)"
else
  COURSE="$ENGINE/Web/courses/$NAME"
fi

# A typo in the id would otherwise fail inside a checker with a parse error,
# which reads like a broken bank rather than a wrong name.
if [[ ! -d "$COURSE" ]]; then
  echo "No course called '$NAME' under $ENGINE/Web/courses" >&2
  exit 1
fi

ID="$(basename "$COURSE")"
EN="$COURSE/data/bank-en.js"
FA="$COURSE/data/bank-fa.js"
JS="$COURSE/course.js"

# Bilingual is not optional. `app.js` resolves a course's bank as
# `banks[lang] || banks.en`, so a course shipping only the English bank deals
# English clues under Persian chrome -- silently, with no error anywhere.
for f in "$EN" "$FA"; do
  if [[ ! -f "$f" ]]; then
    echo "'$ID' is missing $(basename "$f")." >&2
    echo "  A course is both languages or it is not a course." >&2
    exit 1
  fi
done

python3 "$HERE/check_edition.py" "$COURSE" || exit 1

# A course bank has no archive behind it to compare against, so its content
# gate has to read the bank itself. A missing checker is a hard failure rather
# than a skip, because a gate that quietly skips itself is worse than none.
CHECK_BANK="$ENGINE/Tools/check_bank.py"
if [[ ! -f "$CHECK_BANK" ]]; then
  echo "Cannot find the content checker at $CHECK_BANK" >&2
  echo "  It is the only content gate a course bank has." >&2
  exit 1
fi

# `--edition` proves every category reaches a theme clip. It reads the mapping
# out of the course's registration, so a course that declares no theme mapping
# is not a fault -- and a course.js that is absent entirely is the same case.
THEME_ARGS=()
if [[ -f "$JS" ]]; then
  THEME_ARGS=(--edition "$JS")
fi

python3 "$CHECK_BANK" "$EN" --fa "$FA" "${THEME_ARGS[@]+"${THEME_ARGS[@]}"}" || exit 1

# The third gate, and the one the Qajars got past. `check_bank.py` catches a
# repeat *inside one slot*; nothing caught a question asked twice in two
# different categories, which is how one fact ends up on the board at two rungs
# and a contestant can be dealt the same question twice in a match. The Qajar
# bank shipped with eight such pairs in English and two in Persian because a
# one-off converter built the edition and never ran this script at all -- so the
# gate being correct was not enough, and it is now a hard failure here.
CHECK_REPEATS="$ENGINE/Tools/check_repeats.py"
if [[ ! -f "$CHECK_REPEATS" ]]; then
  echo "Cannot find the repeat checker at $CHECK_REPEATS" >&2
  exit 1
fi

for pair in "en:$EN" "fa:$FA"; do
  lang="${pair%%:*}"
  bank="${pair#*:}"
  echo
  python3 "$CHECK_REPEATS" --file "$bank" --lang "$lang" || exit 1
done

# The fourth gate, and the one that closes the loop the whole two-tier model
# rests on: MAIN absorbs a course's entire bank, so a course that has not been
# promoted is not finished. This rebuilds the rows from the course bank -- not
# from MAIN's copy of them -- and looks each one up in the archive by id. A
# course never promoted reports ABSENT on every row; one promoted and then
# edited reports DRIFT, with MAIN still serving a question the course has
# dropped. Both fail here. Neither could be seen until now: the tool crashed on
# the first row of the Iran course that carried no citation at all, so the gate
# that enforces the absorption rule had never once reached its own comparison.
CHECK_PROMOTE="$ENGINE/Tools/promote_course_bank.py"
if [[ ! -f "$CHECK_PROMOTE" ]]; then
  echo "Cannot find the promotion checker at $CHECK_PROMOTE" >&2
  echo "  MAIN absorbs a course's whole bank, and nothing else checks that it did." >&2
  exit 1
fi

echo
python3 "$CHECK_PROMOTE" "$ID" --check || exit 1

echo
echo "'$ID' is fit to play. It ships with the game -- nothing to copy, nothing to"
echo "move: build the app and the course is on the splash."
