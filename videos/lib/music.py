"""Generated background music for the tutorial videos (VIDEOS.md, "The music").

Every video gets its own calm piece, rendered here from a seed (the question's id), so the
music is ours: no download, no licence, no Content ID claim. Pure numpy for the synthesis,
ffmpeg for the loudness and the files.

    python videos/lib/music.py --seed 2 --seconds 60 --out /tmp/m.wav   # a 60 s piece
    python videos/lib/music.py --seed 2 --describe                      # what seed 2 plays
    python videos/lib/music.py --analyse /tmp/m.wav --spectrum /tmp/m.png

The piece:

- a slow progression of 4-8 chords from `PROGRESSIONS` (maj7, maj9, add9, 6/9, sus and
  minor 7/9/11 colours, in Ionian, Lydian or Dorian), 8 beats a chord (5-7.5 s), looped
  with variations: a chord's colour is swapped for a neighbour that stays in the mode,
  the arpeggio shifts its inversion or turns downwards, notes drop out, and every fourth
  pass breathes with fewer notes. It ends on the tonic, held through the fade-out;
- a pad: three detuned voices of a band-limited saw/triangle blend (a wavetable built
  from its harmonics, each weighted by a gentle 2-pole low-pass), slow raised-cosine
  attack and release, a slow brightness drift;
- a soft piano: additive partials with slight inharmonicity (f_n = n f0 sqrt(1 + B n^2)),
  two strings a partial for the beating, a 4 ms attack, a two-stage exponential decay
  (the highs die first), a velocity that also sets the brightness, humanised timing;
- an optional sub-bass, a sine on the roots;
- a reverb: the sum convolved with a synthetic impulse response (decaying noise, 2.6-3.4 s,
  the highs decaying faster, a different noise for each ear, which gives the width);
- a 3 s fade-in and a 4 s fade-out that end exactly at the video's length;
- loudness: ffmpeg's loudnorm in two passes (measure, then a linear gain) to -24 LUFS
  integrated, true peak under -2 dBTP. The narration will sit near -16 LUFS, about 8 dB
  above, and duck the music a few dB more (VIDEOS.md has the filter graph).

The seed picks the progression (and with it the mode), the key, the arpeggio pattern by
fixed rotations (so neighbouring ids never share them), and through a random generator
the tempo, the instrument mix, the reverb and every humanised detail. `describe(seed)`
says what a seed plays.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SR = 48000
TARGET_LUFS = -24.0
TARGET_TP = -2.0
FADE_IN = 3.0
FADE_OUT = 4.0
BEATS_PER_CHORD = 8
FINAL_SECONDS = 9.0          # the closing tonic chord, held through the fade-out
FFMPEG = "ffmpeg"

NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

MODES = {
    "ionian": (0, 2, 4, 5, 7, 9, 11),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
}

# A chord: its tones above the root (for the arpeggio) and the pad's spread voicing above
# the root (the pad also plays the root, below the voicing). No two voiced notes a
# semitone apart.
CHORDS = {
    "maj7":    ((0, 4, 7, 11),         (7, 11, 16)),
    "maj9":    ((0, 4, 7, 11, 14),     (7, 11, 14, 16)),
    "add9":    ((0, 4, 7, 14),         (7, 14, 16)),
    "6/9":     ((0, 4, 7, 9, 14),      (7, 9, 14, 16)),
    "maj7#11": ((0, 4, 7, 11, 18),     (7, 11, 16, 18)),
    "sus2":    ((0, 2, 7),             (7, 14, 19)),
    "sus4":    ((0, 5, 7),             (7, 12, 17)),
    "7sus4":   ((0, 5, 7, 10),         (7, 10, 17)),
    "m7":      ((0, 3, 7, 10),         (7, 10, 15)),
    "m9":      ((0, 3, 7, 10, 14),     (3, 7, 10, 14)),
    "m11":     ((0, 3, 7, 10, 17),     (7, 10, 15, 17)),
}

# Neighbouring colours a variation may swap in (only when every tone stays in the mode).
SUBS = {
    "maj7": ("maj9", "6/9"), "maj9": ("maj7", "6/9"), "add9": ("6/9", "sus2"),
    "6/9": ("add9", "maj9"), "maj7#11": ("maj9", "maj7"), "sus2": ("add9", "sus4"),
    "sus4": ("7sus4", "sus2"), "7sus4": ("sus4",), "m7": ("m9", "m11"),
    "m9": ("m7", "m11"), "m11": ("m9", "m7"),
}

# The curated progressions: (name, mode, [(root above the tonic, chord), ...]). The modes
# alternate, so the rotation by seed moves to another mode for the next id.
PROGRESSIONS = [
    ("I - vi - IV - V", "ionian",
     [(0, "maj9"), (9, "m9"), (5, "maj7"), (7, "7sus4")]),
    ("I - II - vi - V", "lydian",
     [(0, "maj7#11"), (2, "add9"), (9, "m9"), (7, "add9")]),
    ("i - IV - bIII - bVII", "dorian",
     [(0, "m9"), (5, "add9"), (3, "maj7"), (10, "6/9")]),
    ("IV - I - vi - V - IV - iii - ii - V", "ionian",
     [(5, "maj9"), (0, "add9"), (9, "m7"), (7, "sus4"),
      (5, "maj7"), (4, "m7"), (2, "m9"), (7, "sus2")]),
    ("I - II - I - II - iii - V", "lydian",
     [(0, "maj9"), (2, "add9"), (0, "6/9"), (2, "sus2"), (4, "m7"), (7, "add9")]),
    ("i - bVII - IV - v", "dorian",
     [(0, "m11"), (10, "maj9"), (5, "add9"), (7, "m7")]),
    ("I - iii - vi - IV - ii - V", "ionian",
     [(0, "maj7"), (4, "m7"), (9, "m9"), (5, "6/9"), (2, "m9"), (7, "7sus4")]),
    ("I - V - vi - II", "lydian",
     [(0, "maj7#11"), (7, "maj7"), (9, "m7"), (2, "add9")]),
    ("i - IV - i - IV - bIII - bVII - v - IV", "dorian",
     [(0, "m9"), (5, "6/9"), (0, "m7"), (5, "add9"),
      (3, "maj9"), (10, "add9"), (7, "m11"), (5, "sus2")]),
]

KEYS = [0, 2, 3, 5, 7, 9, 10]        # C, D, Eb, F, G, A, Bb

# The piano's patterns over a chord of 8 beats: (beat, index in the chord-tone ladder).
# "melody" is generated per phrase instead.
PATTERNS = {
    "waves":  [(0, 0), (1, 2), (2, 4), (3, 3), (4, 1), (5, 3), (6, 5), (7, 4)],
    "rise":   [(0, 0), (0.5, 1), (1, 2), (1.5, 3), (2, 4), (4, 2), (5, 3), (6, 5)],
    "sparse": [(0, 2), (1.5, 4), (3, 3), (4.5, 5), (6, 4)],
    "pairs":  [(0, 1), (0.5, 3), (2, 2), (2.5, 4), (4, 1), (4.5, 3), (6, 4), (6.5, 5)],
    "melody": None,
}
MELODY_RHYTHMS = [(0, 3, 4.5, 6), (0, 2, 4), (1, 2, 3, 5), (0, 1.5, 3, 6), (0, 2.5, 4, 5.5)]

FINAL_CHORD = {"ionian": "maj9", "lydian": "maj7#11", "dorian": "m9"}


def mtof(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12)


def fits(root: int, chord: str, mode: str) -> bool:
    scale = set(MODES[mode])
    return all((root + iv) % 12 in scale for iv in CHORDS[chord][0])


@dataclass
class Plan:
    seed: int
    key: int
    mode: str
    prog_name: str
    prog: list
    pattern: str
    bpm: float
    saw: float              # the pad's saw share (the rest is triangle)
    cutoff: float           # the pad's low-pass, Hz
    detune: float           # cents
    spread: float           # the pad's voices, -spread .. +spread in the stereo field
    piano: float            # the piano's level against the pad
    sub: float              # 0 when the piece has no sub-bass
    rt60: float
    wet: float
    arp_low: int            # the lowest note of the arpeggio's ladder
    extra: dict = field(default_factory=dict)

    def summary(self) -> str:
        key = NOTE_NAMES[self.key]
        chords = " ".join(f"{NOTE_NAMES[(self.key + r) % 12]}{q}" for r, q in self.prog)
        return (f"seed {self.seed}: {key} {self.mode}, {self.prog_name} ({chords}), "
                f"{self.pattern} at {self.bpm:.0f} bpm, pad saw {self.saw:.2f} / "
                f"low-pass {self.cutoff:.0f} Hz, piano {self.piano:.2f}, "
                f"sub {'on' if self.sub else 'off'}, reverb {self.rt60:.1f} s")


def plan(seed: int) -> Plan:
    """What a seed plays. The progression, key and pattern rotate with the seed by
    multipliers prime to their counts, so consecutive ids differ in all three."""
    rng = np.random.default_rng([0x4D55, seed])
    name, mode, prog = PROGRESSIONS[(seed * 5) % len(PROGRESSIONS)]
    for r, q in prog:
        assert fits(r, q, mode), (name, r, q)
    pats = list(PATTERNS)
    return Plan(
        seed=seed, key=KEYS[(seed * 3) % len(KEYS)], mode=mode, prog_name=name,
        prog=list(prog), pattern=pats[(seed * 3) % len(pats)],
        bpm=float(rng.uniform(66, 88)),
        saw=float(rng.uniform(0.25, 0.8)), cutoff=float(rng.uniform(900, 1600)),
        detune=float(rng.uniform(4, 9)), spread=float(rng.uniform(0.3, 0.55)),
        piano=float(rng.uniform(0.95, 1.25)),
        sub=float(rng.uniform(0.25, 0.4)) if rng.random() < 0.75 else 0.0,
        rt60=float(rng.uniform(2.6, 3.4)), wet=float(rng.uniform(0.45, 0.6)),
        arp_low=int(rng.integers(58, 63)),
    )


def describe(seed: int) -> str:
    return plan(seed).summary()


# --- envelopes and helpers ------------------------------------------------------------

def rcos(n: int) -> np.ndarray:
    """A raised-cosine ramp from 0 to 1 over n samples (both ends smooth)."""
    if n <= 1:
        return np.ones(max(n, 0))
    return 0.5 - 0.5 * np.cos(np.pi * np.arange(n) / (n - 1))


def pan_gains(p: float) -> tuple[float, float]:
    """Equal-power pan, p in -1 (left) .. +1 (right)."""
    a = (p + 1) * np.pi / 4
    return math.cos(a), math.sin(a)


def add(buf: np.ndarray, start: int, sig: np.ndarray, gl: float, gr: float) -> None:
    end = min(start + len(sig), buf.shape[1])
    if end <= start:
        return
    buf[0, start:end] += gl * sig[:end - start]
    buf[1, start:end] += gr * sig[:end - start]


TABLE = 4096


def wavetable(f0: float, saw: float, cutoff: float) -> np.ndarray:
    """One period of the pad's wave: a saw/triangle blend from its harmonics, each through
    a 2-pole low-pass at `cutoff`, nothing above 7 kHz. One extra sample for the
    interpolation."""
    nmax = max(1, int(min(7000.0, SR * 0.4) // f0))
    n = np.arange(1, nmax + 1)
    sawa = 1.0 / n
    tri = np.where(n % 2 == 1, 1.0 / n ** 2, 0.0) * np.where((n // 2) % 2 == 0, 1.0, -1.0)
    amp = (saw * sawa + (1 - saw) * tri * 1.5) / np.sqrt(1 + (n * f0 / cutoff) ** 4)
    x = np.arange(TABLE + 1) / TABLE
    tab = np.sin(2 * np.pi * np.outer(x, n)) @ amp
    return tab / np.max(np.abs(tab))


def lookup(tab: np.ndarray, phase: np.ndarray) -> np.ndarray:
    pos = (phase % 1.0) * TABLE
    i = pos.astype(np.int64)
    frac = pos - i
    return tab[i] * (1 - frac) + tab[i + 1] * frac


# --- the voices -------------------------------------------------------------------------

def pad_note(buf, t0: float, dur: float, midi: float, p: Plan, rng, level: float,
             bright_lfo: tuple[float, float]) -> None:
    attack, release = 2.2, 2.8
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    env = np.ones(n)
    na, nr = int(attack * SR), int(release * SR)
    env[:na] = rcos(na)
    env[n - nr:] = rcos(nr)[::-1]
    f0 = mtof(midi)
    dark = wavetable(f0, p.saw, p.cutoff)
    bright = wavetable(f0, p.saw, p.cutoff * 1.7)
    period, phase0 = bright_lfo
    m = 0.35 * (0.5 - 0.5 * np.cos(2 * np.pi * (t + t0) / period + phase0))
    start = int(t0 * SR)
    for k, cents in enumerate((-p.detune, 0.0, p.detune)):
        f = f0 * 2 ** (cents / 1200)
        rate, depth = rng.uniform(0.07, 0.15), rng.uniform(0.0004, 0.0008)
        ph0 = rng.random()
        # a slow pitch drift, integrated: f (1 + depth sin(2 pi rate t))
        phase = ph0 + f * t - f * depth * np.cos(2 * np.pi * rate * t) / (2 * np.pi * rate)
        sig = (1 - m) * lookup(dark, phase) + m * lookup(bright, phase)
        gl, gr = pan_gains((k - 1) * p.spread)
        add(buf, start, sig * env * (level / 3), gl, gr)


def piano_note(buf, t0: float, midi: float, vel: float, stop: float | None,
               rng, pan: float) -> None:
    f0 = mtof(midi)
    b = 0.00025
    tau = float(np.clip(3.2 * (261.6 / f0) ** 0.5, 1.4, 5.0))
    natural = min(7.0, tau * 3.0)
    length = natural if stop is None else max(0.6, min(natural, stop - t0))
    n = int(length * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    k = 1
    while True:
        fk = k * f0 * math.sqrt(1 + b * k * k)
        if fk > 6500 or k > 10:
            break
        bright = 0.35 - 0.2 * vel           # a harder note is brighter
        amp = k ** -1.1 * math.exp(-(k - 1) * bright) / (1 + (fk / 2800) ** 2)
        tk = tau / (1 + 0.45 * (k - 1))
        env = 0.65 * np.exp(-t / (0.3 * tk)) + 0.35 * np.exp(-t / tk)
        d = rng.uniform(0.00015, 0.0003)     # two strings, a fraction of a cent apart
        ph = rng.random() * 2 * np.pi
        out += amp * env * (np.sin(2 * np.pi * fk * (1 - d) * t + ph)
                            + np.sin(2 * np.pi * fk * (1 + d) * t + ph * 0.7)) / 2
        k += 1
    na = int(0.004 * SR)
    out[:na] *= rcos(na)
    nr = min(int(0.35 * SR), n // 2)
    out[n - nr:] *= rcos(nr)[::-1]
    gl, gr = pan_gains(pan)
    add(buf, int(t0 * SR), out * vel, gl, gr)


def sub_note(buf, t0: float, dur: float, midi: float) -> None:
    attack, release = 1.0, 1.6
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    env = np.ones(n)
    env[:int(attack * SR)] = rcos(int(attack * SR))
    env[n - int(release * SR):] = rcos(int(release * SR))[::-1]
    f = mtof(midi)
    sig = (np.sin(2 * np.pi * f * t) + 0.12 * np.sin(4 * np.pi * f * t)) * env
    add(buf, int(t0 * SR), sig, 0.7071, 0.7071)


# --- the arrangement --------------------------------------------------------------------

def ladder(root_pc: int, chord: str, low: int) -> list[int]:
    pcs = {(root_pc + iv) % 12 for iv in CHORDS[chord][0]}
    return [m for m in range(low, low + 27) if m % 12 in pcs]


def pad_voicing(root_pc: int, chord: str) -> list[int]:
    root = 43 + (root_pc - 43) % 12            # the root in MIDI 43..54
    return [root] + [root + iv for iv in CHORDS[chord][1]]


def melody_phrase(chords, key: int, mode: str, low: int, rng) -> list[list[tuple[float, int]]]:
    """A phrase of a few notes per chord: a walk on the scale, landing on a chord tone at
    the chord's first note and at beat 4."""
    scale = [m for m in range(low + 3, low + 26) if (m - key) % 12 in MODES[mode]]
    cur = len(scale) // 2
    phrase = []
    for root_pc, chord in chords:
        pcs = {(root_pc + iv) % 12 for iv in CHORDS[chord][0]}
        rhythm = MELODY_RHYTHMS[rng.integers(len(MELODY_RHYTHMS))]
        notes = []
        for j, beat in enumerate(rhythm):
            cur = int(np.clip(cur + rng.choice([-2, -1, -1, 1, 1, 2, 0]), 0, len(scale) - 1))
            if j == 0 or beat == 4:
                tones = [i for i, m in enumerate(scale) if m % 12 in pcs]
                cur = min(tones, key=lambda i: abs(i - cur))
            notes.append((beat, scale[cur]))
        phrase.append(notes)
    return phrase


