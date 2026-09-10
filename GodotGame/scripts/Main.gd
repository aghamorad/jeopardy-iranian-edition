extends Control
## Jeopardy - Iranian Edition. Broadcast quiz show in Godot.
## Flow: SPLASH -> LOBBY -> ROUND 1 board -> ROUND 2 -> FINAL -> RESULTS

class Player:
	var idx := -1
	var name := ""
	var is_bot := false
	var persona := ""     # e.g. HISTORIAN (displayed for bots)
	var skill := 0.6      # 0..1 answering strength
	var score := 0
	var color := Color.WHITE
	var hotkey := ""      # "1".."9", "" for bots
	var right := 0        # correct answers this show

const W := 1280.0
const H := 800.0
const SkylineScr = preload("res://scripts/ui/Skyline.gd")

# ---- persistent UI roots ----------------------------------------------------
var _bg: Control
var _screen: Control          # content area rebuilt per phase
var _top: Control             # top chrome (logo/round/lang) rebuilt per phase
var _over: Control            # toast layer

# ---- match state ------------------------------------------------------------
var _rng := RandomNumberGenerator.new()
var _phase := "splash"        # splash lobby board clue dd final results
var _players: Array = []
var _cur: Dictionary = {}     # current clue being played
var _round_key := "single"    # single | double
var _board: Array = []        # columns of {name, taken:[], clues:[]}
var _col := -1
var _tier := -1
var _picker := 0              # whose turn to pick
var _mc := false              # answer mode: multiple choice vs typed
var _clue_stage := ""         # read armed ring answer correct reveal
var _ring_pool: Array = []    # player idx allowed to ring now
var _ans_pool: Array = []     # idx still may answer this clue
var _used: Array = []         # bool per player, reset per clue
var _responder := -1
var _dd := false
var _dd_amt := 0
var _seq := 0                 # stale-callback guard
var _read_t := 0.0
var _deadline := 0.0
var _ring_open := false
var _log: Array = []
var _final := {}              # final state
var _emblem: Texture2D
var _gate := false            # opening host taunt holds the first board
var _announced_open := false  # opening VO plays once per launch
var _t0 := 0.0                # launch time (reject stale launch key events)
var _strip_l: TextureRect
var _strip_r: TextureRect

# ---- live UI refs (refreshed without full rebuild) --------------------------
var _score_lbls := {}         # idx -> Label
var _chip_boxes := {}         # idx -> StyleBoxFlat
var _chip_btns := {}          # idx -> Button
var _phase_lbl: Label
var _cell_btns := []          # tier lists
var _buzz_light: ColorRect

# ---- default bot persona pool ----------------------------------------------
const BOTS := [
	["NIMA", 0.82, "HISTORIAN"], ["PARVIN", 0.9, "PERSIANIST"],
	["SHIRIN", 0.68, "CINEPHILE"], ["KAVUS", 0.6, "ARCHIVIST"],
	["BAHRAM", 0.52, "OILMAN"], ["TURAN", 0.46, "GAMBLER"],
	["SETAREH", 0.72, "LITERARY"], ["ARMAN", 0.64, "MILITARIST"],
]

var _lobby_humans: Array = []  # {name, line: LineEdit}
var _lobby_bots: Array = []    # dict of chosen persona idx


func _ready() -> void:
	Game._ensure_fonts()
	_rng.randomize()
	_t0 = Time.get_ticks_msec()
	_emblem = load("res://assets/img/emblem_w.png")
	# Base fullscreen structure
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_bg = _make_layer()
	_top = _make_layer()
	_screen = _make_layer()
	_over = _make_layer()
	_go_splash()


func _make_layer() -> Control:
	var c := Control.new()
	c.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(c)
	return c


func _wm(px: int, col: Color, ecol: Color) -> Wordmark:
	var wm := Wordmark.new()
	wm.set_mark(Game.display_font, px, col, _emblem, ecol, true)
	wm.size = wm.custom_minimum_size
	return wm


func _wm_center(wm: Control, y: float) -> void:
	wm.position = Vector2((W - wm.size.x) / 2.0, y)


# --------------------------------------------------------------------------- #
#  SPLASH                                                                    #
# --------------------------------------------------------------------------- #
func _go_splash() -> void:
	_phase = "splash"
	_clear()
	Audio.music("theme_title")
	if not _announced_open:
		_announced_open = true
		_bot_after(0.7, _play_open_announce)
	_build_splash()


func _play_open_announce() -> void:
	if _phase != "splash":
		return
	Audio.voice("announce_open")


func _build_splash() -> void:
	# cinematic backdrop: Tehran skyline drawn in-engine, low key
	var sky := SkylineScr.new()
	sky.position = Vector2(0, 0)
	sky.size = Vector2(W, H)
	sky.strength = 1.0
	sky.tower_alpha = 0.30
	_screen.add_child(sky)

	# green (LEFT) / red (RIGHT) breathing light columns
	var lw := 176.0
	_strip_l = _light_column(0.0, lw, Color("#2f9b45"))
	_strip_r = _light_column(W - lw, lw, Color("#c22f28"))
	_screen.add_child(_strip_l)
	_screen.add_child(_strip_r)
	_floor_reflect(0.0, lw, Color("#2f9b45"))
	_floor_reflect(W - lw, lw, Color("#c22f28"))

	# white word runs climb the two columns
	_side_words(true)
	_side_words(false)

	# wordmark: JEOPARDY! with the Iranian emblem where the O would be
	var wm := _wm(116, Color.WHITE, Color("#d8332a"))
	_wm_center(wm, 178)
	_screen.add_child(wm)

	var sub := Game.styled_label("IRANIAN  EDITION", 28, Game.SL_SOFT)
	sub.position = Vector2(0, 356)
	sub.size = Vector2(W, 40)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_screen.add_child(sub)

	var fa_sub := Game.styled_label("نسخهٔ ایرانی", 20, Color(1, 1, 1, 0.5))
	fa_sub.position = Vector2(0, 396)
	fa_sub.size = Vector2(W, 34)
	fa_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_screen.add_child(fa_sub)

	# the irreverent tagline (exactly as the user wrote it)
	var tag := Game.styled_label(
		"BECAUSE YOU FUCKERS DON'T KNOW YOUR HISTORY\nAND IT'S TIME YOU LEARN A GODDAMN THING OR TWO.",
		21, Game.SL_SOFT)
	tag.position = Vector2(280, 452)
	tag.size = Vector2(720, 86)
	tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_screen.add_child(tag)

	var tagfa := Game.styled_label("زمانش رسیده چندتا چیز بدانی…", 17, Color(1, 1, 1, 0.45))
	tagfa.position = Vector2(280, 528)
	tagfa.size = Vector2(720, 30)
	tagfa.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_screen.add_child(tagfa)

	# press to begin — white on dark, thin border, not a glossy pill
	var b := _make_btn(Game.t("PRESS ANY KEY TO BEGIN", "برای شروع، هر کلیدی بزن"), "", 22, "lined")
	b.position = Vector2((W - 460) / 2.0, 652)
	b.size = Vector2(460, 66)
	_screen.add_child(b)


func _light_column(x: float, w: float, col: Color) -> TextureRect:
	## Vertical light beam of the given flag color, tint baked into the gradient
	## so `modulate.a` alone drives the breathing in _process.
	var tr := TextureRect.new()
	tr.position = Vector2(x, 0)
	tr.size = Vector2(w, H)
	var g := Gradient.new()
	g.set_color(0, Color(col.r, col.g, col.b, 0.0))
	g.set_color(1, Color(col.r, col.g, col.b, 0.0))
	g.add_point(0.13, Color(col.r, col.g, col.b, 0.05))
	g.add_point(0.40, Color(col.r, col.g, col.b, 0.30))
	g.add_point(0.72, Color(col.r, col.g, col.b, 0.13))
	var gt := GradientTexture2D.new()
	gt.gradient = g
	gt.width = 4
	gt.height = 256
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	tr.texture = gt
	tr.stretch_mode = TextureRect.STRETCH_SCALE
	tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return tr


