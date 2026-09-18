#!/usr/bin/env python3
"""Put a course's music pack into the shape the engine resolves.

A pack arrives as a folder of 24-bit WAVs named after what they are and how
long they run. The engine knows neither: it asks for a *slot* -- `menu_theme`,
`correct`, `final` -- and resolves it through the course's own `EDITION_SOUND`
to `courses/<id>/assets/audio/<file>.m4a`. So a pack has to be renamed into the
slot names, and it has to become m4a, because the shell plays m4a and mp3 and
nothing else. A WAV in that folder is a file the game cannot hear.

Two things follow from the house format and are not free choices:

  * 44100 Hz, stereo, AAC around 128 kbps. That is what MAIN's whole
    soundtrack is, and a course that lands at 48 kHz lands eight per cent
    heavier for no audible gain on a phone speaker.
  * the ten `course_*` slots are the ones every course has. They are what a
    course's `course.js` points at. Anything the pack carries beyond them --
    a week stinger, a hard-thinking bed -- is staged under its own name so a
    later `SOUND` table can reach it without the file moving.

The silent placeholders are part of the same job. A host whose lines are
written but not yet recorded still needs a clip behind every cue, because the
bubble on the floor is measured by the audio that is playing: no file means no
duration means a bubble that closes on the next frame. So each course gets a
pair of silent m4a files -- one the length of a verdict line, one the length of
a spoken scene -- and its `EDITION_SOUND` points every one of its host cues at
them. When the voice is cloned, the substitution is deleted per cue and the
real clip lands under the cue's own name.

    python3 Tools/stage_course_audio.py --course qajars
    python3 Tools/stage_course_audio.py --course pahlavis
    python3 Tools/stage_course_audio.py --course qajars --check

Deterministic in what it names, not in what it writes: afconvert is a lossy
encoder, so a re-run replaces the file with a different one of the same length
and the same loudness. Re-run it only when the pack changes.
"""

import argparse
import os
import subprocess
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RATE = 44100
CHANNELS = 2
BITRATE = '128000'

# One entry per course. `pack` is the folder as delivered; `slots` maps a file
# inside it to the name it is staged under; `extras` is everything in the pack
# that no engine slot claims.
#
# Every `pack` points *inside* this tree, under `Course/Masters/<course>/`, and
# never at the Desktop the pack was handed over on. A delivered folder is a drop
# folder only until the drop is over; a mapping that points at one is a mapping
# that stops resolving the first time the Desktop is swept. So the delivery is
# copied into the tree, checksummed against what it came from, and mapped from
# there -- after which the copy on the Desktop is a stray and belongs to whoever
# made the delivery.
PACKS = {
    'qajars': {
        'pack': os.path.join(ROOT, 'Course', 'Masters', 'Qajars', 'Soundtrack'),
        'slots': {
            '01_music_beds/01_qajar_main_theme_polished_70s.wav': 'course_splash',
            '01_music_beds/02_qajar_lobby_archive_loop_polished_64s.wav': 'course_theme',
            '01_music_beds/03_qajar_thinking_standard_loop_polished_30s.wav': 'course_thinking',
            '01_music_beds/05_qajar_final_jeopardy_polished_30s.wav': 'course_final',
            '01_music_beds/06_qajar_results_restrained_victory_polished_22s.wav': 'course_winner',
            '02_stingers/03_qajar_daily_double_polished_8s.wav': 'course_daily_double',
            '03_sfx/01_qajar_category_select_polished_1s.wav': 'course_select',
            '03_sfx/02_qajar_buzzed_first_lockin_polished_1s.wav': 'course_lock_in',
            '03_sfx/03_qajar_correct_answer_polished_2s.wav': 'course_correct',
            '03_sfx/04_qajar_wrong_answer_polished_2s.wav': 'course_wrong',
        },
        'extras': {
            '01_music_beds/04_qajar_thinking_hard_loop_polished_30s.wav': 'qajar_thinking_hard',
            '02_stingers/01_qajar_board_reveal_polished_6s.wav': 'qajar_board_reveal',
            '02_stingers/02_qajar_clue_reveal_polished_2s.wav': 'qajar_clue_reveal',
            '02_stingers/04_qajar_countdown_last_5s_polished.wav': 'qajar_countdown',
            '02_stingers/05_qajar_end_round_ledger_polished_10s.wav': 'qajar_end_round',
            '02_stingers/06_week1_russo_iranian_wars_polished_6s.wav': 'qajar_week1_russo_iranian_wars',
            '02_stingers/07_week2_ulama_authority_polished_6s.wav': 'qajar_week2_ulama_authority',
            '02_stingers/08_week3_army_reform_failed_modernity_polished_6s.wav': 'qajar_week3_army_reform',
            '02_stingers/09_week4_reformist_thought_polished_6s.wav': 'qajar_week4_reformist_thought',
            '02_stingers/10_week5_tobacco_protest_polished_6s.wav': 'qajar_week5_tobacco_protest',
            '02_stingers/11_week6_constitutional_revolution_polished_7s.wav': 'qajar_week6_constitutional_revolution',
            '02_stingers/12_week7_britain_russia_great_game_polished_7s.wav': 'qajar_week7_britain_russia_great_game',
            '02_stingers/13_week8_women_political_life_polished_7s.wav': 'qajar_week8_women_political_life',
        },
    },
    'pahlavis': {
        # V3 reads from inside the tree. Its delivered copy sits loose on the
        # Desktop, which is where a project's drop folder goes when the drop is
        # over, so the masters were archived under `Course/Masters/` with the
        # other courses' and the mapping points there: a re-stage after the
        # Desktop is cleaned still names a path that exists.
        'pack': os.path.join(ROOT, 'Course', 'Masters', 'Pahlavis', 'Soundtrack'),
        'slots': {
            # Nine, not ten: the pack carries no results bed, and no winner cue
            # was cut from one. `app.js` fires `winner` when the trophy lands, so
            # a Pahlavis match ends on the engine's own sting.
            '01_Pahlavi_Main_Theme_65s.wav': 'course_theme',
            '17_Splash_Theme.wav': 'course_splash',
            '02_Thinking_Loop_30s.wav': 'course_thinking',
            '03_Daily_Double.wav': 'course_daily_double',
            '04_Final_Round_45s.wav': 'course_final',
            '13_Correct_Answer.wav': 'course_correct',
            '14_Wrong_Answer.wav': 'course_wrong',
            '15_Buzzed_First_LockIn.wav': 'course_lock_in',
            '16_Category_Selection.wav': 'course_select',
        },
        'extras': {
            # The eight taught weeks, in seminar order. Nothing plays them yet;
            # they are staged under their own names so that wiring one up is a
            # line in the engine rather than a re-cut of the album.
            '05_1921_Coup.wav': 'pahlavi_week1_1921_coup',
            '06_Reza_Shah_State_Building.wav': 'pahlavi_week2_reza_shah',
            '07_Allied_Occupation_1941.wav': 'pahlavi_week3_allied_occupation',
            '08_Mossadegh_Oil_1953.wav': 'pahlavi_week4_mossadegh_oil',
            '09_White_Revolution.wav': 'pahlavi_week5_white_revolution',
            '10_The_Left.wav': 'pahlavi_week6_the_left',
            '11_Gender_and_Modernity.wav': 'pahlavi_week7_gender_modernity',
            '12_Iran_and_the_Cold_War.wav': 'pahlavi_week8_cold_war',
        },
    },
}