def render(seed: int, seconds: float) -> tuple[np.ndarray, Plan]:
    """The piece for `seed`, exactly `seconds` long, as float64 stereo (2, n), unnormalised."""
    p = plan(seed)
    rng = np.random.default_rng([0x5EED, seed])
    total = round(seconds * SR)
    buf = np.zeros((2, total + int(8 * SR)))
    pad_buf, piano_buf, sub_buf = (np.zeros_like(buf) for _ in range(3))

    # chords of 8 beats near the seed's tempo, stretched so whole passes of the
    # progression end where the closing tonic chord starts
    nominal = BEATS_PER_CHORD * 60 / p.bpm
    final = min(FINAL_SECONDS, seconds / 3)
    body = max(seconds - final, nominal)
    plen = len(p.prog)
    passes = max(1, round(body / (plen * nominal)))
    slot = body / (passes * plen)
    if not 4.0 <= slot <= 8.0:               # a short piece: drop the whole-pass rule
        slot = float(np.clip(nominal, 4.0, 8.0))
        passes = max(1, math.ceil(body / (plen * slot)))
    p.extra.update(slot=slot, passes=passes, bpm=BEATS_PER_CHORD * 60 / slot)
    beat = slot / BEATS_PER_CHORD

    lfo = (rng.uniform(11, 17), rng.uniform(0, 2 * np.pi))
    slots = []                               # (start, length, root_pc, chord, pass)
    t = 0.0
    for ps in range(passes):
        for r, q in p.prog:
            if t >= body - 1e-6:
                break
            if ps % 2 == 1 and rng.random() < 0.5:
                options = [s for s in SUBS[q] if fits(r, s, p.mode)]
                if options:
                    q = options[rng.integers(len(options))]
            slots.append((t, min(slot, body - t), (p.key + r) % 12, q, ps))
            t += slot
    slots.append((body, seconds - body, p.key, FINAL_CHORD[p.mode], -1))

    phrase = None
    for i, (t0, length, root_pc, q, ps) in enumerate(slots):
        last = ps == -1
        # the pad: root + spread voicing, each note a little late or early
        for midi in pad_voicing(root_pc, q):
            jitter = rng.uniform(0, 0.08)
            pad_note(pad_buf, t0 + jitter, length - jitter + (FADE_OUT if last else 0),
                     midi, p, rng, 1.0, lfo)
        if p.sub and ps != 0:
            sub_note(sub_buf, t0, length + (FADE_OUT if last else 0),
                     pad_voicing(root_pc, q)[0] - 12)

        # the piano
        stop = None if last else t0 + length + 0.6
        lad = ladder(root_pc, q, p.arp_low)
        if last:
            for j, m in enumerate(lad[:5]):          # a rolled tonic chord, then one high note
                piano_note(piano_buf, t0 + 0.12 * j, m, 0.55, None, rng, (m - 66) / 40)
            high = lad[min(6, len(lad) - 1)]
            piano_note(piano_buf, t0 + 4 * beat, high, 0.45, None, rng, 0.2)
            continue
        density = 0.55 if ps == 0 else (0.45 if ps % 4 == 3 else 0.88)
        if p.pattern == "melody":
            k = i % plen
            if k == 0 and (phrase is None or ps % 2 == 0):
                chords = [((p.key + r) % 12, qq) for r, qq in p.prog]
                phrase = melody_phrase(chords, p.key, p.mode, p.arp_low, rng)
            events = list(phrase[k])
            if rng.random() < 0.6:
                events.append((0, lad[0]))           # a low chord tone under the melody
            notes = [(b, m) for b, m in events]
        else:
            shift = int(rng.choice([0, 0, 1, -1])) if ps else 0
            pat = PATTERNS[p.pattern]
            if ps % 3 == 2:                          # this pass turns downwards
                top = max(ix for _, ix in pat)
                pat = [(b, top - ix) for b, ix in pat]
            notes = [(b, lad[int(np.clip(ix + shift, 0, len(lad) - 1))]) for b, ix in pat]
        for b, m in notes:
            if b > 0 and rng.random() > density:
                continue
            accent = 1.0 if b == 0 else (0.85 if b == 4 else 0.72)
            vel = accent * rng.uniform(0.7, 1.0)
            when = t0 + b * beat + rng.normal(0, 0.012) + 0.01
            piano_note(piano_buf, max(0.0, when), m, vel, stop, rng, (m - 66) / 40)

    # the mix: each stem to its level against the pad's RMS
    def rms(x):
        s = x[:, :total]
        return float(np.sqrt(np.mean(s ** 2))) or 1.0

    pad_buf /= rms(pad_buf)
    piano_buf *= p.piano / rms(piano_buf)
    if p.sub:
        sub_buf *= p.sub / rms(sub_buf)
    dry = pad_buf + piano_buf + sub_buf
    send = 0.65 * pad_buf + 0.6 * piano_buf + 0.1 * sub_buf
    wet = reverb(send, p.rt60, rng)
    mix = dry + p.wet * wet[:, :dry.shape[1]]
    mix = mix[:, :total]

    nin, nout = int(FADE_IN * SR), int(FADE_OUT * SR)
    mix[:, :nin] *= rcos(nin)
    mix[:, total - nout:] *= rcos(nout)[::-1]
    return mix / np.max(np.abs(mix)) * 0.5, p


