#!/usr/bin/env python3
import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100

def write_wav_file(filepath, samples, channels=1):
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        max_v = max(abs(s) for s in samples) if samples else 0
        scale = 28000.0 / max_v if max_v > 0 else 1.0
        raw = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32768, min(32767, val))
            raw.extend(struct.pack('<h', val))
        wav.writeframes(raw)
    print(f"Generated {filepath} ({len(samples)/(SAMPLE_RATE*channels):.2f}s)")

def synthesize_jeopardy_main_theme():
    # 12-Second High-Energy TV Game Show Orchestral Theme
    # Brass Fanfare, Xylophone, Walking Bass, Percussion, and Broadcast Chords
    duration = 12.0
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Tempo: 132 BPM -> ~0.4545s per beat
    beat = 60.0 / 132.0

    # Drum track (Kick, Snare, Hi-hat)
    num_beats = int(duration / beat)
    for b in range(num_beats):
        b_time = b * beat
        b_pos = int(b_time * SAMPLE_RATE)
        # Kick on 1 and 3 (b % 4 == 0 or 2)
        if b % 2 == 0:
            for i in range(int(0.12 * SAMPLE_RATE)):
                t = i / SAMPLE_RATE
                f = 120.0 * math.exp(-25.0 * t)
                env = math.exp(-18.0 * t)
                if b_pos + i < total_samples:
                    samples[b_pos + i] += math.sin(2 * math.pi * f * t) * env * 12000.0
        # Snare on 2 and 4 (b % 2 == 1)
        if b % 2 == 1:
            for i in range(int(0.18 * SAMPLE_RATE)):
                t = i / SAMPLE_RATE
                noise = random.uniform(-1.0, 1.0)
                body = math.sin(2 * math.pi * 180.0 * t) * 0.4
                env = math.exp(-15.0 * t)
                if b_pos + i < total_samples:
                    samples[b_pos + i] += (noise + body) * env * 10000.0
        # Hi-hat on every half-beat
        for sub in [0.0, 0.5]:
            hh_pos = int((b_time + sub * beat) * SAMPLE_RATE)
            for i in range(int(0.04 * SAMPLE_RATE)):
                t = i / SAMPLE_RATE
                noise = random.uniform(-1.0, 1.0)
                env = math.exp(-60.0 * t)
                if hh_pos + i < total_samples:
                    samples[hh_pos + i] += noise * env * 4000.0

    # Walking Bassline (Funk/Game Show Jazz in C Major / A Minor)
    bass_notes = [
        # Measure 1 (C - E - G - A)
        (130.81, 0 * beat, beat), (164.81, 1 * beat, beat), (196.00, 2 * beat, beat), (220.00, 3 * beat, beat),
        # Measure 2 (Bb - G - E - C)
        (233.08, 4 * beat, beat), (196.00, 5 * beat, beat), (164.81, 6 * beat, beat), (130.81, 7 * beat, beat),
        # Measure 3 (F - A - C - D)
        (174.61, 8 * beat, beat), (220.00, 9 * beat, beat), (261.63, 10 * beat, beat), (293.66, 11 * beat, beat),
        # Measure 4 (G - B - D - F)
        (196.00, 12 * beat, beat), (246.94, 13 * beat, beat), (293.66, 14 * beat, beat), (349.23, 15 * beat, beat),
        # Measure 5-6 (Climax Chords)
        (130.81, 16 * beat, beat * 2), (174.61, 18 * beat, beat * 2), (196.00, 20 * beat, beat * 2), (261.63, 22 * beat, beat * 4)
    ]
    for freq, start, dur in bass_notes:
        pos = int(start * SAMPLE_RATE)
        sub_len = int(dur * SAMPLE_RATE)
        for i in range(sub_len):
            if pos + i < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-2.5 * t)
                # Funky slap/electric bass
                val = math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(4 * math.pi * freq * t) + 0.15 * math.sin(6 * math.pi * freq * t)
                samples[pos + i] += val * env * 9000.0

    # Orchestral Brass Fanfare Melody (Trombones & Trumpets)
    # The classic uplifting TV game show opening hook!
    melody = [
        # Catchy syncopated game show hook
        (523.25, 0.0 * beat, 0.4 * beat),   # C5
        (523.25, 0.5 * beat, 0.4 * beat),   # C5
        (659.25, 1.0 * beat, 0.8 * beat),   # E5
        (783.99, 2.0 * beat, 0.8 * beat),   # G5
        (880.00, 3.0 * beat, 0.6 * beat),   # A5
        (783.99, 3.75 * beat, 1.2 * beat),  # G5

        (523.25, 5.0 * beat, 0.4 * beat),   # C5
        (659.25, 5.5 * beat, 0.4 * beat),   # E5
        (783.99, 6.0 * beat, 0.8 * beat),   # G5
        (1046.50, 7.0 * beat, 1.8 * beat),  # C6 (High fanfare!)

        (880.00, 9.0 * beat, 0.4 * beat),   # A5
        (987.77, 9.5 * beat, 0.4 * beat),   # B5
        (1046.50, 10.0 * beat, 0.8 * beat), # C6
        (880.00, 11.0 * beat, 0.8 * beat),  # A5
        (783.99, 12.0 * beat, 0.8 * beat),  # G5
        (659.25, 13.0 * beat, 0.8 * beat),  # E5

        # Grand Resolution Stabs
        (523.25, 14.0 * beat, 0.3 * beat),  # C5
        (659.25, 14.5 * beat, 0.3 * beat),  # E5
        (783.99, 15.0 * beat, 0.3 * beat),  # G5
        (1046.50, 15.5 * beat, 2.5 * beat), # C6 Final Big Sustained Brass Chord!
    ]

    for freq, start, dur in melody:
        pos = int(start * SAMPLE_RATE)
        sub_len = int(dur * SAMPLE_RATE)
        for i in range(sub_len):
            if pos + i < total_samples:
                t = i / SAMPLE_RATE
                env = 1.0 if t < dur * 0.7 else max(0.0, (dur - t) / (dur * 0.3))
                # Brass bright saw harmonics
                val = math.sin(2 * math.pi * freq * t)
                val += 0.6 * math.sin(2 * math.pi * freq * 2 * t)
                val += 0.35 * math.sin(2 * math.pi * freq * 3 * t)
                val += 0.20 * math.sin(2 * math.pi * freq * 4 * t)
                # Harmony third
                harm = math.sin(2 * math.pi * (freq * 1.25) * t) * 0.5
                samples[pos + i] += (val + harm) * env * 6500.0

    return samples

