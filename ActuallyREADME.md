# Setup (einmalig, ca. 30 Minuten)

Ziel: Python 3.13, VS Code und das Projekt laufen auf deinem Rechner.
Repo: https://github.com/aakset/wintertourismus-schnee

## 1. Installieren

- **Python 3.13** von python.org (nicht 3.14 oder neuer, wir nutzen alle dieselbe Version)
  - Windows: im Installer **"Add python.exe to PATH"** anhaken, nicht die Microsoft-Store-Version nehmen
  - Mac: danach im Finder unter Programme/Python 3.13 einmal **Install Certificates.command** doppelklicken
- **VS Code** mit den Erweiterungen **Python** und **Jupyter** (beide von Microsoft)
- **Git**
  - Mac: im Terminal `xcode-select --install`
  - Windows: Git for Windows von git-scm.com
- **Docker Desktop** (starten musst du es erst später, installiert sein reicht)

Die GitHub-Einladung per Mail annehmen.

## 2. Git einrichten

Im Terminal (Windows: PowerShell), einmalig:

```
git config --global user.name "Vorname Nachname"
git config --global user.email "deine@mail.ch"
git config --global pull.rebase false
```

Zusätzlich:
- Mac: `git config --global core.autocrlf input`
- Windows: `git config --global core.autocrlf true` und `git config --global core.longpaths true`

## 3. Projekt klonen

Nicht in iCloud (Mac) oder OneDrive (Windows) speichern, das zerstört die virtuelle Umgebung.

```
cd ~/Documents                  # Windows: cd $HOME\Documents
git clone https://github.com/aakset/wintertourismus-schnee.git
cd wintertourismus-schnee
```

Beim ersten Mal fragt GitHub nach der Anmeldung (Browser-Fenster oder Konto in VS Code verbinden).
Dann in VS Code: File, Open Folder, Projektordner wählen.

## 4. Umgebung anlegen

Im VS Code Terminal (Terminal, New Terminal).

**Mac** (steht vorne `(base)`, zuerst `conda deactivate`):
```
python3.13 -m venv .venv
source .venv/bin/activate
```
Falls `python3.13` nicht gefunden wird:
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m venv .venv`

**Windows**:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

Vorne muss jetzt `(.venv)` stehen. Prüfen mit `python --version`, es muss 3.13.x zeigen.

## 5. Pakete installieren

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Das dauert einige Minuten.

## 6. Testen

In VS Code ein neues Notebook öffnen (Cmd/Strg+Shift+P, "Create: New Jupyter Notebook").
Oben rechts **Select Kernel**, dann `.venv` wählen. In eine Zelle:

```python
import pandas, geopandas
print("ok")
```

Kommt `ok`, bist du fertig. Schreib kurz in den Gruppenchat.

## Arbeitsregel mit Git

Vor dem Arbeiten `git pull`, danach:

```
git add .
git commit -m "Was ich gemacht habe"
git push
```

Ein Notebook gehört immer einer Person, sonst gibt es Merge-Konflikte.

## Wenn etwas nicht klappt

Fehlermeldung kopieren, in den Gruppenchat schicken und ins KI-Log (`docs/ki_log.md`) eintragen.
