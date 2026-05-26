# CERN: MISJA HIGGS — Dokumentacja Projektu

**Uwaga:** Projekt nie został ukończony ze względu na ograniczenia czasowe. Zrealizowanea została cześć głównych założeń symulacji (Negative Ion Source + LEBT w Linac4), natomiast pozostałe odcinki akceleratorów (RFQ, MEBT, DTL, CCDTL, PIMS, Booster, PS, SPS, LHC) są zaplanowane, lecz jeszcze niezaimplementowane.

---

## Opis projektu

**CERN: Misja Higgs** to interaktywny symulator konsolowy napisany w Pythonie, który pozwala użytkownikowi wcielić się w rolę inżyniera CERN i przeprowadzić wiązkę cząstek przez kolejne etapy rzeczywistego kompleksu akceleratorów — od źródła jonów aż po Wielki Zderzacz Hadronów (LHC).

Projekt łączy elementy edukacyjne z mechaniką gry: gracz musi ustawić parametry fizyczne każdego odcinka akceleratora w poprawnym zakresie, aby wiązka przeżyła i dotarła do detektorów.

---

## Wymagania

- Python 3.10+
- Biblioteka standardowa (brak zewnętrznych zależności pip)
- Moduł `turtle` (wbudowany w Python)
- Terminal obsługujący kody ANSI (Windows: Terminal / PowerShell; Linux/macOS: dowolny terminal)
- Zalecana szerokość okna terminala: **minimum 112 znaków**

---

## Uruchomienie

```bash
python main.py
```

---

## Struktura plików

| Plik | Opis |
|---|---|
| `main.py` | Punkt wejścia programu — inicjalizuje obiekty i uruchamia kolejne panele sterowania |
| `commands.py` | Wszystkie klasy konsol CMD (`AuthorizationPanel`, `ControlPanelIonSource`, `ControlPanelLinac4`) |
| `physics.py` | Silnik fizyczny — klasy `NegativeIonSource` i `Linac4` z metodami obliczeniowymi |
| `objects.py` | Modele danych: `User`, `Beam`, `AcceleratorData`, `AcceleratorEnvironment` |
| `cern_map.py` | Mapa graficzna kompleksu CERN rysowana w oknie Turtle z animacją wiązki |
| `utils.py` | Style ANSI, ekran tytułowy, pasek postępu (`Create_progress_bar`) |

---

## Przebieg rozgrywki

### 1. Ekran tytułowy
Program wyświetla animowany ekran tytułowy z paskiem ładowania.

### 2. Autoryzacja
Gracz musi się zalogować. Dane dostępowe:
- Komenda: `login <nazwa_użytkownika>`
- Komenda: `password <hasło>` — hasło podane jest w dokumentacji projektu

### 3. Negative Ion Source
Gracz konfiguruje źródło jonów wodorowych H⁻. Kroki w kolejności:

| Krok | Komenda | Zakres wartości |
|---|---|---|
| 1 | `otworz_zawor <czas [µs]>` | tak, by ciśnienie mieściło się w [2.8, 4.2] Pa |
| 2 | `moc_startowa_RF <moc [kW]>` | [20, 100] kW |
| 3 | `moc_RF <moc [kW]>` | [10, 50] kW |
| 4 | `temp_cezu <temperatura [°C]>` | (40, 100) °C |
| 5 | `gotowe` | przejście do Linac4 |

### 4. Linac4 — odcinek LEBT
Gracz prowadzi wiązkę przez odcinek niskiej energii (Low Energy Beam Transport, długość 1.8 m). Cel: utrzymać wiązkę na osi rury i nie stracić jej o ścianki.

| Komenda | Opis | Zakres |
|---|---|---|
| `prad_solenoidu <A>` | Skupia wiązkę magnetycznie | [200, 300] A |
| `napiecie_magnesu_korekcyjnego <V>` | Koryguje odchylenie poprzeczne Y | [-50, 50] V |
| `pompa_prozni <on/off>` | Obniża ciśnienie resztkowe gazu | cel: < 1×10⁻⁴ Pa |
| `gotowe` | Zamknięcie odcinka LEBT | — |

### 5. Raport końcowy
Po zakończeniu LEBT wyświetlany jest pełny raport stanu wiązki.

---

## Komendy systemowe (dostępne wszędzie)

| Komenda | Opis |
|---|---|
| `help` | Wyświetla menu pomocy dla aktywnego panelu |
| `help <komenda>` | Szczegółowy opis konkretnej komendy |
| `podpowiedz` | Podpowiedź co należy zrobić w aktualnym kroku |
| `mapa` | Otwiera okno graficzne z mapą kompleksu CERN |
| `status_wiazki` | Pełny raport parametrów wiązki (dostępny w Linac4) |
| `clear` / `cls` / `wyczysc` | Czyści terminal |
| `exit` | Zamyka aktywny panel |