# What the placeholder pair is cut to. A verdict line is one sentence and lands
# around three seconds; a scene line is a short paragraph. Both are the length
# the bubble is on the floor, so they are reading times, not arbitrary numbers.
PLACEHOLDERS = {'host_line_placeholder': 3.4, 'host_scene_placeholder': 9.0}


def encode(src, dst):
    """afconvert is the one tool on this machine that writes what the shell
    plays. libmp3lame is not installed and a bare AAC at 48 kHz is the louder
    file, not the better one."""
    cmd = ['afconvert', '-f', 'm4af', '-d', 'aac@%d' % RATE, '-b', BITRATE,
           src, dst]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.PIPE)


def write_silence(dst, seconds):
    """A WAV of digital silence, then encoded. Not an empty file: the browser
    has to be able to read a duration off it, and a cue with no duration holds
    the floor for no time at all."""
    tmp = dst + '.silence.wav'
    frames = int(RATE * seconds)
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(CHANNELS)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b'\x00' * (CHANNELS * 2 * frames))
    try:
        encode(tmp, dst)
    finally:
        os.unlink(tmp)
    return frames


def stage(course, check, placeholders_only):
    spec = PACKS[course]
    pack = spec['pack']
    out = os.path.join(ROOT, 'Web', 'courses', course, 'assets', 'audio')

    if placeholders_only:
        if not check:
            os.makedirs(out, exist_ok=True)
        for name, seconds in sorted(PLACEHOLDERS.items()):
            dst = os.path.join(out, name + '.m4a')
            if check:
                print('  %-38s <- %gs of silence' % (name + '.m4a', seconds))
                continue
            write_silence(dst, seconds)
            print('  %-38s %7d bytes' % (name + '.m4a', os.path.getsize(dst)))
        return

    if not os.path.isdir(pack):
        sys.exit('missing pack: %s' % pack)

    plan = sorted(spec['slots'].items()) + sorted(spec['extras'].items())
    missing = [src for src, _ in plan if not os.path.exists(os.path.join(pack, src))]
    if missing:
        sys.exit('the pack no longer holds these files, so the mapping has '
                 'drifted:\n  ' + '\n  '.join(missing))

    # Every file in the pack has to appear in the plan. A pack that gained a
    # track would otherwise stage silently and the new track would be a file
    # nobody could name.
    staged = {src for src, _ in plan}
    loose = []
    for base, _dirs, names in os.walk(pack):
        for n in names:
            if not n.lower().endswith('.wav'):
                continue
            rel = os.path.relpath(os.path.join(base, n), pack)
            if rel not in staged:
                loose.append(rel)
    if loose:
        sys.exit('the pack holds wavs no slot claims:\n  ' + '\n  '.join(sorted(loose)))

    if not check:
        os.makedirs(out, exist_ok=True)

    for src, name in plan:
        dst = os.path.join(out, name + '.m4a')
        if check:
            print('  %-38s <- %s' % (name + '.m4a', src))
            continue
        encode(os.path.join(pack, src), dst)
        print('  %-38s %7d bytes' % (name + '.m4a', os.path.getsize(dst)))

    for name, seconds in sorted(PLACEHOLDERS.items()):
        dst = os.path.join(out, name + '.m4a')
        if check:
            print('  %-38s <- %gs of silence' % (name + '.m4a', seconds))
            continue
        write_silence(dst, seconds)
        print('  %-38s %7d bytes' % (name + '.m4a', os.path.getsize(dst)))

    print('%s: %d slots, %d extras, %d placeholders -> %s'
          % (course, len(spec['slots']), len(spec['extras']),
             len(PLACEHOLDERS), os.path.relpath(out, ROOT)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--course', required=True, choices=sorted(PACKS))
    ap.add_argument('--check', action='store_true',
                    help='name the files that would be written, write nothing')
    ap.add_argument('--placeholders', action='store_true',
                    help='cut the silent cue files only, leave the pack alone')
    args = ap.parse_args()
    stage(args.course, args.check, args.placeholders)


if __name__ == '__main__':
    main()
