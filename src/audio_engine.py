#!/usr/bin/env python3
from __future__ import annotations
"""
True Studio Field-Recording Acoustic Rain & Gentle Piano Ambient Audio Engine.

Key Psychoacoustic Discovery (verified by direct multimodal ear audition):
- Why previous mixes sounded harsh or roaring:
  1. AI video Foley (Veo 3.1) sounds like frying bacon on plastic.
  2. Boosting rain RMS to 0.07-0.08 (-22 dBFS) and stacking multiple copies with +5 dB at 200 Hz
     turns gentle rain into a loud, fatiguing waterfall/wind-tunnel roar.
- What actually sounds deeply cozy and pleasant to the human ear:
  1. Single-perspective, natural stereo field recording (`gentle_night_rain.mp3`) kept at a
     true intimate ASMR level (`RMS = 0.023`), with zero multi-layer comb filtering and zero
     boomy 200 Hz EQ boost.
  2. For Account 2 (Cozy Chill / Ambient), blending soft natural rain (`RMS = 0.016`) with
     delicate, crystalline acoustic piano (`soft_piano_rain.mp3`, `RMS = 0.028`) at natural
     full-bandwidth clarity (`lowpass=9500Hz`, subtle `0.988x` warm tuning).
"""

import os
import subprocess
from pathlib import Path
import numpy as np

FFMPEG_BIN = "/Users/nowy/homebrew/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

BASE_DIR = Path(__file__).resolve().parent.parent
BEDS_DIR = BASE_DIR / "assets" / "audio_beds"


def _load_clean_stereo(
    path: Path,
    af_filter: str,
    duration_sec: float = 60.0,
    sr: int = 44100,
) -> np.ndarray:
    """Decodes an audio bed once with transparent acoustic filtering into a float32 stereo array."""
    n_expected = int(duration_sec * sr)
    cmd = [
        FFMPEG_BIN, "-v", "error",
        "-i", str(path),
        "-vn",
        "-af", af_filter,
        "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"
    ]
    raw_bytes = subprocess.check_output(cmd)
    arr = np.frombuffer(raw_bytes, dtype=np.float32).reshape(-1, 2).copy()
    if len(arr) > int(4.0 * sr):
        arr = arr[int(1.0 * sr) : -int(1.0 * sr)]
    if len(arr) < n_expected:
        reps = (n_expected // len(arr)) + 2
        arr = np.tile(arr, (reps, 1))
    return arr[:n_expected]


def _make_seamless_loop(stereo: np.ndarray, loop_sec: int = 50, fade_sec: float = 5.0, sr: int = 44100) -> np.ndarray:
    """Creates a 100% seamless `loop_sec` stereo cycle using a smooth 5.0-second raised-cosine crossfade."""
    n_target = loop_sec * sr
    fade_n = int(fade_sec * sr)
    if len(stereo) < n_target + fade_n:
        reps = ((n_target + fade_n) // len(stereo)) + 2
        stereo = np.tile(stereo, (reps, 1))

    body = stereo[fade_n : fade_n + n_target].copy()
    head = stereo[:fade_n].copy()
    alpha = 0.5 * (1.0 - np.cos(np.pi * np.arange(fade_n, dtype=np.float32) / fade_n))[:, None]
    body[-fade_n:] = body[-fade_n:] * (1.0 - alpha) + head * alpha
    return body


def _norm(x: np.ndarray, target_rms: float) -> np.ndarray:
    rms = float(np.sqrt(np.mean(x ** 2)) + 1e-8)
    return x * (target_rms / rms)


def _build_cozy_camper_rain_cycle(sr: int = 44100, variant: str = "account1") -> np.ndarray:
    gentle_path = BEDS_DIR / "gentle_night_rain.mp3"
    piano_path = BEDS_DIR / "soft_piano_rain.mp3"

    # Pure, transparent gentle night rain (no boomy 200Hz boost, no multi-copy comb filtering)
    af_rain = "highpass=f=120,lowpass=f=7500"
    rain = _load_clean_stereo(gentle_path, af_rain, duration_sec=56.0, sr=sr)

    if variant == "account1":
        # Intimate, quiet ASMR night rain level (exact match to cand_0_15s.mp3 = 0.022 RMS)
        mix = _norm(rain, 0.022)
    else:
        # Cozy Ambient Piano + Gentle Night Rain at delicate, crystalline ASMR level
        af_piano = "asetrate=44100*0.988,aresample=44100,highpass=f=110,lowpass=f=9000"
        piano = _load_clean_stereo(piano_path, af_piano, duration_sec=56.0, sr=sr)
        mix = _norm(rain[:, ::-1], 0.012) + _norm(piano, 0.028)

    return _make_seamless_loop(mix, loop_sec=50, fade_sec=5.0, sr=sr)


def _encode_looped_m4a(
    cycle_pcm: np.ndarray,
    sr: int,
    cycle_sec: int,
    total_dur_sec: int,
    output_path: str,
) -> str:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    pcm_s16 = (np.clip(cycle_pcm, -1.0, 1.0) * 32767.0).astype(np.int16)

    tmp_base = out.with_name(out.stem + "_base.m4a")
    cmd_encode = [
        FFMPEG_BIN, "-y",
        "-f", "s16le",
        "-ar", str(sr),
        "-ac", "2",
        "-i", "-",
        "-c:a", "aac", "-b:a", "192k",
        str(tmp_base),
    ]
    proc = subprocess.Popen(cmd_encode, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc.communicate(input=pcm_s16.tobytes())
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg audio encode failed with {proc.returncode}")

    loops = max(1, (total_dur_sec // cycle_sec) + 2)
    cmd_loop = [
        FFMPEG_BIN, "-y",
        "-stream_loop", str(loops),
        "-i", str(tmp_base),
        "-t", str(total_dur_sec),
        "-af", "afade=t=in:st=0:d=0.6",
        "-c:a", "aac", "-b:a", "192k",
        str(out),
    ]
    subprocess.run(cmd_loop, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp_base.exists():
        tmp_base.unlink()

    return str(out)


def generate_sleep_rain_track(
    output_path: str,
    duration_sec: int = 3600,
    seed: int = 42,
    raw_clip_path: str = "",
) -> str:
    sr = 44100
    cycle_sec = 50
    cycle = _build_cozy_camper_rain_cycle(sr=sr, variant="account1")
    return _encode_looped_m4a(cycle, sr, cycle_sec, duration_sec, output_path)


def generate_chill_lofi_rain_track(
    output_path: str,
    duration_sec: int = 3600,
    seed: int = 99,
    raw_clip_path: str = "",
) -> str:
    sr = 44100
    cycle_sec = 50
    cycle = _build_cozy_camper_rain_cycle(sr=sr, variant="account2")
    return _encode_looped_m4a(cycle, sr, cycle_sec, duration_sec, output_path)
