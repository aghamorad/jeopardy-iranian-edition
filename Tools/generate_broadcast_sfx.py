#!/usr/bin/env python3
import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100

def create_wav(filename, samples):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        # Normalize to avoid clipping
        max_val = max(abs(s) for s in samples) if samples else 0
        scale = 32000.0 / max_val if max_val > 32000.0 else (28000.0 / max_val if max_val > 0 else 1.0)
        raw_data = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32768, min(32767, val))
            raw_data.extend(struct.pack('<h', val))
        wav_file.writeframes(raw_data)
    print(f"Created {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")

def make_chime(frequencies, duration, decay=3.0, harmonics=True):
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    for f in frequencies:
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            env = math.exp(-decay * t)
            # Fundamental + harmonics
            val = math.sin(2 * math.pi * f * t)
            if harmonics:
                val += 0.5 * math.sin(2 * math.pi * f * 2 * t)
                val += 0.25 * math.sin(2 * math.pi * f * 3 * t)
                val += 0.125 * math.sin(2 * math.pi * f * 4 * t)
            samples[i] += val * env * 10000.0
    return samples

def make_buzzer(freq=130.0, duration=0.45):
    # Punchy, aggressive game-show lockout buzzer
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        env = 1.0 if t < 0.35 else max(0.0, (duration - t) / 0.1)
        # Saturated square + saw with dissonance
        saw1 = 2.0 * ((t * freq) % 1.0) - 1.0
        saw2 = 2.0 * ((t * (freq * 1.015)) % 1.0) - 1.0 # Slight detune for harshness
        sq1 = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        sq2 = 1.0 if math.sin(2 * math.pi * (freq * 1.414) * t) > 0 else -1.0 # Tritone
        val = (saw1 * 0.4 + saw2 * 0.3 + sq1 * 0.3 + sq2 * 0.35) * env * 18000.0
        samples[i] = val
    return samples

def make_wrong_thud(duration=0.65):
    # Descending game-show fail cue
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-3.5 * t)
        # Descending pitch from 160Hz down to 60Hz
        cur_freq = 160.0 - 110.0 * (t / duration)
        val = math.sin(2 * math.pi * cur_freq * t) + 0.6 * math.sin(2 * math.pi * (cur_freq * 0.95) * t)
        # Sub thud
        sub = math.sin(2 * math.pi * (cur_freq * 0.5) * t) * 0.8
        samples[i] = (val + sub) * env * 22000.0
    return samples

def make_applause(duration=2.2):
    # Simulated crowd clapping and cheering
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    random.seed(42)
    # Generate crowd noise bed
    filtered_noise = [0.0] * total_samples
    prev = 0.0
    for i in range(total_samples):
        r = random.uniform(-1.0, 1.0)
        # Low-pass filter noise
        prev = prev * 0.85 + r * 0.15
        filtered_noise[i] = prev
    
    # Add random claps (impulses with micro decay)
    claps = [0.0] * total_samples
    num_claps = int(duration * 120)
    for _ in range(num_claps):
        pos = int(random.uniform(0.05, duration - 0.2) * SAMPLE_RATE)
        strength = random.uniform(0.4, 1.0)
        decay_len = int(SAMPLE_RATE * 0.04)
        for d in range(decay_len):
            if pos + d < total_samples:
                claps[pos + d] += (random.uniform(-1.0, 1.0) * strength * math.exp(-d / (SAMPLE_RATE * 0.008)))

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        fade_in = min(1.0, t / 0.15)
        fade_out = min(1.0, (duration - t) / 0.4)
        env = fade_in * fade_out
        samples[i] = (filtered_noise[i] * 0.4 + claps[i] * 0.8) * env * 18000.0
    return samples

def make_correct_chime():
    # Ascending joyful chime (C6, E6, G6, C7) with applause
    chime_samples = [0.0] * int(SAMPLE_RATE * 2.5)
    notes = [1046.50, 1318.51, 1567.98, 2093.00] # C6, E6, G6, C7
    delays = [0.0, 0.08, 0.16, 0.24]
    for note, delay in zip(notes, delays):
        start_idx = int(delay * SAMPLE_RATE)
        sub_chime = make_chime([note], 2.2, decay=3.2)
        for i in range(len(sub_chime)):
            if start_idx + i < len(chime_samples):
                chime_samples[start_idx + i] += sub_chime[i]
    
    # Layer with soft cheering
    applause = make_applause(2.5)
    for i in range(len(chime_samples)):
        t = i / SAMPLE_RATE
        crowd_vol = 0.55 if t > 0.3 else t * 1.8
        chime_samples[i] += applause[i] * crowd_vol * 0.65
    return chime_samples

def make_select_chime():
    # Crisp game-show tile select laser whoosh
    duration = 0.18
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        freq = 440.0 + 880.0 * (t / duration)
        env = math.exp(-12.0 * t) if t > 0.05 else t / 0.05
        samples[i] = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * env * 20000.0
    return samples