func _floor_reflect(x: float, w: float, col: Color) -> void:
	## Faint mirror streak of a light column on the dark floor.
	var tr := TextureRect.new()
	tr.position = Vector2(x - w * 0.5, H - 190.0)
	tr.size = Vector2(w * 2.0, 190.0)
	var g := Gradient.new()
	g.set_color(0, Color(col.r, col.g, col.b, 0.20))
	g.set_color(1, Color(col.r, col.g, col.b, 0.0))
	var gt := GradientTexture2D.new()
	gt.gradient = g
	gt.width = 4
	gt.height = 256
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	tr.texture = gt
	tr.stretch_mode = TextureRect.STRETCH_SCALE
	tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_screen.add_child(tr)


func _side_words(left_side: bool) -> void:
	## Stacked white category words climbing each flanking light column.
	var words := ["PEOPLE", "PLACES", "EMPIRES", "CULTURE", "REVOLUTIONS", "ART", "SCIENCE", "SPORT", "OIL", "GOLD", "DEEDS"] \
		if left_side else \
		["KINGS", "POETS", "WARS", "CINEMA", "SONGS", "MYTHS", "EYES", "LINES", "OIL", "MORE"]
	var x := 0.0
	if not left_side:
		x = W - 176.0
	var y := 118.0
	for i in words.size():
		var lb := Game.styled_label(words[i], 15, Color(1, 1, 1, 0.88), 1)
		lb.position = Vector2(x + 6, y)
		lb.size = Vector2(164, 26)
		_screen.add_child(lb)
		y += 52.0
		if y > H - 150.0:
			break


# --------------------------------------------------------------------------- #
#  LOBBY                                                                     #
# --------------------------------------------------------------------------- #
func _go_lobby() -> void:
	_phase = "lobby"
	_clear()
	Audio.music("theme_title")

	# backdrop
	var img := TextureRect.new()
	img.texture = load("res://assets/img/stage_isfahan.png")
	img.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	img.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	img.set_anchors_preset(Control.PRESET_FULL_RECT)
	img.modulate = Color(1, 1, 1, 0.16)
	_screen.add_child(img)

	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.03, 0.05, 0.78)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_screen.add_child(shade)

	_lobby_humans = []
	_lobby_bots = []
	if _players.is_empty():
		_lobby_humans.append({"name": "YOU", "line": null})
		_lobby_bots.append(0)
		_lobby_bots.append(1)

	# title wordmark top center
	var wm := _wm(52, Color("#e9c464"), Color("#1b9a49"))
	_wm_center(wm, 34)
	_screen.add_child(wm)

	# Left: roster panel -------------------------------------------------------
	var pan := ColorRect.new()
	pan.color = Color("#0b0f16")
	pan.position = Vector2(70, 150)
	pan.size = Vector2(560, 420)
	_screen.add_child(pan)
	_border(pan)

	var t1 := Game.styled_label(Game.t("CONTESTANTS", "شرکت‌کنندگان"), 26, Game.GOLD, 1)
	t1.position = Vector2(70, 168)
	t1.size = Vector2(560, 40)
	_screen.add_child(t1)

	_lobby_humans = _refresh_roster_rows()


	# Right: settings ----------------------------------------------------------
	var s1 := Game.styled_label(Game.t("LANGUAGE", "زبان"), 26, Game.GOLD, 1)
	s1.position = Vector2(700, 180)
	s1.size = Vector2(360, 34)
	_screen.add_child(s1)

	var langbar := _seg_bar(700, 220, [Game.t("ENGLISH", "انگلیسی"), Game.t("فارسی", "فارسی")], 0 if Game.lang == "en" else 1, _on_lang_pick)
	_screen.add_child(langbar)

	var s2 := Game.styled_label(Game.t("ANSWER MODE", "نحوهٔ پاسخ"), 26, Game.GOLD, 1)
	s2.position = Vector2(700, 300)
	s2.size = Vector2(360, 34)
	_screen.add_child(s2)

	var modebar := _seg_bar(700, 340, [Game.t("TYPE", "متن آزاد"), Game.t("CHOOSE", "چندگزینه‌ای")], 1 if _mc else 0, _on_mode_pick)
	_screen.add_child(modebar)

	var how := Game.styled_label(
		Game.t("Pick a clue · buzz with 1/Space when armed · type the answer.\nGet it right, the money is yours. Miss it, you pay.",
		"یک سؤال انتخاب کن · با کلید ۱/اسپیس زنگ بزن · پاسخ را بنویس.\nدرست بگویی، پول مال توست. اشتباه بگویی، کم می‌شود."),
		18, Game.MUTED)
	how.position = Vector2(700, 440)
	how.size = Vector2(360, 120)
	how.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_screen.add_child(how)

	var start := _make_btn(Game.t("START THE SHOW", "شروع نمایش"), "_start_show", 30, "start")
	start.position = Vector2(700, 596)
	start.size = Vector2(360, 78)
	_screen.add_child(start)


func _refresh_roster_rows() -> Array:
	# remove previous rows
	for k in _screen.get_children():
		if k.has_method("is_in_group") and k.is_in_group("roster_row"):
			k.queue_free()
	var rows := 216
	var y0 := rows
	for i in _lobby_humans.size():
		var human: Dictionary = _lobby_humans[i]
		var h := ColorRect.new()
		h.color = Color("#111a26")
		h.position = Vector2(86, y0)
		h.size = Vector2(380, 46)
		h.add_to_group("roster_row")
		_screen.add_child(h)
		_border(h, Color("#24334a"))
		var name := LineEdit.new()
		name.text = human.name
		_style_line(name)
		name.position = Vector2(100, y0 + 5)
		name.size = Vector2(250, 36)
		_screen.add_child(name)
		name.add_to_group("roster_row")
		human.name = name.text
		human.line = name
		name.text_changed.connect(func(x): human.name = x)
		var lab := Game.styled_label(Game.t("HUMAN", "انسان"), 15, Color("#7fd0a0"))
		lab.position = Vector2(358, y0 + 6)
		lab.size = Vector2(64, 34)
		_screen.add_child(lab)
		lab.add_to_group("roster_row")
		y0 += 56

	for bi in _lobby_bots.size():
		var bpi: int = _lobby_bots[bi]
		var bp: Array = BOTS[bpi % BOTS.size()]
		var h := ColorRect.new()
		h.color = Color("#111a26")
		h.position = Vector2(86, y0)
		h.size = Vector2(380, 46)
		h.add_to_group("roster_row")
		_screen.add_child(h)
		_border(h, Color("#24334a"))
		var nm := Game.styled_label(str(bp[0]) + " · BOT", 20, Color.WHITE)
		nm.position = Vector2(100, y0 + 4)
		nm.size = Vector2(170, 38)
		_screen.add_child(nm)
		nm.add_to_group("roster_row")
		var ps := Game.styled_label(str(bp[2]), 15, Color("#8fa7ff"))
		ps.position = Vector2(260, y0 + 6)
		ps.size = Vector2(120, 34)
		_screen.add_child(ps)
		ps.add_to_group("roster_row")
		var del := _make_btn("✕", "", 16, "ghost")
		del.position = Vector2(430, y0 + 7)
		del.size = Vector2(30, 32)
		del.pressed.connect(_on_del_bot.bind(bi))
		_screen.add_child(del)
		del.add_to_group("roster_row")
		y0 += 56

	var add := _make_btn(Game.t("+ ADD BOT", "افزودن ربات"), "", 17, "ghost")
	add.position = Vector2(86, y0)
	add.size = Vector2(180, 40)
	add.pressed.connect(_on_add_bot)
	_screen.add_child(add)
	add.add_to_group("roster_row")
	y0 += 54

	var addh := _make_btn(Game.t("+ PLAYER", "افزودن بازیکن"), "", 17, "ghost")
	addh.position = Vector2(286, y0 - 54)
	addh.size = Vector2(180, 40)
	addh.pressed.connect(_on_add_human)
	addh.visible = _lobby_humans.size() < 3
	_screen.add_child(addh)
	addh.add_to_group("roster_row")
	return _lobby_humans


func _on_add_bot() -> void:
	if _lobby_humans.size() + _lobby_bots.size() < 6:
		_lobby_bots.append((_lobby_bots.size() + 2) % BOTS.size())
		_refresh_roster_rows()


func _on_del_bot(i: int) -> void:
	_lobby_bots.remove_at(i)
	_refresh_roster_rows()


func _on_add_human() -> void:
	_lobby_humans.append({"name": "P" + str(_lobby_humans.size() + 1), "line": null})
	_refresh_roster_rows()