def reverb(x: np.ndarray, rt60: float, rng) -> np.ndarray:
    """Convolve each channel with its own synthetic impulse response: noise, the lows
    decaying in `rt60`, the highs (above ~2 kHz) in 0.55 of it, everything above ~6 kHz
    rolled off, a 22 ms pre-delay and a 12 ms onset. Overlap-add with numpy's rFFT."""
    n_ir = int((rt60 + 0.3) * SR)
    t = np.arange(n_ir) / SR
    freqs = np.fft.rfftfreq(n_ir, 1 / SR)
    lowband = 1 / np.sqrt(1 + (freqs / 2000) ** 4)
    highband = np.sqrt(np.clip(1 - lowband ** 2, 0, 1)) / np.sqrt(1 + (freqs / 6000) ** 4)
    out = np.zeros((2, x.shape[1] + n_ir))
    pre = int(0.022 * SR)
    for ch in range(2):
        spec = np.fft.rfft(rng.standard_normal(n_ir))
        low = np.fft.irfft(spec * lowband, n_ir) * 10 ** (-3 * t / rt60)
        high = np.fft.irfft(spec * highband, n_ir) * 10 ** (-3 * t / (0.55 * rt60))
        ir = low + 0.7 * high
        ir[:int(0.012 * SR)] *= rcos(int(0.012 * SR))
        ir = np.concatenate([np.zeros(pre), ir])[:n_ir]
        ir /= np.sqrt(np.sum(ir ** 2))
        block = 1 << 17
        nfft = 1 << math.ceil(math.log2(block + n_ir))
        irf = np.fft.rfft(ir, nfft)
        for s in range(0, x.shape[1], block):
            seg = x[ch, s:s + block]
            y = np.fft.irfft(np.fft.rfft(seg, nfft) * irf, nfft)[:len(seg) + n_ir - 1]
            out[ch, s:s + len(y)] += y
    return out


