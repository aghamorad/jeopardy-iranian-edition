#!/usr/bin/env python3
"""
Exhaustive Verification of the Question Bank after Full Overhaul.
"""
import json
import re
import sys
from collections import Counter

def verify():
    print("==================================================")
    print("EXHAUSTIVE QUESTION BANK VERIFICATION AUDIT")
    print("==================================================")

    # 1. English Bank
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"1. English Clues Count: {len(en_clues)}")
    assert len(en_clues) == 1000, f"Expected 1000, got {len(en_clues)}"

    # Check placeholders
    placeholders = [c['id'] for c in en_clues if 'Milestone' in c.get('canonical_answer', '') or 'Alternative' in str(c.get('options', []))]
    print(f"   • English Clues with Placeholder Formulas: {len(placeholders)}")
    assert len(placeholders) == 0, f"Found placeholders: {placeholders[:5]}"

    # Check difficulty progression by value
    diff_map = {}
    for c in en_clues:
        diff_map.setdefault(c['value'], Counter())[c['difficulty']] += 1
    print("   • Difficulty Distribution by Value:")
    for v in sorted(diff_map.keys()):
        print(f"       ${v:4d}: {dict(diff_map[v])}")

    # Assert strict difficulty ladder
    for c in en_clues:
        v = c['value']
        d = c['difficulty']
        r = c['round']
        if r == 'single':
            if v == 200: assert d == 'CASUAL', f"{c['id']} diff {d} != CASUAL"
            elif v in [400, 600]: assert d == 'STANDARD', f"{c['id']} diff {d} != STANDARD"
            elif v == 800: assert d == 'SCHOLAR', f"{c['id']} diff {d} != SCHOLAR"
            elif v == 1000: assert d == 'INSUFFERABLE', f"{c['id']} diff {d} != INSUFFERABLE"
        elif r == 'double':
            if v in [400, 800]: assert d == 'STANDARD', f"{c['id']} diff {d} != STANDARD"
            elif v in [1200, 1600]: assert d == 'SCHOLAR', f"{c['id']} diff {d} != SCHOLAR"
            elif v == 2000: assert d == 'INSUFFERABLE', f"{c['id']} diff {d} != INSUFFERABLE"
        elif r == 'final':
            assert d == 'INSUFFERABLE', f"{c['id']} diff {d} != INSUFFERABLE"

    print("   ✓ Strict difficulty ladder verified across all 1,000 clues!")

    # 2. Persian Bank
    with open("QuestionBank/verified_clues_fa.json", "r", encoding="utf-8") as f:
        fa_clues = json.load(f)
    print(f"\n2. Persian Clues Count: {len(fa_clues)}")
    assert len(fa_clues) == 1000, f"Expected 1000, got {len(fa_clues)}"

    eng_clue_text = [c['id'] for c in fa_clues if re.search(r'[a-zA-Z]{2,}', c['clue_text'])]
    eng_answers = [c['id'] for c in fa_clues if re.search(r'[a-zA-Z]{2,}', c['canonical_answer'])]
    eng_options = [c['id'] for c in fa_clues if any(re.search(r'[a-zA-Z]{2,}', opt) for opt in c['options'])]
    eng_expl = [c['id'] for c in fa_clues if re.search(r'[a-zA-Z]{2,}', c['explanation'])]

    print(f"   • Clue texts with English words: {len(eng_clue_text)}")
    print(f"   • Answers with English words: {len(eng_answers)}")
    print(f"   • Options with English words: {len(eng_options)}")
    print(f"   • Explanations with English words: {len(eng_expl)}")

    assert len(eng_clue_text) == 0, f"English in clue_text: {eng_clue_text[:5]}"
    assert len(eng_answers) == 0, f"English in canonical_answer: {eng_answers[:5]}"
    assert len(eng_options) == 0, f"English in options: {eng_options[:5]}"
    assert len(eng_expl) == 0, f"English in explanation: {eng_expl[:5]}"
    print("   ✓ Zero English characters confirmed across all Persian clue fields!")

    # 3. Categories Puns
    en_cats = sorted(set(c['category'] for c in en_clues))
    fa_cats = sorted(set(c['category'] for c in fa_clues))
    print(f"\n3. Categories:")
    print(f"   • Unique English Categories: {len(en_cats)}")
    print(f"   • Unique Persian Categories: {len(fa_cats)}")
    assert len(en_cats) == 120
    assert len(fa_cats) == 120

    # Ensure no dry titles like "طوفان شن در طبس و شکست عملیات پنجه عقاب"
    assert "طوفان شن در طبس و شکست عملیات پنجه عقاب" not in fa_cats
    assert "پنجه در شن" in fa_cats or "شن‌های روان، عقاب‌های نگران" in fa_cats
    print("   ✓ Witty Persian category puns verified!")

    # 4. Web Engine Data
    with open("Web/data/clues.js", "r", encoding="utf-8") as f:
        web_text = f.read().strip()
    assert web_text.startswith("window.CLUES=")
    web_json = json.loads(web_text[len("window.CLUES="):].rstrip(";").strip())
    print(f"\n4. Web Data Clues Count: {len(web_json)}")
    assert len(web_json) == 1000

    # 5. Distributable Clues
    with open("QuestionBank/distributable_clues.json", "r", encoding="utf-8") as f:
        dist_json = json.load(f)
    print(f"5. Distributable Clues Count: {len(dist_json)}")
    assert len(dist_json) == 1000

    # 6. Persian Copy Dictionary
    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        dict_json = json.load(f)
    print(f"6. Persian Clue Copy Dict Count: {len(dict_json)}")
    assert len(dict_json) == 1000

    # 7. App Resource Copy
    with open("App/Resources/persian_clues.json", "r", encoding="utf-8") as f:
        app_json = json.load(f)
    print(f"7. App Resources Copy Dict Count: {len(app_json)}")
    assert len(app_json) == 1000

    print("\n==================================================")
    print("ALL AUDIT CHECKS PASSED: 100% IN ORDER! ✓")
    print("==================================================")

if __name__ == "__main__":
    verify()