func _on_lang_pick(i: int) -> void:
	Game.lang = "fa" if i == 1 else "en"
	_rebuild()


func _on_mode_pick(i: int) -> void:
	_mc = (i == 1)
	_rebuild()


func _start_show() -> void:
	var humans: Array = []
	for hi in _lobby_humans.size():
		var h: Dictionary = _lobby_humans[hi]
		var nm: String = str(h.get("name", "")).strip_edges()
		if nm.is_empty():
			nm = "P" + str(humans.size() + 1)
		humans.append(nm)
	if humans.is_empty():
		humans.append("YOU")
	# Build player pool: humans first, then bots.
	var cfg: Array = []
	for i in humans.size():
		cfg.append({"name": humans[i], "is_bot": false, "persona": "HUMAN", "skill": 0.85})
	for bi in _lobby_bots:
		var bp = BOTS[bi % BOTS.size()]
		cfg.append({"name": str(bp[0]), "is_bot": true, "persona": str(bp[2]), "skill": float(bp[1])})
	if cfg.size() > 6:
		cfg = cfg.slice(0, 6)
	_players = []
	var palettes := [Game.IRAN_W, Game.GOLD, Color("#6fc7ff"), Color("#ff9d7a"), Game.IRAN_G, Color("#c78be0")]
	for i in cfg.size():
		var p := Player.new()
		p.idx = i
		p.name = cfg[i].name
		p.is_bot = cfg[i].is_bot
		p.persona = cfg[i].persona
		p.skill = cfg[i].skill
		p.color = palettes[i % palettes.size()]
		if not cfg[i].is_bot:
			p.hotkey = str(i + 1)
		_players.append(p)
	_seq += 1
	_gate = true
	Audio.voice("challenge_open")   # start-game host taunt, before round one is live
	_begin_match()
	_release_gate_after_taunt()


func _release_gate_after_taunt() -> void:
	var release := func() -> void:
		if not _gate:
			return
		_gate = false
		# main theme is pre-game atmosphere: let it go as play becomes live
		_bot_after(0.4, func(): Audio.stop_music(1.2))
		_bot_pick_if_picker()
	Audio.voice_finished.connect(release, CONNECT_ONE_SHOT)
	# safety: a broken/absent VO must never strand the match on the title gate
	_bot_after(15.0, release)


func _begin_match() -> void:
	_seq += 1
	_round_key = "single"
	_start_round()


func _start_round() -> void:
	_seq += 1
	_board = Bank.build_round(_rng, _round_key)
	# one daily double per round on a random open slot
	var slots: Array = []
	for ci in _board.size():
		for ti in 5:
			slots.append([ci, ti])
	var ddpos = slots[_rng.randi_range(0, slots.size() - 1)]
	_board[ddpos[0]]["dd"] = [ddpos[1]]
	_picker = _leading_idx()
	_go_board()


func _leading_idx() -> int:
	var best := 0
	for i in range(1, _players.size()):
		if _players[i].score > _players[best].score:
			best = i
	return best


func _go_board() -> void:
	_phase = "board"
	_clear()
	_draw_chrome()
	_draw_board_grid()
	_draw_podium()
	_bot_pick_if_picker()


# --------------------------------------------------------------------------- #
#  Chrome (wordmark mini + round name + lang)                                #
# --------------------------------------------------------------------------- #
func _draw_chrome() -> void:
	var wm := _wm(26, Color("#e9c464"), Color("#1b9a49"))
	wm.position = Vector2(18, 8)
	_top.add_child(wm)

	var rname := Game.styled_label(_round_label(), 22, Color("#cfd9ea"))
	rname.position = Vector2(0, 10)
	rname.size = Vector2(W, 30)
	rname.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_top.add_child(rname)

	var langbtn := _make_btn(Game.t("EN", "فا"), "", 15, "ghost")
	langbtn.position = Vector2(W - 66, 12)
	langbtn.size = Vector2(52, 30)
	langbtn.pressed.connect(func(): _on_lang_pick(1 if Game.lang == "en" else 0))
	_top.add_child(langbtn)

	var quit := _make_btn(Game.t("MENU", "منو"), "", 15, "ghost")
	quit.position = Vector2(W - 132, 12)
	quit.size = Vector2(58, 30)
	quit.pressed.connect(_to_lobby)
	_top.add_child(quit)


func _round_label() -> String:
	var num := "ONE" if _round_key == "single" else "TWO"
	return Game.t("ROUND %s" % num, ("دور یک" if _round_key == "single" else "دور دو"))


