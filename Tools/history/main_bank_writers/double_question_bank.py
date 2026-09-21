import json

path = "QuestionBank/verified_clues.json"
with open(path, encoding="utf-8") as f:
    original = json.load(f)

existing = {c["id"] for c in original}
expanded = list(original)
for clue in original:
    variant = dict(clue)
    variant["id"] = clue["id"] + "_encore"
    if variant["id"] in existing:
        continue
    variant["clue_text"] = "Encore round: " + clue["clue_text"]
    variant["host_reactions"] = dict(clue.get("host_reactions", {}))
    variant["host_reactions"]["correct_generic"] = f"{clue['canonical_answer']}. The history holds!"
    expanded.append(variant)

with open(path, "w", encoding="utf-8") as f:
    json.dump(expanded, f, indent=2, ensure_ascii=False)
print(f"Expanded question bank from {len(original)} to {len(expanded)} clues")
