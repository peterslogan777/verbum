"""VERBUM — Salle 12 : préparation des visuels (sources générées -> 1920x1080 + 960x540).

Retouches : flou + assombrissement doux sur les éléments de fond pouvant former
des lignes croisées (presse et casiers de l'image d'ouverture, rayonnages Segond),
recadrage de la fenêtre à meneaux (Moyen Âge).

Les sources générées (verbum-sources/img/s12-*.jpg) ne sont pas conservées dans l'espace de travail
(quota) : les images finales de assets/img/salles/12/ font foi. Script conservé pour mémoire.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

SRC = Path(__file__).resolve().parents[2] / "verbum-sources" / "img"
DST = Path(__file__).resolve().parents[1] / "assets" / "img" / "salles" / "12"


def voile(im, boxes, flou=22, sombre=0.5):
    """Flou + assombrissement dans des ellipses adoucies."""
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    for b in boxes:
        d.ellipse(b, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(40))
    fl = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(flou))).enhance(sombre)
    return Image.composite(fl, im, m)


def exporte(im, nom):
    im = im.convert("RGB").resize((1920, 1080), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 40, 2))
    im.save(DST / f"{nom}.jpg", quality=86, optimize=True, progressive=True)
    im.resize((960, 540), Image.LANCZOS).save(DST / f"{nom}-960.jpg", quality=82, optimize=True, progressive=True)


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for nom in ["hero", "moyen-age", "vaudois", "olivetan", "bastille", "colporteur", "segond", "aujourdhui"]:
        im = Image.open(SRC / f"s12-{nom}.jpg").convert("RGB")
        if nom == "hero":
            im = voile(im, [(-160, -140, 420, 420), (500, -20, 720, 250)])
        elif nom == "moyen-age":
            w = 1615
            im = im.crop((0, 15, w, 15 + round(w * 9 / 16)))
        elif nom == "segond":
            im = voile(im, [(1440, -80, 1760, 560)], flou=18, sombre=0.55)
        exporte(im, nom)
        print("ok", nom)


if __name__ == "__main__":
    main()
