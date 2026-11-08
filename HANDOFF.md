# HANDOFF - Fabryka Wideo YouTube (Deszcz w Kamperze POV)

## Cel projektu
Zautomatyzowany potok produkcyjny do generowania fotorealistycznych, długich filmów relaksacyjnych i nasennych (`1h 20m` = `4800s`) w jakości **4K Ultra HD (`3840x2160`)** oraz pionowych **YouTube Shorts (`9:16`, `1080x1920`)** na kanał YouTube (`@lazyjackproduction`, `lazyjackproduction@gmail.com`) ze stałym wnętrzem drewnianego kampera i kojącymi krajobrazami w deszczu.

## Wykonane rezultaty i ścieżki (Odcinek 02 - Polskie Mazury o Zmierzchu i Burza)
- **Pełne filmy 1h 20m (`4800 sekund`) w 4K Ultra HD (`3840x2160`, `24 fps`)**:
  - Wariant 1 (Sleep / Czysty Deszcz ASMR): [02_masurian_lakes_dusk_account1_sleep.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_1_sleep/02_masurian_lakes_dusk_account1_sleep.mp4) (`2.34 GB`, `4800s`)
  - Wariant 2 (Chill / Deszcz + Ciepłe Pianino): [02_masurian_lakes_dusk_account2_chill.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_2_chill/02_masurian_lakes_dusk_account2_chill.mp4) (`2.26 GB`, `4800s`)
- **40-sekundowe Dopracowane Mastery 4K Ultra HD (`3840x2160`)**:
  - Wariant 1 (Sleep ASMR - 40s Master 4K): [master_40s_4k_account1_sleep.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_1_sleep/master_40s_4k_account1_sleep.mp4) (`19.6 MB`)
  - Wariant 2 (Chill Piano - 40s Master 4K): [master_40s_4k_account2_chill.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_2_chill/master_40s_4k_account2_chill.mp4) (`18.9 MB`)
- **15-sekundowe Podglądy 4K (`3840x2160`)**:
  - [preview_15s_account1_sleep.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_1_sleep/preview_15s_account1_sleep.mp4)
  - [preview_15s_account2_chill.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/account_2_chill/preview_15s_account2_chill.mp4)
- **Pakiet 3 YouTube Shorts (`9:16`, `1080x1920`, wycięte z natywnego 4K) z lejkiem do filmu 1h 20m (`Powiązany film` / `Related Video`)**:
  - Short 1 (`24s` - Najazd Pan-and-Scan 4K od kubka na nadchodzącą burzę i pomost): [short_01_storm_onset_pan_9x16.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/shorts/short_01_storm_onset_pan_9x16.mp4)
  - Short 2 (`22s` - Pionowy kadr 4K na fizykę deszczu na pomoście, jeziorze i wiatr w trzcinach): [short_02_pier_reeds_rain_9x16.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/shorts/short_02_pier_reeds_rain_9x16.mp4)
  - Short 3 (`25s` - Wieczorny powrót kamery do wnętrza kampera z pianinem): [short_03_cozy_piano_camper_9x16.mp4](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/shorts/short_03_cozy_piano_camper_9x16.mp4)
  - Metadane i instrukcja podpięcia odnośnika "Powiązany film": [shorts_youtube_metadata.txt](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/output/02_masurian_lakes_dusk/shorts/shorts_youtube_metadata.txt)
