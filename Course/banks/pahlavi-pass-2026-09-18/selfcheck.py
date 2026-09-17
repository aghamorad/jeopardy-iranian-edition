#!/usr/bin/env python3
"""Self-check one authoring batch of the Pahlavi course pass.

    python3 selfcheck.py <group>

Reads batches/<group>-en.json and batches/<group>-fa.json and reports every
rule from BRIEF.md a row can break. Exits 0 when clean, 1 otherwise.

It is a checklist, not a verdict: every complaint names the row.
"""

import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent

KEYS = [
    "id", "language", "category", "historical_period", "theme", "difficulty",
    "value", "round", "clue_text", "canonical_answer", "accepted_aliases",
    "partial_answers", "specificity_prompt", "options", "correct_option_index",
    "distractor_rationales", "explanation", "source_id", "book_title", "author",
    "chapter", "page", "supporting_passage", "evidence_type", "confidence",
    "editorial_validation_status", "host_reactions",
]

RUNG = {
    ("single", 200): ("CASUAL", "PERSIAN_BUCKETS_PLACEHOLDER"),
    ("single", 400): ("STANDARD", None),
    ("single", 600): ("STANDARD", None),
    ("single", 800): ("SCHOLAR", None),
    ("single", 1000): ("INSUFFERABLE", None),
    ("double", 400): ("STANDARD", None),
    ("double", 800): ("STANDARD", None),
    ("double", 1200): ("SCHOLAR", None),
    ("double", 1600): ("SCHOLAR", None),
    ("double", 2000): ("INSUFFERABLE", None),
    ("final", 0): ("INSUFFERABLE", None),
}
LADDER = {k: v[0] for k, v in RUNG.items()}

SINGLE_VALUES = [200, 400, 600, 800, 1000]
DOUBLE_VALUES = [400, 800, 1200, 1600, 2000]

PERSIAN_BUCKET_KEYS = [
    "trailblazer", "hero", "maestro", "instrument", "tragic", "pioneer", "figure",
    "coronation", "epistolary", "monarchy", "royal",
    "geograph", "mountain", "river", "desert", "lake", "maritime", "capital", "strait",
    "frontier", "garden", "archaeolog", "monument", "territorial", "island", "shore",
    "valley", "caspian", "gulf", "ecology", "city",
    "war", "battle", "empire", "dynast", "revolt", "rebellion", "revolution", "liberation",
    "coup", "occupation", "conquest", "siege", "barricade", "movement", "uprising",
    "conflict", "military", "combat", "aftermath", "constitution", "reform", "purge",
    "destiny", "turning point", "crime",
    "poet", "poetic", "verse", "literature", "novel", "prose", "fiction", "cinema",
    "directing", "palme", "art", "calligraph", "architecture", "music", "radif", "vocal",
    "sound", "handicraft", "cuisine", "festival", "culture", "material", "memoir",
    "linguistic", "religion", "theolog", "mystic", "philosoph", "shrine", "pilgrimage",
    "clergy", "science", "medicine", "engineering", "aviation", "mytholog", "spectacle",
    "politic", "diploma", "intelligence", "statecraft", "governance", "geopolit", "opec",
    "petroleum", "oil", "econom", "press", "education", "activism", "espionage", "spy",
    "secret societ", "coalition", "ideolog", "party", "parliament", "treasury", "commerce",
    "trade", "boycott", "sanction", "law", "legal", "capitulation", "advisor", "concession",
    "commodit", "infrastructure", "institution", "agriculture",
]

STOCK_TAILS = ["spot on!", "the history holds!", "quite right."]

