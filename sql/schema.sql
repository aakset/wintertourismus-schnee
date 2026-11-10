-- Schema Schnee & Betten. Läuft unverändert in SQLite und PostgreSQL.
DROP VIEW IF EXISTS v_panel_winter;
DROP TABLE IF EXISTS wetter;
DROP TABLE IF EXISTS herkunft;
DROP TABLE IF EXISTS hotellerie;
DROP TABLE IF EXISTS zeit;
DROP TABLE IF EXISTS gemeinde;

CREATE TABLE gemeinde (
    bfs_nr            INTEGER PRIMARY KEY,
    name              TEXT NOT NULL,
    kanton            TEXT,
    lat               DOUBLE PRECISION,
    lon               DOUBLE PRECISION,
    hoehe_m           DOUBLE PRECISION,
    hoehenklasse      TEXT,
    hoehenklasse_1000 TEXT,
    winteranteil      DOUBLE PRECISION,
    ausgewaehlt       BOOLEAN NOT NULL,
    ort_gefunden      TEXT,
    korrigiert        BOOLEAN NOT NULL
);

CREATE TABLE zeit (
    jahr            INTEGER NOT NULL,
    monat           INTEGER NOT NULL CHECK (monat BETWEEN 1 AND 12),
    winter          INTEGER NOT NULL,
    winter_label    TEXT NOT NULL,
    covid           INTEGER NOT NULL,
    ostern_im_monat INTEGER NOT NULL,
    PRIMARY KEY (jahr, monat)
);

CREATE TABLE hotellerie (
    bfs_nr           INTEGER NOT NULL REFERENCES gemeinde (bfs_nr),
    jahr             INTEGER NOT NULL,
    monat            INTEGER NOT NULL CHECK (monat BETWEEN 1 AND 12),
    betten           DOUBLE PRECISION,
    bettenauslastung DOUBLE PRECISION,
    logiernaechte    DOUBLE PRECISION,
    zimmer           DOUBLE PRECISION,
    zimmerauslastung DOUBLE PRECISION,
    zimmernaechte    DOUBLE PRECISION,
    PRIMARY KEY (bfs_nr, jahr, monat)
);

CREATE TABLE herkunft (
    bfs_nr         INTEGER NOT NULL REFERENCES gemeinde (bfs_nr),
    jahr           INTEGER NOT NULL,
    monat          INTEGER NOT NULL CHECK (monat BETWEEN 1 AND 12),
    ln_total       DOUBLE PRECISION,
    ln_schweiz     DOUBLE PRECISION,
    ln_ausland     DOUBLE PRECISION,
    anteil_ausland DOUBLE PRECISION,
    PRIMARY KEY (bfs_nr, jahr, monat)
);

CREATE TABLE wetter (
    bfs_nr          INTEGER NOT NULL REFERENCES gemeinde (bfs_nr),
    jahr            INTEGER NOT NULL,
    monat           INTEGER NOT NULL CHECK (monat BETWEEN 1 AND 12),
    temp_mittel     DOUBLE PRECISION,
    schneefall_cm   DOUBLE PRECISION,
    niederschlag_mm DOUBLE PRECISION,
    schneetage      INTEGER,
    PRIMARY KEY (bfs_nr, jahr, monat)
);

-- Panel: nur gewählte Gemeinden, nur Wintermonate Dez-Mär 2013/14 bis 2025/26 (Filter über zeit)
CREATE VIEW v_panel_winter AS
SELECT h.bfs_nr, g.name, g.kanton, g.lat, g.lon, g.hoehe_m,
       g.hoehenklasse, g.hoehenklasse_1000, g.winteranteil, g.korrigiert,
       h.jahr, h.monat, z.winter, z.winter_label, z.covid, z.ostern_im_monat,
       h.betten, h.bettenauslastung, h.logiernaechte, h.zimmer,
       h.zimmerauslastung, h.zimmernaechte,
       k.ln_total, k.ln_schweiz, k.ln_ausland, k.anteil_ausland,
       w.temp_mittel, w.schneefall_cm, w.niederschlag_mm, w.schneetage
FROM hotellerie h
JOIN gemeinde g ON g.bfs_nr = h.bfs_nr
JOIN zeit z ON z.jahr = h.jahr AND z.monat = h.monat
LEFT JOIN herkunft k ON k.bfs_nr = h.bfs_nr AND k.jahr = h.jahr AND k.monat = h.monat
LEFT JOIN wetter w ON w.bfs_nr = h.bfs_nr AND w.jahr = h.jahr AND w.monat = h.monat
WHERE g.ausgewaehlt;