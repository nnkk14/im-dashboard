# Automatische Prüfung bei jedem Hochladen (GitHub Actions) und lokal:
#   python werkzeuge/ci_pruefung.py [Pfad zu index.html]
# 1. Syntax des Skripts in index.html mit Node prüfen
# 2. Alle Bereiche der App mit Beispieldaten auf Handy und großem Bildschirm öffnen
# Beendet sich mit Fehlercode, wenn etwas kaputt ist.
import os, re, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
P = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "index.html")
html = open(P, encoding="utf-8").read()
fehler = []
v = re.search(r'const VERSION="(\d+)"', html)
if not v:
    fehler.append("Keine Versionsnummer (const VERSION) gefunden")
js = max(re.findall(r"<script>([\s\S]*?)</script>", html), key=len)
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
    f.write(js)
r = subprocess.run(["node", "-e", f'new Function(require("fs").readFileSync({f.name!r},"utf8"))'], capture_output=True, text=True)
if r.returncode:
    zeilen = r.stderr.strip().splitlines() or ["?"]
    fehler.append("Syntaxfehler: " + next((z for z in zeilen if "Error" in z), zeilen[0])[:300])
SCHRITTE = [("heute", "setTab('heute')"), ("plan", "setTab('training');setSub('plan')"), ("fortschritt", "setSub('fort')"), ("verlauf", "setSub('verlauf')"),
    ("erholung", "setTab('erholung')"), ("einstellungen", "open('mSet')"), ("hilfe", "close('mSet');open('mHelp')"), ("feedback", "close('mHelp');openFb()"),
    ("verpflegung", "close('mFb');openFuel()"), ("checkin", "close('mFuel');close('mInfo');openChk()"), ("rueckblick", "close('mChk');wrapOpen&&wrapOpen('week')"),
    ("einheit", "close('mWrap');setTab('training');setSub('verlauf');actInfo(DATA.activities[DATA.activities.length-1])"), ("woche", "close('mInfo');weekInfo(addDays(today(),-7))")]
os.makedirs("pruefung", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [("handy", 390, 844), ("gross", 1280, 860)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, timezone_id="Europe/Berlin")
        pg = ctx.new_page()
        pg.on("pageerror", lambda e, n=name: fehler.append(f"{n} JS: {e}"))
        pg.on("console", lambda m, n=name: m.type == "error" and "net::" not in m.text and "ERR_" not in m.text and "Failed to load resource" not in m.text and fehler.append(f"{n} Konsole: {m.text[:300]}"))
        pg.add_init_script("localStorage.setItem('imOnb','true')")
        pg.goto("file://" + P)
        pg.wait_for_timeout(3500)
        for s, code in SCHRITTE:
            try:
                pg.evaluate(code); pg.wait_for_timeout(400); pg.screenshot(path=f"pruefung/{name}_{s}.png")
            except Exception as e:
                fehler.append(f"{name} {s}: {str(e)[:200]}")
        try:
            t = pg.evaluate("(document.getElementById('apperr')||{}).textContent||''")
        except Exception as e:
            t = ""; fehler.append(f"{name}: App nicht geladen ({str(e)[:120]})")
        if t.strip():
            fehler.append(f"{name} Fehleranzeige der App: {t[:200]}")
        ctx.close()
    b.close()
print("Version", v.group(1) if v else "?")
if fehler:
    print("FEHLER:")
    for x in fehler:
        print("  " + x)
    sys.exit(1)
print("Keine Fehler.")
