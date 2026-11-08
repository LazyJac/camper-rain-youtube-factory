# Camper Rain YouTube Factory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an end-to-end automated production pipeline that takes our Master Camper Frame (`16:9` wooden camper POV with steaming mug on the left shelf and open rear tailgate), generates rainy location clips in Google Flow, synthesizes two distinct 1-3h audio soundscapes (Pure Camper Rain ASMR for Account 1, Camper Rain + Cozy Ambient/Lo-Fi for Account 2), renders two visually and algorithmically unique looped videos (anti-duplicate video hash) with custom thumbnails and SEO metadata, and prepares/uploads them to YouTube via the user's logged-in Chrome browser.

**Architecture:** Modular Python + FFmpeg local production engine paired with browser automation for Google Flow (`labs.google/fx/tools/flow`) and YouTube Studio (`studio.youtube.com`). A single Google Flow clip is transformed into two completely independent digital assets (Account 1: Sleep/Dark Cooling Grading, 100% frame, Pure Rain + Thunder; Account 2: Cozy Study/Warm Amber Grading, 104% micro-zoom + film grain, Rain + Generative Ambient/Lo-Fi Pad).

**Tech Stack:** Python 3, FFmpeg (`libx264`, `aac`, `xfade`, `colorkey`, audio DSP synthesis), Chrome DevTools / Playwright CDP (`127.0.0.1:9222`).

## Global Constraints

- **Język komunikacji:** Polski (tytuły/opisy filmów na YouTube po angielsku pod globalny RPM, chyba że użytkownik wskaże inaczej).
- **Zakaz długich myślników:** Nigdy nie używaj `—` ani `–` w kodzie, opisach YouTube ani dokumentacji - wyłącznie zwykły myślnik `-`.
- **Wzorzec wizualny:** Zawsze kadr nr 1 (`master_camper_v1.jpg` - drewniany klasyk z parującym kubkiem po lewej stronie, ciemną pościelą na dole, lampkami LED po bokach i uniesioną klapą bagażnika u góry).
- **Ochrona przed Reused / Inauthentic Content:** Dwa filmy wygenerowane z jednej sceny muszą mieć różny kadr (`100%` vs `104%`), różny grading kolorystyczny, różną długość pętli, inną długość całkowitą (np. `1h 15m` vs `1h 05m` lub docelowe `1-3h`) oraz w 100% unikalne ścieżki audio i miniaturki.

---

### Task 1: Finalize Master Camper Frame (With Steaming Mug) & Scene Catalog

**Files:**
- Create: `assets/master_camper_v1.jpg`
- Create: `prompts/camper_scenes.json`
- Test: `tests/test_scenes.py`

**Interfaces:**
- Produces: `prompts/camper_scenes.json` containing `base_frame_path`, `base_prompt`, and `locations[]` (`id`, `name`, `scene_prompt`, `motion_prompt`, `yt_title_sleep`, `yt_title_chill`).

- [ ] **Step 1: Write test for scene catalog validation**

```python
import json
from pathlib import Path

def test_camper_scenes_schema():
    p = Path("prompts/camper_scenes.json")
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert Path(data["base_frame_path"]).exists()
    assert len(data["locations"]) >= 5
    for loc in data["locations"]:
        assert "id" in loc
        assert "scene_prompt" in loc
        assert "motion_prompt" in loc
        assert "—" not in loc["yt_title_sleep"]
        assert "–" not in loc["yt_title_sleep"]
```

- [ ] **Step 2: Create `prompts/camper_scenes.json` and verify `assets/master_camper_v1.jpg`**

- [ ] **Step 3: Run test to verify schema and assets**

---

### Task 2: Procedural Multi-Layer Audio Engine (2 Distinct Channels)

**Files:**
- Create: `src/audio_engine.py`
- Test: `tests/test_audio_engine.py`

**Interfaces:**
- Produces:
  - `generate_sleep_rain_track(output_path: str, duration_sec: int, seed: int) -> str` (Account 1: Pure camper tin roof rain + wide open tailgate rain + randomized distant soft thunder rumbles, low-pass filtered for deep sleep).
  - `generate_chill_lofi_rain_track(output_path: str, duration_sec: int, seed: int) -> str` (Account 2: Soft camper rain `-6 dB` + warm evolving ambient/lo-fi Rhodes/pad chords synthesized procedurally with zero Copyright/Content ID claims).

- [ ] **Step 1: Write test for audio engine generation**

```python
import subprocess
from pathlib import Path
from src.audio_engine import generate_sleep_rain_track, generate_chill_lofi_rain_track

def test_audio_tracks_generation(tmp_path):
    sleep_wav = tmp_path / "sleep.m4a"
    chill_wav = tmp_path / "chill.m4a"
    generate_sleep_rain_track(str(sleep_wav), duration_sec=15, seed=42)
    generate_chill_lofi_rain_track(str(chill_wav), duration_sec=15, seed=99)
    assert sleep_wav.exists() and sleep_wav.stat().st_size > 10000
    assert chill_wav.exists() and chill_wav.stat().st_size > 10000
```

- [ ] **Step 2: Implement `src/audio_engine.py` using FFmpeg DSP filters (`anoisesrc`, resonance eq, thunder envelopes, warm chord synthesis)**

- [ ] **Step 3: Run tests and verify audio quality**

---

### Task 3: Seamless Video Loop, Chroma/Flow Compositor & Anti-Duplicate Dual Renderer

**Files:**
- Create: `src/video_builder.py`
- Test: `tests/test_video_builder.py`

**Interfaces:**
- Consumes: Raw clip from Google Flow (or background rain loop + `assets/master_camper_v1.jpg` composite) and audio tracks from `src/audio_engine.py`.
- Produces:
  - `build_seamless_base_loop(raw_clip_path: str, output_loop_path: str, variant: str) -> str`
  - `render_dual_youtube_videos(raw_clip_path: str, scene_id: str, duration_sleep_sec: int, duration_chill_sec: int, out_dir: str) -> dict`

- [ ] **Step 1: Write test for seamless loop and dual anti-duplicate video rendering**

```python
from pathlib import Path
from src.video_builder import render_dual_youtube_videos

def test_dual_render(tmp_path):
    # Verify Account 1 and Account 2 outputs have distinct visual hashes, durations, and thumbnails
    pass
```

- [ ] **Step 2: Implement `src/video_builder.py` with `xfade` seamless looping, steam animation overlay on the mug, Midnight Storm grading (Account 1) vs Golden Camper Glow + 104% zoom (Account 2), and dual thumbnail extractor**

- [ ] **Step 3: Run test to verify both rendered MP4s and thumbnails**

---

### Task 4: YouTube SEO Metadata Packager & Chrome Automation (Google Flow + YouTube Studio)

**Files:**
- Create: `src/yt_packager.py`
- Create: `src/chrome_flow_yt.py`
- Test: `tests/test_yt_packager.py`

**Interfaces:**
- Produces:
  - `generate_youtube_packages(scene_id: str, out_dir: str) -> dict` (Generates `account_1_sleep/youtube_metadata.txt` and `account_2_chill/youtube_metadata.txt` with titles, anti-ban production descriptions, timestamps, hashtags, and 18 long-tail tags).
  - Browser automation helper connecting to user's logged-in Chrome (`DevToolsActivePort`) to drive Google Flow generation and YouTube Studio upload.
