#!/usr/bin/env python3
"""
Automatyzacja pełnej konfiguracji kanału YouTube (Lazy Jack Production)
oraz publikacji i ustawienia miniatur dla filmów w YouTube Studio przez Google Chrome.
Wymaga włączonej opcji: Widok -> Deweloper -> Zezwól na kod JavaScript z Apple Events.
"""
import base64
import json
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run_yt_js(js_code: str) -> str:
    apple_escaped = js_code.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    apple = f"""
tell application "Google Chrome"
    repeat with w from 1 to count of windows
        repeat with t from 1 to count of tabs of window w
            if URL of tab t of window w contains "studio.youtube.com" then
                return execute tab t of window w javascript "{apple_escaped}"
            end if
        end repeat
    end repeat
end tell
"""
    res = subprocess.run(["osascript", "-"], input=apple, text=True, capture_output=True)
    if res.stderr:
        raise RuntimeError(res.stderr.strip())
    return res.stdout.strip()


CHANNEL_KEYWORDS = (
    "rain on camper roof, camper van rain sounds, rain sounds for sleeping, "
    "cozy camper van ambience, heavy rain on tin roof no ads, van life rain sounds, "
    "sleeping in camper van during rain, forest lake rain sounds, cozy rain and ambient lofi, "
    "study ambience rain, deep sleep rain sounds, nature sounds no thunder spikes, "
    "dark screen rain sounds, asmr rain on car roof, relaxing rain soundscape, "
    "insomnia relief rain, warm cabin rain ambience"
)

CHANNEL_DESCRIPTION = """Welcome to Lazy Jack Production - your cozy wooden camper van sanctuary for deep sleep, peaceful relaxation, and distraction-free focus.

We craft high-definition, uninterrupted ambient soundscapes recorded and mixed around natural lakeside rainfall, resonant camper van roofs, and warm 2000K cabin lighting. Every session is engineered using psychoacoustic principles (smooth pink-spectrum rainfall, zero harsh high-frequency transients, and gentle night dimming) to help you fall asleep faster, calm anxiety, mask tinnitus, or lock into deep study and coding sessions.

New long-form rain and cozy van life episodes every week:
- Pure Rain on Camper Van Roof for Deep Sleep (No Mid-Roll Interruptions)
- Cozy Twilight Forest Lake & Warm Ambient Lo-Fi for Study, Reading & Focus
- Gentle Night-Dimming Soundscapes for Natural Melatonin & Stress Recovery

Settle under the warm blankets, grab a mug of hot chocolate, and let the rain wash away the day."""


def configure_channel_settings():
    print("1. Otwieranie Ustawień kanału...")
    run_yt_js("""
    (function() {
        const items = Array.from(document.querySelectorAll("tp-yt-paper-icon-item, a.menu-item-link"));
        for (const el of items) {
            if (el.innerText && el.innerText.includes("Ustawienia")) {
                el.click();
                return "clicked_settings";
            }
        }
        return "no_settings";
    })()
    """)
    time.sleep(1.8)

    run_yt_js("""
    (function() {
        const items = Array.from(document.querySelectorAll("tp-yt-paper-item, li"));
        for (const el of items) {
            if (el.innerText && el.innerText.trim() === "Kanał") {
                el.click();
                return "clicked_kanal";
            }
        }
        return "no_kanal";
    })()
    """)
    time.sleep(1.5)

    print("2. Wpisywanie słów kluczowych kanału (Basic Info)...")
    js_kw = f"""
    (function() {{
        const dlg = document.querySelector("ytcp-settings-dialog, tp-yt-paper-dialog");
        if (!dlg) return "no_dlg";
        const inputs = Array.from(dlg.querySelectorAll("input"));
        for (const inp of inputs) {{
            const ph = inp.getAttribute("placeholder") || inp.getAttribute("aria-label") || "";
            if (ph.includes("przecinkami") || ph.includes("Słowa kluczowe") || inp.id === "text-input") {{
                inp.focus();
                inp.value = {json.dumps(CHANNEL_KEYWORDS)};
                inp.dispatchEvent(new Event("input", {{bubbles: true}}));
                inp.dispatchEvent(new KeyboardEvent("keydown", {{key: "Enter", keyCode: 13, bubbles: true}}));
                inp.blur();
                return "filled_channel_keywords";
            }}
        }}
        return "no_kw_input";
    }})()
    """
    print("   ->", run_yt_js(js_kw))
    time.sleep(1.0)

    print("3. Ustawianie Odbiorców kanału (Nieprzeznaczony dla dzieci) w Ustawieniach zaawansowanych...")
    run_yt_js("""
    (function() {
        const tabs = Array.from(document.querySelectorAll("tp-yt-paper-tab"));
        for (const t of tabs) {
            if (t.innerText && t.innerText.includes("Ustawienia zaawansowane")) {
                t.click();
                return "clicked_adv";
            }
        }
        return "no_adv";
    })()
    """)
    time.sleep(1.2)
    print("   ->", run_yt_js("""
    (function() {
        const radios = Array.from(document.querySelectorAll("tp-yt-paper-radio-button"));
        for (const r of radios) {
            if (r.innerText && r.innerText.includes("Nie, oznacz ten kanał jako nieprzeznaczony dla dzieci")) {
                r.click();
                return "selected_not_mfk_channel";
            }
        }
        return "no_radio";
    })()
    """))
    time.sleep(1.0)

    print("4. Zapisywanie Ustawień kanału...")
    print("   ->", run_yt_js("""
    (function() {
        const btns = Array.from(document.querySelectorAll("ytcp-button#save-button button, ytcp-button[label=\\"Zapisz\\"] button, button"));
        for (const b of btns) {
            if (b.innerText && b.innerText.trim() === "Zapisz") {
                b.click();
                return "saved_settings";
            }
        }
        return "no_save";
    })()
    """))
    time.sleep(2.5)


def configure_channel_customization():
    print("5. Przechodzenie do Dostosowywanie -> Informacje podstawowe (Opis kanału)...")
    run_yt_js("""
    (function() {
        const items = Array.from(document.querySelectorAll("tp-yt-paper-icon-item, a.menu-item-link"));
        for (const el of items) {
            if (el.innerText && el.innerText.includes("Dostosowywanie")) {
                el.click();
                return "clicked_customization";
            }
        }
        return "no_customization";
    })()
    """)
    time.sleep(2.5)

    js_desc = f"""
    (function() {{
        const boxes = Array.from(document.querySelectorAll("#textbox, textarea"));
        for (const b of boxes) {{
            const label = b.getAttribute("aria-label") || b.getAttribute("placeholder") || "";
            if (label.includes("Opis") || label.includes("widzom") || b.id === "textbox") {{
                b.focus();
                b.innerText = {json.dumps(CHANNEL_DESCRIPTION)};
                b.dispatchEvent(new Event("input", {{bubbles: true}}));
                return "filled_channel_description";
            }}
        }}
        return "no_desc_box";
    }})()
    """
    print("   ->", run_yt_js(js_desc))
    time.sleep(1.2)

    print("   ->", run_yt_js("""
    (function() {
        const btns = Array.from(document.querySelectorAll("ytcp-button#publish-button button, button"));
        for (const b of btns) {
            if (b.innerText && b.innerText.trim() === "Opublikuj") {
                b.click();
                return "published_customization";
            }
        }
        return "no_publish_btn";
    })()
    """))
    time.sleep(2.5)


if __name__ == "__main__":
    configure_channel_settings()
    configure_channel_customization()
    print("Gotowe!")