# --------------------------------------------------------------------------- #
#  Board                                                                      #
# --------------------------------------------------------------------------- #
func _draw_board_grid() -> void:
	var MARGIN := 15.0
	var GAP := 8.0
	var COLS := _board.size()
	var CW := (W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
	var HEAD_Y := 78.0
	var HEAD_H := 96.0
	var CELL_H := 86.0

	for ci in COLS:
		var col: Dictionary = _board[ci]
		var x := MARGIN + ci * (CW + GAP)
		# category header
		var head := _panel(x, HEAD_Y, CW, HEAD_H, Color("#101c36"), Color("#31415f"))
		_screen.add_child(head)
		var hdr := Game.styled_label(str(col.name), 19, Color.WHITE, 1)
		hdr.position = Vector2(x, HEAD_Y + 6)
		hdr.size = Vector2(CW, HEAD_H - 12)
		hdr.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_screen.add_child(hdr)

		_cell_btns = []
		for ti in 5:
			var cell := _make_btn("", "", 0, "cell")
			cell.position = Vector2(x, HEAD_Y + HEAD_H + ti * (CELL_H + 6))
			cell.size = Vector2(CW, CELL_H)
			cell.pressed.connect(_pick_cell.bind(ci, ti))
			_screen.add_child(cell)
			if not _cell_btns.has(ci):
				_cell_btns.resize(ci + 1)
			if not _cell_btns[ci] is Array:
				_cell_btns[ci] = []
			_cell_btns[ci].append(cell)
			_style_cell(cell, ci, ti)

	_refresh_picker_hint()


func _style_cell(btn: Button, ci: int, ti: int) -> void:
	var col: Dictionary = _board[ci]
	var done: bool = col.taken[ti]
	var val := Bank.slot_tooman(_round_key, ti)
	var disp := Game.money_full(val)
	btn.text = ""
	if done:
		btn.disabled = true
		btn.modulate = Color(1, 1, 1, 0.06)
		var dl := Game.styled_label("·", 30, Color(0.3, 0.35, 0.45, 0.4), 1)
		dl.position = btn.position + Vector2(btn.size.x * 0.5 - 6, 26)
		dl.size = Vector2(12, 30)
		_screen.add_child(dl)
	else:
		var lb := Game.styled_label(disp, 26, Color("#f4e6b0"), 1, false, Game.display_font)
		lb.position = btn.position + Vector2(0, 27)
		lb.size = Vector2(btn.size.x, 40)
		_screen.add_child(lb)
		btn.add_theme_stylebox_override("normal", _sb(Color("#1a3f8e"), Color("#4a6ec0"), 1, 8))
		btn.add_theme_stylebox_override("hover", _sb(Color("#2452a8"), Color("#6f90d6"), 1, 8))
		btn.add_theme_stylebox_override("pressed", _sb(Color("#123069"), Color("#2c4a94"), 1, 8))
		btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND


func _pick_cell(ci: int, ti: int) -> void:
	if _phase != "board":
		return
	var col: Dictionary = _board[ci]
	if col.taken[ti]:
		return
	if _gate:
		return  # opening taunt still playing
	# Only the current picker may choose. For a party game any human may act as
	# picker, but a running bot picker yields.
	var p: Player = _players[_picker]
	if p.is_bot:
		return
	# check human: all humans act as one picker unless another human is set
	_execute_pick(ci, ti)


func _execute_pick(ci: int, ti: int) -> void:
	var col: Dictionary = _board[ci]
	_col = ci
	_tier = ti
	_seq += 1
	Audio.sfx("select")   # category selection, at the moment it is confirmed
	# daily double?
	if col.has("dd") and ti == col.dd[0]:
		_begin_dd()
	else:
		_open_clue()


# --------------------------------------------------------------------------- #
#  Podium / score chips                                                       #
# --------------------------------------------------------------------------- #
func _draw_podium() -> void:
	_score_lbls = {}
	_chip_boxes = {}
	_chip_btns = {}
	var n := _players.size()
	var m := 14.0
	var pw := (W - m * 2 - (n - 1) * 8) / n
	var py := H - 152.0
	for i in n:
		var p: Player = _players[i]
		var x := m + i * (pw + 8)
		var box := _panel(x, py, pw, 140, Color("#0e1520"), Color("#2b3d5a"))
		_screen.add_child(box)
		_chip_boxes[i] = box

		var nm := p.name
		if not p.is_bot:
			nm += "  (" + (p.hotkey if p.hotkey else "") + ")"
		var tag := "YOU" if not p.is_bot else "BOT·" + p.persona
		var nm_lbl := Game.styled_label(nm, 17, p.color, 1)
		nm_lbl.position = Vector2(x + 4, py + 6)
		nm_lbl.size = Vector2(pw - 8, 24)
		_screen.add_child(nm_lbl)
		var tag_lbl := Game.styled_label(tag, 12, Color(0.7, 0.75, 0.82, 0.8), 1)
		tag_lbl.position = Vector2(x + 4, py + 30)
		tag_lbl.size = Vector2(pw - 8, 18)
		_screen.add_child(tag_lbl)
		var sc := Game.styled_label("0", 26, Color.WHITE, 1, false, Game.display_font)
		sc.position = Vector2(x + 2, py + 54)
		sc.size = Vector2(pw - 4, 40)
		_screen.add_child(sc)
		_score_lbls[i] = sc

		var buzz := _make_btn("BUZZ", "_try_buzz_btn", 20, "buzz")
		buzz.position = Vector2(x + pw * 0.5 - 55, py + 96)
		buzz.size = Vector2(110, 36)
		buzz.visible = false
		_screen.add_child(buzz)
		_chip_btns[i] = buzz
	# color name chip hover? not needed


func _refresh_scores() -> void:
	for i in _score_lbls:
		var p: Player = _players[i]
		_score_lbls[i].text = Game.money_full(p.score)


func _refresh_picker_hint() -> void:
	# highlight current picker chip
	if _chip_boxes.is_empty():
		return
	for i in _chip_boxes:
		var p: Player = _players[i]
		var is_pick: bool = (i == _picker) and (_phase == "board")
		var sb := _chip_boxes[i] as ColorRect
		if is_pick:
			_panel_paint(sb, Color("#232f12"), Color(Game.GOLD, 0.9))
			_set_children_alpha(i, 1.0)
		else:
			_panel_paint(sb, Color("#0e1520"), Color("#2b3d5a"))


func _panel_paint(sb: ColorRect, bg: Color, border: Color) -> void:
	sb.color = bg


func _set_children_alpha(_i: int, _a: float) -> void:
	pass


func _to_lobby() -> void:
	_seq += 1
	_players = []
	Audio.stop_amb()   # leave any clue/final thinking bed behind
	_go_lobby()


# --------------------------------------------------------------------------- #
#  Bots: picking + buzzing + answering                                        #
# --------------------------------------------------------------------------- #
func _bot_pick_if_picker() -> void:
	if _phase != "board":
		return
	if _gate:
		return
	var p: Player = _players[_picker]
	if not p.is_bot:
		return
	_bot_after(0.9 + _rng.randf() * 1.4, _bot_pick)


func _bot_pick() -> void:
	if _phase != "board":
		return
	var avail: Array = []
	for ci in _board.size():
		for ti in 5:
			if not _board[ci].taken[ti]:
				avail.append([ci, ti])
	if avail.is_empty():
		return
	# bots prefer easy mid values but vary
	avail.shuffle()
	var pick = avail[0]
	for a in avail:
		if _rng.randf() < 0.55:
			pick = a
			break
	_execute_pick(pick[0], pick[1])


func _bot_after(sec: float, fn: Callable) -> void:
	if sec <= 0:
		fn.call()
		return
	get_tree().create_timer(sec).timeout.connect(fn)


func _bot_ring_when_armed() -> void:
	if _phase != "clue" or not _ring_open:
		return
	# each not-yet-used bot may decide to ring after a delay
	for i in _ring_pool:
		var p: Player = _players[i]
		if not p.is_bot:
			continue
		var want := _rng.randf() < _bot_conf(p)
		if not want:
			continue
		var delay := lerpf(0.15, 1.1, 1.0 - p.skill) + _rng.randf() * 0.7
		_bot_after(delay, _bot_ring_attempt.bind(i))


func _bot_ring_attempt(i: int) -> void:
	if _phase != "clue" or not _ring_open:
		return
	if i in _used:
		return
	_try_ring(i)


func _bot_conf(p: Player) -> float:
	var d := clampf(float(_tier) / 4.0, 0.0, 1.0)
	return clampf(p.skill * (1.15 - 0.3 * d), 0.05, 0.98)


func _bot_answer_if_needed() -> void:
	# only called for responder bot
	if _responder == -1:
		return
	var p: Player = _players[_responder]
	if not p.is_bot:
		return
	_bot_after(0.5 + _rng.randf() * 1.1, _bot_submit)


func _bot_submit() -> void:
	if _phase != "clue" or _clue_stage != "answer":
		return
	if _responder == -1:
		return
	var p: Player = _players[_responder]
	if not p.is_bot:
		return
	var correct := _rng.randf() < _bot_conf(p)
	var text := ""
	if _mc:
		var opts: Array = _cur.get("options", [])
		var ci_ok: int = int(_cur.get("correct_option_index", 0))
		var pick_idx := ci_ok if correct else _wrong_opt(opts, ci_ok)
		_submit_mc(pick_idx)
	else:
		if correct:
			text = str(_cur.get("canonical_answer", ""))
		else:
			text = _wrong_text()
		_submit_typed(text)


func _wrong_opt(opts: Array, correct: int) -> int:
	var tries := 0
	while tries < 20:
		var j := _rng.randi_range(0, opts.size() - 1)
		if j != correct:
			return j
		tries += 1
	return (correct + 1) % opts.size()


func _wrong_text() -> String:
	var opts: Array = _cur.get("options", [])
	var can := _normalize(str(_cur.get("canonical_answer", "")))
	for k in 12:
		var j := _rng.randi_range(0, opts.size() - 1)
		var s := str(opts[j])
		if _normalize(s) != can:
			return s
	return "Hmm, no."


func _normalize(s: String) -> String:
	return Bank.answer_ok(_cur, s).matched if false else s.to_lower()


# --------------------------------------------------------------------------- #
#  Clue opening & phases                                                      #
# --------------------------------------------------------------------------- #
func _open_clue() -> void:
	_cur = _board[_col].clues[_tier]
	_dd = false
	_phase = "clue"
	_clue_stage = "read"
	_ring_open = false
	_ans_pool = []
	_used = []
	_used.resize(_players.size())
	_ring_pool = []
	for i in _players.size():
		_ring_pool.append(i)
		_ans_pool.append(i)
	_responder = -1
	# how long the host "reads" (display time) before the floor arms
	var read_s := clampf(3.0 + float(str(_cur.get("clue_text", "")).length()) * 0.05, 3.5, 12.0)
	_read_t = read_s
	# thinking music starts once the clue is fully on screen; the main theme is
	# pre-game atmosphere only and must be gone before any clue plays
	Audio.stop_music(0.7)
	Audio.stop_amb()
	Audio.amb("think_loop")
	_draw_clue()
	# arm after reading completes (early human buzz cancels this)
	get_tree().create_timer(read_s).timeout.connect(_arm_floor)


func _arm_floor() -> void:
	if _phase != "clue" or _clue_stage != "read":
		return
	_clue_stage = "armed"
	_ring_open = true
	_draw_clue()
	_bot_ring_when_armed()
	# nobody rings -> reveal after grace
	get_tree().create_timer(16.0).timeout.connect(_auto_reveal)


func _auto_reveal() -> void:
	if _phase != "clue" or not _ring_open:
		return
	_ring_open = false
	_reveal_current()


func _reveal_current() -> void:
	## Nobody can answer: show the canonical answer, then close the slot.
	if _phase != "clue":
		return
	Audio.stop_amb()
	_ring_open = false
	_clue_stage = "reveal"
	_draw_clue()
	get_tree().create_timer(3.4).timeout.connect(_after_reveal_done)


func _after_reveal_done() -> void:
	if _phase != "clue" or _clue_stage != "reveal":
		return
	_mark_current_done()
	_back_to_board()


func _early_buzz_allowed() -> bool:
	return _clue_stage == "read"


func _try_ring(i: int) -> void:
	if _phase != "clue":
		return
	if i in _used:
		return
	if not _ring_open and _clue_stage != "read":
		return
	if _clue_stage == "read" and _players[i].is_bot:
		return  # bots only ring when floor armed
	# accept (even early from a human => opens floor to everyone immediately):
	# thinking music stops first so the lock-in sfx lands clean and alone
	Audio.stop_amb()
	Audio.sfx("buzz")
	_responder = i
	_ring_open = true
	_clue_stage = "answer"
	_ring_pool = []
	_ans_pool = []
	for j in _players.size():
		if j != i:
			_ans_pool.append(j)
	_set_timer(15.0)
	_draw_clue()
	if _players[i].is_bot:
		_bot_answer_if_needed()


func _set_timer(sec: float) -> void:
	_deadline = Time.get_ticks_msec() / 1000.0 + sec


func _time_left() -> float:
	return _deadline - (Time.get_ticks_msec() / 1000.0)


func _process(_delta: float) -> void:
	# countdown label for timed answer
	if _phase == "clue" and _clue_stage == "answer":
		if _time_left() <= 0:
			_on_timeout()
			return
	# slow breathing on the splash light columns
	if _phase == "splash":
		var t := Time.get_ticks_msec() * 0.0012
		var p := 0.78 + 0.16 * (0.5 + 0.5 * sin(t))
		if _strip_l:
			_strip_l.modulate.a = p
		if _strip_r:
			_strip_r.modulate.a = p


func _on_timeout() -> void:
	if _clue_stage != "answer":
		return
	_used[_responder] = true
	_responder = -1
	_reopen_floor()


func _reopen_floor() -> void:
	if _phase != "clue":
		return
	_ring_open = true
	_clue_stage = "armed"
	_draw_clue()
	if _ans_pool.is_empty():
		_reveal_current()
		return
	# others may still answer, so the unresolved-clue thinking loop resumes
	Audio.stop_amb()
	Audio.amb("think_loop")
	_bot_ring_when_armed()
	get_tree().create_timer(9.0).timeout.connect(_auto_reveal)


func _submit_typed(text: String) -> void:
	if _clue_stage != "answer" or _responder == -1:
		return
	var res := Bank.answer_ok(_cur, text)
	_finish_answer(res.ok, text)


func _submit_mc(idx: int) -> void:
	if _clue_stage != "answer" or _responder == -1:
		return
	var ok := Bank.mc_ok(_cur, idx)
	var opts: Array = _cur.get("options", [])
	_finish_answer(ok, str(opts[idx]) if idx < opts.size() else "")


func _finish_answer(ok: bool, text: String) -> void:
	if _clue_stage != "answer":
		return
	Audio.stop_amb()   # verdict sfx plays clean, never on top of thinking music
	_clue_stage = "correct" if ok else "wrong"
	var p: Player = _players[_responder]
	var val := _dd_amt if _dd else Bank.slot_tooman(_round_key, _tier)
	if ok:
		p.score += val
		p.right += 1
		Audio.sfx("correct")
	else:
		p.score -= val
		Audio.sfx("wrong")
		_used[_responder] = true
	_cur_responder_text = text
	_refresh_scores()
	_draw_clue()
	# hold on the verdict card a beat, then continue
	get_tree().create_timer(2.2).timeout.connect(_after_verdict.bind(ok))


func _after_verdict(ok: bool) -> void:
	if _phase != "clue":
		return
	if ok:
		_picker = _responder
		_mark_current_done()
		_back_to_board()
	elif _dd:
		_mark_current_done()
		_back_to_board()
	else:
		_responder = -1
		_reopen_floor()


func _mark_current_done() -> void:
	_board[_col].taken[_tier] = true


func _back_to_board() -> void:
	_cur = {}
	if _round_complete():
		_next_round()
	else:
		_go_board()


func _round_complete() -> bool:
	for ci in _board.size():
		for ti in 5:
			if not _board[ci].taken[ti]:
				return false
	return true


func _next_round() -> void:
	_seq += 1
	if _round_key == "single":
		_round_key = "double"
		Audio.amb("sting_double", Audio.AMB_DB, false)   # Double Jeopardy transition sting
		_start_round()
	else:
		_start_final()


# --------------------------------------------------------------------------- #
#  Daily Double                                                               #
# --------------------------------------------------------------------------- #
func _begin_dd() -> void:
	_cur = _board[_col].clues[_tier]
	_dd = true
	_dd_amt = 0
	_phase = "dd"
	_clue_stage = "wager"
	_draw_dd_wager()
	if _players[_picker].is_bot:
		_bot_after(1.1, _bot_dd_wager)


func _bot_dd_wager() -> void:
	if _phase != "dd":
		return
	var p: Player = _players[_picker]
	var cap := maxi(p.score, Bank.slot_tooman(_round_key, _tier))
	var w: int
	if p.skill >= 0.75:
		w = cap                       # confident players go all-in
	elif p.skill >= 0.55:
		w = int(cap / 2)
	else:
		w = Bank.slot_tooman(_round_key, _tier)
	_dd_wager_set(w)


func _draw_dd_wager() -> void:
	_clear()
	var card := _panel(240, 180, W - 480, 420, Color("#15121c"), Color("#4a3a20"))
	_screen.add_child(card)
	var t := Game.styled_label("DAILY DOUBLE", 40, Game.GOLD, 1)
	t.position = Vector2(240, 220)
	t.size = Vector2(W - 480, 60)
	_screen.add_child(t)
	var p: Player = _players[_picker]
	var you := Game.styled_label(p.name + "  —  " + Game.money_full(p.score), 24, Color.WHITE, 1)
	you.position = Vector2(240, 300)
	you.size = Vector2(W - 480, 44)
	_screen.add_child(you)

	var cap := maxi(p.score, Bank.slot_tooman(_round_key, _tier))
	var half := int(cap / 2)
	var labs := [[str(Game.t("ALL IN", "همهٔ موجودی")), cap], [str(Game.t("HALF", "نصف")), half], [str(Game.t("SLOT VALUE", "ارزش سؤال")), Bank.slot_tooman(_round_key, _tier)]]
	var by := 400
	for l in labs:
		var bb := _make_btn(str(l[0]), "", 22, "gold")
		bb.position = Vector2(430, by)
		bb.size = Vector2(220, 52)
		bb.pressed.connect(_dd_wager_set.bind(l[1]))
		_screen.add_child(bb)
		by += 66
	var hint := Game.styled_label(Game.t("Wager up to what you hold.", "هرچه داری شرط بگذار."), 17, Game.MUTED, 1)
	hint.position = Vector2(240, 640)
	hint.size = Vector2(W - 480, 30)
	_screen.add_child(hint)
	_refresh_scores()


func _dd_wager_set(v: int) -> void:
	var p: Player = _players[_picker]
	var cap := maxi(p.score, Bank.slot_tooman(_round_key, _tier))
	_dd_amt = clampi(v, 0, cap)
	_responder = _picker
	_clue_stage = "answer"
	_ring_open = false
	_ans_pool = []
	_used = []
	_used.resize(_players.size())
	_set_timer(20.0)
	_phase = "clue"
	Audio.stop_music(0.7)
	Audio.stop_amb()
	Audio.amb("think_loop")
	_draw_clue()
	_p = _players[_picker]
	if _p.is_bot:
		_bot_answer_if_needed()


# --------------------------------------------------------------------------- #
#  Clue UI                                                                    #
# --------------------------------------------------------------------------- #
var _p: Player = null
var _cur_responder_text := ""


func _draw_clue() -> void:
	_clear()
	var p: Player = _players[_picker] if _picker < _players.size() else _players[0]
	# backdrop stays dark with faint emblem
	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.03, 0.05, 0.82)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_screen.add_child(shade)

	# card
	var card_w := 980.0
	var card_h := 470.0
	var cx := (W - card_w) / 2.0
	var cy := 88.0
	var card := _panel(cx, cy, card_w, card_h, Color("#e9e0cf"), Color("#7a5f2e"))
	_screen.add_child(card)

	var cat := str(_cur.get("category", "?"))
	var value_txt := Game.money_unit(Bank.slot_tooman(_round_key, _tier))
	if _dd:
		value_txt = Game.t("DAILY DOUBLE", "DAILY DOUBLE")
	var head := Game.styled_label("%s   ·   %s" % [cat, value_txt], 30, Color("#7a2408"), 1)
	head.position = Vector2(cx, cy + 18)
	head.size = Vector2(card_w, 40)
	_screen.add_child(head)

	var clue_txt := str(_cur.get("clue_text", ""))
	var body := Game.styled_label(clue_txt, 38, Color("#131826"), 1)
	body.position = Vector2(cx + 60, cy + 90)
	body.size = Vector2(card_w - 120, card_h - 150)
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_screen.add_child(body)

	# bottom status area below card
	var status := Game.styled_label(_status_text(), 22, Color("#d9c27f"), 1)
	status.position = Vector2(0, cy + card_h + 18)
	status.size = Vector2(W, 34)
	_screen.add_child(status)

	_draw_podium()

	match _clue_stage:
		"answer":
			_draw_answer_box(p)
		"read", "armed":
			_draw_buzz_bar()
		"correct":
			_draw_verdict(true)
		"wrong":
			_draw_verdict(false)
		"reveal":
			_draw_reveal_overlay()
	_refresh_scores()


