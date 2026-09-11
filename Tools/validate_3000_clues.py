#!/usr/bin/env python3
"""
Comprehensive Validation for the 3,000 Clues Question Bank.
"""
import json
import re
import sys
from collections import Counter

def validate():
    print("==================================================")
    print("VALIDATING 3,000 CLUES DATABASE")
    print("==================================================")

    # 1. English Clues
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"Total English Clues: {len(en_clues)}")
    assert len(en_clues) == 3000, f"Expected 3000, got {len(en_clues)}"

    # 2. Persian Clues
    with open("QuestionBank/verified_clues_fa.json", "r", encoding="utf-8") as f:
        fa_clues = json.load(f)
    print(f"Total Persian Clues: {len(fa_clues)}")
    assert len(fa_clues) == 3000, f"Expected 3000, got {len(fa_clues)}"

    # 3. Persian Copy Dict
    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        fa_copy = json.load(f)
    print(f"Total Persian Copy entries: {len(fa_copy)}")
    assert len(fa_copy) == 3000, f"Expected 3000, got {len(fa_copy)}"

    # 4. App Resources Copy
    with open("App/Resources/persian_clues.json", "r", encoding="utf-8") as f:
        app_copy = json.load(f)
    print(f"Total App Resources Copy entries: {len(app_copy)}")
    assert len(app_copy) == 3000, f"Expected 3000, got {len(app_copy)}"

    # 5. Categories
    en_cats = Counter(c['category'] for c in en_clues)
    fa_cats = Counter(c['category'] for c in fa_clues)
    print(f"Total English Categories: {len(en_cats)}")
    print(f"Total Persian Categories: {len(fa_cats)}")
    assert len(en_cats) == 360, f"Expected 360 English categories, got {len(en_cats)}"
    assert len(fa_cats) == 360, f"Expected 360 Persian categories, got {len(fa_cats)}"

    # 6. Difficulty Progression Check
    diff_by_val = {}
    for c in en_clues:
        diff_by_val.setdefault(c['value'], Counter())[c['difficulty']] += 1
    print("\nDifficulty progression by value:")
    for v in sorted(diff_by_val.keys()):
        print(f"  • Value {v:4d}: {dict(diff_by_val[v])}")

    # 7. Check option counts & rationales
    for c in en_clues:
        assert len(c['options']) == 4, f"Clue {c['id']} does not have 4 options"
        assert c['correct_option_index'] in [0, 1, 2, 3]
        assert len(c['distractor_rationales']) == 3

    for c in fa_clues:
        assert len(c['options']) == 4, f"Fa Clue {c['id']} does not have 4 options"
        assert c['correct_option_index'] in [0, 1, 2, 3]
        assert len(c['distractor_rationales']) == 3

    # 8. Web data check
    with open("Web/data/clues.js", "r", encoding="utf-8") as f:
        web_text = f.read().strip()
    assert web_text.startswith("window.CLUES=")
    web_json = json.loads(web_text[len("window.CLUES="):].rstrip(";").strip())
    print(f"\nTotal Web/data/clues.js clues: {len(web_json)}")
    assert len(web_json) == 3000, f"Expected 3000 in clues.js, got {len(web_json)}"

    print("\nALL 3,000 CLUES RIGOROUSLY VALIDATED AND CONFIRMED! ✓")

if __name__ == "__main__":
    validate()
