"""
zusatz_panel.py - ergaenzt panel_winter.csv um die vier fehlenden Zusatzvariablen
(Feedback Dozent):

    eur_chf, ferientage_de, feiertage_ch   (Schritt 1.7, gleich fuer alle Gemeinden)
    sonnenstunden                          (Schritt 1.5, pro Gemeinde)

Aufruf (PowerShell, im Projektordner, mit aktivierter .venv):
    python scripts\\zusatz_panel.py

Das Skript
  * ueberschreibt panel_winter.csv NICHT, sondern schreibt panel_winter_erweitert.csv
  * speichert alle Rohdaten in data/raw/kontext und data/raw/sonne
  * kann jederzeit neu gestartet werden: vorhandene Dateien werden nicht erneut geladen
"""
import io
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

try:
    import holidays
except ImportError:
    sys.exit("Paket 'holidays' fehlt. Bitte ausfuehren:  pip install holidays")

# ---------------------------------------------------------------- Pfade
ROOT = Path(__file__).resolve().parent
while not (ROOT / "data").exists():
    if ROOT.parent == ROOT:
        sys.exit("Ordner 'data' nicht gefunden. Skript innerhalb des Projektordners ablegen.")
    ROOT = ROOT.parent

PROC = ROOT / "data" / "processed"
RAW_KONTEXT = ROOT / "data" / "raw" / "kontext"
RAW_SONNE = ROOT / "data" / "raw" / "sonne"
RAW_WETTER = ROOT / "data" / "raw" / "wetter"      # falls 1.5 schon Rohdaten hat
for p in (PROC, RAW_KONTEXT, RAW_SONNE):
    p.mkdir(parents=True, exist_ok=True)

PANEL_IN = PROC / "panel_winter.csv"
PANEL_OUT = PROC / "panel_winter_erweitert.csv"
NEUE_SPALTEN = ["eur_chf", "ferientage_de", "feiertage_ch", "sonnenstunden"]


# ---------------------------------------------------------------- 1.7 Kontext
def lade_wechselkurs():
    """EUR/CHF Monatsmittel aus dem SNB-Datenportal."""
    datei = RAW_KONTEXT / "snb_devkum.csv"
    if datei.exists():
        text = datei.read_text(encoding="utf-8")
    else:
        r = requests.get("https://data.snb.ch/api/cube/devkum/data/csv/de", timeout=60)
        r.raise_for_status()
        text = r.text
        datei.write_text(text, encoding="utf-8")

    zeilen = text.splitlines()
    # Kopfzeilen vor der Tabelle ueberspringen: Tabelle beginnt bei der Zeile mit "Date"
    start = next((i for i, z in enumerate(zeilen) if z.replace('"', "").startswith("Date")), None)
    if start is None:
        sys.exit("SNB-Datei: Kopfzeile 'Date' nicht gefunden. Datei data/raw/kontext/snb_devkum.csv "
                 "in VS Code oeffnen und aufbau ansehen.")
    snb = pd.read_csv(io.StringIO("\n".join(zeilen[start:])), sep=";")

    fx = snb[(snb["D1"] == "EUR1") & (snb["D0"] == "M0")].copy()
    if fx.empty:
        print("D0 vorhanden:", sorted(snb["D0"].unique())[:10])
        print("D1 vorhanden:", sorted(snb["D1"].unique())[:15])
        sys.exit("Keine Zeilen fuer EUR1 / M0. Codes in der SNB-Datei pruefen und im Skript anpassen.")
    fx["jahr"] = fx["Date"].astype(str).str[:4].astype(int)
    fx["monat"] = fx["Date"].astype(str).str[5:7].astype(int)
    fx["eur_chf"] = pd.to_numeric(fx["Value"], errors="coerce")
    return fx[["jahr", "monat", "eur_chf"]].drop_duplicates(["jahr", "monat"])


def lade_ferien_de():
    """Deutsche Schulferientage pro Monat, gewichtet nach Anzahl Bundeslaender (OpenHolidays API)."""
    tage = []
    for jahr in range(2013, 2027):
        datei = RAW_KONTEXT / f"ferien_de_{jahr}.json"
        if datei.exists():
            daten = json.loads(datei.read_text(encoding="utf-8"))
        else:
            r = requests.get(
                "https://openholidaysapi.org/SchoolHolidays",
                params={"countryIsoCode": "DE", "languageIsoCode": "DE",
                        "validFrom": f"{jahr}-01-01", "validTo": f"{jahr}-12-31"},
                timeout=60,
            )
            r.raise_for_status()
            daten = r.json()
            datei.write_text(json.dumps(daten), encoding="utf-8")
            time.sleep(1)
        for f in daten:
            gewicht = max(len(f.get("subdivisions", [])), 1) / 16
            for d in pd.date_range(f["startDate"], f["endDate"]):
                if d.year == jahr:                      # Ferien ueber den Jahreswechsel nur einmal zaehlen
                    tage.append({"jahr": d.year, "monat": d.month, "gewicht": gewicht})
    return (pd.DataFrame(tage).groupby(["jahr", "monat"])["gewicht"].sum()
            .round().astype(int).rename("ferientage_de").reset_index())


def feiertage_ch():
    """Gesetzliche Feiertage Schweiz (national) pro Monat, Paket 'holidays'."""
    ch = holidays.Switzerland(years=range(2013, 2027))
    s = pd.Series(1, index=pd.to_datetime(list(ch.keys())))
    return (s.groupby([s.index.year, s.index.month]).sum()
            .rename("feiertage_ch").rename_axis(["jahr", "monat"]).reset_index())