---

## Mapa CERN (`cern_map.py`)

Komenda `mapa` otwiera okno Turtle z interaktywną mapą kompleksu, zawierającą:
- **LINAC 4** — linia startowa (czerwona)
- **BOOSTER** — pierwszy pierścień (pomarańczowy)
- **PS** (Proton Synchrotron) — żółty
- **SPS** (Super Proton Synchrotron) — zielony
- **LHC** (Large Hadron Collider) — niebieski
- Linie transferowe między akceleratorami (szare)
- Cztery główne detektory: **ATLAS**, **CMS**, **ALICE**, **LHCb**
- Animacja wiązki poruszającej się przez cały kompleks

Mapa automatycznie skaluje się do rozmiaru okna (trzy layouty: large / medium / small).

---

## Architektura fizyczna (physics.py)

### Klasy stałych fizycznych

- `PhysicalConstants` — prędkość światła, stała Boltzmanna, liczba Avogadra
- `Electron`, `Proton`, `Hydrogen`, `HydrideIon` — masy, ładunki, parametry cząstek

### NegativeIonSource — implementowane metody

| Metoda | Opis |
|---|---|
| `I_S_calculate_mass_hydrogen` | Masa H₂ w komorze po otwarciu zaworu (symulacja całkowania dt=100 ns) |
| `I_S_calculate_number_density` | Koncentracja cząsteczek (gęstość liczbowa) |
| `I_S_calculate_chamber_pressure` | Ciśnienie przez równanie gazu doskonałego |
| `I_S_calculate_ionization_efficiency` | Wydajność jonizacji RF (sigmoid względem mocy) |
| `I_S_calculate_RF_field_energy` | Energia pola RF dostarczona do plazmy |
| `I_S_calculate_electron_density` | Koncentracja elektronów w plazmie |
| `I_S_calculate__beam_current` | Prąd wiązki H⁻ (prawo Childa-Langmuira + wzór Gaussa dla cezu) |
| `I_S_calculate_beam_intensity` | Liczba jonów w impulsie |
| `I_S_calculate_beam_emittance` | Znormalizowana emitancja termiczna |

### Linac4 — LEBT — implementowane metody

| Metoda | Opis |
|---|---|
| `lebt_calculate_vacuum` | Ciśnienie w rurze po jednym kroku — napływ gazu vs. pompowanie |
| `lebt_calculate_transmission` | Straty prądu przez zderzenia jonów z resztkami gazu |
| `lebt_calculate_solenoid_focus` | Siła skupiająca solenoidu |
| `lebt_calculate_scraping_and_nominal_losses` | Straty przez uderzenia o ścianki + straty nominalne |
| `lebt_apply_environmental_drift` | Degradacja termiczna solenoidu, desorpcja gazu, drgania mechaniczne |
| `lebt_calculate_trajectory_step` | Nowe position_y i kąt wiązki po przebyciu dx metrów |
| `lebt_process_automatic_step` | Orkiestracja — wywołuje wszystkie powyższe w odpowiedniej kolejności |

---

## Model danych (objects.py)

### Beam
Główny obiekt śledzony przez cały symulator.

| Atrybut | Jednostka | Opis |
|---|---|---|
| `position_x` | m | Droga wzdłuż tunelu |
| `position_y` | m | Poprzeczne odchylenie od osi |
| `angle` | rad | Kąt trajektorii |
| `energy` | MeV | Energia kinetyczna |
| `current` | mA | Prąd wiązki |
| `N_Intensity` | — | Liczba jonów w paczce |
| `epsilon` | mm·mrad | Emitancja |
| `is_alive` | bool | Flaga zniszczenia wiązki |

### AcceleratorEnvironment
Zarządza stanem każdego akceleratora osobno. Metody `set_accelerator(name)` i `copy_data(from, to)` pozwalają na przełączanie kontekstu i przenoszenie parametrów między odcinkami.

---

## Planowane rozszerzenia (niezrealizowane)

- **RFQ** (Radio-Frequency Quadrupole) — pierwsza akceleracja do 3 MeV
- **MEBT** (Medium Energy Beam Transport) — transport przy 3 MeV
- **DTL** (Drift Tube Linac) — akceleracja do 50 MeV
- **CCDTL** (Cell-Coupled DTL) — akceleracja do 100 MeV
- **PIMS** (Pi-Mode Structure) — akceleracja do 160 MeV
- **Booster / PS / SPS / LHC** — kolejne pierścienie z logiką synchronotronową
- Zapis/wczytywanie stanu gry

---

## Autorzy
Damian Mrazewski
Projekt stworzony w ramach **Gigathon 2026**.