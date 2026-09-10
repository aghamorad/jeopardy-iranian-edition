extends Control
## Procedural Tehran backdrop — Alborz ridgelines, Milad Tower, reflective floor.
## Drawn once per screen in-engine (never a static pasted image), very low key so
## UI text stays crisp. Tune with `strength` (overall) and `tower_center` (0..1).

var strength := 1.0
var tower_center := 0.5
var tower_alpha := 0.34

var _rads := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _draw() -> void:
	var w := size.x
	var h := size.y
	if w <= 0 or h <= 0:
		return
	var s := clampf(strength, 0.0, 1.0)
	# night-sky gradient (deep slate -> black)
	var bands := 28
	for i in bands:
		var f := float(i) / float(bands)
		var col := Color(0.10, 0.115, 0.16).lerp(Color(0.028, 0.033, 0.045), f)
		var y0 := h * f
		draw_rect(Rect2(0, y0, w, h / bands + 1.0), col)

	var horizon := h * 0.72

	# ---- far Alborz ridge (subtle) ----
	_ridge(horizon, 0.30, Color(0.82, 0.86, 1.0, 0.10 * s), w, h, 140.0)
	# ---- nearer ridge (a touch darker/heavier) ----
	_ridge(horizon, 0.10, Color(0.60, 0.65, 0.82, 0.13 * s), w, h, 84.0)

	# ---- Milad Tower silhouette ----
	_draw_tower(w * tower_center, horizon, h, tower_alpha * s, w)

	# ---- reflective dark floor ----
	var fy := horizon + h * 0.01
	var fh := h - fy
	var fb := 22
	for i in fb:
		var f := float(i) / float(fb)
		var col := Color(0.028, 0.033, 0.045).lerp(Color(0.02, 0.024, 0.034), f)
		draw_rect(Rect2(0, fy + fh * f, w, fh / fb + 1.0), col)
	# subtle floor sheen: faint reflection pools under the tower
	var tw := w * tower_center
	_draw_glow(tw, fy + fh * 0.30, w * 0.16, Color(0.5, 0.55, 0.8, 0.05 * s))
	_draw_glow(tw, fy + fh * 0.78, w * 0.05, Color(0.8, 0.7, 0.55, 0.05 * s))


func _ridge(base_y: float, amp_frac: float, col: Color, w: float, h: float, step: float) -> void:
	## Low-poly ridge using deterministic pseudo-noise.
	var amp := h * amp_frac
	var pts := PackedVector2Array()
	var n := int(w / step) + 1
	for i in range(n + 1):
		var x := float(i) * step
		if x > w:
			break
		var t := x / w
		var nz := _noise(t * 6.0) * 0.5 + _noise(t * 13.0 + 3.0) * 0.5
		var y := base_y - amp * (0.35 + 0.65 * nz)
		pts.append(Vector2(x, y))
	# close to the floor at right and left edges so it reads as a clean mass
	pts.append(Vector2(w, h))
	pts.append(Vector2(0, h))
	draw_colored_polygon(pts, col)


func _noise(x: float) -> float:
	return 0.5 + 0.5 * sin(x * 1.7 + _rads[0]) * 0.4 + 0.3 * sin(x * 3.1 + _rads[1]) + 0.2 * sin(x * 7.3)


func _draw_tower(cx: float, ground: float, h: float, a: float, w: float) -> void:
	if a <= 0.003:
		return
	var col := Color(0.90, 0.93, 1.0, a)
	# antenna + upper stem (thin)
	var base_top := ground - h * 0.56
	var x_half := w * 0.006
	draw_rect(Rect2(cx - x_half, base_top - h * 0.06, x_half * 2.0, h * 0.56), col)
	# viewing pod: bulb at ~ mid height + upper pod
	var pod_y := ground - h * 0.44
	var pod_h := h * 0.10
	draw_circle(Vector2(cx, pod_y), x_half * 3.4, col)
	draw_rect(Rect2(cx - x_half * 3.4, pod_y, x_half * 6.8, pod_h * 1.5), col)
	# lower skirt flares wider then tapers to a tripod base
	draw_colored_polygon(PackedVector2Array([
		Vector2(cx - x_half * 2.2, pod_y + pod_h * 2.0),
		Vector2(cx + x_half * 2.2, pod_y + pod_h * 2.0),
		Vector2(cx + x_half * 1.1, ground - h * 0.10),
		Vector2(cx - x_half * 1.1, ground - h * 0.10),
	]), col)


func _draw_glow(cx: float, cy: float, rad: float, col: Color) -> void:
	## Cheap radial glow via stacked translucent circles.
	var steps := 12
	for i in steps:
		var f := float(i) / float(steps)
		var c := Color(col.r, col.g, col.b, col.a * (1.0 - f))
		draw_circle(Vector2(cx, cy), rad * (1.0 - f * 0.85), c)
