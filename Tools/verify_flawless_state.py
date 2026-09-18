#!/usr/bin/env python3
"""
Exhaustive Verification of the Question Bank after Full Overhaul.
"""
import json
import re
import sys
from collections import Counter

# A maximal run of Latin letters, hyphens and dots -- one name, not one letter.
LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z'’&.\-]*(?:\s+[A-Za-z][A-Za-z'’&.\-]*)*")

# Every Latin run the Persian bank is known to carry, reviewed one by one.
# Acronyms, official English names, romanized institutions, one citation, and the
# Avestan terms. A new run here means someone read it -- see the check in verify().
LATIN_OK = {
    # acronyms and designations
    "AIOC", "APOC", "IPC", "ISSIGID", "NIOC", "NSFNET", "PCP", "SUN", "TERENA",
    "Y", "iatc",
    # official names, kept in parentheses beside their Persian rendering
    "Council of Islamic Union", "Girls' Scouts", "Home Management", "Net Nanny",
    "OpenDNS", "Organization for the Cultivation of Thought", "Secure Computing",
    "SmartFilter", "Websense",
    # romanized institutions, a citation, and the Avestan
    "Edareh-ye Monkarat", "Howzeh-ye Andisheh va Honar-e Eslami", "Jacqz",
    "airyanem vaejah", "ariya", "editormyself.com",
}

def verify():
    print("==================================================")
    print("EXHAUSTIVE QUESTION BANK VERIFICATION AUDIT")
    print("==================================================")

    # 1. English Bank
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        en_clues = json.load(f)
    print(f"1. English Clues Count: {len(en_clues)}")
    assert len(en_clues) == 3752, f"Expected 3752, got {len(en_clues)}"

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

    print(f"   ✓ Strict difficulty ladder verified across all {len(en_clues):,} clues!")

    # 2. Persian Bank
    with open("QuestionBank/verified_clues_fa.json", "r", encoding="utf-8") as f:
        fa_clues = json.load(f)
    print(f"\n2. Persian Clues Count: {len(fa_clues)}")
    assert len(fa_clues) == 3752, f"Expected 3752, got {len(fa_clues)}"

    # Latin script is not foreign matter in the Persian bank. Acronyms, official
    # English names, romanized institutions and the Avestan terms all sit in Latin,
    # in parentheses or guillemets, beside their Persian rendering. So the invariant
    # is not "no Latin" but "no *unreviewed* Latin" -- a word that slipped through
    # untranslated, or a Latin letter dropped into a Persian word. The rule this
    # replaced -- any run of two or more Latin letters fails -- could not tell those
    # apart: it failed on twenty-five names the bank is right to keep while saying
    # nothing about ژنrال, a Latin r inside the rank "general". Hence a baseline.
    #
    # Aliases are exempt and stay exempt: a Persian row's aliases are its answer's
    # transliterations, Latin by construction.
    unreviewed = []
    for c in fa_clues:
        for field in ("clue_text", "canonical_answer", "explanation", "options"):
            value = c.get(field)
            for s in (value if isinstance(value, list) else [value]):
                for run in LATIN_RUN.findall(s or ""):
                    if run not in LATIN_OK:
                        unreviewed.append((c["id"], field, run))

    print(f"   • Latin runs, reviewed: {len(LATIN_OK)}; unreviewed: {len(unreviewed)}")
    for cid, field, run in unreviewed[:20]:
        print(f"       {cid}  {field}: {run}")
    assert not unreviewed, (
        "%d Latin run(s) in the Persian bank that nobody has read. Each one is "
        "either untranslated English or a Latin letter dropped into a Persian "
        "word, and for either of those the fix is the text -- or it is a name the "
        "bank is right to keep, and then it belongs in LATIN_OK."
        % len(unreviewed))
    print("   ✓ Every Latin run in the Persian bank has been read and allowed.")

    # 3. Categories Puns
    en_cats = sorted(set(c['category'] for c in en_clues))
    fa_cats = sorted(set(c['category'] for c in fa_clues))
    print(f"\n3. Categories:")
    print(f"   • Unique English Categories: {len(en_cats)}")
    print(f"   • Unique Persian Categories: {len(fa_cats)}")
    assert len(en_cats) == 707
    assert len(fa_cats) == 708

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
    assert len(web_json) == 3752

    # 5. Distributable Clues -- a separate release artifact, and a pre-cleanup
    # snapshot: its passages are synthetic notes, not the archive's quotes. It is
    # deliberately NOT regenerated by the promotion, so the invariant that matters
    # is that it names nothing MAIN does not have. See C3PO_LOG for the open call
    # on bringing it back in step.
    with open("QuestionBank/distributable_clues.json", "r", encoding="utf-8") as f:
        dist_json = json.load(f)
    dist_ids = set(c["id"] for c in dist_json)
    arch_ids = set(c["id"] for c in en_clues)
    print(f"5. Distributable Clues Count: {len(dist_json)} "
          f"(MAIN carries {len(en_clues)}; {len(arch_ids - dist_ids)} not yet in it)")
    assert dist_ids <= arch_ids, \
        f"distributable names ids MAIN lacks: {sorted(dist_ids - arch_ids)[:5]}"

    # 6. Persian Copy Dictionary
    with open("QuestionBank/persian_clues.json", "r", encoding="utf-8") as f:
        dict_json = json.load(f)
    print(f"6. Persian Clue Copy Dict Count: {len(dict_json)}")
    assert len(dict_json) == 3752

    # 7. App Resource Copy
    with open("App/Resources/persian_clues.json", "r", encoding="utf-8") as f:
        app_json = json.load(f)
    print(f"7. App Resources Copy Dict Count: {len(app_json)}")
    assert len(app_json) == 3752

    print("\n==================================================")
    print("ALL AUDIT CHECKS PASSED: 100% IN ORDER! ✓")
    print("==================================================")

if __name__ == "__main__":
    verify()
