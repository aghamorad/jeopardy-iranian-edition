extends Node
## Global language + visual system for Jeopardy - Iranian Edition.

var lang: String = "en"   # "en" | "fa"

# ---- Archival-Iranian palette -----------------------------------------------
const INK       := Color("#0b0e15")
const INK_HI    := Color("#111624")
const PANEL     := Color("#151c2a")
const CARD      := Color("#1b2434")
const CARD_HI   := Color("#25314a")
const BORDER    := Color("#33405c")
const BRONZE    := Color("#c9a24b")
const BRONZE_D  := Color("#8a6d2e")
const GOLD      := Color("#e6c873")
const PARCH     := Color("#eae2d2")
const MUTED     := Color("#93a0b4")
const NAVY      := Color("#0d1b3e")
const NAVY_LO   := Color("#081020")
const RED       := Color("#b23a33")
const GREEN     := Color("#27a05c")
const IRAN_G    := Color("#239f40")
const IRAN_R    := Color("#da291c")
const IRAN_W    := Color("#f3f3f3")

# ---- Sleek dark system (single source: the 3 reference frames) --------------
# near-black cinematic base, white typography, restrained green-left/red-right,
# thin borders, subtle glow. No blue-and-gold.
const SL_TOP     := Color("#0d1118")   # night sky
const SL_BOTTOM  := Color("#04060a")   # floor / deepest black
const SL_TXT     := Color("#f2f4f7")   # primary text (near-white)
const SL_SOFT    := Color("#c7cdd8")   # secondary text
const SL_DIM     := Color("#8a94a2")   # muted / hints
const SL_FAINT   := Color(1, 1, 1, 0.42)
const SL_LINE    := Color(1, 1, 1, 0.16)    # thin border
const SL_LINE_HI := Color(1, 1, 1, 0.34)
const SL_GRN     := Color("#2fae58")   # Iranian green (accent, LEFT)
const SL_RED     := Color("#e5483f")   # Iranian red   (accent, RIGHT)
const SL_CELL    := Color(0.035, 0.04, 0.05, 0.78)  # translucent tile

# ---- Fonts ------------------------------------------------------------------
var font_sans: FontFile
var display_font: FontVariation  # pseudo-bold for titles / wordmark
var _loaded := false

const FA_DIGITS := ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"]


func _ensure_fonts() -> void:
	if _loaded:
		return
	_loaded = true
	font_sans = FontFile.new()
	var err := font_sans.load_dynamic_font("res://assets/fonts/iransans.ttf")
	if err == OK:
		font_sans.antialiasing = TextServer.FONT_ANTIALIASING_GRAY
		# IRANSansWeb does not carry every Latin glyph; let missing ones fall
		# back to the OS so English never renders as tofu.
		font_sans.allow_system_fallback = true
	display_font = FontVariation.new()
	display_font.base_font = font_sans
	display_font.variation_embolden = 1.2


func t(en: String, fa: String) -> String:
	return fa if lang == "fa" else en


func fa_int(n: int) -> String:
	var s := str(n)
	var out := ""
	for ch in s:
		if ch >= "0" and ch <= "9":
			out += FA_DIGITS[ch.to_int()]
		else:
			out += ch
	return out


func digits(s: String) -> String:
	if lang != "fa":
		return s
	var out := ""
	for ch in s:
		if ch >= "0" and ch <= "9":
			out += FA_DIGITS[ch.to_int()]
		else:
			out += ch
	return out


func _group(n: int, sep: String) -> String:
	var neg := ""
	var v := n
	if v < 0:
		neg = "-"
		v = -v
	var s := str(v)
	var out := ""
	var cnt := 0
	for i in range(s.length() - 1, -1, -1):
		out = s[i] + out
		cnt += 1
		if cnt == 3 and i != 0:
			out = sep + out
			cnt = 0
	return neg + out


func money_full(n: int) -> String:
	## Localized grouped integer: 25,000,000 / ۲۵٬۰۰۰٬۰۰۰
	if lang == "fa":
		var g := _group(n, "٬")
		var out := ""
		for ch in g:
			if ch >= "0" and ch <= "9":
				out += FA_DIGITS[ch.to_int()]
			else:
				out += ch
		return out
	return _group(n, ",")


func money_unit(n: int) -> String:
	## Compact broadcast label: ۲۵ میلیون تومان / 25 million toman
	var neg := ""
	var v := n
	if v < 0:
		neg = "-"
		v = -v
	var base: float = float(v)
	var unit := ""
	if v >= 1_000_000_000:
		base = float(v) / 1_000_000_000.0
		unit = t("billion", "میلیارد")
	elif v >= 1_000_000:
		base = float(v) / 1_000_000.0
		unit = t("million", "میلیون")
	elif v >= 1_000:
		base = float(v) / 1_000.0
		unit = t("thousand", "هزار")
	else:
		base = float(v)
	if base == floor(base):
		return "%s%s %s %s" % [neg, digits(str(int(base))), unit, t("toman", "تومان")]
	var one := str(int(base))
	var dec := str(int(round((base - floor(base)) * 10.0)))
	if lang == "fa":
		return "%s%s٫%s %s %s" % [neg, digits(one), digits(dec), unit, "تومان"]
	return "%s%s.%s %s toman" % [neg, one, dec, unit]


func tooman(n: int, with_label := true) -> String:
	if with_label:
		return "%s %s" % [money_full(n), t("toman", "تومان")]
	return money_full(n)


func is_rtl() -> bool:
	return lang == "fa"


func h_align(ltr_align: int) -> int:
	## 0 = LEFT, 1 = CENTER, 2 = RIGHT (HorizontalAlignment).
	if is_rtl():
		if ltr_align == 0: return 2
		if ltr_align == 2: return 0
	return ltr_align


# ---- Text styling -----------------------------------------------------------
func styled_label(text_: String, size: int, color: Color = PARCH,
		halign := 0, boldish := false, custom_font: Font = null) -> Label:
	var lb := Label.new()
	lb.text = text_
	var use_font: Font = custom_font if custom_font else font_sans
	lb.add_theme_font_override("font", use_font)
	lb.add_theme_font_size_override("font_size", size)
	lb.add_theme_color_override("font_color", color)
	lb.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.55))
	lb.add_theme_constant_override("shadow_offset_x", 1)
	lb.add_theme_constant_override("shadow_offset_y", 2)
	lb.add_theme_constant_override("outline_size", 0)
	lb.horizontal_alignment = halign if not is_rtl() else (2 if halign == 0 else halign)
	lb.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART if size < 40 else TextServer.AUTOWRAP_OFF
	if is_rtl():
		lb.text_direction = Control.TEXT_DIRECTION_RTL
	lb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return lb


func title(text_: String, size := 46, color: Color = BRONZE) -> Label:
	return styled_label(text_, size, color, 1)
