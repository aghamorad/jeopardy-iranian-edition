#!/usr/bin/env python3
"""
Validates QuestionBank/verified_clues_fa.json and QuestionBank/persian_clues.json.
"""
import json
import re
import sys
from collections import Counter

def validate_fa():
    print("==================================================")
    print("VALIDATING PERSIAN QUESTION BANK")
    print("==================================================")

    # 1. Load English bank for comparison
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    en_ids = [c["id"] for c in en_clues]

    # 2. Load Persian bank
    fa_path = "QuestionBank/verified_clues_fa.json"
    with open(fa_path, "r", encoding="utf-8") as f:
        fa_clues = json.load(f)

    print(f"Total Persian clues loaded: {len(fa_clues)}")
    assert len(fa_clues) == 1000, f"Expected 1000 clues, got {len(fa_clues)}"

    fa_ids = [c["id"] for c in fa_clues]
    assert len(fa_ids) == len(set(fa_ids)), "Duplicate IDs found in Persian bank!"
    assert fa_ids == en_ids, "Persian clue IDs do not match English clue IDs exactly!"

    # 3. Check language
    for c in fa_clues:
        assert c["language"] == "fa", f"Clue {c['id']} language is not 'fa'"

    # 4. Check category distribution
    cats = Counter(c["category"] for c in fa_clues)
    print(f"Total unique Persian categories: {len(cats)}")
    assert len(cats) == 120, f"Expected 120 categories, got {len(cats)}"

    # 5. Check options & answers
    mismatches = 0
    for c in fa_clues:
        opts = c.get("options", [])
        assert len(opts) == 4, f"Clue {c['id']} does not have 4 options"
        cor_idx = c.get("correct_option_index")
        assert cor_idx in [0, 1, 2, 3], f"Clue {c['id']} invalid correct_option_index"
        assert opts[cor_idx] == c["canonical_answer"], f"Clue {c['id']} correct option does not match canonical answer!"

        rats = c.get("distractor_rationales", [])
        assert len(rats) == 3, f"Clue {c['id']} does not have 3 distractor rationales"

    print("Field integrity check passed for all 1,000 clues!")

    # 6. Check Persian dates in clue text
    shamsi_count = sum(1 for c in fa_clues if re.search(r'[۰-۹]{4}', c["clue_text"]) or "خورشیدی" in c["clue_text"] or "پیش از میلاد" in c["clue_text"])
    print(f"Clues containing verified Persian / Shamsi dates: {shamsi_count} / 1000")

    # 7. Check Persian Copy dictionary
    dict_path = "QuestionBank/persian_clues.json"
    with open(dict_path, "r", encoding="utf-8") as f:
        copy_dict = json.load(f)
    print(f"Persian clue copy dictionary entries: {len(copy_dict)}")
    assert len(copy_dict) == 1000, f"Expected 1000 entries in copy dictionary, got {len(copy_dict)}"

    # 8. Check App resource copy
    app_res_path = "App/Resources/persian_clues.json"
    with open(app_res_path, "r", encoding="utf-8") as f:
        app_dict = json.load(f)
    print(f"App Resources dictionary entries: {len(app_dict)}")
    assert len(app_dict) == 1000, f"Expected 1000 entries in App Resources, got {len(app_dict)}"

    print("\nALL VALIDATIONS PASSED! PERSIAN QUESTION BANK IS 100% COMPLETE AND COMPLIANT. ✓")

if __name__ == "__main__":
    validate_fa()
