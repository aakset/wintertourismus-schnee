# Setup: Python-Umgebung einrichten

Ziel: Ihr könnt das Projekt in VS Code ausführen und habt dieselben Pakete wie Aakash. Dauer: ca. 30 bis 45 Minuten.

Wir verwenden alle **Python 3.13**.

Repo: https://github.com/aakset/wintertourismus-schnee

**Zuerst für beide:** Nehmt die Einladung zum Repo an (Mail von GitHub oder unter github.com/aakset/wintertourismus-schnee). Ohne das könnt ihr nicht pushen.

---

## Oliver (macOS)

### 1. Programme installieren

- **Python 3.13** von python.org (Downloads, “macOS 64-bit universal2 installer”). Nicht 3.12 oder 3.14 nehmen.
- Danach im Finder: Programme → “Python 3.13” → **Install Certificates.command** einmal doppelklicken. Sonst scheitern später die API-Abfragen.
- **VS Code** mit den Erweiterungen **Python** und **Jupyter** (beide von Microsoft).
- **Git**: Terminal öffnen, `xcode-select --install` eingeben und bestätigen.
- **Docker Desktop** (Version für Apple Silicon oder Intel, je nach Chip). Brauchen wir erst im nächsten Schritt, installieren kannst du es schon jetzt.

### 2. Git einrichten (einmalig)

```
git config --global user.name "Vorname Nachname"
git config --global user.email "deine@mail.ch"
git config --global core.autocrlf input
git config --global pull.rebase false
```

Nimm die Mail, die du bei GitHub hinterlegt hast.

### 3. Repo klonen

Nicht in einen iCloud-Ordner. Am sichersten ist `~/Developer`.

```
mkdir -p ~/Developer
cd ~/Developer
git clone https://github.com/aakset/wintertourismus-schnee.git
cd wintertourismus-schnee
code .
```

Falls `code .` nicht geht: VS Code öffnen → File → Open Folder → `wintertourismus-schnee`.

### 4. Umgebung anlegen

In VS Code: Terminal → New Terminal. Falls vorne `(base)` steht (Anaconda), zuerst `conda deactivate` eingeben.

```
python3.13 -m venv .venv
source .venv/bin/activate
python --version
```

Es muss `Python 3.13.x` erscheinen, und vorne im Prompt steht `(.venv)`.
Falls `python3.13` nicht gefunden wird, nimm den vollen Pfad:
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m venv .venv`

### 5. Pakete installieren

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Das dauert ein paar Minuten.

### 6. Testen

1. Cmd+Shift+P → “Create: New Jupyter Notebook”
2. Oben rechts “Select Kernel” → `.venv` wählen
3. In die erste Zelle schreiben und mit Shift+Enter ausführen:

```python
import pandas, geopandas
print("ok")
```

Steht dort `ok`, bist du fertig. Das Test-Notebook musst du nicht speichern.

---

## Jelmer (Windows)

### 1. Programme installieren

- **Python 3.13** von python.org (Downloads, “Windows installer 64-bit”). Im Installer unbedingt **“Add python.exe to PATH”** anhaken. Nicht die Version aus dem Microsoft Store nehmen.
- **VS Code** mit den Erweiterungen **Python** und **Jupyter** (beide von Microsoft).
- **Git for Windows** von git-scm.com. Die Standardeinstellungen im Installer übernehmen.
- **Docker Desktop**. Es installiert WSL 2 mit, danach ist ein Neustart nötig. Brauchen wir erst im nächsten Schritt, installieren kannst du es schon jetzt.

### 2. Git einrichten (einmalig)

Im VS-Code-Terminal (PowerShell):

```
git config --global user.name "Vorname Nachname"
git config --global user.email "deine@mail.ch"
git config --global core.autocrlf true
git config --global core.longpaths true
git config --global pull.rebase false
```

Nimm die Mail, die du bei GitHub hinterlegt hast.

### 3. Repo klonen

Nicht in OneDrive und nicht in einen langen Pfad. Am sichersten ist `C:\dev`.

```
mkdir C:\dev
cd C:\dev
git clone https://github.com/aakset/wintertourismus-schnee.git
cd wintertourismus-schnee
code .
```

Beim ersten Klonen oder Pushen öffnet sich ein Browserfenster: dort mit GitHub einloggen.
Falls `code .` nicht geht: VS Code öffnen → File → Open Folder → `C:\dev\wintertourismus-schnee`.

### 4. Umgebung anlegen

In VS Code: Terminal → New Terminal (PowerShell).

Einmalig, sonst blockiert PowerShell das Aktivieren:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Dann:

```
py -3.13 --version
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python --version
```

Es muss `Python 3.13.x` erscheinen, und vorne im Prompt steht `(.venv)`.

### 5. Pakete installieren

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Das dauert ein paar Minuten. Falls `geopandas` einen Fehler wirft, kopiere die Fehlermeldung in den Gruppenchat. Das ist unter Windows der häufigste Stolperstein.

### 6. Testen

1. Ctrl+Shift+P → “Create: New Jupyter Notebook”
2. Oben rechts “Select Kernel” → `.venv` wählen
3. In die erste Zelle schreiben und mit Shift+Enter ausführen:

```python
import pandas, geopandas
print("ok")
```

Steht dort `ok`, bist du fertig. Das Test-Notebook musst du nicht speichern.

---

## Arbeitsregeln mit Git

- Vor dem Arbeiten: `git pull`
- Nach dem Arbeiten: `git add .`, `git commit -m "Was ich gemacht habe"`, `git push`
- Pro Notebook ist eine Person verantwortlich. Zwei Personen im selben Notebook geben Konflikte.
- Nie die Datei `.env` oder Passwörter committen.

## Wenn etwas nicht klappt

Fehlermeldung kopieren und in den Gruppenchat stellen. Wenn du dafür KI genutzt hast, trage es im KI-Log ein (`docs/ki_log.md`).
