#!/usr/bin/env python3
"""
IR4595 Dual-Language Iranian Jeopardy Pipeline
Automates syllabus extraction, schema validation, and question bank compilation.
"""

import os
import sys
import json
import re
import fcntl
import time
from pathlib import Path

READINGS_DIR = Path("/Users/Morad/Desktop/IR4595 Iran in World Politics-Readings")
OUTPUT_FILE = Path("/Users/Morad/Spark/iranian_jeopardy_bank.json")

def validate_clue_schema(clue):
    """Validates a single clue object against the game engine schema."""
    req_fields = [
        "id", "round", "value", "difficulty", "category", "clue_text",
        "canonical_answer", "accepted_aliases", "options", "correct_option_index",
        "distractor_rationales", "adversarial_confusion_set", "specificity_prompt",
        "host_reactions", "explanation", "provenance"
    ]
    for rf in req_fields:
        if rf not in clue:
            raise ValueError(f"Missing required field: {rf}")

    # Check slot keys & difficulty mapping
    round_val = clue["round"]
    val = clue["value"]
    diff = clue["difficulty"]
    if round_val == "single":
        if val not in [200, 400, 600, 800, 1000]:
            raise ValueError(f"Invalid single round value: {val}")
        mapping = {200: "CASUAL", 400: "STANDARD", 600: "STANDARD", 800: "SCHOLAR", 1000: "INSUFFERABLE"}
        if diff != mapping[val]:
            raise ValueError(f"Slot {val} mapped to {diff}, expected {mapping[val]}")
    elif round_val == "double":
        if val not in [400, 800, 1200, 1600, 2000]:
            raise ValueError(f"Invalid double round value: {val}")
        mapping = {400: "STANDARD", 800: "STANDARD", 1200: "SCHOLAR", 1600: "SCHOLAR", 2000: "INSUFFERABLE"}
        if diff != mapping[val]:
            raise ValueError(f"Slot {val} mapped to {diff}, expected {mapping[val]}")

    # Ensure zero Latin characters in Persian fields
    def check_fa(val, name):
        if isinstance(val, str):
            latin = re.findall(r'[a-zA-Z]', val)
            if latin:
                raise ValueError(f"Latin characters found in {name}: {latin}")
            if re.search(r'\s[،.؟!]', val):
                raise ValueError(f"Space before punctuation in {name}")
            if re.search(r'\s-\s', val):
                raise ValueError(f"Bare hanging dash in {name}")
        elif isinstance(val, list):
            for i, item in enumerate(val):
                check_fa(item, f"{name}[{i}]")
        elif isinstance(val, dict):
            for k, item in val.items():
                if name.endswith("common_wrong_answers"):
                    check_fa(k, f"{name}.key_{k}")
                check_fa(item, f"{name}.{k}")

    check_fa(clue["category"]["fa"], "category.fa")
    check_fa(clue["clue_text"]["fa"], "clue_text.fa")
    check_fa(clue["canonical_answer"]["fa"], "canonical_answer.fa")
    check_fa(clue["accepted_aliases"]["fa"], "accepted_aliases.fa")
    check_fa(clue["options"]["fa"], "options.fa")
    check_fa(clue["adversarial_confusion_set"]["fa"], "adversarial_confusion_set.fa")
    check_fa(clue["specificity_prompt"]["fa"], "specificity_prompt.fa")
    check_fa(clue["host_reactions"]["fa"]["correct_generic"], "host_reactions.fa.correct_generic")
    check_fa(clue["host_reactions"]["fa"]["wrong_generic"], "host_reactions.fa.wrong_generic")
    check_fa(clue["host_reactions"]["fa"]["common_wrong_answers"], "host_reactions.fa.common_wrong_answers")
    check_fa(clue["explanation"]["fa"], "explanation.fa")

    # Options count and index
    if len(clue["options"]["en"]) != 4 or len(clue["options"]["fa"]) != 4:
        raise ValueError("Options must have exactly 4 items")
    c_idx = clue["correct_option_index"]
    if clue["options"]["en"][c_idx] != clue["canonical_answer"]["en"]:
        raise ValueError("EN options[correct_option_index] mismatch with canonical_answer")
    if clue["options"]["fa"][c_idx] != clue["canonical_answer"]["fa"]:
        raise ValueError("FA options[correct_option_index] mismatch with canonical_answer")

    return True

def append_validated_clues(new_clues):
    """Appends new clues to the bank after verifying schema with file locking."""
    for c in new_clues:
        validate_clue_schema(c)

    lock_file_path = OUTPUT_FILE.with_suffix(".lock")
    with open(lock_file_path, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            if OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0:
                with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = []

            existing_ids = {item["id"] for item in data}
            added = 0
            for c in new_clues:
                if c["id"] not in existing_ids:
                    data.append(c)
                    existing_ids.add(c["id"])
                    added += 1

            # Atomic write
            temp_file = OUTPUT_FILE.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file.replace(OUTPUT_FILE)
            print(f"Appended {added} new clues. Total in bank: {len(data)}")
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
            for i, it in enumerate(items):
                validate_clue_schema(it)
            print(f"All {len(items)} clues in {OUTPUT_FILE.name} are valid.")
        else:
            print(f"File {OUTPUT_FILE} not found.")
