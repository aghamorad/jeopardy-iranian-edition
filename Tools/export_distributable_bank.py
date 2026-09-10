#!/usr/bin/env python3
"""
Separates Private Editorial Archival Material from Public Distributable Game Clues.
Generates:
    QuestionBank/distributable_clues.json (Safe for shipping: citations preserved, long copyrighted verbatim text removed)
"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT, "QuestionBank", "verified_clues.json")
DST_PATH = os.path.join(ROOT, "QuestionBank", "distributable_clues.json")

def export_distributable():
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        clues = json.load(f)

    distributable_clues = []
    for c in clues:
        dist_clue = {
            "id": c["id"],
            "language": c["language"],
            "category": c["category"],
            "historical_period": c["historical_period"],
            "theme": c["theme"],
            "difficulty": c["difficulty"],
            "value": c["value"],
            "round": c["round"],
            "clue_text": c["clue_text"],
            "canonical_answer": c["canonical_answer"],
            "accepted_aliases": c["accepted_aliases"],
            "partial_answers": c.get("partial_answers", []),
            "specificity_prompt": c.get("specificity_prompt"),
            "options": c["options"],
            "correct_option_index": c["correct_option_index"],
            "distractor_rationales": c["distractor_rationales"],
            "explanation": c["explanation"],
            # Short citation reference only — no copyrighted book paragraphs
            "citation": f"{c['author']}, {c['book_title']} ({c['chapter']}, p. {c['page']})",
            "evidence_type": c["evidence_type"],
            "host_reactions": c["host_reactions"]
        }
        distributable_clues.append(dist_clue)

    with open(DST_PATH, "w", encoding="utf-8") as f:
        json.dump(distributable_clues, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(distributable_clues)} distributable clues to {DST_PATH}")
    print("Zero copyrighted verbatim source paragraphs included.")

if __name__ == "__main__":
    export_distributable()
