#!/usr/bin/env python3
"""
YouTube SEO & Anti-Ban Metadata Packager for Account 1 (Sleep) and Account 2 (Cozy Chill).
"""

import json
from pathlib import Path
from src.vidiq_analyzer import analyze_niche_vidiq


def _format_chapters(duration_sec: int, mode: str) -> str:
    if mode == "sleep":
        return (
            "00:00 Cozy Camper Van Setup & Sudden Masurian Storm Onset\n"
            "15:00 Deep Rainstorm Resonance & Wind in Lakeside Reeds\n"
            "35:00 Raindrops on Wooden Pier & Lake Surface (No Thunder Spikes)\n"
            "55:00 Night Dimming Mode for Melatonin & Deep Sleep\n"
            "01:10:00 Continuous Uninterrupted Rain on Tin Van Roof (1h 20m)"
        )
    return (
        "00:00 Warm Camper Van, Steaming Mug & Masurian Storm Onset\n"
        "15:00 Deep Focus Rain, Wind in Reeds & Warm Acoustic Piano\n"
        "35:00 Cozy Late Night Reading & Study Flow by the Lake\n"
        "55:00 Gentle Rain on Wooden Pier & Soft Rhodes Chords\n"
        "01:10:00 Uninterrupted Lo-Fi Rain & Camper Warmth (1h 20m)"
    )


def generate_youtube_packages(scene_id: str, out_dir: str, dur_sleep_sec: int = 5400, dur_chill_sec: int = 4500) -> dict:
    scenes_path = Path("prompts/camper_scenes.json")
    scenes_data = json.loads(scenes_path.read_text(encoding="utf-8"))
    scene = next((s for s in scenes_data["locations"] if s["id"] == scene_id), scenes_data["locations"][0])

    vidiq_data = analyze_niche_vidiq(scene["primary_keyword"], scene.get("secondary_keywords", []))

    out_base = Path(out_dir)
    acc1_dir = out_base / "account_1_sleep"
    acc2_dir = out_base / "account_2_chill"
    acc1_dir.mkdir(parents=True, exist_ok=True)
    acc2_dir.mkdir(parents=True, exist_ok=True)

    # Account 1: Sleep / Pure Rain ASMR
    title_1 = scene["yt_title_sleep"].replace("—", "-").replace("–", "-")
    desc_1 = f"""{title_1}

Welcome inside our wooden camper van parked at {scene['name']}. Settle into the warm blankets with a steaming mug of hot chocolate on the shelf while heavy rain drums steadily against the metal van roof and pours outside the open rear tailgate.

This soundscape features zero mid-roll ad interruptions and a gentle night-toned atmosphere designed to help you fall asleep fast, block out distractions, and relieve late-night stress.

CHAPTERS:
{_format_chapters(dur_sleep_sec, "sleep")}

ABOUT OUR PRODUCTION PROCESS (ORIGINAL AUDIO & VISUAL ART):
Every episode on this channel is custom-crafted from our original wooden camper van POV artwork and multi-layered acoustic sound design. The audio is mixed in-house by combining resonant metallic camper roof rain textures, wide stereo open-door rainfall, and low-pass filtered distant thunder rumbles so there are never any harsh frequencies to wake you up.

#RainOnCamperRoof #CamperVanRain #RainSoundsForSleeping #NoAdsRain #TinRoofRain #DeepSleep #VanLifeAmbience
"""

    meta_1_text = (
        f"=== KONTO 1 (SLEEP / PURE RAIN ASMR) ===\n"
        f"VIDIQ OPPORTUNITY SCORE: {vidiq_data['vidiq_overall_score']}/100 "
        f"(Demand: {vidiq_data['vidiq_demand_score']}/100, Competition: {vidiq_data['vidiq_competition_score']}/100)\n\n"
        f"TYTUL (Wklej w YouTube Studio):\n{title_1}\n\n"
        f"OPIS (Wklej w YouTube Studio):\n{desc_1}\n"
        f"TAGI VIDIQ (Skopiuj w pole Tagi w YouTube Studio - Ponizej 500 znakow):\n{vidiq_data['tags_csv']}\n"
    )
    meta_1_file = acc1_dir / "youtube_metadata.txt"
    meta_1_file.write_text(meta_1_text, encoding="utf-8")

    # Account 2: Cozy Chill / Rain + Warm Ambient Lo-Fi
    title_2 = scene["yt_title_chill"].replace("—", "-").replace("–", "-")
    tags_2_list = [
        "cozy camper van ambience",
        "rain and lofi study",
        "camper van rain sounds",
        "ambient rain for studying",
        "cozy van life rain",
        "warm ambient music and rain",
        "reading ambience rain",
        "focus music rain in car",
    ] + [t for t in vidiq_data["recommended_tags"] if t not in ("black screen rain", "dark screen rain")][:10]
    tags_2_csv = ", ".join(dict.fromkeys(tags_2_list))[:460]

    desc_2 = f"""{title_2}

Grab a warm mug of coffee or hot chocolate and relax inside our wooden camper van overlooking {scene['name']}. Outside the open rear doors, a steady rainstorm washes over the landscape while warm fairy lights and soft, evolving ambient chords fill the cabin.

Created for deep focus, coding, reading, late-night study sessions, or unwinding after a long day.

CHAPTERS:
{_format_chapters(dur_chill_sec, "chill")}

HOW WE CREATE OUR VIDEOS (ORIGINAL SOUND & VISUAL DESIGN):
Each visual and audio session is originally produced and mixed for our camper van series. We combine custom-synthesized warm analog-style ambient harmonic pads with multi-layered camper roof rainfall and subtle interior foley to create a distraction-free workspace.

#CozyCamperVan #RainAndAmbient #StudyAmbience #VanLifeRain #CozyRain #FocusMusic #RainSounds
"""

    meta_2_text = (
        f"=== KONTO 2 (COZY FOCUS / RAIN + AMBIENT LO-FI) ===\n"
        f"VIDIQ OPPORTUNITY SCORE: {vidiq_data['vidiq_overall_score']}/100\n\n"
        f"TYTUL (Wklej w YouTube Studio):\n{title_2}\n\n"
        f"OPIS (Wklej w YouTube Studio):\n{desc_2}\n"
        f"TAGI VIDIQ (Skopiuj w pole Tagi w YouTube Studio - Ponizej 500 znakow):\n{tags_2_csv}\n"
    )
    meta_2_file = acc2_dir / "youtube_metadata.txt"
    meta_2_file.write_text(meta_2_text, encoding="utf-8")

    # Save raw JSON analysis as well
    (out_base / "vidiq_report.json").write_text(json.dumps(vidiq_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "account_1_metadata": str(meta_1_file),
        "account_2_metadata": str(meta_2_file),
        "vidiq_report": str(out_base / "vidiq_report.json"),
        "title_1": title_1,
        "title_2": title_2,
    }
