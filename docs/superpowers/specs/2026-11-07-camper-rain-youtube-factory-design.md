# Specyfikacja Projektu: Camper Rain YouTube Factory

**Data:** 2026-11-07
**Projekt:** `/Users/nowy/Documents/Projekty AI/Deszcz youtube`

---

## 1. Cel Biznesowy i Strategia Kanałów

Budowa zautomatyzowanego systemu produkcyjnego ("fabryki") dla **dwóch niezależnych kanałów YouTube** w niszy *Rain / Cozy Ambience / Sleep & Study Utility*:
- **Kanał 1 (Sleep & Insomnia Utility):** Czyste ASMR deszczu uderzającego o dach kampera (*Tin/Van Roof*) + szum ulewy za otwartymi drzwiami + losowe, miękkie grzmoty w oddali (bez muzyki).
- **Kanał 2 (Cozy Focus / Chill Study):** Deszcz w kamperze połączony z ciepłym, relaksującym podkładem *Ambient / Lo-Fi* (do nauki, pracy i czytania).

### Zasada dźwigni produkcyjnej (1 Generacja = 2 Unikalne Filmy)
Z jednej wygenerowanej sceny w Google Flow system lokalnie produkuje **dwa technicznie i wizualnie odrębne filmy (1-3h)** o innym odcisku cyfrowym (perceptual video hash), innym gradingu kolorystycznym, minimalnie innym wykadrowaniu, innej długości pętli oraz dwóch różnych ścieżkach dźwiękowych i miniaturkach. Chroni to oba kanały przed flagami *Reused Content* i *Inauthentic Content*.

---

## 2. Identyfikacja Wizualna ("Master Camper Frame")

Każdy film na kanale ma w 100% rozpoznawalną kompozycję pierwszoplanową w proporcjach `16:9` (YouTube Widescreen):
- **Perspektywa (POV):** Widz siedzi wewnątrz przerobionego do spania kampera/vana na wygodnym materacu i patrzy na wprost w stronę otwartych na oścież tylnych drzwi bagażnika (klapy podniesionej do góry).
- **Brzegi kadru (Rama samochodu):**
  - **Dół kadru:** Miękki materac, zmięty przytulny koc/pościel, poduszki po bokach.
  - **Lewa i prawa krawędź:** Ścianki wnętrza kampera (drewniana boazeria / tapicerka vana, drobne przytulne detale jak kubek czy lampka, uszczelki drzwiowe).
  - **Górna krawędź:** Podniesiona do góry klapa tylnego bagażnika z widoczną krawędzią dachu, z której spływają krople deszczu, oraz ciepłe światełka LED (fairy lights) wewnątrz vana.
  - **Brak ludzi i zwierząt:** Czysty widok pierwszoosobowy (POV).
- **Środek kadru (Otwór bagażnika):** Na etapie wzorca bazowego ("Master Frame") wypełniony jednolitym zielonym tłem (Chroma Key Green) lub neutralnym tłem referencyjnym, co pozwala:
  1. Dopracować w 100% sam wygląd wnętrza kampera.
  2. Używać go w Google Flow jako stałego **Składnika (Ingredient / Image Reference)**, w którym zmienia się wyłącznie sceneria i deszcz za otwartym bagażnikiem.

---

## 3. Architektura Techniczna (4 Moduły)

### Moduł 1: Wzorzec Kampera i Generacja w Google Flow (`prompts/`)
- Wybór 1 docelowego kadru bazowego ("Master Camper Frame") spośród 6 wygenerowanych propozycji `16:9`.
- Zapisanie kadru bazowego jako stałego odnośnika (Ingredient) w Google Flow (`labs.google/fx/tools/flow`).
- Dla każdego odcinka: generowanie nowej lokacji w deszczu w **Nano Banana 2 / Pro** na bazie wzorca kampera, a następnie animacja wideo najtańszym modelem o wysokiej jakości ruchu (**Omni Flash** lub **Veo 3.1 Lite/Fast**).

### Moduł 2: Proceduralny Silnik Audio (`src/audio_engine.py`)
Generuje dwie w 100% unikalne ścieżki audio o długości 1-3 godzin:
- **Wariant A (Konto 1 - Pure Camper Rain):** Wielowarstwowy miks dudnienia deszczu o blaszany dach kampera + szeroki szum ulewy z otwartych drzwi + losowo rozmieszczone w czasie pomruki odległego grzmotu (z filtrem dolnoprzepustowym ucinającym ostre częstotliwości).
- **Wariant B (Konto 2 - Camper Rain + Cozy Ambient/Lo-Fi):** Deszcz obniżony o `-6 dB` + ciepły, wolno ewoluujący podkład muzyczny *Ambient Pad / Chill Lo-Fi* (wolny od roszczeń Content ID).

### Moduł 3: Silnik Bezszwowej Pętli i Anty-Duplikatu (`src/video_builder.py`)
Przetwarza krótki klip wideo z Google Flow w dwa gotowe, długie filmy `.mp4`:
- **Bezszwowa pętla (`xfade`):** Łączy koniec i początek klipu miękkim przejściem (1,5s), eliminując przeskok klatek.
- **Transformacja Anty-Duplikatowa:**
  - *Konto 1 (Sleep):* Chłodniejszy nocny grading (*Midnight Blue*), oryginalny kadr `100%`, opcjonalne przyciemnienie nocne po 25 minutach, długość np. `2h 12m`.
  - *Konto 2 (Focus/Chill):* Ciepły bursztynowy grading (*Golden Camper Glow*), mikro-zoom `104%` z subtelnym ziarnem 35mm, inna długość pojedynczego cyklu pętli, długość filmu np. `1h 47m`.
- **Szybki eksport (`-stream_loop`):** Renderowanie pełnego 2-godzinnego filmu 1080p/4K w kilka minut.

### Moduł 4: Pakowacz YouTube SEO (`src/yt_packager.py`)
Automatycznie generuje dla obu kont:
- Dwie odrębne miniaturki `1280x720` (`thumbnail_account1.jpg`, `thumbnail_account2.jpg`).
- Pliki `youtube_metadata_account1.txt` i `youtube_metadata_account2.txt` zawierające:
  - Klikalne tytuły z haczykiem `(NO ADS)` i nazwą lokacji.
  - Naturalny opis z sekcją *Behind the Scenes / Production Process* (tarcza przed odrzuceniem monetyzacji za *Inauthentic Content*).
  - Znaczniki czasu (rozdziały), 5-8 hashtagów i zestaw 18 tagów długiego ogona (*long-tail keywords*).
