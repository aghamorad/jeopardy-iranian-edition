extends Node
## Audio system for Jeopardy - Iranian Edition.
## Buses: Music (title/theme bed), Ambience (clue thinking / sting), SFX (cues),
##        Voice (announcer). Voiceovers duck the music/ambience automatically.

signal voice_finished

var _voice: AudioStreamPlayer
var _music: AudioStreamPlayer
var _amb: AudioStreamPlayer
var _pool: Array = []

var _music_cue := ""
var _amb_tw: Tween
var _mus_tw: Tween

const MUSIC_DB := -6.0
const AMB_DB := -8.0
const DUCK_DB := -18.0

var _restore_after := false


func _ready() -> void:
	_ensure_bus("Music")
	_ensure_bus("Ambience")
	_ensure_bus("SFX")
	_ensure_bus("Voice")

	_music = AudioStreamPlayer.new()
	_music.bus = "Music"
	add_child(_music)
	_amb = AudioStreamPlayer.new()
	_amb.bus = "Ambience"
	add_child(_amb)
	_voice = AudioStreamPlayer.new()
	_voice.bus = "Voice"
	add_child(_voice)
	for i in 6:
		var p := AudioStreamPlayer.new()
		p.bus = "SFX"
		add_child(p)
		_pool.append(p)

	# music beds
	_register("theme_title", "res://assets/sounds/theme_title.wav", "music")      # 65s main theme
	_register("results_theme", "res://assets/sounds/menu_theme.wav", "music")      # results bed
	# ambience beds (clue thinking + transitions)
	_register("think_loop", "res://assets/sounds/think_loop.wav", "amb")
	_register("final_music", "res://assets/sounds/final_music.wav", "amb")
	_register("sting_double", "res://assets/sounds/sting_double.wav", "amb")
	# authoritative gameplay SFX (fixed cues)
	_register("select", "res://assets/sounds/z_select_category.wav", "sfx")  # = jeopardy_category_selection
	_register("buzz", "res://assets/sounds/z_lockin.wav", "sfx")             # = jeopardy_buzzed_first_lockin
	_register("correct", "res://assets/sounds/z_correct.wav", "sfx")         # = jeopardy_correct_answer_happy
	_register("wrong", "res://assets/sounds/z_wrong.wav", "sfx")             # = jeopardy_wrong_answer_buzzer
	# results fanfare (composer original, separate from fixed cues)
	_register("winner", "res://assets/sounds/winner.wav", "sfx")
	# voiceovers (announcer)
	_register("announce_open", "res://assets/sounds/announce_open.mp3", "voice")
	_register("challenge_open", "res://assets/sounds/challenge_open.mp3", "voice")


func _register(cue: String, path: String, kind: String) -> void:
	_sounds[cue] = {"path": path, "kind": kind}


func _ensure_bus(name: String) -> void:
	if AudioServer.get_bus_index(name) == -1:
		AudioServer.add_bus()
		AudioServer.set_bus_name(AudioServer.bus_count - 1, name)
		AudioServer.set_bus_send(AudioServer.bus_count - 1, "Master")


var _sounds := {}


func _load(path: String) -> AudioStream:
	if ResourceLoader.exists(path):
		return load(path)
	push_warning("Missing audio: " + path)
	return null


func _next_sfx() -> AudioStreamPlayer:
	for p in _pool:
		if not p.playing:
			return p
	return _pool[0]


func _set_loop(s: AudioStream, on: bool) -> void:
	if s is AudioStreamWAV:
		var w := s as AudioStreamWAV
		w.loop_mode = AudioStreamWAV.LOOP_FORWARD if on else AudioStreamWAV.LOOP_DISABLED
		w.loop_begin = 0
		if w.data != null and w.data.size() > 0:
			w.loop_end = w.data.size() / 4
	elif s is AudioStreamOggVorbis:
		(s as AudioStreamOggVorbis).loop = on
	elif s is AudioStreamMP3:
		(s as AudioStreamMP3).loop = on


# ---- SFX --------------------------------------------------------------------
func sfx(cue: String, vol := 0.0) -> void:
	var info = _sounds.get(cue)
	if info == null or info.kind != "sfx":
		return
	var s := _load(info.path)
	if s == null:
		return
	var p := _next_sfx()
	p.stream = s
	p.volume_db = vol
	p.play()


# ---- Music / ambience beds ---------------------------------------------------
func music(cue: String, vol := MUSIC_DB) -> void:
	var info = _sounds.get(cue)
	if info == null or info.kind != "music":
		return
	var s := _load(info.path)
	if s == null:
		return
	# keep the same bed running across screen rebuilds
	if _music_cue == cue and _music.playing:
		return
	_music_cue = cue
	_set_loop(s, true)
	_music.stream = s
	_music.volume_db = vol
	if _mus_tw:
		_mus_tw.kill()
	if not _music.playing:
		_music.play()


func stop_music(fade := 0.4) -> void:
	if _music.playing:
		_mus_tw = create_tween()
		_mus_tw.tween_property(_music, "volume_db", -40.0, fade)
		_mus_tw.tween_callback(func():
			_music.stop()
			_music.volume_db = MUSIC_DB)
	_music_cue = ""


func amb(cue: String, vol := AMB_DB, loop := true) -> void:
	## Bed that can be stopped instantly. `loop = false` plays a one-shot sting.
	var info = _sounds.get(cue)
	if info == null or info.kind != "amb":
		return
	var s := _load(info.path)
	if s == null:
		return
	if _amb_tw:
		_amb_tw.kill()
	_set_loop(s, loop)
	_amb.stream = s
	_amb.volume_db = vol
	_amb.play()


func stop_amb(fade := 0.1) -> void:
	if _amb.playing:
		_amb_tw = create_tween()
		_amb_tw.tween_property(_amb, "volume_db", -60.0, fade)
		_amb_tw.tween_callback(func():
			_amb.stop()
			_amb.volume_db = AMB_DB)


# ---- Voice (announcer). Ducks music/ambience while talking. ------------------
func voice(cue: String) -> void:
	var info = _sounds.get(cue)
	if info == null or info.kind != "voice":
		return
	var s := _load(info.path)
	if s == null:
		return
	_voice.stream = s
	_voice.volume_db = 0.0
	if _voice.playing:
		_voice.stop()
	_voice.play()
	_restore_after = true
	# duck beds under the voiceover
	var mus := _music.volume_db
	var ambv := _amb.volume_db
	var tw := create_tween().set_parallel(true)
	tw.tween_property(_music, "volume_db", DUCK_DB, 0.15)
	tw.tween_property(_amb, "volume_db", DUCK_DB, 0.15)
	# restore when it finishes
	var fin := _voice.finished.connect(func():
		if not _restore_after:
			return
		_restore_after = false
		var tw2 := create_tween().set_parallel(true)
		tw2.tween_property(_music, "volume_db", mus, 0.35)
		tw2.tween_property(_amb, "volume_db", ambv, 0.35)
		voice_finished.emit(), CONNECT_ONE_SHOT)


# ---- volume -----------------------------------------------------------------
func _bus(name: String) -> int:
	var i := AudioServer.get_bus_index(name)
	return i if i != -1 else 0


func set_vol(bus: String, v: float) -> void:
	AudioServer.set_bus_volume_db(_bus(bus), linear_to_db(clampf(v, 0.0001, 1.0)))
