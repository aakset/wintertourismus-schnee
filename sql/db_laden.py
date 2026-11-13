"""PostgreSQL (Docker) mit dem aktuellen Stand aus data/processed/ neu laden.

Gleiche Logik wie notebooks/03_datenbank.ipynb (Schema neu anlegen, fünf Tabellen laden),
aber ohne Notebook. Wird nach jedem `git pull` automatisch vom Hook in .githooks/ aufgerufen,
wenn sich Daten oder Schema geändert haben. Manuell: python sql/db_laden.py
"""
import pathlib
import subprocess
import sys
import time
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "data" / "processed"


def engine_aus_env():
    if not (ROOT / ".env").exists():
        sys.exit("Keine .env gefunden. Zuerst .env aus .env.example erstellen.")
    load_dotenv(ROOT / ".env")
    return create_engine(
        f"postgresql+psycopg://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
        f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}"
    )


def erreichbar(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def db_starten(engine, warten=60):
    """Startet den Container mit docker compose, falls die DB nicht antwortet."""
    if erreichbar(engine):
        return
    print("PostgreSQL antwortet nicht, starte Container mit `docker compose up -d` ...")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], cwd=ROOT, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        sys.exit(f"Docker konnte nicht gestartet werden ({e}). Läuft Docker Desktop?")
    for _ in range(warten):
        if erreichbar(engine):
            return
        time.sleep(1)
    sys.exit(f"PostgreSQL nach {warten} s noch nicht erreichbar.")


def main():
    engine = engine_aus_env()
    db_starten(engine)

    gem = pd.read_csv(P / "gemeinden.csv")
    hot = pd.read_csv(P / "hotellerie_monat.csv")
    her = pd.read_csv(P / "herkunft_monat.csv")
    wet = pd.read_csv(P / "wetter_monat.csv")
    panel = pd.read_csv(P / "panel_winter.csv")
    zeit = panel[["jahr", "monat", "winter", "winter_label", "covid", "ostern_im_monat"]].drop_duplicates()
    tabellen = {"gemeinde": gem, "zeit": zeit, "hotellerie": hot, "herkunft": her, "wetter": wet}

    schema = (ROOT / "sql" / "schema.sql").read_text(encoding="utf-8")
    with engine.begin() as conn:                      # eine Transaktion: bei Fehler bleibt der alte Stand
        for stmt in schema.split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        for name, d in tabellen.items():              # Reihenfolge wegen Fremdschlüsseln
            d.to_sql(name, conn, if_exists="append", index=False, chunksize=5000)

    with engine.connect() as conn:
        n = conn.execute(text("SELECT COUNT(*) FROM v_panel_winter")).scalar()
    print(f"PostgreSQL aktualisiert: v_panel_winter mit {n} Zeilen (erwartet {len(panel)}).")
    if n != len(panel):
        sys.exit("Zeilenzahl stimmt nicht mit panel_winter.csv überein.")


if __name__ == "__main__":
    main()
