# Variablen (Features)

Übersicht aller Variablen für die Modelle. Analyseeinheit: Gemeinde × Monat (Wintermonate), 2013–2026, für die 45 Wintersportorte (`ausgewaehlt` in `data/processed/gemeinden.csv`: mindestens 1/3 der Logiernächte von Dezember bis März).

**Ebene:** *Gemeinde × Monat* = unterscheidet sich zwischen Orten und über die Zeit. *Gemeinde* = fest pro Ort. *Monat* = gleich für alle Gemeinden, ändert sich nur über die Zeit. Monatsvariablen erklären also Schwankungen zwischen Monaten und Jahren, nicht Unterschiede zwischen Orten.

## Zielgrösse

| Name | Bedeutung | Einheit | Ebene | Quelle | Datei |
|---|---|---|---|---|---|
| `zimmerauslastung` | Belegte Zimmernächte / verfügbare Zimmernächte | % | Gemeinde × Monat | BFS HESTA, STAT-TAB Tabelle 201 (1.2) | `data/processed/hotellerie_monat.csv` |

Zimmerauslastung statt Logiernächte: Sie hängt nicht von der Grösse des Ortes ab, Logiernächte absolut schon.

## Erklärende Variablen

| Name | Bedeutung | Einheit | Ebene | Quelle | Erwartete Wirkung auf Auslastung | Status |
|---|---|---|---|---|---|---|
| Neuschnee | Schneefall im Monat, als Abweichung vom langjährigen Mittel der Gemeinde | cm | Gemeinde × Monat | Open-Meteo Historical Weather API, ERA5 (1.5) | **+** mehr Schnee als üblich → bessere Pistenverhältnisse → höhere Auslastung (H1), in tiefen Gemeinden stärker (H2) | offen |
| Temperatur | Monatsmittel der Lufttemperatur | °C | Gemeinde × Monat | Open-Meteo, ERA5 (1.5) | **−** wärmer → weniger Schnee, kürzere Saison → tiefere Auslastung, v.a. in tiefen Gemeinden (H3) | offen |
| Sonnenstunden | Sonnenscheindauer im Monat | h | Gemeinde × Monat | Open-Meteo, ERA5 (1.5) | **+** schönes Wetter zieht Tagesgäste und Kurzaufenthalte an | offen |
| `hoehe_m`, `hoehenklasse`, `hoehenklasse_1000` | Höhe des Ortes; Klassen tief < 1200 m, mittel 1200–1500 m, hoch > 1500 m (13 / 19 / 13 Orte). `hoehenklasse_1000`: gleiche Einteilung mit Grenze 1000 m als Robustheitscheck (nur 3 tiefe Orte) | m ü. M. / Kategorie | Gemeinde | Open-Meteo Geocoding API, manuell korrigiert (1.4) | Moderator: Schnee-Effekt in tiefen Gemeinden grösser (H2) | ✓ |
| `zimmer`, `betten` | Hotelkapazität | Anzahl | Gemeinde × Monat | BFS HESTA, Tabelle 201 (1.2) | **−/?** grosse Orte haben mehr Konkurrenz und Stadthotellerie; vor allem Kontrollvariable | ✓ |
| `anteil_ausland` | Anteil Logiernächte ausländischer Gäste | 0–1 | Gemeinde × Monat | BFS HESTA, Tabelle 101 (1.3) | Teilfrage (a): Orte mit vielen ausländischen Gästen reagieren schwächer auf kurzfristigen Schnee (Buchung lange im Voraus), aber stärker auf EUR/CHF | ✓ |
| `eur_chf` | Wechselkurs, CHF pro 1 EUR, Monatsmittel | CHF | Monat | SNB-Datenportal, Cube `devkum`, D0 = M0, D1 = EUR1 (1.7) | **+** höherer Kurs → Schweiz für Gäste aus dem Euroraum günstiger → mehr ausländische Gäste → höhere Auslastung (H4) | ✓ |
| `ferientage_de` | Schulferientage in Deutschland im Monat, gemittelt über die 16 Bundesländer | Tage | Monat | OpenHolidays API, `countryIsoCode=DE` (1.7) | **+** Deutschland ist der grösste Auslandsmarkt; mehr Ferientage → mehr Gäste (H4) | ✓ |
| `ferientage_ch` | Schulferientage in der Schweiz im Monat, gemittelt über die 26 Kantone. **⚠ 2013–2019 Annahme** (siehe unten) | Tage | Monat | OpenHolidays API, `countryIsoCode=CH` (1.7), davor eigene Schätzung | **+** Schweizer Gäste reisen in den Ferien, v.a. Sportferien im Februar; Gegenstück zu `ferientage_de` für Teilfrage (a) | ✓ (Annahme) |
| `ferientage_ch_annahme` | Anteil der Kantons-Tage im Monat, deren Ferienwert geschätzt ist | 0–1 | Monat | eigene Berechnung (1.7) | Keine Modellvariable, sondern Kennzeichnung: 1 = vollständig Annahme, 0 = vollständig echte Daten | ✓ |
| `feiertage_ch` | Gesetzliche Feiertage in der Schweiz im Monat, gemittelt über die 26 Kantone | Tage | Monat | Python-Paket `holidays` (1.7) | **+** Feiertage und verlängerte Wochenenden (Ostern, Auffahrt) → mehr Kurzaufenthalte | ✓ |
| Corona-Markierung | Winter 2019/20 ab März und Winter 2020/21 | 0/1 | Monat | eigene Definition | Ausschluss bzw. Markierung: Auslastung durch Schliessungen und Reisebeschränkungen verzerrt, nicht durch Schnee | offen |