def baue_kontext():
    print("1/3 Kontext: Wechselkurs, Ferien, Feiertage ...")
    monate = pd.DataFrame([(j, m) for j in range(2013, 2027) for m in range(1, 13)],
                          columns=["jahr", "monat"])
    kontext = (monate.merge(lade_wechselkurs(), how="left", on=["jahr", "monat"])
               .merge(lade_ferien_de(), how="left", on=["jahr", "monat"])
               .merge(feiertage_ch(), how="left", on=["jahr", "monat"])
               .fillna({"ferientage_de": 0, "feiertage_ch": 0}))
    kontext.to_csv(PROC / "kontext_monat.csv", index=False)
    print("   kontext_monat.csv gespeichert (%d Zeilen)" % len(kontext))
    return kontext


# ---------------------------------------------------------------- 1.5 Sonnenstunden
def tageswerte_sonne(row, start="2013-11-01", end="2026-04-30"):
    """Tageswerte der Sonnenscheindauer (Sekunden). Erst vorhandene Rohdaten aus 1.5 nutzen, sonst API.
    Gibt (Tageswerte, von_api) zurueck."""
    alt = RAW_WETTER / f"{row.bfs_nr}.json"
    if alt.exists():
        d = json.loads(alt.read_text(encoding="utf-8")).get("daily", {})
        if "sunshine_duration" in d:
            return d, False

    ziel = RAW_SONNE / f"{row.bfs_nr}.json"
    if ziel.exists():
        return json.loads(ziel.read_text(encoding="utf-8"))["daily"], False

    params = {"latitude": row.lat, "longitude": row.lon, "elevation": row.hoehe_m,
              "start_date": start, "end_date": end, "daily": "sunshine_duration",
              "models": "era5", "timezone": "Europe/Zurich"}     # gleiche Einstellungen wie 1.5
    for versuch in range(4):
        r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params, timeout=90)
        if r.status_code == 429:
            grund = ""
            try:
                grund = r.json().get("reason", "")
            except Exception:
                pass
            if "aily" in grund:                                  # Tageslimit
                raise RuntimeError("Tageslimit erreicht. Skript morgen erneut starten, "
                                   "bereits geladene Gemeinden werden uebersprungen.")
            print("   Minutenlimit, warte 65 s ...")
            time.sleep(65)
            continue
        r.raise_for_status()
        daten = r.json()
        ziel.write_text(json.dumps(daten), encoding="utf-8")
        return daten["daily"], True
    raise RuntimeError("Open-Meteo antwortet dauerhaft mit 429. Spaeter erneut starten.")


def baue_sonne(panel):
    print("2/3 Sonnenstunden pro Gemeinde ...")
    gem = panel[["bfs_nr", "lat", "lon", "hoehe_m"]].drop_duplicates("bfs_nr")
    teile, fehlend = [], []
    for i, row in enumerate(gem.itertuples(index=False), 1):
        try:
            tage, von_api = tageswerte_sonne(row)
            d = pd.DataFrame(tage)
        except RuntimeError as e:
            print("   STOPP:", e)
            fehlend = list(gem["bfs_nr"].iloc[i - 1:])
            break
        d["bfs_nr"] = int(row.bfs_nr)
        teile.append(d[["time", "sunshine_duration", "bfs_nr"]])
        if i % 10 == 0 or i == len(gem):
            print("   %d/%d Gemeinden" % (i, len(gem)))
        if von_api:
            time.sleep(3)                                        # hoeflich bleiben, Limit vermeiden
    if not teile:
        sys.exit("Keine Sonnendaten geladen.")

    w = pd.concat(teile)
    w["time"] = pd.to_datetime(w["time"])
    w["jahr"], w["monat"] = w["time"].dt.year, w["time"].dt.month
    sonne = (w.groupby(["bfs_nr", "jahr", "monat"])["sunshine_duration"]
             .sum().div(3600).rename("sonnenstunden").reset_index())   # Sekunden -> Stunden
    sonne.to_csv(PROC / "sonne_monat.csv", index=False)
    if fehlend:
        print("   Achtung: %d Gemeinden noch ohne Sonnendaten (Limit). Skript spaeter erneut starten."
              % len(fehlend))
    return sonne


# ---------------------------------------------------------------- Zusammenfuehren
def main():
    if not PANEL_IN.exists():
        sys.exit("panel_winter.csv nicht gefunden: %s" % PANEL_IN)
    panel = pd.read_csv(PANEL_IN)
    n0 = len(panel)
    panel = panel.drop(columns=[c for c in NEUE_SPALTEN if c in panel.columns])

    kontext = baue_kontext()
    sonne = baue_sonne(panel)

    print("3/3 Zusammenfuehren ...")
    panel = panel.merge(kontext, on=["jahr", "monat"], how="left", validate="m:1")
    panel = panel.merge(sonne, on=["bfs_nr", "jahr", "monat"], how="left", validate="m:1")
    assert len(panel) == n0, "Zeilenzahl hat sich beim Merge veraendert!"
    panel.to_csv(PANEL_OUT, index=False)

    print("\nFertig: %s (%d Zeilen, %d Spalten)" % (PANEL_OUT.name, len(panel), panel.shape[1]))
    print("Fehlende Werte in den neuen Spalten:")
    print(panel[NEUE_SPALTEN].isna().sum().to_string())


if __name__ == "__main__":
    main()