def make_armed_chime():
    # Clean two-tone TV game show alert (A5 - E6)
    duration = 0.35
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        if t < 0.12:
            f = 880.0
            env = math.exp(-6.0 * t)
        else:
            f = 1318.5
            env = math.exp(-7.0 * (t - 0.12))
        samples[i] = (math.sin(2 * math.pi * f * t) + 0.4 * math.sin(4 * math.pi * f * t)) * env * 22000.0
    return samples

def make_daily_double_fanfare():
    # The iconic 3-laser sting + dramatic regal brass fanfare!
    duration = 2.4
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # 3 laser bloops at t=0.0, 0.18, 0.36
    chirp_times = [0.0, 0.18, 0.36]
    for ct in chirp_times:
        c_samples = int(0.12 * SAMPLE_RATE)
        for i in range(c_samples):
            t = i / SAMPLE_RATE
            f = 500.0 + 1200.0 * (t / 0.12)
            env = math.sin(math.pi * (t / 0.12))
            idx = int(ct * SAMPLE_RATE) + i
            if idx < total_samples:
                samples[idx] += math.sin(2 * math.pi * f * t) * env * 20000.0

    # Regal Brass Fanfare chord at t=0.65 (Bb3, F4, Bb4, D5)
    brass_start = int(0.60 * SAMPLE_RATE)
    brass_freqs = [233.08, 349.23, 466.16, 587.33, 698.46]
    for i in range(total_samples - brass_start):
        t = i / SAMPLE_RATE
        env = math.exp(-1.8 * t)
        val = 0.0
        for f in brass_freqs:
            # Brass saw with odd harmonics
            val += math.sin(2 * math.pi * f * t)
            val += 0.6 * math.sin(2 * math.pi * f * 2 * t)
            val += 0.35 * math.sin(2 * math.pi * f * 3 * t)
        samples[brass_start + i] += val * env * 4500.0

    return samples

def make_final_think_theme():
    # 30-Second Dramatic Final Jeopardy Thinking Suite
    # Syncopated Iranian-modal marimba & bells with a steady clock tick and building orchestral hit
    duration = 30.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Clock tick every 1.0 second
    for sec in range(30):
        tick_pos = int(sec * SAMPLE_RATE)
        for i in range(int(0.06 * SAMPLE_RATE)):
            t = i / SAMPLE_RATE
            freq = 2400.0 if sec % 2 == 0 else 1800.0
            env = math.exp(-45.0 * t)
            samples[tick_pos + i] += math.sin(2 * math.pi * freq * t) * env * 14000.0
            # Woodblock click
            samples[tick_pos + i] += (random.uniform(-1.0, 1.0) * math.exp(-80.0 * t)) * 8000.0

    # Melodic motif in D minor / Bayat-e Esfahan (D, E, F, G, A, Bb, C#, D)
    # 120 BPM: 0.5s per quarter note
    # Repeating 4-bar phrase (8 seconds)
    melody_notes = [
        # Measure 1
        (293.66, 0.0, 0.4),   # D4
        (329.63, 0.5, 0.4),   # E4
        (349.23, 1.0, 0.4),   # F4
        (392.00, 1.5, 0.4),   # G4
        # Measure 2
        (440.00, 2.0, 0.7),   # A4
        (392.00, 2.75, 0.2),  # G4
        (349.23, 3.0, 0.4),   # F4
        (329.63, 3.5, 0.4),   # E4
        # Measure 3
        (293.66, 4.0, 0.4),   # D4
        (440.00, 4.5, 0.4),   # A4
        (466.16, 5.0, 0.6),   # Bb4
        (440.00, 5.75, 0.2),  # A4
        # Measure 4
        (392.00, 6.0, 0.4),   # G4
        (349.23, 6.5, 0.4),   # F4
        (329.63, 7.0, 0.8),   # E4
    ]

    bass_notes = [
        (146.83, 0.0, 1.8),   # D3
        (146.83, 2.0, 1.8),   # D3
        (116.54, 4.0, 1.8),   # Bb2
        (110.00, 6.0, 1.8),   # A2
    ]

    # Cycle melody for ~24 seconds
    for cycle in range(3):
        offset = cycle * 8.0
        for f, start, dur in melody_notes:
            pos = int((offset + start) * SAMPLE_RATE)
            sub_samples = int(dur * SAMPLE_RATE)
            for i in range(sub_samples):
                if pos + i < total_samples:
                    t = i / SAMPLE_RATE
                    env = math.exp(-3.5 * t)
                    # Bell / marimba timbre
                    val = math.sin(2 * math.pi * f * t) + 0.5 * math.sin(4 * math.pi * f * t) + 0.25 * math.sin(6 * math.pi * f * t)
                    samples[pos + i] += val * env * 9000.0

        for f, start, dur in bass_notes:
            pos = int((offset + start) * SAMPLE_RATE)
            sub_samples = int(dur * SAMPLE_RATE)
            for i in range(sub_samples):
                if pos + i < total_samples:
                    t = i / SAMPLE_RATE
                    env = math.exp(-1.5 * t)
                    val = math.sin(2 * math.pi * f * t) + 0.3 * math.sin(4 * math.pi * f * t)
                    samples[pos + i] += val * env * 11000.0

    # Tension build at 24.0s - 29.5s: rapid pulsating arpeggio rising in pitch
    build_start = 24.0
    build_notes = [293.66, 329.63, 349.23, 392.00, 440.00, 466.16, 554.37, 587.33] # D4 up to D5
    for step in range(22):
        t_pos = build_start + step * 0.25
        pos = int(t_pos * SAMPLE_RATE)
        f = build_notes[step % len(build_notes)] * (1.0 + step * 0.02)
        for i in range(int(0.24 * SAMPLE_RATE)):
            if pos + i < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-6.0 * t)
                val = math.sin(2 * math.pi * f * t) + 0.4 * math.sin(4 * math.pi * f * t)
                samples[pos + i] += val * env * (7000.0 + step * 400.0)

    # Climax at 29.5s: Final Dramatic Orchestral Strike + Gong Crash!
    climax_pos = int(29.5 * SAMPLE_RATE)
    chord_freqs = [146.83, 220.00, 293.66, 349.23, 440.00, 587.33] # Grand D minor hit
    for i in range(total_samples - climax_pos):
        t = i / SAMPLE_RATE
        env = math.exp(-1.2 * t)
        val = 0.0
        for f in chord_freqs:
            val += math.sin(2 * math.pi * f * t)
            val += 0.5 * math.sin(2 * math.pi * f * 2 * t)
            val += 0.25 * math.sin(2 * math.pi * f * 3 * t)
        # Add metallic gong noise
        gong = random.uniform(-1.0, 1.0) * math.exp(-5.0 * t)
        samples[climax_pos + i] += (val * env * 6000.0) + (gong * 8000.0)

    return samples

