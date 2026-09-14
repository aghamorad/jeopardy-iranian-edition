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
#
# The first is a board that will not deal; the second is a board that deals
# wrong. A bank has to pass both. See BANK_SPEC.md for the shapes.

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

# The content checker is the only gate a course bank has: unlike MAIN's, there
# is no archive behind it to compare against. A missing checker is a hard
# failure rather than a skip, because a gate that quietly skips itself is worse
# than none.
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

echo
echo "'$ID' is fit to play. It ships with the game -- nothing to copy, nothing to"
echo "move: build the app and the course is on the splash."
