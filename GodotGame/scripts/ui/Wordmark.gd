class_name Wordmark
extends Control
## Draws "JE◉PARDY" style wordmark: letters via a Font, with a square emblem
## texture substituted for the O so the Iranian emblem sits in the brand mark.

var font: Font
var px := 60
var letter_color := Color.WHITE
var emblem_tex: Texture2D
var emblem_color := Color(0.85, 0.19, 0.12)
var with_bang := false       # append "!" after PARDY
var letters_a := "JE"        # pre-O segment
var letters_b := "PARDY"     # post-O segment
var spacing := 0.06          # extra fraction of px between glyph runs

func _draw() -> void:
	if font == null:
		return
	var f := font
	var fs := px
	var base := f.get_ascent(fs)
	var cursor := 0.0
	var seg_a := f.get_string_size(letters_a, HORIZONTAL_ALIGNMENT_LEFT, -1, fs)
	var seg_b := f.get_string_size(letters_b, HORIZONTAL_ALIGNMENT_LEFT, -1, fs)
	var o_w := f.get_string_size("O", HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	var bang := f.get_string_size("!", HORIZONTAL_ALIGNMENT_LEFT, -1, fs) if with_bang else Vector2.ZERO
	var gap := spacing * fs

	# Baseline so the cap height sits inside the control.
	var baseline := base * 1.04
	var center_y := baseline - base * 0.5

	draw_string(f, Vector2(cursor, baseline), letters_a, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, letter_color)
	cursor += seg_a.x + gap

	# Emblem O: fill the glyph box, vertically centered on the cap line.
	if emblem_tex != null:
		var tex := emblem_tex
		var aspect := float(tex.get_width()) / float(tex.get_height())
		var draw_w := o_w
		var draw_h := draw_w / aspect
		var ox := cursor
		var oy := center_y - draw_h * 0.5
		draw_texture_rect(tex, Rect2(ox, oy, draw_w, draw_h), false, emblem_color)
	cursor += o_w + gap

	draw_string(f, Vector2(cursor, baseline), letters_b, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, letter_color)
	cursor += seg_b.x
	if with_bang:
		cursor += gap
		draw_string(f, Vector2(cursor, baseline), "!", HORIZONTAL_ALIGNMENT_LEFT, -1, fs, letter_color)


func _min_size() -> Vector2:
	if font == null:
		return Vector2(200, 60)
	var fs := px
	var line_h := font.get_height(fs)
	var w := font.get_string_size(letters_a, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	w += spacing * fs
	w += font.get_string_size("O", HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	w += spacing * fs
	w += font.get_string_size(letters_b, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	if with_bang:
		w += spacing * fs + font.get_string_size("!", HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	custom_minimum_size = Vector2(w, line_h)
	return Vector2(w, line_h)


func set_mark(p: Font, size: int, lcol: Color, tex: Texture2D, ecol: Color, bang := false) -> void:
	font = p
	px = size
	letter_color = lcol
	emblem_tex = tex
	emblem_color = ecol
	with_bang = bang
	_min_size()
	queue_redraw()