def synthesize_round_bumper(is_double=False):
    # 4-Second TV Game Show Round Transition Bumper
    duration = 4.0
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    base_freq = 329.63 if is_double else 261.63 # E4 for double (higher tension), C4 for single
    notes = [base_freq, base_freq * 1.25, base_freq * 1.5, base_freq * 2.0]
    for idx, f in enumerate(notes):
        start = idx * 0.35
        pos = int(start * SAMPLE_RATE)
        dur = 1.2 if idx == 3 else 0.4
        sub_len = int(dur * SAMPLE_RATE)
        for i in range(sub_len):
            if pos + i < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-2.0 * t)
                val = math.sin(2 * math.pi * f * t) + 0.5 * math.sin(4 * math.pi * f * t) + 0.25 * math.sin(6 * math.pi * f * t)
                samples[pos + i] += val * env * 9000.0

    # Add cymbal crash at 1.4s
    cym_pos = int(1.4 * SAMPLE_RATE)
    for i in range(int(2.2 * SAMPLE_RATE)):
        if cym_pos + i < total_samples:
            t = i / SAMPLE_RATE
            noise = random.uniform(-1.0, 1.0)
            env = math.exp(-3.5 * t)
            samples[cym_pos + i] += noise * env * 5000.0

    return samples

def main():
    target_dir = "App/Resources/Sounds"
    os.makedirs(target_dir, exist_ok=True)

    print("Generating Authentic Television Game Show Music...")
    write_wav_file(os.path.join(target_dir, "menu_theme.wav"), synthesize_jeopardy_main_theme())
    write_wav_file(os.path.join(target_dir, "round1_bumper.wav"), synthesize_round_bumper(is_double=False))
    write_wav_file(os.path.join(target_dir, "round2_bumper.wav"), synthesize_round_bumper(is_double=True))
    print("Television Game Show Music generation complete!")

if __name__ == "__main__":
    main()
