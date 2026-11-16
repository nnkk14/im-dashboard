# Hinweise für Claude

Code der Web-App „Mein Training“: alles steht in `index.html` (dazu `sw.js`, `manifest.json` und Symbole). Die App läuft über GitHub Pages unter https://nnkk14.github.io/im-dashboard/.

Fahrplan, Arbeitsregeln und Quellen liegen im privaten Repository `nnkk14/mein-training-team`. Liegt es neben diesem Ordner (`../mein-training-team`), lies zuerst dessen `CLAUDE.md`, `fahrplan.md` und `technik-und-arbeitsweise.md`.

## Kurzregeln
- Neue Funktionen kommen als eigener Block `/* ---------- vNN ---------- */` direkt vor `/* ---------- Wettkämpfe ---------- */`, CSS mit `/* vNN */` vor `</style>`. `const VERSION="NN"` wird bei jeder Änderung hochgezählt. Bestehende Funktionen werden umhüllt statt umgeschrieben.
- Vor jedem Push: `python werkzeuge/ci_pruefung.py index.html` (Syntax und alle Bildschirme mit Beispieldaten auf Handy und großem Bildschirm). Dieselbe Prüfung läuft nach jedem Push als GitHub Action „Prüfung“.
- Texte in der App: Deutsch, Du-Form, kurz, ohne Fachkürzel, keine Gedankenstriche als Satzzeichen, keine Semikolons. Die KI heißt in der App „KI“. Kosten sind für Nutzer nie sichtbar.
- Dieses Repository ist öffentlich: keine Schlüssel, keine persönlichen Daten, keine internen Pläne.