func _status_text() -> String:
	match _clue_stage:
		"read":
			return Game.t("READING THE CLUE…  (ring early with %s to steal it)" % _players[0].hotkey,
				"سؤال در حال خواندن…  (با کلید %s زودتر زنگ بزن)" % _players[0].hotkey)
		"armed":
			return Game.t("BUZZ IN!", "زنگ بزن!")
		"answer":
			return Game.t("%s is answering" % _players[_responder].name, "در حال پاسخ…")
		"correct":
			return Game.t("CORRECT!", "درست!")
		"wrong":
			return Game.t("WRONG.", "اشتباه!")
		"reveal":
			return Game.t("The answer", "پاسخ")
	return ""


func _draw_buzz_bar() -> void:
	for i in _chip_btns:
		var p: Player = _players[i]
		var btn: Button = _chip_btns[i]
		if p.is_bot:
			btn.visible = false
			continue
		btn.visible = true
		btn.text = (Game.t("BUZZ", "زنگ") if (_ring_open or not p.is_bot) else "…")
		btn.pressed.connect(_try_ring.bind(i))
		btn.disabled = false


func _try_buzz_btn(i: int) -> void:
	_try_ring(i)


func _draw_answer_box(_p: Player) -> void:
	var box_w := 760.0
	var box := _panel((W - box_w) / 2, 330, box_w, 210, Color("#131c2c"), Color("#33507f"))
	_screen.add_child(box)
	var who := Game.styled_label(_players[_responder].name, 24, Game.GOLD, 1)
	who.position = Vector2((W - box_w) / 2, 350)
	who.size = Vector2(box_w, 40)
	_screen.add_child(who)
	if _mc:
		var opts: Array = _cur.get("options", [])
		var by := 408.0
		for i in opts.size():
			var b := _make_btn(str(opts[i]), "", 21, "mc")
			b.position = Vector2((W - box_w) / 2 + 40, by)
			b.size = Vector2(box_w - 80, 58)
			b.pressed.connect(_submit_mc.bind(i))
			_screen.add_child(b)
			by += 70
	else:
		var line := LineEdit.new()
		line.placeholder_text = Game.t("type the answer… (Persian works too)", "پاسخ را بنویس…")
		_style_line(line)
		line.position = Vector2((W - box_w) / 2 + 40, 408)
		line.size = Vector2(box_w - 160, 58)
		line.text_submitted.connect(_on_typed)
		_screen.add_child(line)
		line.grab_focus()
		var ok := _make_btn(Game.t("SUBMIT", "تأیید"), "", 24, "gold")
		ok.position = Vector2((W - box_w) / 2 + box_w - 120, 408)
		ok.size = Vector2(90, 58)
		ok.pressed.connect(func(): _on_typed(line.text))
		_screen.add_child(ok)
		var give := _make_btn(Game.t("give up", "منصرف شدم"), "", 15, "ghost")
		give.position = Vector2((W - box_w) / 2 + 40, 480)
		give.size = Vector2(150, 34)
		give.pressed.connect(func(): _on_giveup())
		_screen.add_child(give)


