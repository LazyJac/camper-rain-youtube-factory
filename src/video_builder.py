#!/usr/bin/env python3
from __future__ import annotations
"""
4K Ultra HD (3840x2160) Two-Layer Locked-Camper & Fixed-Buoy Weathervane Video Builder.

Implements the user's exact visual & physical requirements for Episode 02 (Masurian Lakes Dusk):
1. Strict Two-Layer Separation ("Samochód stoi i się nie rusza i się nie zmieni, a zmieniasz tylko to, co tam jest w środku, a tutaj jest tak jakby nieruszalne"):
   - Top Layer (`_camper_locked_matte_4k.png`, 3840x2160 RGBA): 100% opaque (`alpha = 255`) and 100% immovable
     across the entire camper van interior, wooden walls, 2000K fairy lights, mug, book, black rubber door seal,
     raised rear tailgate hatch (`klapa`), hydraulic gas strut (`teleskop`), and dark bed blanket (`koc`).
   - Bottom Layer (Window Cutout ONLY, `alpha = 0`): Pure native Google Flow 4K Upscaled (`3840x2160`) video
     streams with zero synthetic grain overlays (`_4k_highfreq_grain.png` removed) and zero double-vision ghosting.
2. Stationary Original Mooring Buoy & Sailboat Weathervane Physics ("Zwróć uwagę, że łódka może się obracać,
   ale ta bojka, do której jest przymocowana, musi zostać w miejscu i ona się obraca wokół tej bojki w zależności
   od kierunku wiatru"):
   - Keeps ONLY the original photographic mooring buoy attached to the boat (zero synthetic drawn buoys),
     locked 100% in place (`x = 2296, y = 1071` in 4K) while the sailboat gently pivots/weathervanes around it
     in response to the storm wind.
3. 40-Second Perfected 4K Master -> Multiplied to 1 Hour 20 Minutes (`4800s` = `01:20:00`):
   - Builds an ~8.8s 4K Storm-Onset Intro (starting from the exact `2.0001` frame) + a 30.0s seamless
     4K Storm & Wind Master Loop (`~39-40s` combined 4K Master), and concatenates it via `-f concat -c copy`
     to a full 1 hour 20 minute (`4800s`) 4K Ultra HD stream.
"""

import os
import subprocess
from pathlib import Path
from src.audio_engine import generate_sleep_rain_track, generate_chill_lofi_rain_track
from src.yt_packager import generate_youtube_packages

FFMPEG_BIN = "/Users/nowy/homebrew/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

FFPROBE_BIN = "/Users/nowy/homebrew/bin/ffprobe"
if not os.path.exists(FFPROBE_BIN):
    FFPROBE_BIN = "ffprobe"


