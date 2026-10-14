"""VERBUM — Codex H, images « avant / après » à partir d'une photographie de feuillet (exécuté une fois, hors build).

Source : verbum-sources/img/codexh-feuillet-base.jpg (photographie générée d'un feuillet de parchemin vierge, JPG).
Produit, en 1920 × 1080 (+ variantes 960 × 540) :
  assets/img/salles/05/codexh-avant.jpg   feuillet à l'œil nu : l'empreinte en miroir est à peine perceptible
  assets/img/salles/05/codexh-apres.jpg   le même feuillet, pixel pour pixel, en « fausses couleurs » multispectrales :
                                          les lignes d'onciales inversées deviennent lisibles
Les deux images sont calculées à partir de la même photographie : elles se superposent exactement dans le curseur.
Le texte (1 Co 13:7-10, en lignes de sens) est celui de la vitrine « Texte révélé » ; c'est une démonstration du principe.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

from textures import encre

# 1 Corinthiens 13:7-10 en onciales, sigma lunaire, sans espaces ni accents, en « lignes de sens »
# (le Codex H est justement célèbre pour sa mise en page en lignes de sens). Passage choisi sans la lettre khi,
# dont la forme en X est exclue des visuels du musée.
STIQUES = ["ΠΑΝΤΑϹΤΕΓΕΙ", "ΠΑΝΤΑΠΙϹΤΕΥΕΙ", "ΠΑΝΤΑΕΛΠΙΖΕΙ", "ΠΑΝΤΑΥΠΟΜΕΝΕΙ",
           "ΗΑΓΑΠΗΟΥΔΕΠΟΤΕΠΙΠΤΕΙ",
           "ΕΙΤΕΔΕΠΡΟΦΗΤΕΙΑΙ", "ΚΑΤΑΡΓΗΘΗϹΟΝΤΑΙ", "ΕΙΤΕΓΛΩϹϹΑΙ", "ΠΑΥϹΟΝΤΑΙ", "ΕΙΤΕΓΝΩϹΙϹ", "ΚΑΤΑΡΓΗΘΗϹΕΤΑΙ",
           "ΕΚΜΕΡΟΥϹΓΑΡΓΙΝΩϹΚΟΜΕΝ", "ΚΑΙΕΚΜΕΡΟΥϹΠΡΟΦΗΤΕΥΟΜΕΝ",
           "ΟΤΑΝΔΕΕΛΘΗΤΟΤΕΛΕΙΟΝ", "ΤΟΕΚΜΕΡΟΥϹΚΑΤΑΡΓΗΘΗϹΕΤΑΙ"]
DEBUTS = (0, 4, 5, 11, 13)      # débuts de phrase, sans retrait

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/user/verbum-sources")
BASE = SRC / "img" / "codexh-feuillet-base.jpg"
F_GRC = str(SRC / "fonts" / "NotoSerif.ttf")
OUT = ROOT / "assets/img/salles/05"
W, H = 1920, 1080


def charger():
    im = Image.open(BASE).convert("RGB").resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(1.4, 45, 2))


def masque_feuillet(im):
    """Le feuillet est clair, la table sombre : seuil sur la luminance, adouci."""
    g = im.convert("L").filter(ImageFilter.GaussianBlur(3))
    m = g.point(lambda v: 255 if v > 95 else 0).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(2.5))
    return m


def masque_texte():
    font = ImageFont.truetype(F_GRC, 54)
    try: font.set_variation_by_name("Regular")
    except Exception: pass
    BW, BH = 1200, 15 * 60 + 40
    def draw(d):
        y = 10
        for i, s in enumerate(STIQUES):
            indent = 0 if i in DEBUTS else 48                    # retraits des lignes de sens
            d.text((10 + indent, y), s, font=font, fill=255)
            y += 60
    _, bloc = encre((BW, BH), draw, flou=0.8, seed=9)
    bloc = bloc.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.7))   # traits plus pleins, façon onciale
    bloc = ImageOps.mirror(bloc)                                   # l'empreinte (« offset ») est inversée
    bb = bloc.getbbox()
    bloc = bloc.crop(bb)
    m = Image.new("L", (W, H), 0)
    # centré dans la surface d'écriture (à droite de la pliure de reliure)
    cx, cy = 1050, 545
    m.paste(bloc, (cx - bloc.width // 2, cy - bloc.height // 2))
    return m


def bruit(px, seed):
    np.random.seed(seed)
    n = Image.fromarray((np.random.rand(H // px + 2, W // px + 2) * 255).astype("uint8")).resize((W, H), Image.BICUBIC)
    return n.filter(ImageFilter.GaussianBlur(px / 2))


def main():
    im = charger()
    leaf = masque_feuillet(im)
    txt = ImageChops.multiply(masque_texte(), leaf)

    # AVANT : une ombre brune, diffuse et lacunaire, à peine perceptible
    blot = bruit(40, 3).point(lambda v: int(40 + v * .75))
    faint = ImageChops.multiply(txt.filter(ImageFilter.GaussianBlur(1.8)), blot).point(lambda v: int(v * .34))
    ombre = ImageChops.multiply(im, Image.new("RGB", (W, H), (168, 140, 112)))
    avant = Image.composite(ombre, im, faint)
    avant.save(OUT / "codexh-avant.jpg", quality=90, optimize=True, progressive=True)

    # APRÈS : rendu « fausses couleurs » (type analyse en composantes principales), même cadrage
    g = im.convert("L").filter(ImageFilter.GaussianBlur(1.1))
    g = ImageOps.autocontrast(g, cutoff=1.5, mask=leaf)
    fc = ImageOps.colorize(g, black=(34, 20, 70), mid=(124, 98, 176), white=(222, 212, 242))
    fond = ImageOps.colorize(im.convert("L"), black=(6, 4, 14), white=(70, 56, 104))      # la table
    fc = Image.composite(fc, fond, leaf)
    lis = bruit(28, 7).point(lambda v: int(150 + v * .42))                                # encre inégale, plus réaliste
    ink = ImageChops.multiply(txt.filter(ImageFilter.GaussianBlur(.9)), lis).point(lambda v: min(255, int(v * 1.25)))
    apres = Image.composite(Image.new("RGB", (W, H), (16, 9, 40)), fc, ink)
    apres = apres.filter(ImageFilter.UnsharpMask(1.0, 30, 2))
    apres.save(OUT / "codexh-apres.jpg", quality=90, optimize=True, progressive=True)

    for n, img in (("avant", avant), ("apres", apres)):
        img.resize((960, 540), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 40, 2)).save(
            OUT / f"codexh-{n}-960.jpg", quality=82, optimize=True, progressive=True)
    print("Codex H : avant / après 1920×1080 + 960×540")


if __name__ == "__main__":
    main()