func _on_typed(txt: String) -> void:
	_submit_typed(txt)


func _on_giveup() -> void:
	# no penalty: responder yields without answering
	if _responder != -1:
		_used[_responder] = true
		_responder = -1
	_reopen_floor()


func _draw_verdict(ok: bool) -> void:
	var center := Game.styled_label(Game.t("CORRECT!" if ok else "WRONG.", "درست!" if ok else "اشتباه."),
		90, Color("#37d67a") if ok else Color("#e05545"), 1)
	center.position = Vector2(0, 260)
	center.size = Vector2(W, 140)
	center.set("theme_override_constants/shadow_offset_x", 2)
	center.set("theme_override_constants/shadow_offset_y", 4)
	_screen.add_child(center)
	var disp := _cur_responder_text.strip_edges()
	if ok:
		var res := Bank.answer_ok(_cur, disp if not disp.is_empty() else " ")
		var canon := str(res.canonical)
		var sub := Game.styled_label(canon, 34, Color("#e6c873"), 1)
		sub.position = Vector2(0, 420)
		sub.size = Vector2(W, 60)
		_screen.add_child(sub)
		var exp := str(_cur.get("explanation", ""))
		if not exp.is_empty():
			var ex := Game.styled_label(exp, 20, Color(0.9, 0.9, 0.9, 0.7), 1)
			ex.position = Vector2(180, 520)
			ex.size = Vector2(W - 360, 90)
			ex.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			_screen.add_child(ex)


func _draw_reveal_overlay() -> void:
	var can := str(_cur.get("canonical_answer", ""))
	var head := Game.styled_label(Game.t("NOBODY RANG IN — THE ANSWER WAS", "هیچ‌کس زنگ نزد — پاسخ این بود"), 24, Color("#cfd9ea"), 1)
	head.position = Vector2(0, 560)
	head.size = Vector2(W, 40)
	_screen.add_child(head)
	var ans := Game.styled_label(can, 44, Game.GOLD, 1, false, Game.display_font)
	ans.position = Vector2(0, 600)
	ans.size = Vector2(W, 70)
	_screen.add_child(ans)
	var exp := str(_cur.get("explanation", ""))
	if not exp.is_empty():
		var ex := Game.styled_label(exp, 18, Color(1, 1, 1, 0.65), 1)
		ex.position = Vector2(180, 680)
		ex.size = Vector2(W - 360, 80)
		ex.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_screen.add_child(ex)


# --------------------------------------------------------------------------- #
#  Final Jeopardy                                                             #
# --------------------------------------------------------------------------- #
func _start_final() -> void:
	# Only players with a positive bank contest.
	var finalists: Array = []
	for i in _players.size():
		if _players[i].score > 0:
			finalists.append(i)
	if finalists.is_empty():
		_final = {"none": true}
		_results()
		return
	_final = {"cat": "", "clue": {}, "finalists": finalists, "stage": "wager",
			  "locked": {}, "answers": {}, "wagers": {}}
	_final.clue = Bank.pick_final(_rng)
	_final.cat = str(_final.clue.get("category", "FINAL"))
	Audio.music("theme_title")   # build-up bed over the secret-wager screen
	_phase = "final"
	_draw_final_wager()


func _draw_final_wager() -> void:
	_clear()
	var card := _panel(200, 150, W - 400, 460, Color("#0e1220"), Color("#5a3a10"))
	_screen.add_child(card)
	var t := Game.styled_label(Game.t("FINAL JEOPARDY", "فینال"), 34, Color("#e9c464"), 1)
	t.position = Vector2(200, 176)
	t.size = Vector2(W - 400, 54)
	_screen.add_child(t)
	var cat_l := Game.styled_label(_final.cat, 30, Color.WHITE, 1)
	cat_l.position = Vector2(200, 240)
	cat_l.size = Vector2(W - 400, 50)
	_screen.add_child(cat_l)

	var fs: Array = _final.finalists
	var y := 320
	for i in fs:
		var p: Player = _players[i]
		var row := Game.styled_label("%s —  %s" % [p.name, Game.money_full(p.score)], 22, p.color, 1)
		row.position = Vector2(240, y)
		row.size = Vector2(560, 40)
		_screen.add_child(row)
		y += 46
	var hint := Game.styled_label(Game.t("Wagers are secret until the reveal.", "مبلغ شرط تا زمان نمایش محرمانه است."), 17, Game.MUTED, 1)
	hint.position = Vector2(200, 620)
	hint.size = Vector2(W - 400, 40)
	_screen.add_child(hint)
	var cont := _make_btn(Game.t("LOCK WAGERS · REVEAL CLUE", "قفل شرط‌ها · نمایش سؤال"), "", 24, "start")
	cont.position = Vector2(440, 680)
	cont.size = Vector2(400, 64)
	cont.pressed.connect(_reveal_final_clue)
	_screen.add_child(cont)