# --- loudness and files -----------------------------------------------------------------

def _run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if r.returncode:
        raise RuntimeError(f"{' '.join(cmd[:6])}…: {r.stderr[-2000:]}")
    return r.stderr


def _loudnorm_json(stderr: str) -> dict:
    return json.loads(stderr[stderr.rindex("{"):stderr.rindex("}") + 1])


def write_wav(mix: np.ndarray, path: Path) -> dict:
    """Normalise to TARGET_LUFS / TARGET_TP with loudnorm in two passes (measure, then a
    linear gain) and write a 24-bit 48 kHz stereo WAV. Returns pass 2's report."""
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "mix.f32"
        np.ascontiguousarray(mix.T, dtype="<f4").tofile(raw)
        src = [FFMPEG, "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2",
               "-i", str(raw)]
        base = f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA=20"
        m = _loudnorm_json(_run([*src, "-af", base + ":print_format=json", "-f", "null", "-"]))
        second = (f"{base}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
                  f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
                  f":offset={m['target_offset']}:linear=true:print_format=json")
        path.parent.mkdir(parents=True, exist_ok=True)
        rep = _loudnorm_json(_run([*src, "-af", f"{second},aresample={SR}", "-ar", str(SR),
                                   "-c:a", "pcm_s24le", "-y", str(path)]))
    if rep.get("normalization_type") != "linear":
        print(f"warn {path.name}: loudnorm fell back to {rep.get('normalization_type')}",
              file=sys.stderr)
    return rep


