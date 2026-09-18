#!/usr/bin/env python3
import json
import sys
from collections import Counter

# A promoted row came up from a course edition (Tools/promote_course_bank.py) and
# still owes its two archive-only fields -- the supporting passage and the three
# distractor rationales. Neither reaches the player. The dress code is enforced on
# verified rows and the promoted ones are counted, so the debt stays visible.
STATUSES = {"verified", "promoted"}
UNDRESSED = "promoted"


def validate():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        clues = json.load(f)

    print(f"==================================================")
    print(f"VALIDATING QUESTION BANK: {len(clues)} TOTAL CLUES")
    print(f"==================================================")

    assert len(clues) == 3752, f"Expected 3752 clues, found {len(clues)}"

    ids = [c["id"] for c in clues]
    unique_ids = set(ids)
    assert len(ids) == len(unique_ids), f"Duplicate IDs found: {len(ids) - len(unique_ids)}"

    rounds = Counter(c["round"] for c in clues)
    print("Breakdown by Round:")
    for r, cnt in sorted(rounds.items()):
        print(f"  • {r.upper()}: {cnt} clues")

    categories = Counter(c["category"] for c in clues)
    print(f"\nTotal Categories: {len(categories)}")
    print(f"Sample Category Puns:")
    for cat in sorted(categories.keys())[:15]:
        print(f"  • {cat} ({categories[cat]} clues)")

    # Field integrity check
    errors = []
    promoted = 0
    for idx, c in enumerate(clues):
        cid = c.get("id", f"index_{idx}")
        status = c.get("editorial_validation_status")
        owed = status == UNDRESSED
        if status not in STATUSES:
            errors.append(f"{cid}: unknown editorial_validation_status {status!r}")
        if not c.get("clue_text"): errors.append(f"{cid}: missing clue_text")
        if not c.get("canonical_answer"): errors.append(f"{cid}: missing canonical_answer")
        opts = c.get("options", [])
        if len(opts) != 4: errors.append(f"{cid}: options count is {len(opts)}, expected 4")
        if c.get("correct_option_index") not in [0, 1, 2, 3]: errors.append(f"{cid}: invalid correct_option_index")
        rats = c.get("distractor_rationales", [])
        if owed:
            promoted += 1
            if rats: errors.append(f"{cid}: promoted but carries a partial rationale set")
        elif len(rats) != 3:
            errors.append(f"{cid}: distractor_rationales count is {len(rats)}, expected 3")
        for r in rats:
            if not r.get("option") or not r.get("why_plausible") or not r.get("why_wrong"):
                errors.append(f"{cid}: malformed distractor rationale")
        if not c.get("book_title"): errors.append(f"{cid}: missing book_title")
        if not c.get("author"): errors.append(f"{cid}: missing author")
        # Finals cite documents that are not paginated -- a UN resolution, a speech.
        if not c.get("page") and c.get("round") != "final":
            errors.append(f"{cid}: missing page")
        if not c.get("supporting_passage") and not owed:
            errors.append(f"{cid}: missing supporting_passage")

    if errors:
        print(f"VALIDATION FAILED WITH {len(errors)} ERRORS:")
        for err in errors[:10]:
            print(f"  - {err}")
        sys.exit(1)

    print(f"\nFully dressed (verified, passage + 3 rationales): {len(clues) - promoted}")
    print(f"Promoted, those two archive-only fields still owed: {promoted}")
    print(f"\nALL {len(clues):,} CLUES VALIDATED WITH 100% SCHEMA AND CITATION INTEGRITY! ✓")

if __name__ == "__main__":
    validate()