func _reveal_final_clue() -> void:
	# human quick wagers: all-in by default
	for i in _final.finalists:
		var p: Player = _players[i]
		var w := p.score if (not p.is_bot or _rng.randf() < 0.6) else int(p.score * 0.5)
		_final.wagers[i] = maxi(0, w)
	_final.stage = "answer"
	_phase = "final"
	_clear()
	# Show final clue + per-human secret answer fields
	var card := _panel(200, 96, W - 400, 420, Color("#0e1220"), Color("#5a3a10"))
	_screen.add_child(card)
	var t := Game.styled_label("FINAL JEOPARDY — " + _final.cat, 28, Game.GOLD, 1)
	t.position = Vector2(220, 116)
	t.size = Vector2(W - 440, 44)
	_screen.add_child(t)
	var clue_txt := str(_final.clue.get("clue_text", ""))
	var body := Game.styled_label(clue_txt, 30, Color.WHITE, 1)
	body.position = Vector2(240, 180)
	body.size = Vector2(W - 480, 180)
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_screen.add_child(body)
	var humans: Array = []
	for i in _final.finalists:
		if not _players[i].is_bot:
			humans.append(i)
	# bots "write" their answers already
	for i in _final.finalists:
		if _players[i].is_bot:
			var correct := _rng.randf() < _bot_conf(_players[i])
			_final.answers[i] = str(_final.clue.get("canonical_answer", "")) if correct else _final_wrong_text()
	# human answer fields
	var y := 540
	for i in humans:
		var p: Player = _players[i]
		var row := Game.styled_label(p.name, 20, p.color)
		row.position = Vector2(320, y)
		row.size = Vector2(200, 40)
		_screen.add_child(row)
		var line := LineEdit.new()
		line.placeholder_text = Game.t("your answer…", "پاسخ تو…")
		_style_line(line)
		line.position = Vector2(500, y)
		line.size = Vector2(430, 46)
		line.text_submitted.connect(_final_lock.bind(i, line))
		_screen.add_child(line)
		if humans.size() == 1:
			line.grab_focus()
		y += 62
	# all answered by bots => reveal immediately; humans by "lock all"
	if humans.is_empty():
		get_tree().create_timer(1.5).timeout.connect(_reveal_final)
	else:
		var lock := _make_btn(Game.t("REVEAL ANSWERS", "نمایش پاسخ‌ها"), "", 22, "start")
		lock.position = Vector2(500, y + 6)
		lock.size = Vector2(300, 56)
		lock.pressed.connect(_final_lock_all)
		_screen.add_child(lock)
		var hint := Game.styled_label(Game.t("30 seconds on the clock.", "۳۰ ثانیه فرصت داری."), 16, Game.MUTED, 1)
		hint.position = Vector2(320, y + 12)
		hint.size = Vector2(200, 40)
		_screen.add_child(hint)
	# Final Jeopardy thinking music while the contestants write their answers
	Audio.stop_music(0.7)
	Audio.stop_amb()
	Audio.amb("final_music")
	_set_timer(30.0)
	_pump_final_timeout()


func _final_lock(i: int, line: LineEdit, txt: String) -> void:
	_final.answers[i] = txt
	line.editable = false


func _final_lock_all() -> void:
	_reveal_final()


func _pump_final_timeout() -> void:
	if _phase == "final" and _final.stage == "answer":
		if _time_left() <= 0:
			_reveal_final()
			return
	get_tree().create_timer(0.5).timeout.connect(_pump_final_timeout)


func _final_wrong_text() -> String:
	var opts: Array = _final.clue.get("options", [])
	var can := _normalize(str(_final.clue.get("canonical_answer", "")))
	for k in 20:
		var j := _rng.randi_range(0, opts.size() - 1)
		var s := str(opts[j])
		if _normalize(s) != can:
			return s
	return "No idea."


func _reveal_final() -> void:
	_final.stage = "reveal"
	_phase = "final"
	Audio.stop_amb()   # stop the 30s thinking music once answers resolve
	# judge each answer
	for i in _final.finalists:
		var txt: String = _final.answers.get(i, "")
		var res := Bank.answer_ok(_final.clue, txt)
		_final.judge = res.ok
		var w: int = _final.wagers.get(i, 0)
		if res.ok:
			_players[i].score += w
		else:
			_players[i].score -= w
	_refresh_scores()
	_draw_final_reveal()
	get_tree().create_timer(4.0).timeout.connect(_results)


func _draw_final_reveal() -> void:
	_clear()
	var t := Game.styled_label("THE REVEAL", 40, Game.GOLD, 1)
	t.position = Vector2(0, 100)
	t.size = Vector2(W, 70)
	_screen.add_child(t)
	var can := str(_final.clue.get("canonical_answer", ""))
	var exp := str(_final.clue.get("explanation", ""))
	var fs: Array = _final.finalists
	var y := 210
	for i in fs:
		var p: Player = _players[i]
		var ok: bool = _final.judge
		# recompute judge per player (already applied)
		var res := Bank.answer_ok(_final.clue, str(_final.answers.get(i, "")))
		var w: int = _final.wagers.get(i, 0)
		var ans_txt := str(_final.answers.get(i, ""))
		var line := Game.styled_label(
			"%s   %s   %s   %s" % [p.name, Game.t("wager" if false else "W", ""), ans_txt, "✓" if res.ok else "✗"],
			24, p.color if res.ok else Color("#e05545"), 1)
		line.position = Vector2(200, y)
		line.size = Vector2(W - 400, 40)
		_screen.add_child(line)
		y += 48
	var canon := Game.styled_label(Game.t("The answer: ", "پاسخ صحیح: ") + can, 30, Color.WHITE, 1)
	canon.position = Vector2(0, y + 30)
	canon.size = Vector2(W, 60)
	_screen.add_child(canon)
	if not exp.is_empty():
		var ex := Game.styled_label(exp, 18, Color(1, 1, 1, 0.6), 1)
		ex.position = Vector2(220, y + 100)
		ex.size = Vector2(W - 440, 90)
		ex.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_screen.add_child(ex)


# --------------------------------------------------------------------------- #
#  Results                                                                    #
# --------------------------------------------------------------------------- #
func _results() -> void:
	_phase = "results"
	Audio.music("results_theme")
	Audio.sfx("winner")
	_clear()
	var shade := ColorRect.new()
	shade.color = Color(0.01, 0.02, 0.04, 0.8)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_screen.add_child(shade)

	# sort
	var order := range(_players.size())
	order.sort_custom(func(a, b): return _players[a].score > _players[b].score)
	var champ: Player = _players[order[0]]

	var wm := _wm(60, Game.GOLD, Color("#1b9a49"))
	_wm_center(wm, 60)
	_screen.add_child(wm)

	var champ_l := Game.styled_label(Game.t("CHAMPION", "قهرمان") + "  ·  " + champ.name, 40, Color("#ffe9a3"), 1)
	champ_l.position = Vector2(0, 190)
	champ_l.size = Vector2(W, 70)
	_screen.add_child(champ_l)

	var trophy := TextureRect.new()
	trophy.texture = load("res://assets/img/trophy_cup.png")
	trophy.custom_minimum_size = Vector2(0, 0)
	trophy.position = Vector2(W / 2 - 70, 280)
	trophy.size = Vector2(140, 140)
	trophy.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	trophy.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_screen.add_child(trophy)

	var y := 460
	for i in order:
		var p: Player = _players[i]
		var med := ("🥇" if i == order[0] else ("🥈" if i == order[1] else ("🥉" if i == order[2] else "  ")))
		var line := Game.styled_label(med + " " + p.name + "   " + Game.money_full(p.score), 26, p.color, 1)
		line.position = Vector2(0, y)
		line.size = Vector2(W, 44)
		_screen.add_child(line)
		y += 52

	var again := _make_btn(Game.t("BACK TO LOBBY", "بازگشت به لابی"), "", 24, "start")
	again.position = Vector2(W / 2 - 210, 700)
	again.size = Vector2(420, 64)
	again.pressed.connect(_to_lobby)
	_screen.add_child(again)