def make_winner_fanfare():
    # Grand victory fanfare (D Major brass triumph) + ecstatic crowd cheering!
    duration = 4.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Brass fanfare motif: D4, F#4, A4, D5 hold!
    fanfare_notes = [
        (293.66, 0.0, 0.2),   # D4
        (293.66, 0.2, 0.2),   # D4
        (293.66, 0.4, 0.2),   # D4
        (370.00, 0.6, 0.35),  # F#4
        (440.00, 0.95, 0.35), # A4
        (587.33, 1.3, 2.5),   # D5 (Sustained grand triumph)
    ]
    harmony_notes = [
        (220.00, 0.0, 0.2),
        (220.00, 0.2, 0.2),
        (220.00, 0.4, 0.2),
        (293.66, 0.6, 0.35),
        (370.00, 0.95, 0.35),
        (440.00, 1.3, 2.5),
    ]

    for (f1, start, dur), (f2, _, _) in zip(fanfare_notes, harmony_notes):
        pos = int(start * SAMPLE_RATE)
        sub_samples = int(dur * SAMPLE_RATE)
        for i in range(sub_samples):
            if pos + i < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-1.0 * t) if dur > 1.0 else math.exp(-2.5 * t)
                b1 = math.sin(2 * math.pi * f1 * t) + 0.6 * math.sin(4 * math.pi * f1 * t) + 0.3 * math.sin(6 * math.pi * f1 * t)
                b2 = math.sin(2 * math.pi * f2 * t) + 0.6 * math.sin(4 * math.pi * f2 * t) + 0.3 * math.sin(6 * math.pi * f2 * t)
                samples[pos + i] += (b1 + b2) * env * 12000.0

    # Layer with surging victory applause and cheering starting at 1.2s
    applause = make_applause(3.0)
    app_pos = int(1.2 * SAMPLE_RATE)
    for i in range(len(applause)):
        if app_pos + i < total_samples:
            samples[app_pos + i] += applause[i] * 1.1

    return samples

def main():
    target_dir = "App/Resources/Sounds"
    os.makedirs(target_dir, exist_ok=True)
    
    print("Synthesizing broadcast-quality sound effects...")
    create_wav(os.path.join(target_dir, "buzz.wav"), make_buzzer())
    create_wav(os.path.join(target_dir, "incorrect.wav"), make_wrong_thud())
    create_wav(os.path.join(target_dir, "correct.wav"), make_correct_chime())
    create_wav(os.path.join(target_dir, "select.wav"), make_select_chime())
    create_wav(os.path.join(target_dir, "join.wav"), make_select_chime())
    create_wav(os.path.join(target_dir, "armed.wav"), make_armed_chime())
    create_wav(os.path.join(target_dir, "wager.wav"), make_daily_double_fanfare())
    create_wav(os.path.join(target_dir, "final.wav"), make_final_think_theme())
    create_wav(os.path.join(target_dir, "winner.wav"), make_winner_fanfare())
    print("Sound effects synthesis complete!")

if __name__ == "__main__":
    main()