## Hinweise zur Berechnung

- **`eur_chf`:** Die SNB-CSV hat zwei Kopfzeilen und eine Leerzeile vor der Tabelle (`skiprows=2`). Für Oktober–Dezember 2026 gibt es noch keine Werte (leer).
- **`ferientage_de`:** Die API liefert pro Ferienblock ein Bundesland. Gezählt wird jeder Tag pro Bundesland, danach durch 16 geteilt. Wert 10 heisst: Im Schnitt hat ein Bundesland 10 Ferientage in diesem Monat. Ferien über den Jahreswechsel kommen in zwei Jahresabfragen vor und werden nur einmal gezählt. Wochenenden innerhalb der Ferien zählen mit.
- **`feiertage_ch`:** National kennt `holidays` nur Neujahr, Auffahrt, 1. August und Weihnachten. Ostern fehlt, weil Karfreitag und Ostermontag kantonal geregelt sind. Darum zählt der Mittelwert über alle 26 Kantone: Ein Feiertag in 13 von 26 Kantonen zählt als 0.5.
- **`ferientage_ch` – ⚠ ANNAHME für 2013–2019:**
  - **Problem:** OpenHolidays liefert Schweizer Schulferien erst ab Ende 2019. Für 2013–2018 gibt es keine Einträge, für 2019 nur die Weihnachtsferien 2019/20 einzelner Kantone.
  - **Echte Daten:** pro Kanton ab dem Beginn seines ersten Ferieneintrags in der API. Das ist zwischen 21.12.2019 (z.B. GR, BL, BS) und 10.4.2020 (ZH). Ab 2021 sind alle Werte echt.
  - **Annahme davor:** Für jeden Kanton und jede Kalenderwoche wird der durchschnittliche Ferienanteil der vollständigen Jahre 2021–2026 genommen und auf die Jahre davor übertragen. Das Ergebnis ist ein Erwartungswert. Er kann Bruchteile von Tagen enthalten, wenn eine Woche nur in manchen Jahren Ferien war.
  - **Was die Annahme nicht abbildet:** Änderungen der kantonalen Ferienordnungen vor 2020. Frühlingsferien, die sich nach Ostern richten, werden nicht verschoben.
  - **Rückwärtstest:** 2025 wurde nur aus dem Muster von 2021–2024 und 2026 geschätzt und mit den echten Werten verglichen. Im Mittel weicht die Schätzung um **0.9 Tage pro Monat** ab. In den **Wintermonaten** ist sie ungenauer: Februar +2.9, März −1.9, Januar −1.0 Tage, weil sich die Sportferien von Jahr zu Jahr leicht verschieben.
  - **Kennzeichnung:** Die Spalte `ferientage_ch_annahme` gibt pro Monat den geschätzten Anteil an (2013–2018: 1.0, Dezember 2019 bis April 2020 Übergang, ab Mai 2020: 0).
  - **Regionen und Gruppen:** Graubünden und Appenzell Innerrhoden haben regionale Ferien. Jede Region zählt als Einheit, der Kantonswert ist das Mittel der Regionen. Unterschiede nach Schultyp oder Sprachregion innerhalb einer Einheit werden nicht unterschieden: Hat eine Gruppe Ferien, zählt der Tag als Ferientag.
  - **Für Modell und Präsentation:** Ergebnisse mit `ferientage_ch` für 2013–2019 beruhen auf einer Annahme. Das muss in der Präsentation gesagt werden. Robustheitscheck: Modell mit und ohne `ferientage_ch` rechnen bzw. nur für 2020–2026.
- **Rohdaten:** `data/raw/kontext/snb_devkum.csv` , `data/raw/kontext/ferien_de_JJJJ.json` und `data/raw/kontext/ferien_ch_JJJJ.json`. Jede API wird nur einmal pro Jahr abgefragt, bereits gespeicherte Dateien werden nicht neu geladen (Notebook 01, Abschnitt 6).
- **Join in 3.2:** `kontext_monat.csv` wird über `jahr` und `monat` an die Gemeinde-Monats-Tabelle gehängt. Zeilenzahl vorher und nachher protokollieren. Sie muss gleich bleiben.
