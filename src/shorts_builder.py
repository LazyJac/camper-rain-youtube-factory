#!/usr/bin/env python3
from __future__ import annotations
"""
YouTube Shorts (9:16 Vertical 1080x1920 from Native 3840x2160 4K Master) Builder & Funnel Packager.

Generates 3 distinct high-retention YouTube Shorts (1080x1920, 24fps) directly from the 4K Ultra HD
Master files + Studio ASMR Rain / Piano audio, along with YouTube Studio 'Related Video' (Powiazany film)
funnel metadata and pinned comments.
"""

import os
import subprocess
from pathlib import Path

FFMPEG_BIN = "/Users/nowy/homebrew/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"


def build_episode_shorts(
    out_episode_dir: str = "output/02_masurian_lakes_dusk",
    scene_id: str = "02_masurian_lakes_dusk",
) -> dict:
    base = Path(out_episode_dir)
    shorts_dir = base / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)

    master_sleep = base / "account_1_sleep" / "master_40s_4k_account1_sleep.mp4"
    master_chill = base / "account_2_chill" / "master_40s_4k_account2_chill.mp4"

    if not master_sleep.exists():
        master_sleep = base / "account_1_sleep" / f"{scene_id}_account1_sleep.mp4"
    if not master_chill.exists():
        master_chill = base / "account_2_chill" / f"{scene_id}_account2_chill.mp4"

    short1 = shorts_dir / "short_01_storm_onset_pan_9x16.mp4"
    short2 = shorts_dir / "short_02_pier_reeds_rain_9x16.mp4"
    short3 = shorts_dir / "short_03_cozy_piano_camper_9x16.mp4"

    # Short 1 (24s): Smooth 4K Pan-and-Scan from Cozy Steaming Mug (x=420) across the Camper Window
    # to the Masurian Lake, Swaying Reeds, Omega Sailboat & Wet Wooden Pier (x=1680) as the storm hits!
    vf_short1 = (
        "crop=w=1215:h=2160:x='420+1260*(0.5-0.5*cos(PI*min(t,14)/14))':y=0,"
        "scale=1080:1920:flags=lanczos,cas=strength=0.35,format=yuv420p"
    )
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-i", str(master_sleep),
            "-t", "24",
            "-vf", vf_short1,
            "-af", "afade=t=in:st=0:d=0.6,afade=t=out:st=23.2:d=0.8",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(short1),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Short 2 (22s): Pure Storm & Material Physics 4K Vertical Crop (t=10..32s of 4K Master)
    # Framed on the raised camper hatch at top, Omega sailboat in middle, wet wooden pier micro-splashes,
    # wind-swaying reeds on right, concentric lake ripples on left, and cozy blanket at bottom!
    vf_short2 = (
        "crop=w=1215:h=2160:x=1820:y=0,"
        "scale=1080:1920:flags=lanczos,cas=strength=0.35,format=yuv420p"
    )
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-ss", "10",
            "-i", str(master_sleep),
            "-t", "22",
            "-vf", vf_short2,
            "-af", "afade=t=in:st=0:d=0.6,afade=t=out:st=21.2:d=0.8",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(short2),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Short 3 (25s): Cozy Piano & Rain Camper POV (Account 2 Chill Master)
    # Slow gentle pan from the Masurian storm pier back toward the warm 2000K fairy lights & steaming mug
    vf_short3 = (
        "crop=w=1215:h=2160:x='1720-1180*(0.5-0.5*cos(PI*min(t,18)/18))':y=0,"
        "scale=1080:1920:flags=lanczos,cas=strength=0.35,format=yuv420p"
    )
    subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-ss", "6",
            "-i", str(master_chill),
            "-t", "25",
            "-vf", vf_short3,
            "-af", "afade=t=in:st=0:d=0.8,afade=t=out:st=24.0:d=1.0",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(short3),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    meta_txt = shorts_dir / "shorts_youtube_metadata.txt"
    meta_content = """=== PAKIET YOUTUBE SHORTS (9:16, 1080x1920) Z LEJKIEM DO FILMU 1H 20M ===

JAK PODPIAC ODNOSNIK DO PELNEGO FILMU 1H 20M W YOUTUBE STUDIO:
1. Wgraj wybrany plik Shorta (`short_01`, `short_02` lub `short_03`) w YouTube Studio na koncie @lazyjackproduction.
2. W kroku "Szczegoly" (lub w edycji filmu po prawej stronie pod "Widocznosc") kliknij pole **"Powiazany film" (Related video)**.
3. Wybierz z listy swoj pelny, 1-godzinny i 20-minutowy film 4K z Mazur.
4. Dzieki temu kazdy widz ogladajacy Shorta na telefonie zobaczy nad tytulem klikalny przycisk z odtwarzaczem prowadzacy prosto do pelnego filmu 1h 20m!

-------------------------------------------------------------------------
SHORT 1: `short_01_storm_onset_pan_9x16.mp4` (24s - Nagla burza na Mazurach z kampera POV)
-------------------------------------------------------------------------
TYTUL:
Sudden Rainstorm Hits Our Cozy Camper Van by the Lake 🌧️🚐 #Shorts #RainSounds #VanLife

OPIS:
Watching a sudden evening storm roll over the Masurian lake from inside our cozy wooden camper van. Listen to the heavy rain hitting the metal roof, wooden pier, and lake water while the reeds sway in the wind.

👉 Full 1 Hour 20 Min 4K Ultra HD version for deep sleep (No Mid-Roll Ads) is linked right above the title in the "Related Video" button!

#Shorts #RainOnCamperRoof #CamperVanRain #RainSoundsForSleeping #CozyCamper #ASMRRain #SleepSounds

PRZYPIETY KOMENTARZ (Wklej i przypnij pod Shortem):
🌧️ Pelna wersja 1h 20m w jakosci 4K Ultra HD do zasypiania i relaksu czeka w przycisku "Powiazany film" na dole ekranu (nad tytulem Shorta)! Slodkich snow! 🚐✨

-------------------------------------------------------------------------
SHORT 2: `short_02_pier_reeds_rain_9x16.mp4` (22s - Fizyka deszczu na pomoscie i wiatr w trzcinach 4K)
-------------------------------------------------------------------------
TYTUL:
Heavy Rain on Wooden Pier & Camper Roof 🌧️ Cozy Lake Storm #Shorts #ASMRRain #Sleep

OPIS:
Pure binaural rain sounds from inside our warm wooden camper van parked by a quiet Masurian lake pier. Watch the raindrops splash on the wet timber planks and lake surface while storm gusts bend the tall reeds.

👉 Tap the Related Video link at the bottom of the screen for the full 1h 20m 4K sleep session!

#Shorts #RainSounds #TinRoofRain #CozyRain #VanLifeAmbience #DeepSleep #Rainstorm

PRZYPIETY KOMENTARZ:
🎧 Chcesz zasnac przy tym dzwieku? Kliknij powiazany film nad tytulem Shorta - czeka tam pelne 1h 20m w 4K Ultra HD!

-------------------------------------------------------------------------
SHORT 3: `short_03_cozy_piano_camper_9x16.mp4` (25s - Wieczor w kamperze: Deszcz + Cieple Pianino)
-------------------------------------------------------------------------
TYTUL:
Cozy Camper Van Rain & Soft Piano by the Lake ☕🌧️ #Shorts #CozyAmbience #StudyMusic

OPIS:
Hot tea, warm 2000K fairy lights, gentle acoustic piano chords, and a heavy evening rainstorm outside the open camper van hatch.

👉 Tap the Related Video link above the title for the full 1h 20m 4K Ultra HD session for studying, reading, and relaxing!

#Shorts #CozyCamperVan #RainAndPiano #StudyAmbience #CalmMusic #VanLife #RainyEvening

PRZYPIETY KOMENTARZ:
☕ Pelna wersja 1h 20m (Deszcz + Cieple Pianino w 4K Ultra HD) jest podpieta jako "Powiazany film" na dole ekranu!
"""
    meta_txt.write_text(meta_content, encoding="utf-8")

    return {
        "short_1_storm_onset": str(short1),
        "short_2_pier_reeds": str(short2),
        "short_3_cozy_piano": str(short3),
        "shorts_metadata": str(meta_txt),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_episode_shorts(), indent=2))
