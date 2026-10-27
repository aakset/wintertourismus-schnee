# KI-Log (docs/ki_log.md)

| Datum | Wer | Tool | Aufgabe | Prompt (Kurzfassung) | Ergebnis | Funktioniert? | Was war falsch / wie korrigiert |
|---|---|---|---|---|---|---|---|
| 22.10. | A | Claude | PxWeb-Abfrage | "Schreibe POST-Query für Tabelle 201 …" | Code lief | teilweise | Gemeinde-Filter "all" lieferte Fehler, auf Werteliste umgestellt |
| 27.10. | O | Claude Code | Setup Python-Umgebung | "ModuleNotFoundError: No module named 'pandas', pls fix" | requirements.txt in .venv installiert, Import von pandas/geopandas getestet | ja | Ursache war ein abgebrochener pip-Download, nicht die KI. Leeres Zusatz-Environment .venv-1 entdeckt |
| 27.10. | O | Claude Code | KI-Log und CLAUDE.md anlegen | "Erstelle CLAUDE.md, damit Claude das KI-Log automatisch nachführt" | docs/ki_log.md und CLAUDE.md erstellt | ja | – |
