# Schnee & Betten

Data Analytics, Gruppenprojekt HS 2026, ZHAW

## Forschungsfrage

Wie stark beeinflussen Schneefall und Temperatur die Zimmerauslastung von Schweizer Hotels im Winter, und reagieren tief gelegene Tourismusgemeinden (unter 1000 m ü. M.) stärker als hoch gelegene (über 1500 m ü. M.)?

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
