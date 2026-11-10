# Schnee & Betten

Data Analytics, Gruppenprojekt HS 2026, ZHAW

## Forschungsfrage

Wie stark beeinflussen Schneefall und Temperatur die Zimmerauslastung von Schweizer Hotels im Winter, und reagieren tief gelegene Wintersportorte (unter 1200 m ü. M.) stärker als hoch gelegene (über 1500 m ü. M.)?

**Auswahl und Höhenklassen:** Untersucht werden die 45 Wintersportorte unter den 186 Gemeinden der BFS-Statistik, also Gemeinden mit mindestens 1/3 der Logiernächte von Dezember bis März (2013–2025, ohne 2020 und 2021). Höhenklassen: tief unter 1200 m (13 Orte), mittel 1200–1500 m (19), hoch über 1500 m (13). Die Grenze liegt bei 1200 statt 1000 m, weil nur 3 Wintersportorte unter 1000 m liegen. Damit wäre kein Vergleich möglich. Die Einteilung mit 1000 m wird als Robustheitscheck mitgeführt (`hoehenklasse_1000`).

Die Frage geht über eine reine Vorhersage hinaus: Im Zentrum steht der Vergleich der Höhenklassen, also die Frage, *für wen* der Schnee wichtiger ist.

### Teilfragen

- (a) Reagieren Orte mit vielen inländischen Gästen anders als solche mit vielen ausländischen?
- (b) Ist die Schneeabhängigkeit 2022–2026 stärker als 2013–2019?

### Hypothesen

- **H1:** Mehr Neuschnee als üblich erhöht die Zimmerauslastung.
- **H2:** Der Effekt ist in tiefen Gemeinden grösser als in hohen.
- **H3:** Wärmere Monate senken die Auslastung in tiefen Gemeinden.
- **H4:** Ein höherer EUR/CHF-Kurs und deutsche Schulferien erhöhen die Auslastung.
- **H5:** Auch unter Berücksichtigung dieser Faktoren bleibt ein eigener Schnee-Effekt.

### Zielgrösse und Variablen

- **Zielgrösse:** Zimmerauslastung in %. Sie hängt nicht von der Grösse des Ortes ab, Logiernächte absolut schon.
- **Wetter:** Neuschnee (Abweichung vom Üblichen), Temperatur, Sonnenstunden
- **Ort:** Höhe bzw. Höhenklasse, Hotelkapazität (Zimmer, Betten), Anteil ausländischer Gäste
- **Zeit (gleich für alle Gemeinden):** Wechselkurs EUR/CHF, Schulferientage Deutschland, Schulferientage Schweiz*, Feiertage Schweiz

\* **Annahme:** Schweizer Schulferien gibt es als Daten erst ab Ende 2019. Für 2013–2019 ist das Ferienmuster 2021–2026 pro Kanton und Kalenderwoche zurückgeschrieben (Abweichung im Rückwärtstest Ø 0.9 Tage pro Monat, im Februar bis 3 Tage). Details in docs/features.md.

Details mit Einheit, Quelle und erwarteter Wirkung: [docs/features.md](docs/features.md)

### Abgrenzung

Die Corona-Winter 2019/20 (ab März 2020) und 2020/21 werden ausgeschlossen bzw. markiert. Die Auslastung war dort durch Schliessungen und Reisebeschränkungen bestimmt, nicht durch Schnee.

## Team

Gruppe 35
- Aakash Sethi
- Jelmer d'Hollosy
- Oliver Moser

## Daten

- BFS STAT-TAB Hotellerie (PxWeb-API): monatliche Zimmerauslastung und Herkunft der Gäste, 186 Gemeinden, seit 2013
- Open-Meteo Historical Weather API (ERA5): Temperatur und Schneefall
- Open-Meteo Geocoding API: Koordinaten und Höhe der Gemeinden
- swisstopo swissBOUNDARIES3D, Version 2026-01: Gemeindegrenzen (Rohdatei nicht im Repo). Download: [swissboundaries3d_2026-01_2056_5728.gpkg.zip](https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip) ([Produktseite](https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d)), entpacken nach `data/raw/geo/`

Verknüpfung über BFS-Gemeindenummer, Jahr und Monat.

## Methoden

PostgreSQL, explorative Datenanalyse, ANOVA, lineare Regression mit Höhenklassen-Vergleich, k-Means, Karten.

## Ausführen

1. Python 3.12 installieren, Repo klonen
2. Virtuelle Umgebung anlegen und aktivieren
   - macOS: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows: `py -3.12 -m venv .venv` und `.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. Datenbank starten: `.env` aus `.env.example` erstellen, dann `docker compose up -d`
5. Notebooks in `notebooks/` der Reihe nach ausführen (01 bis 06)

## Ordner

- `data/` Rohdaten, manuelle Korrekturen, bereinigte Daten
- `notebooks/` Analyse in Jupyter
- `sql/` Schema und Abfragen
- `figures/` Grafiken
- `docs/` KI-Log, Integrationsprotokoll
- `presentation/` Folien
