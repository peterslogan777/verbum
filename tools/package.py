#!/usr/bin/env python3
"""VERBUM — fabrique l'archive ZIP complète du musée.

    python3 tools/package.py                  # → ../dist/verbum-musee-virtuel-de-la-bible.zip
    python3 tools/package.py --site-seul      # sans tools/ ni docs/ (prêt à déposer chez un hébergeur)
"""
import os, sys, zipfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(os.path.dirname(ROOT), "dist")
NOM = "verbum-musee-virtuel-de-la-bible"
EXCLUS_DOSSIERS = {"__pycache__", ".git", "dist", "node_modules", ".venv"}
EXCLUS_FICHIERS = {".DS_Store", "Thumbs.db"}
SITE_SEUL = "--site-seul" in sys.argv
if SITE_SEUL:
    EXCLUS_DOSSIERS |= {"tools", "docs", ".github"}


def main():
    os.makedirs(DIST, exist_ok=True)
    cible = os.path.join(DIST, NOM + ("-site" if SITE_SEUL else "") + ".zip")
    n, total = 0, 0
    t0 = time.time()
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for dossier, sous, fichiers in os.walk(ROOT):
            sous[:] = sorted(d for d in sous if d not in EXCLUS_DOSSIERS)
            for f in sorted(fichiers):
                if f in EXCLUS_FICHIERS or f.endswith(".pyc"):
                    continue
                chemin = os.path.join(dossier, f)
                rel = os.path.relpath(chemin, ROOT)
                # JPG et MP3 sont déjà compressés : on les range sans recompresser
                mode = zipfile.ZIP_STORED if f.lower().endswith((".jpg", ".jpeg", ".mp3", ".woff2")) else zipfile.ZIP_DEFLATED
                z.write(chemin, os.path.join("verbum", rel), compress_type=mode)
                n += 1
                total += os.path.getsize(chemin)
    print(f"Archive : {cible}")
    print(f"{n} fichiers, {total / 1e6:.1f} Mo de contenu, archive de {os.path.getsize(cible) / 1e6:.1f} Mo ({time.time() - t0:.1f} s)")


if __name__ == "__main__":
    main()
