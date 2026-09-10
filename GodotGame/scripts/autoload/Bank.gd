extends Node
## Question bank loader + board builder + answer judge.
## Content: 650-clue bank (single/double/final). All question content English;
## Persian lives in accepted_aliases (and UI chrome handled by Game.gd).

var clues: Array = []          # all raw clues
var by_round := {"single": [], "double": [], "final": []}
var categories := {"single": [], "double": []}  # Array[Dictionary] precomputed

# Display economy (tooman) per round, indexed by slot tier.
const DISPLAY_M := {"single": [10, 25, 50, 100, 200], "double": [20, 50, 100, 150, 200]}
const SOURCE_V  := {"single": [200, 400, 600, 800, 1000], "double": [400, 800, 1200, 1600, 2000]}

var _loaded := false


func _ready() -> void:
	_load_bank()


func _load_bank() -> void:
	if _loaded:
		return
	_loaded = true
	var f := FileAccess.open("res://assets/data/verified_clues.json", FileAccess.READ)
	if f == null:
		push_error("Bank: cannot open verified_clues.json")
		return
	var text := f.get_as_text()
	var json := JSON.new()
	if json.parse(text) != OK:
		push_error("Bank: JSON parse failed")
		return
	var data = json.data
	clues = data if data is Array else (data.get("clues", []) if data is Dictionary else [])
	for c in clues:
		var r: String = str(c.get("round", ""))
		if by_round.has(r):
			by_round[r].append(c)
	_precompute_categories()


func _precompute_categories() -> void:
	for r in ["single", "double"]:
		var wanted: Array = SOURCE_V[r]
		var by_cat := {}
		for c in by_round[r]:
			if not by_cat.has(c.category):
				by_cat[c.category] = {}
			by_cat[c.category][int(c.value)] = c
		for cat in by_cat:
			var has_all := true
			for v in wanted:
				if not by_cat[cat].has(v):
					has_all = false
					break
			if has_all:
				var entry := {"name": cat, "clues": by_cat[cat], "used": false}
				categories[r].append(entry)


func slot_tooman(round_key: String, tier: int) -> int:
	var arr: Array = DISPLAY_M[round_key]
	return arr[tier] * 1_000_000


func _pick_round_cats(rng: RandomNumberGenerator, round_key: String, count: int) -> Array:
	## Choose `count` fresh full-tier categories (prefer never-used, fall back to any).
	var pool: Array = categories[round_key]
	var fresh: Array = []
	var rest: Array = []
	for e in pool:
		if e.used:
			rest.append(e)
		else:
			fresh.append(e)
	var ordered: Array = fresh + rest
	# Fisher-Yates
	for i in range(ordered.size() - 1, 0, -1):
		var j := rng.randi_range(0, i)
		var tmp = ordered[i]
		ordered[i] = ordered[j]
		ordered[j] = tmp
	var chosen: Array = ordered.slice(0, mini(count, ordered.size()))
	for e in chosen:
		e.used = true
	return chosen


func build_round(rng: RandomNumberGenerator, round_key: String) -> Array:
	## Returns 6 columns: each {name, tier_taken:[bool x5], clue (id text etc) per tier}.
	var chosen := _pick_round_cats(rng, round_key, 6)
	var board: Array = []
	var src_vals: Array = SOURCE_V[round_key]
	for e in chosen:
		var col := {
			"name": e.name,
			"used": false,
			"clues": [],  # tier index -> raw clue dict (or null)
			"taken": [],  # tier index -> bool
		}
		var row: Array = []
		var taken: Array = []
		for v in src_vals:
			row.append(e.clues[v])
			taken.append(false)
		col.clues = row
		col.taken = taken
		board.append(col)
	return board


func category_names(round_key: String) -> Array:
	var out: Array = []
	for e in categories[round_key]:
		out.append(e.name)
	return out


func pick_final(rng: RandomNumberGenerator) -> Dictionary:
	var pool: Array = by_round["final"]
	if pool.is_empty():
		# fallback: highest double clue
		pool = by_round["double"]
	var i := rng.randi_range(0, pool.size() - 1)
	return pool[i]


# ---- Answer judging ----------------------------------------------------------

func _is_space(ch: String) -> bool:
	var c := ch.unicode_at(0)
	return c == 0x09 or c == 0x0A or c == 0x0D or c == 0x20 or c == 0xA0 \
		or c == 0x200C or c == 0x200B or c == 0x202F or c == 0xFEFF \
		or (c >= 0x2000 and c <= 0x200A)


func _normalize(s: String) -> String:
	## Collapse whitespace/ZWNJ and unify Persian orthography + Arabic lookalikes.
	var out := ""
	var prev_space := false
	for ch in s.strip_edges():
		var code := ch.unicode_at(0)
		# Strip diacritics (harakat) and tatweel
		if code >= 0x064B and code <= 0x065F:
			continue
		if code == 0x0640:  # tatweel ـ
			continue
		if ch == "ي": ch = "ی"
		elif ch == "ك": ch = "ک"
		elif ch == "ٱ" or ch == "أ" or ch == "إ": ch = "ا"
		elif ch == "ۀ": ch = "ه"
		elif _is_space(ch):  # spaces + ZWNJ collapse
			if not prev_space:
				out += " "
				prev_space = true
			continue
		prev_space = false
		out += ch.to_lower()
	return out.strip_edges()


func answer_ok(clue: Dictionary, text: String) -> Dictionary:
	## Returns {ok, matched, canonical}. Accepts canonical, Persian aliases, partials.
	var canonical := str(clue.get("canonical_answer", ""))
	var aliases: Array = clue.get("accepted_aliases", [])
	var partials: Array = clue.get("partial_answers", [])
	var norm := _normalize(text)
	var can := _normalize(canonical)
	var result := {"ok": false, "matched": canonical, "canonical": canonical}

	# Try full alias list
	var fulls: Array = [canonical]
	for a in aliases:
		fulls.append(str(a))
	for p in partials:
		fulls.append(str(p))
	for f_ in fulls:
		if _normalize(str(f_)) == norm:
			result.ok = true
			result.matched = str(f_)
			return result

	# Try partial prefix match against canonical (last tokens). Persian: user may
	# omit honorifics; English: "Amir Kabir" given -> partial "Amir" is too loose,
	# so only accept partial when the bank lists it OR norm is >= half canonical.
	var min_len := maxi(3, int(round(float(can.length()) * 0.45)))
	if can.length() >= min_len and norm.length() <= can.length() and norm.length() >= min_len:
		if can.begins_with(norm) or can.ends_with(norm) or can.contains(norm):
			result.ok = true
			result.matched = canonical
			return result

	# Persian honorific stripping: drop "میرزا"/"آیتالله"/"شاه" lead tokens on both sides.
	var lead_tokens := ["میرزا ", "میرزا", "آیت الله", "آیتالله", "امام ", "امام", "شاه ", "دکتر ", "حاج ", "حاجی "]
	var norm2 := norm
	var can2 := can
	for tok in lead_tokens:
		var tn := _normalize(tok)
		if norm2 == tn + " " or norm2.begins_with(tn + " "):
			norm2 = norm2.substr(tn.length()).strip_edges()
		if can2.begins_with(tn + " "):
			can2 = can2.substr(tn.length()).strip_edges()
	if norm2 != "" and can2 != "" and norm2 == can2:
		result.ok = true
		result.matched = canonical
	return result


func mc_ok(clue: Dictionary, choice_idx: int) -> bool:
	return int(clue.get("correct_option_index", -1)) == choice_idx