def _probe_duration(clip_path: str) -> float:
    """Returns duration in seconds of a media file using ffprobe."""
    try:
        out = subprocess.check_output(
            [
                FFPROBE_BIN,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(clip_path),
            ],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8").strip()
        dur = float(out)
        if dur >= 3.0:
            return dur
    except Exception:
        pass
    return 8.0


def ensure_4k_locked_assets(episode_dir: Path) -> dict[str, Path]:
    """
    Ensures that:
    1. `_camper_locked_matte_4k.png` (3840x2160 RGBA, 100% opaque camper van foreground matte) exists.
    2. `_veo4k_intro_fixed_buoy.mp4` and `_veo4k_storm_swing_back.mp4` (3840x2160 native 4K exterior clips
       with the original mooring buoy locked in place and smooth boat weathervane pivot) exist.
    """
    camper_png = episode_dir / "_camper_locked_matte_4k.png"
    intro_4k = episode_dir / "_veo4k_intro_fixed_buoy.mp4"
    loop_4k = episode_dir / "_veo4k_storm_swing_back.mp4"

    if not (intro_4k.exists() and loop_4k.exists()):
        subprocess.run(["python3", "src/prepare_4k_buoy_locked_clips.py"], check=True)

    return {
        "camper_png": camper_png,
        "intro_4k": intro_4k,
        "loop_4k": loop_4k,
    }


def build_40s_4k_storm_master_and_intro(
    episode_dir: Path,
    out_intro_path: Path,
    out_loop_path: Path,
    assets: dict[str, Path],
    variant: str = "account1",
) -> tuple[str, str]:
    """
    Builds:
    1. `out_intro_path` (~8.8s 4K Ultra HD, 3840x2160):
       Starts from the exact `2.0001` frame and rapidly rolls in the Masurian storm inside the window cutout,
       while `_camper_locked_matte_4k.png` keeps the camper van 100% motionless on top.
    2. `out_loop_path` (`30.00s` seamless 4K Ultra HD Master Loop, 3840x2160):
       Builds a seamless `7.50s` head-to-tail crossfaded 4K unit from `_veo4k_storm_swing_back.mp4` with
       `_camper_locked_matte_4k.png` locked on top, and stream-loops it 4x (`-c copy`) into a `30.00s`
       4K loop in <4 seconds!
    """
    if variant == "account1":
        color_filter = (
            "cas=strength=0.35,"
            "colorbalance=rs=0.01:gs=0.00:bs=0.02:rm=0.01:bm=0.01,"
            "eq=contrast=1.03:saturation=1.02"
        )
    else:
        color_filter = (
            "cas=strength=0.35,"
            "colorbalance=rs=0.03:gs=0.01:bs=-0.01:rm=0.02:gm=0.01:bm=-0.01,"
            "eq=contrast=1.04:saturation=1.05"
        )

    # 1. Build Storm-Onset Intro (~8.8s 4K Ultra HD):
    intro_fc = (
        f"[0:v]setpts=1.13*PTS,fps=24,{color_filter},format=yuv420p[v_ext];"
        f"[v_ext][1:v]overlay=x=0:y=0:format=auto:shortest=1,format=yuv420p[outv]"
    )
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-i", str(assets["intro_4k"]),
            "-loop", "1", "-r", "24", "-i", str(assets["camper_png"]),
            "-filter_complex", intro_fc,
            "-map", "[outv]", "-t", "8.8", "-an",
            "-c:v", "h264_videotoolbox", "-profile:v", "high",
            "-b:v", "18M", "-maxrate", "24M", "-bufsize", "36M",
            "-g", "48", "-pix_fmt", "yuv420p",
            str(out_intro_path),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # 2. Build 7.50s seamless 4K unit (slowed 2.143x -> 9.00s -> 1.50s head-to-tail xfade -> 7.50s exact)
    unit_75s = out_loop_path.with_name(f"_unit75s_{variant}.mp4")
    unit_fc = (
        f"[0:v]setpts=2.143*(PTS-STARTPTS),fps=24,{color_filter},settb=AVTB,format=yuv420p,split=2[vm_src][vh_src];"
        f"[vm_src]trim=start=1.50:end=9.00,setpts=PTS-STARTPTS[vm];"
        f"[vh_src]trim=start=0.00:end=1.50,setpts=PTS-STARTPTS[vh];"
        f"[vm][vh]xfade=transition=fade:duration=1.50:offset=6.00[v_ext_loop];"
        f"[v_ext_loop][1:v]overlay=x=0:y=0:format=auto:shortest=1,format=yuv420p[outv]"
    )
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-i", str(assets["loop_4k"]),
            "-loop", "1", "-r", "24", "-i", str(assets["camper_png"]),
            "-filter_complex", unit_fc,
            "-map", "[outv]", "-t", "7.5", "-an",
            "-c:v", "h264_videotoolbox", "-profile:v", "high",
            "-b:v", "18M", "-maxrate", "24M", "-bufsize", "36M",
            "-g", "48", "-pix_fmt", "yuv420p",
            str(unit_75s),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Multiply 4x via stream_loop (-c copy) -> 30.00s 4K Master Loop in 0.1s!
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-stream_loop", "3",
            "-i", str(unit_75s),
            "-c", "copy",
            str(out_loop_path),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if unit_75s.exists():
        unit_75s.unlink()

    return str(out_intro_path), str(out_loop_path)


def extract_thumbnail(video_path: str, thumb_path: str, variant: str = "account1") -> str:
    """Extracts a vibrant, tack-sharp 1280x720 YouTube thumbnail (<2MB) from the 4K video."""
    out = Path(thumb_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if variant == "account1":
        vf = "scale=1280:720:flags=lanczos,cas=strength=0.4,eq=contrast=1.05:saturation=1.06:brightness=0.01"
        ss = "00:00:01"
    else:
        vf = "scale=1280:720:flags=lanczos,cas=strength=0.4,eq=contrast=1.06:saturation=1.08:brightness=0.02"
        ss = "00:00:12"

    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", ss,
        "-i", str(video_path),
        "-frames:v", "1",
        "-vf", vf,
        "-q:v", "3",
        str(out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return str(out)


def render_dual_youtube_videos(
    raw_clip_path: str,
    scene_id: str,
    duration_sleep_sec: int = 4800,
    duration_chill_sec: int = 4800,
    out_dir: str = "output/02_masurian_lakes_dusk",
) -> dict:
    """
    Renders the 40-second Perfected 4K Master clips (`master_40s_4k_*.mp4`),
    15-second 4K Previews (`preview_15s_*.mp4`), and concatenates/multiplies the 4K Master Loop
    into the full 1 hour 20 minute (`4800s` = `01:20:00`) 4K Ultra HD YouTube videos!
    """
    episode_dir = Path(raw_clip_path).resolve().parent
    out_base = Path(out_dir)
    acc1_dir = out_base / "account_1_sleep"
    acc2_dir = out_base / "account_2_chill"
    acc1_dir.mkdir(parents=True, exist_ok=True)
    acc2_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ensure 4K locked camper matte & 4K fixed-buoy weathervane clips exist
    assets = ensure_4k_locked_assets(episode_dir)

    # 2. Build 4K Storm-Onset Intro (~8.8s) + 30.0s Seamless 4K Master Loop for both variants
    intro1 = acc1_dir / "intro_storm_onset_4k_acc1.mp4"
    loop1 = acc1_dir / "loop_30s_4k_account1_sleep.mp4"
    intro2 = acc2_dir / "intro_storm_onset_4k_acc2.mp4"
    loop2 = acc2_dir / "loop_30s_4k_account2_chill.mp4"

    build_40s_4k_storm_master_and_intro(episode_dir, intro1, loop1, assets, variant="account1")
    build_40s_4k_storm_master_and_intro(episode_dir, intro2, loop2, assets, variant="account2")

    # 3. Generate Studio Field-Recording ASMR Rain & Piano Audio Tracks (4800s = 1h 20m)
    audio1 = acc1_dir / "_audio_acc1.m4a"
    audio2 = acc2_dir / "_audio_acc2.m4a"
    generate_sleep_rain_track(str(audio1), duration_sec=duration_sleep_sec, seed=101, raw_clip_path=raw_clip_path)
    generate_chill_lofi_rain_track(str(audio2), duration_sec=duration_chill_sec, seed=202, raw_clip_path=raw_clip_path)

    # 4. Multiply/Concatenate the 4K Master Loop to 1 Hour 20 Minutes (4800s = 01:20:00)
    concat1_txt = acc1_dir / "_concat_acc1.txt"
    concat2_txt = acc2_dir / "_concat_acc2.txt"

    loop1_dur = _probe_duration(str(loop1))
    loop2_dur = _probe_duration(str(loop2))
    reps1 = max(1, int(duration_sleep_sec // loop1_dur) + 2)
    reps2 = max(1, int(duration_chill_sec // loop2_dur) + 2)

    lines1 = [f"file '{intro1.resolve()}'"] + [f"file '{loop1.resolve()}'"] * reps1
    lines2 = [f"file '{intro2.resolve()}'"] + [f"file '{loop2.resolve()}'"] * reps2
    concat1_txt.write_text("\n".join(lines1) + "\n", encoding="utf-8")
    concat2_txt.write_text("\n".join(lines2) + "\n", encoding="utf-8")

    final_mp4_1 = acc1_dir / f"{scene_id}_account1_sleep.mp4"
    final_mp4_2 = acc2_dir / f"{scene_id}_account2_chill.mp4"

    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat1_txt),
            "-i", str(audio1),
            "-map", "0:v:0", "-map", "1:a:0",
            "-t", str(duration_sleep_sec),
            "-c:v", "copy", "-c:a", "copy",
            "-movflags", "+faststart",
            str(final_mp4_1),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat2_txt),
            "-i", str(audio2),
            "-map", "0:v:0", "-map", "1:a:0",
            "-t", str(duration_chill_sec),
            "-c:v", "copy", "-c:a", "copy",
            "-movflags", "+faststart",
            str(final_mp4_2),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # 5. Save the 40-second Perfected 4K Master videos (with audio), 1-minute 4K Masters, and 15s 4K Previews
    prev1 = acc1_dir / "preview_15s_account1_sleep.mp4"
    prev2 = acc2_dir / "preview_15s_account2_chill.mp4"
    master40_1 = acc1_dir / "master_40s_4k_account1_sleep.mp4"
    master40_2 = acc2_dir / "master_40s_4k_account2_chill.mp4"
    master60_1 = acc1_dir / "master_1min_4k_account1_sleep.mp4"
    master60_2 = acc2_dir / "master_1min_4k_account2_chill.mp4"

    for src_vid, p15, m40, m60 in (
        (final_mp4_1, prev1, master40_1, master60_1),
        (final_mp4_2, prev2, master40_2, master60_2),
    ):
        subprocess.run(
            [FFMPEG_BIN, "-y", "-i", str(src_vid), "-t", "15", "-c", "copy", str(p15)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [FFMPEG_BIN, "-y", "-i", str(src_vid), "-t", "40", "-c", "copy", str(m40)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [FFMPEG_BIN, "-y", "-i", str(src_vid), "-t", "65", "-c", "copy", str(m60)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    for tmp in (intro1, intro2, audio1, audio2, concat1_txt, concat2_txt):
        if tmp.exists():
            tmp.unlink()

    thumb1 = extract_thumbnail(str(final_mp4_1), str(acc1_dir / "thumbnail_account1.jpg"), variant="account1")
    thumb2 = extract_thumbnail(str(final_mp4_2), str(acc2_dir / "thumbnail_account2.jpg"), variant="account2")
    meta = generate_youtube_packages(scene_id, str(out_base), duration_sleep_sec, duration_chill_sec)

    return {
        "account_1_video": str(final_mp4_1),
        "account_1_master_40s_4k": str(master40_1),
        "account_1_master_1min_4k": str(master60_1),
        "account_1_preview": str(prev1),
        "account_1_thumbnail": thumb1,
        "account_1_metadata": meta["account_1_metadata"],
        "account_2_video": str(final_mp4_2),
        "account_2_master_40s_4k": str(master40_2),
        "account_2_master_1min_4k": str(master60_2),
        "account_2_preview": str(prev2),
        "account_2_thumbnail": thumb2,
        "account_2_metadata": meta["account_2_metadata"],
        "vidiq_report": meta["vidiq_report"],
    }
