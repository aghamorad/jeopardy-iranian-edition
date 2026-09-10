#!/usr/bin/env python3
import json
import os

def load_bank():
    with open("QuestionBank/verified_clues.json", "r", encoding="utf-8") as f:
        return {c["id"]: c for c in json.load(f)}

def save_bank(clues_dict):
    clues = list(clues_dict.values())
    print(f"Total clues: {len(clues)}")
    rounds = {}
    cats = set()
    for c in clues:
        rounds[c["round"]] = rounds.get(c["round"], 0) + 1
        cats.add(c["category"])
    print(f"Rounds breakdown: {rounds}")
    print(f"Total categories: {len(cats)}")
    with open("QuestionBank/verified_clues.json", "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2, ensure_ascii=False)
    print("QuestionBank/verified_clues.json written successfully.")

def make_clue(id_str, cat, period, theme, val, round_str, text, ans, aliases, options, correct_idx, rationales, expl, src, book, auth, ch, pg, passage):
    return {
        "id": id_str, "language": "en", "category": cat, "historical_period": period,
        "theme": theme, "difficulty": "STANDARD", "value": val, "round": round_str,
        "clue_text": text, "canonical_answer": ans, "accepted_aliases": aliases,
        "partial_answers": [], "specificity_prompt": "",
        "options": options, "correct_option_index": correct_idx,
        "distractor_rationales": rationales, "explanation": expl,
        "source_id": src, "book_title": book, "author": auth, "chapter": ch, "page": pg,
        "supporting_passage": passage, "evidence_type": "established_fact", "confidence": 1.0,
        "editorial_validation_status": "verified",
        "host_reactions": {
            "correct_generic": f"{ans}. Quite right.",
            "wrong_generic": f"No, we were looking for {ans}.",
            "common_wrong_answers": {}, "specificity_prompt": "", "explanation": expl
        }
    }

# Execute batch additions
clues = load_bank()

# We will define a helper to add 5 clues for a category
def add_cat_5(cat, period, theme, round_str, items):
    vals = [200, 400, 600, 800, 1000] if round_str == "single" else [400, 800, 1200, 1600, 2000]
    for i, item in enumerate(items):
        cid = f"{round_str}_{cat.lower().replace(' ', '_').replace(':', '').replace('&', 'and')}_{vals[i]}"
        c = make_clue(
            cid, cat, period, theme, vals[i], round_str,
            item["text"], item["ans"], item["aliases"],
            item["options"], 0, item["rationales"],
            item["expl"], item["src"], item["book"], item["auth"], item["ch"], item["pg"], item["passage"]
        )
        clues[cid] = c

print("Loaded initial bank:", len(clues))