- **Kod i dokumentacja skilla**:
  - [video_builder.py](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/src/video_builder.py) - silnik 4K łączący separację częstotliwościową `grainmerge` z klatki `5504x3072`, harmoniczne fale wiatru na trzcinach i trawie (`displace`), fizykę mikrorozbryzgów na drewnianym pomoście (bez kręgów wodnych na deskach) oraz bezstratne powielenie `-f concat -c copy` do `4800s` (`1h 20m`).
  - [shorts_builder.py](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/src/shorts_builder.py) - generator pionowych Shortsów `9:16` (`1080x1920`) z natywnego Mastera 4K.
  - [4k_deep_focus_and_location_roadmap.md](file:///Users/nowy/.claude/skills/cozy-rain-youtube-factory/references/4k_deep_focus_and_location_roadmap.md) oraz [SKILL.md](file:///Users/nowy/.claude/skills/cozy-rain-youtube-factory/SKILL.md) - zaktualizowany skill `cozy-rain-youtube-factory`.

## Faktyczna weryfikacja
- Zweryfikowano przez `ffprobe` wymiary `3840x2160` (`24 fps`) i czas trwania `4800.08s` (`1h 20m`) dla obu pełnych filmów oraz `1080x1920` dla 3 Shortsów.
- Przeprowadzono multimodalny audyt słuchowy (`read_file` na próbkach `.mp3`) oraz wzrokowy (`read_file` na klatkach 4K `t=0.5s`, `t=14.0s`, `t=26.0s` i klatce Shorta `9:16`), potwierdzając:
  1. Start dokładnie z kadru `2.0001/Camper_van_interior_looking_out_1c9b0bd5_4K.jpg` i szybkie wejście chmur burzowych oraz ulewy.
  2. Ostrość 4K na pierwszym i drugim planie (deski pomostu, trzciny, żaglówka Omega, las na horyzoncie).
  3. Ruch trzcin (*Phragmites*) i trawy na wietrze oraz zróżnicowaną fizykę deszczu (pionowe mikrorozbryzgi na mokrym drewnie pomostu vs koncentryczne kręgi na wodzie jeziora).

## Decyzje i stan referencji wozu (Camper Asset Lock)
- **Zablokowany wzorzec kampera (Asset Lock)**:
  - Główny plik referencyjny: [master_camper_locked_matte_4k.png](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/assets/master_camper_locked_matte_4k.png) (skopiowany z `assets/episodes/02_masurian_lakes_dusk/_camper_locked_matte_4k.png`).
  - **Zasada stałego kampera**: Wygląd kampera (sosnowe drewno boazerii, girlanda ciepłych lampek LED 2000K, ciemnoszary puszysty koc, drewniana półka po lewej z parującym ceramicznym kubkiem i zamkniętą książką w twardej oprawie, uniesiona tylna klapa z metalowymi siłownikami gazowymi) jest bezwzględnie stały dla wszystkich przyszłych generacji.
  - **Zasada swobody kamery i perspektywy**: W kolejnych odcinkach MOŻEMY dowolnie zmieniać lokalizację kamery, perspektywę i kąt widzenia (np. z głębi wnętrza, szerszy kąt, zbliżenie na półkę z kubkiem, lekki ukos na zewnątrz, kadr przez okno boczne lub otwarty tył). Van jest zawsze tą samą bazą podróżnika.
  - Zaktualizowano definicje w [camper_scenes.json](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/prompts/camper_scenes.json) oraz w skillu [cozy-rain-youtube-factory](file:///Users/nowy/.gemini/config/skills/cozy-rain-youtube-factory/SKILL.md).

## Stan commit / push / wdrożenie
- Pliki zapisane lokalnie w `/Users/nowy/Documents/Projekty AI/Deszcz youtube/output/02_masurian_lakes_dusk/`.
- **Repozytorium Git**: Przygotowano plik [.gitignore](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/.gitignore) ignorujący `output/`, wszystkie pliki `*.mp4`, surowe wideo oraz pliki tymczasowe. Zainicjalizowano lokalny Git (`git init`). Zgodnie z propozycją użytkownika, w każdej chwili możemy założyć prywatne repozytorium na GitHubie (`gh repo create`) dla samego kodu, skryptów, promptów i dokumentacji.
- Zgodnie z regułą Human-in-the-Loop, żaden film nie został jeszcze wysłany na YouTube - oczekuje na poprawki wizualne i akceptację użytkownika.

## Zdiagnozowane poprawki do wykonania (zapisane w `TODO.md`)
1. **Usunięcie efektu "jasno-ciemno" w pętli**: Obecny klip pętli (`_veo4k_storm_swing_back.mp4`) wycinał przedział `t=3.6s..7.8s` z `veo_native_4k_upsampled_02.mp4`, gdzie w `3.6s` było jeszcze jasno (`sky mean = 129.1`), a w `7.8s` ciemno (`sky mean = 54.4`). Pętla musi korzystać wyłącznie z ciemnej fazy nocnej (`t=6.15s..7.80s` z wyrównaną jasnością `sky mean ~ 55`), tak aby noc zapadała tylko raz w Intro (`0..8.8s`), a potem przez całe `1h 20m` panowała stała noc.
2. **Ożywienie pary nad kubkiem w małym wycinku (`x=420..760, y=750..1210` w 4K)**: Maska `_camper_locked_matte_4k.png` zamroziła dym z kubka. Należy oczyścić tło drewnianych desek za parą w tym kwadraciku i nałożyć tam samą zapętloną animację unoszącej się pary, bez ruszania kubka i ścian kampera.
3. **Lekki przebudowany Master (`-threads 2`, `-f concat -c copy`)**: Przeliczyć wyłącznie ~16 sekund materiału bazowego i podmienić strumień wideo bez obciążania laptopa.

## Następny krok
- Wznowić pracę od listy w [TODO.md](file:///Users/nowy/Documents/Projekty%20AI/Deszcz%20youtube/TODO.md): wygenerować poprawiony krótki podgląd ze stałą nocą w pętli i żywą parą z kubka, a po akceptacji podmienić pełny plik `1h 20m` przez `-c copy`.