STOP = set("""a an the of in on at to for and or but with by from as is was were be been
this that these those it its his her their his he she they them we you i not no nor
than then when where which who whom what whose into over under after before during
against between among about above below out off up down only also more most much many
one two three four five six seven eight nine ten first second third later early new old
same other another such very can could may might must shall should will would did does
do has have had him us""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).lower()
    return "".join(c for c in s if c.isalnum() or c.isspace())


def words(s):
    return [w for w in norm(s).split() if w and w not in STOP and len(w) > 2]


def longest_common(a, b):
    """Length of the longest shared substring of two normalised strings."""
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def related(alias, answer):
    """True if an alias plausibly names the same thing as its answer.

    A shared run of four characters catches spelling variants and partial names
    ("Bakhtiari"/"Bakhtiyari", "General Ironside"/"General Edmund Ironside"); a
    shared four-character word stem catches transliteration drift
    ("Divizion"/"Division", "Modarres"/"Mudarris"). It is deliberately loose —
    it is a prompt to look, not a proof.
    """
    if alias in answer or answer in alias:
        return True
    if longest_common(alias, answer) >= 4:
        return True
    for wa in alias.split():
        for wb in answer.split():
            n = 0
            for ca, cb in zip(wa, wb):
                if ca != cb:
                    break
                n += 1
            if n >= 4:
                return True
    return False


def similar(a, b):
    wa, wb = set(words(a)), set(words(b))
    if not wa or not wb:
        return False
    shared = wa & wb
    if len(shared) < 6:
        return False
    shorter, longer = (a, b) if len(wa) <= len(wb) else (b, a)
    sw = words(shorter)
    lw = set(words(longer))
    if not sw:
        return False
    return sum(1 for w in sw if w in lw) / len(sw) >= 0.75


def load(path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def main():
    if len(sys.argv) != 2:
        print("usage: selfcheck.py <group>")
        return 2
    group = sys.argv[1]
    en = load(HERE / "batches" / f"{group}-en.json")
    fa = load(HERE / "batches" / f"{group}-fa.json")
    problems = []
    warnings = []

    for lang, rows in (("en", en), ("fa", fa)):
        if rows is None:
            problems.append(f"[{lang}] file missing")
        elif not isinstance(rows, list) or not rows:
            problems.append(f"[{lang}] not a non-empty JSON array")

    if problems:
        for p in problems:
            print("FAIL", p)
        return 1

    def tag(lang, i, r):
        return f"[{lang} #{i}] {r.get('id', '?')}"

    for lang, rows in (("en", en), ("fa", fa)):
        seen_ids = {}
        for i, r in enumerate(rows):
            t = tag(lang, i, r)
            missing = [k for k in KEYS if k not in r]
            extra = [k for k in r if k not in KEYS]
            if missing:
                problems.append(f"{t} missing keys: {missing}")
            if extra:
                problems.append(f"{t} unexpected keys: {extra}")
            rid = r.get("id")
            if rid in seen_ids:
                problems.append(f"{t} duplicate id (also #{seen_ids[rid]})")
            seen_ids[rid] = i

            if r.get("language") != lang:
                problems.append(f"{t} language is {r.get('language')!r}, expected {lang!r}")
            if r.get("historical_period") != "Pahlavi":
                problems.append(f"{t} historical_period is {r.get('historical_period')!r}")
            if not str(r.get("category", "")).strip():
                problems.append(f"{t} empty category")
            elif r["category"] != r["category"].strip():
                problems.append(f"{t} category has leading/trailing space")

            theme = str(r.get("theme", ""))
            if theme != theme.lower():
                problems.append(f"{t} theme {theme!r} is not lowercase")
            if theme and not any(k in theme for k in PERSIAN_BUCKET_KEYS):
                problems.append(f"{t} theme {theme!r} matches no Persian bucket")

            key = (r.get("round"), r.get("value"))
            want = LADDER.get(key)
            if want is None:
                problems.append(f"{t} illegal (round, value) = {key}")
            elif r.get("difficulty") != want:
                problems.append(
                    f"{t} difficulty {r.get('difficulty')!r} for {key} "
                    f"should be {want!r}")

            ans = str(r.get("canonical_answer", "")).strip()
            clue = str(r.get("clue_text", "")).strip()
            if not clue:
                problems.append(f"{t} empty clue_text")
            if not ans:
                problems.append(f"{t} empty canonical_answer")
            elif norm(ans) and norm(ans) in norm(clue):
                problems.append(f"{t} answer {ans!r} appears in its own clue")

            opts = r.get("options")
            if not isinstance(opts, list) or len(opts) != 4:
                problems.append(f"{t} options is not a list of 4")
            else:
                if len({norm(o) for o in opts}) != 4:
                    problems.append(f"{t} options are not 4 unique entries")
                if norm(opts[0]) != norm(ans):
                    problems.append(f"{t} options[0] {opts[0]!r} != answer {ans!r}")
                if r.get("correct_option_index") != 0:
                    problems.append(f"{t} correct_option_index is "
                                    f"{r.get('correct_option_index')!r}, must be 0")

                dr = r.get("distractor_rationales")
                if not isinstance(dr, list) or len(dr) != 3:
                    problems.append(f"{t} distractor_rationales is not a list of 3")
                else:
                    wrongs = [norm(o) for o in opts[1:]]
                    for j, d in enumerate(dr):
                        if not isinstance(d, dict):
                            problems.append(f"{t} rationale {j} is not an object")
                            continue
                        if set(d) != {"option", "why_plausible", "why_wrong"}:
                            problems.append(f"{t} rationale {j} keys are {sorted(d)}")
                        elif norm(d["option"]) != wrongs[j]:
                            problems.append(
                                f"{t} rationale {j} names {d['option']!r}, "
                                f"but wrong option {j} is {opts[j + 1]!r}")
                        for f in ("why_plausible", "why_wrong"):
                            if not str(d.get(f, "")).strip():
                                problems.append(f"{t} rationale {j} empty {f}")

            al = r.get("accepted_aliases")
            if not isinstance(al, list) or not al:
                problems.append(f"{t} accepted_aliases is empty")
            else:
                na = norm(ans)
                for a in al:
                    if not norm(a):
                        problems.append(f"{t} blank alias")
                    elif na and not related(norm(a), na):
                        warnings.append(f"{t} alias {a!r} shares no word or stem "
                                        f"with {ans!r} — check it names the same thing")
                if norm(al[0]) != na:
                    problems.append(f"{t} accepted_aliases does not lead with the answer")

            if not str(r.get("explanation", "")).strip():
                problems.append(f"{t} empty explanation")
            if not str(r.get("supporting_passage", "")).strip():
                problems.append(f"{t} empty supporting_passage")
            for k in ("book_title", "author", "chapter", "source_id"):
                if not str(r.get(k, "")).strip():
                    problems.append(f"{t} empty {k}")
            if r.get("round") == "final":
                if r.get("page") is not None:
                    problems.append(f"{t} final carries a page ({r.get('page')!r})")
            else:
                if not isinstance(r.get("page"), int):
                    problems.append(f"{t} page is {r.get('page')!r}, expected an int")

            hr = r.get("host_reactions")
            if not isinstance(hr, dict):
                problems.append(f"{t} host_reactions is not an object")
            else:
                if set(hr) != {"correct_generic", "wrong_generic",
                               "common_wrong_answers", "specificity_prompt",
                               "explanation"}:
                    problems.append(f"{t} host_reactions keys are {sorted(hr)}")
                for k in ("correct_generic", "wrong_generic"):
                    line = str(hr.get(k, "")).strip()
                    if not line:
                        problems.append(f"{t} empty host_reactions.{k}")
                    low = line.lower()
                    for tail in STOCK_TAILS:
                        if low.endswith(tail):
                            problems.append(f"{t} {k} ends in stock tail {tail!r}")
                if hr.get("explanation") != r.get("explanation"):
                    problems.append(f"{t} host_reactions.explanation != explanation")

    # category integrity, per language independently
    for lang, rows in (("en", en), ("fa", fa)):
        cats = {}
        for r in rows:
            cats.setdefault(r.get("category"), []).append(r)
        for cat, rs in cats.items():
            rounds = {r.get("round") for r in rs}
            if rs[0].get("round") == "final":
                if len(rs) != 1:
                    problems.append(f"[{lang}] final category {cat!r} has {len(rs)} rows")
                continue
            if len(rounds) != 1:
                problems.append(f"[{lang}] category {cat!r} mixes rounds {sorted(rounds)}")
                continue
            rnd = rounds.pop()
            want_vals = SINGLE_VALUES if rnd == "single" else DOUBLE_VALUES
            got = sorted(r.get("value") for r in rs)
            if got != want_vals:
                problems.append(
                    f"[{lang}] category {cat!r} ({rnd}) has rungs {got}, "
                    f"needs {want_vals}")

    # en/fa category pairing: same partition of ids, different titles
    en_row_cat = {r.get("id"): r.get("category") for r in en}
    fa_row_cat = {r.get("id"): r.get("category") for r in fa}
    en_groups, fa_groups = {}, {}
    for rid, cat in en_row_cat.items():
        en_groups.setdefault(cat, set()).add(rid)
    for rid, cat in fa_row_cat.items():
        fa_groups.setdefault(cat, set()).add(rid)
    if {frozenset(v) for v in en_groups.values()} != {frozenset(v) for v in fa_groups.values()}:
        problems.append(
            f"en and fa disagree on which rows share a category: "
            f"en has {len(en_groups)} categories, fa has {len(fa_groups)}")

    # id mirroring between languages
    en_ids = [r.get("id") for r in en]
    fa_ids = [r.get("id") for r in fa]
    if en_ids != fa_ids:
        if set(en_ids) != set(fa_ids):
            problems.append(f"id sets differ: en-only {sorted(set(en_ids) - set(fa_ids))}, "
                            f"fa-only {sorted(set(fa_ids) - set(en_ids))}")
        else:
            problems.append("ids are the same set but not in the same order")

    # repeats inside the batch, both languages
    for lang, rows in (("en", en), ("fa", fa)):
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                if a.get("round") == "final" or b.get("round") == "final":
                    pass
                if similar(str(a.get("clue_text", "")), str(b.get("clue_text", ""))):
                    problems.append(
                        f"[{lang}] repeated question: {a.get('id')} and {b.get('id')}")

    for w in warnings[:40]:
        print("WARN", w)
    if len(warnings) > 40:
        print(f"WARN ... and {len(warnings) - 40} more alias warnings")

    if problems:
        for p in problems:
            print("FAIL", p)
        print(f"\n{len(problems)} problem(s) in batch {group!r}.")
        return 1

    print(f"OK batch {group!r}: {len(en)} en rows, {len(fa)} fa rows, "
          f"{len({r['category'] for r in en})} categories, "
          f"{len(warnings)} alias warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
