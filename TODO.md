# TODO - Odcinek 02 (Mazury o Zmierzchu): Poprawa Fizyki Nocy i Pary z Kubka

## 1. Zdiagnozowane problemy w obecnym wideo (`output/02_masurian_lakes_dusk/account_1_sleep`)
1. **Zła fizyka światła w pętli (cykliczne rozjaśnianie i ściemnianie nieba co ~7.5 s)**:
   - W `src/prepare_4k_buoy_locked_clips.py` klip pętli (`_veo4k_storm_swing_back.mp4`) został wycięty z `veo_native_4k_upsampled_02.mp4` z przedziału `ss=3.6s, dur=4.2s`.
   - Pomiary jasności nieba wykazały, że w `t=3.6s` jest jeszcze jasny zmierzch (`sky mean = 129.1`, `lake = 145`), a dopiero od `t=6.2s` do `t=7.8s` panuje ciemna noc (`sky mean = 54.4 - 59.0`, `lake = 46.7 - 56.7`).
   - Przez to każde powtórzenie pętli w `src/video_builder.py` wracało z ciemnej nocy do jasnego popołudnia.
2. **Zamrożony dym/para nad kubkiem**:
   - Maska `assets/episodes/02_masurian_lakes_dusk/_camper_locked_matte_4k.png` (`3840x2160` RGBA) ma `alpha = 255` na całym wnętrzu kampera, w tym na obszarze kubka i pary (`x=420..760, y=750..1210` w 4K).
   - Przez to biała smuga pary na tle drewnianych desek stoi nieruchomo jak na fotografii.

## 2. Co trzeba zrobić dalej (bez obciążania laptopa)
1. **Stała noc w pętli po jednorazowym zapadnięciu zmierzchu**:
   - **Intro (`~8.8 s`, tylko raz na początku filmu)**: Zostaje od `t=0.0s` do `t=7.8s` z `veo_native_4k_upsampled_02.mp4` - na początku filmu jednorazowo zapada burzowa noc.
   - **Pętla nocna (`loop_30s_4k_account1_sleep.mp4`)**: Zbudować wyłącznie z ustabilizowanej, ciemnej fazy nocnej (`t=6.15s .. 7.80s`, gdzie `sky mean ~ 55-58`) lub z wyrównaną krzywą ekspozycji Luma (tak, aby początek i koniec pętli miały identyczną ciemną jasność `sky mean = 55.0` i płynny `xfade` bez skoków jasności).
2. **Ożywienie pary nad kubkiem w małym kwadraciku (`x=420..760, y=750..1210`)**:
   - Z klatki `_camper_locked_matte_4k.png` usunąć zamrożoną smugę pary nad kubkiem (zrekonstruować czyste deski sosnowe w tle za parą na wycinku `340x460 px`).
   - Nałożyć w tym wycinku miękką, zapętloną warstwę unoszącej się pary wodnej (wyodrębnioną różnicowo z oryginalnego ujęcia lub animowaną laminarnie w górę), tak aby deski kampera, książka i sam kubek pozostały w 100% nieruchome, a poruszała się wyłącznie para.
3. **Bezpieczne złożenie pliku końcowego (`Zero Laptop Crash`)**:
   - Przeliczyć tylko krótki klip Intro (`~8.8 s`) oraz jedną jednostkę pętli (`~7.5 s`) z ograniczeniem wątków (`-threads 2` i sprzętowym `h264_videotoolbox`).
   - Złożyć 30-sekundowy podgląd oraz pełny film `1h 20m` (`4800 s`) wyłącznie bezstratnym kopiowaniem strumieni (`ffmpeg -f concat -c:v copy -c:a copy`), bez ponownego renderowania ścieżki audio i bez kodowania całego filmu.
