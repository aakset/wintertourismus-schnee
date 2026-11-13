#!/bin/sh
# Lädt PostgreSQL neu, wenn ein Pull Daten (data/processed/) oder das Schema geändert hat.
# Wird von post-merge (git pull) und post-rewrite (git pull --rebase) aufgerufen.
# Bricht den Pull nie ab: bei Problemen nur eine Warnung.

ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT" || exit 0

git rev-parse -q --verify ORIG_HEAD >/dev/null || exit 0
GEAENDERT=$(git diff --name-only ORIG_HEAD HEAD -- data/processed sql/schema.sql sql/db_laden.py)
[ -z "$GEAENDERT" ] && exit 0

echo ""
echo "[db] Daten oder Schema haben sich geändert:"
echo "$GEAENDERT" | sed 's/^/[db]   /'

if [ -x .venv/bin/python ]; then PY=.venv/bin/python
elif [ -x .venv/Scripts/python.exe ]; then PY=.venv/Scripts/python.exe
else
    echo "[db] Keine .venv gefunden, PostgreSQL NICHT aktualisiert. Manuell: python sql/db_laden.py"
    exit 0
fi

if "$PY" sql/db_laden.py; then
    echo "[db] Fertig."
else
    echo "[db] WARNUNG: PostgreSQL NICHT aktualisiert (siehe Meldung oben). Später manuell: $PY sql/db_laden.py"
fi
exit 0
