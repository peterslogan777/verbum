"""VERBUM — icônes du site, en JPG uniquement (exécuté une fois, hors build).

Source : verbum-sources/img/icone-verbum.jpg (emblème photoréaliste 1254 × 1254 : V doré entre deux rouleaux).
Produit :
  favicon-32.jpg              onglet du navigateur : cadrage serré sur le V et les rouleaux, lisible à 32 px
  apple-touch-icon.jpg        écran d'accueil iPhone/iPad (180 × 180, plein cadre, iOS arrondit lui-même les coins)
  assets/img/icon-512.jpg     grand format (manifeste, données structurées), emblème complet avec marge de sécurité
"""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/user/verbum-sources/img/icone-verbum.jpg")
def fond_de(im):
    """Couleur moyenne des quatre coins : le fond bleu nuit de l'emblème."""
    w, h = im.size
    px = [im.getpixel((x, y)) for x in (4, w - 5) for y in (4, h - 5)]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))


def sur_fond(im, taille, echelle):
    """Place l'image réduite au centre d'un carré du même bleu nuit, avec un bord fondu (aucune couture visible)."""
    c = Image.new("RGB", (taille, taille), fond_de(im))
    s = round(taille * echelle)
    r = im.resize((s, s), Image.LANCZOS)
    m = Image.new("L", (s, s), 0)
    b = max(8, s // 14)
    m.paste(255, (b, b, s - b, s - b))
    c.paste(r, ((taille - s) // 2, (taille - s) // 2), m.filter(ImageFilter.GaussianBlur(b / 2)))
    return c


def reduire(im, taille, nettete=(1.0, 60, 1)):
    """Réduction progressive (moins d'aliasing), puis accentuation adaptée à la taille."""
    while im.width > taille * 2:
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im = im.resize((taille, taille), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(*nettete))


def enregistrer(im, chemin):
    # qualité maximale, sans sous-échantillonnage des couleurs (indispensable pour les petites icônes)
    im.save(chemin, "JPEG", quality=95, subsampling=0, optimize=True)
    print(f"{chemin.relative_to(ROOT)} : {im.size[0]}×{im.size[1]}, {chemin.stat().st_size / 1024:.1f} Ko")


def main():
    src = Image.open(SRC).convert("RGB")
    W = src.width

    # Grand format 512 : emblème entier (anneau + losange), 8 % de marge de chaque côté
    grand = sur_fond(src, 1254, 0.90)
    enregistrer(reduire(grand, 512, (1.2, 50, 2)), ROOT / "assets/img/icon-512.jpg")

    # Écran d'accueil Apple 180 : emblème légèrement agrandi, iOS rogne les coins arrondis
    apple = sur_fond(src.crop((int(W * .05), int(W * .03), int(W * .95), int(W * .93))), 1254, 0.94)
    apple = ImageEnhance.Contrast(apple).enhance(1.06)
    enregistrer(reduire(apple, 180, (1.0, 70, 1)), ROOT / "apple-touch-icon.jpg")

    # Onglet 32 : seul le cœur reste lisible ; cadrage serré sur le V et les deux rouleaux
    coeur = src.crop((int(W * .24), int(W * .265), int(W * .76), int(W * .785)))
    coeur = ImageEnhance.Contrast(coeur).enhance(1.18)
    coeur = ImageEnhance.Brightness(coeur).enhance(1.08)
    enregistrer(reduire(coeur, 32, (0.6, 90, 0)), ROOT / "favicon-32.jpg")


if __name__ == "__main__":
    main()