def measure(path: Path) -> dict:
    """Integrated loudness, range and true peak by ffmpeg's ebur128, and the clicks check:
    the largest sample-to-sample step against the RMS, and the count of second-difference
    spikes above 12 times their local RMS (a click is such a spike)."""
    err = _run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af",
                "ebur128=peak=true:framelog=quiet", "-f", "null", "-"])
    summary = err[err.rindex("Summary:"):]
    num = lambda label: float(re.search(label + r":\s+(-?[\d.]+|-inf)", summary).group(1))
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2",
                          "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype="<f4").reshape(-1, 2).T.astype(np.float64)
    rms = float(np.sqrt(np.mean(x ** 2)))
    d = np.diff(x, axis=1)
    d2 = np.abs(np.diff(x, n=2, axis=1))
    win = int(0.05 * SR)
    spikes = 0
    for ch in range(2):
        c = np.concatenate([[0.0], np.cumsum(d2[ch] ** 2)])
        lo = np.clip(np.arange(len(d2[ch])) - win // 2, 0, len(d2[ch]))
        hi = np.clip(lo + win, 0, len(d2[ch]))
        local = np.sqrt((c[hi] - c[lo]) / np.maximum(hi - lo, 1)) + 1e-9
        spikes += int(np.sum(d2[ch] > 12 * local))
    return {"lufs": num("I"), "lra": num("LRA"), "true_peak": num("Peak"),
            "sample_peak_db": 20 * math.log10(float(np.max(np.abs(x))) + 1e-12),
            "rms_db": 20 * math.log10(rms + 1e-12),
            "max_step_over_rms": float(np.max(np.abs(d)) / rms), "spikes": spikes,
            "seconds": x.shape[1] / SR, "first": float(np.max(np.abs(x[:, :10]))),
            "last": float(np.max(np.abs(x[:, -10:])))}


def spectrum_png(path: Path, png: Path) -> None:
    _run([FFMPEG, "-hide_banner", "-y", "-i", str(path), "-lavfi",
          "showspectrumpic=s=1600x600:mode=combined:scale=log:fscale=log:legend=1", str(png)])


def make(seed: int, seconds: float, path: Path) -> dict:
    """Render the piece for `seed`, exactly `seconds` long, to the WAV `path`; returns the
    plan's summary and the measurements."""
    mix, p = render(seed, seconds)
    write_wav(mix, path)
    info = measure(path)
    info["piece"] = p.summary()
    info["slot"], info["passes"] = p.extra["slot"], p.extra["passes"]
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description="Render or analyse a video's generated music.")
    ap.add_argument("--seed", type=int, help="the seed (the question's id)")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--out", type=Path, help="the WAV to write")
    ap.add_argument("--describe", action="store_true", help="only say what the seed plays")
    ap.add_argument("--analyse", type=Path, help="measure an existing WAV")
    ap.add_argument("--spectrum", type=Path, help="also draw a spectrogram PNG")
    args = ap.parse_args()
    if args.describe:
        print(describe(args.seed))
        return 0
    path = args.analyse
    if path is None:
        if args.seed is None or args.out is None:
            ap.error("--seed and --out (or --analyse)")
        info = make(args.seed, args.seconds, args.out)
        path = args.out
    else:
        info = measure(path)
    if args.spectrum:
        spectrum_png(path, args.spectrum)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