# --------------------------------------------------------------------------- #
#  UI primitives + styles                                                    #
# --------------------------------------------------------------------------- #
func _clear() -> void:
	_seq += 1
	for c in _bg.get_children():
		c.queue_free()
	for c in _top.get_children():
		c.queue_free()
	for c in _screen.get_children():
		c.queue_free()
	for c in _over.get_children():
		c.queue_free()
	_bg = _make_layer()
	_top = _make_layer()
	_screen = _make_layer()
	_over = _make_layer()
	_score_lbls = {}
	_chip_btns = {}
	_cell_btns = []
	_players_alpha_refs = {}


var _players_alpha_refs := {}


func _bg_dark() -> void:
	var base := ColorRect.new()
	base.color = Color(0.02, 0.03, 0.05, 1.0)
	base.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bg.add_child(base)


func _rebuild() -> void:
	match _phase:
		"splash": _go_splash()
		"lobby": _go_lobby()
		"board": _go_board()
		"clue": _draw_clue()
		"dd": _draw_dd_wager()
		"final": _draw_final_wager() if _final.stage == "wager" else (_reveal_final() if _final.stage == "reveal" else _reveal_final_clue())
		"results": _results()


func _panel(x: float, y: float, w: float, h: float, bg: Color, border: Color) -> ColorRect:
	var c := ColorRect.new()
	c.color = bg
	c.position = Vector2(x, y)
	c.size = Vector2(w, h)
	return c


func _border(c: Control, col := Color("#2b3d5a"), w := 1.0) -> void:
	# adds a thin border using a stylebox on the Control's draw? ColorRect has none;
	# emulated by a draw child outline is complex, so border set via an underlay.
	var over := ColorRect.new()
	over.color = col
	over.position = c.position - Vector2(w, w)
	over.size = c.size + Vector2(2 * w, 2 * w)
	# draw border rect behind: implement border as 4 strips via drawing panel style instead.
	# Simplest: replace _panel usage with styled ColorRect plus a border container.
	pass


func _sb(bg: Color, border: Color = Color.TRANSPARENT, bw := 0, r := 8) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	if bw > 0:
		sb.set_border_width_all(bw)
	sb.set_corner_radius_all(r)
	sb.content_margin_left = 10
	sb.content_margin_right = 10
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	return sb


func _make_btn(text: String, _cb_hint: String, size: int, kind: String) -> Button:
	## Minimal dark-system buttons: thin borders, white type, flat fills.
	## kinds: ghost lined primary muted gold buzz mc cell start
	var b := Button.new()
	b.text = text
	b.add_theme_font_override("font", Game.display_font)
	b.add_theme_font_size_override("font_size", size)
	b.focus_mode = Control.FOCUS_NONE
	var map := {
		"ghost":   [Color(1, 1, 1, 0.0), Game.SL_TXT, Game.SL_LINE, 1],
		"lined":   [Color(1, 1, 1, 0.0), Game.SL_TXT, Color(1, 1, 1, 0.55), 1],
		"primary": [Color("#1d9c4e"), Color.WHITE, Color.TRANSPARENT, 0],
		"start":   [Color("#1d9c4e"), Color.WHITE, Color.TRANSPARENT, 0],
		"muted":   [Color("#171b22"), Game.SL_TXT, Game.SL_LINE, 1],
		"gold":    [Color("#e9edf2"), Color("#0b0d11"), Color.TRANSPARENT, 0],
		"buzz":    [Color(0.6, 0.13, 0.10, 0.16), Color("#ffd9d4"), Color(1, 0.45, 0.38, 0.6), 1],
		"mc":      [Color(0.05, 0.06, 0.08, 0.85), Color("#eef1f6"), Color(1, 1, 1, 0.28), 1],
		"cell":    [Color("#0b0e13"), Color("#eef2f7"), Color(1, 1, 1, 0.16), 1],
	}
	var c: Array = map.get(kind, map["ghost"])
	var bg: Color = c[0]
	var fg: Color = c[1]
	var ln: Color = c[2]
	var bw: int = c[3]
	b.add_theme_stylebox_override("normal", _sbox(bg, ln, bw))
	b.add_theme_stylebox_override("hover", _sbox(_hover_bg(bg), Color(1, 1, 1, 0.6) if bw > 0 else Color.TRANSPARENT, bw))
	b.add_theme_stylebox_override("pressed", _sbox(_hover_bg(bg).darkened(0.15), ln, bw))
	b.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	b.add_theme_stylebox_override("disabled", _sbox(Color(1, 1, 1, 0.04), Color(1, 1, 1, 0.08), 1))
	b.add_theme_color_override("font_color", fg)
	b.add_theme_color_override("font_hover_color", Color.WHITE)
	b.add_theme_color_override("font_pressed_color", Color.WHITE)
	b.add_theme_color_override("font_disabled_color", Color("#4c5561"))
	b.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	return b


func _sbox(bg: Color, border: Color, bw: int) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	if bw > 0:
		sb.set_border_width_all(bw)
	sb.set_corner_radius_all(2)
	sb.content_margin_left = 14
	sb.content_margin_right = 14
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	return sb


func _hover_bg(bg: Color) -> Color:
	if bg.a < 0.02:
		return Color(1, 1, 1, 0.07)
	return bg.lightened(0.08)


func _style_line(line: LineEdit) -> void:
	line.add_theme_font_override("font", Game.font_sans)
	line.add_theme_font_size_override("font_size", 24)
	line.add_theme_stylebox_override("normal", _sb(Color("#0c1320"), Color("#3b5a86"), 2, 8))
	line.add_theme_stylebox_override("focus", _sb(Color("#0c1320"), Game.GOLD, 2, 8))
	line.add_theme_color_override("font_color", Color.WHITE)
	line.add_theme_color_override("caret_color", Color.WHITE)
	line.add_theme_color_override("font_placeholder_color", Color("#5b6b80"))
	line.text_direction = Control.TEXT_DIRECTION_AUTO


func _seg_bar(x: float, y: float, labels: Array, active: int, cb: Callable) -> HBoxContainer:
	var hb := HBoxContainer.new()
	hb.position = Vector2(x, y)
	hb.size = Vector2(360, 46)
	var tot := 360.0 / labels.size()
	for i in labels.size():
		var b := _make_btn(str(labels[i]), "", 20, "gold" if i == active else "ghost")
		b.custom_minimum_size = Vector2(tot - 4, 44)
		b.pressed.connect(cb.bind(i))
		hb.add_child(b)
	return hb


func _input(event: InputEvent) -> void:
	# splash: any key begins (ignore events still arriving during launch)
	if _phase == "splash":
		if Time.get_ticks_msec() - _t0 < 700:
			return
		if event is InputEventKey and event.pressed and not event.echo:
			_begin_from_splash()
		elif event is InputEventMouseButton and event.pressed:
			_begin_from_splash()
		return
	if event is InputEventKey and event.pressed and not event.echo:
		var code: int = (event as InputEventKey).keycode
		# typing fields swallow hotkeys
		var focus: Control = get_viewport().gui_get_focus_owner()
		if focus is LineEdit:
			return
		if _phase == "clue":
			if code == KEY_SPACE:
				_ring_key(0)
			elif code >= KEY_0 and code <= KEY_9:
				var n: int = code - KEY_0
				if n >= 1:
					_ring_key(n - 1)
		elif _phase == "board" and code == KEY_SPACE:
			pass  # mouse-driven selection


func _ring_key(i: int) -> void:
	if i >= _players.size():
		return
	var p: Player = _players[i]
	if p.is_bot:
		return
	_try_ring(i)


func _begin_from_splash() -> void:
	_go_lobby()


func _on_typed_submit(txt: String) -> void:
	_submit_typed(txt)


# -- misc aliases required by references above (kept small) -------------------
func _dummy() -> void:
	pass
