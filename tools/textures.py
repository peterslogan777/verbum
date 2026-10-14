"""VERBUM — génération des textures « texte réel sur parchemin » (exécuté une fois, hors build).

Produit :
  assets/img/salles/03/rouleau-esaie53.jpg      bande 4096×1024 : Ésaïe 53 (texte consonantique) en colonnes, texture du visualiseur 3D
  assets/img/salles/03/fragment-esaie53.jpg     1920×1080 : fragment (colonne des v. 9-12) sur fond noir, pour la loupe
  (les images « avant / après » du Codex H sont désormais produites par tools/codexh_photo.py
   à partir d'une photographie de feuillet ; la fonction codex_h() ci-dessous n'est plus appelée)
  tools/data/rouleau_colonnes.json              répartition des versets par colonne (utilisée par salle_qumran.py)

Le texte hébreu provient du texte massorétique (Sefaria, « Miqra according to the Masorah »),
dont on retire voyelles et accents pour imiter l'aspect d'un rouleau de Qumrân.
"""
import json
import random
import re
import unicodedata
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/home/user/verbum-sources")
PARCH = SRC / "img" / "parchemin-vierge.jpg"
F_HEB = str(SRC / "fonts" / "FrankRuhlLibre.ttf")
F_GRC = str(SRC / "fonts" / "NotoSerif.ttf")
random.seed(53)

ESAIE_53 = """מִ֥י הֶאֱמִ֖ין לִשְׁמֻעָתֵ֑נוּ וּזְר֥וֹעַ יְהֹוָ֖ה עַל־מִ֥י נִגְלָֽתָה׃
וַיַּ֨עַל כַּיּוֹנֵ֜ק לְפָנָ֗יו וְכַשֹּׁ֙רֶשׁ֙ מֵאֶ֣רֶץ צִיָּ֔ה לֹא־תֹ֥אַר ל֖וֹ וְלֹ֣א הָדָ֑ר וְנִרְאֵ֥הוּ וְלֹֽא־מַרְאֶ֖ה וְנֶחְמְדֵֽהוּ׃
נִבְזֶה֙ וַחֲדַ֣ל אִישִׁ֔ים אִ֥ישׁ מַכְאֹב֖וֹת וִיד֣וּעַ חֹ֑לִי וּכְמַסְתֵּ֤ר פָּנִים֙ מִמֶּ֔נּוּ נִבְזֶ֖ה וְלֹ֥א חֲשַׁבְנֻֽהוּ׃
אָכֵ֤ן חֳלָיֵ֙נוּ֙ ה֣וּא נָשָׂ֔א וּמַכְאֹבֵ֖ינוּ סְבָלָ֑ם וַאֲנַ֣חְנוּ חֲשַׁבְנֻ֔הוּ נָג֛וּעַ מֻכֵּ֥ה אֱלֹהִ֖ים וּמְעֻנֶּֽה׃
וְהוּא֙ מְחֹלָ֣ל מִפְּשָׁעֵ֔נוּ מְדֻכָּ֖א מֵעֲוֺנֹתֵ֑ינוּ מוּסַ֤ר שְׁלוֹמֵ֙נוּ֙ עָלָ֔יו וּבַחֲבֻרָת֖וֹ נִרְפָּא־לָֽנוּ׃
כֻּלָּ֙נוּ֙ כַּצֹּ֣אן תָּעִ֔ינוּ אִ֥ישׁ לְדַרְכּ֖וֹ פָּנִ֑ינוּ וַיהֹוָה֙ הִפְגִּ֣יעַ בּ֔וֹ אֵ֖ת עֲוֺ֥ן כֻּלָּֽנוּ׃
נִגַּ֨שׂ וְה֣וּא נַעֲנֶה֮ וְלֹ֣א יִפְתַּח־פִּיו֒ כַּשֶּׂה֙ לַטֶּ֣בַח יוּבָ֔ל וּכְרָחֵ֕ל לִפְנֵ֥י גֹזְזֶ֖יהָ נֶאֱלָ֑מָה וְלֹ֥א יִפְתַּ֖ח פִּֽיו׃
מֵעֹ֤צֶר וּמִמִּשְׁפָּט֙ לֻקָּ֔ח וְאֶת־דּוֹר֖וֹ מִ֣י יְשׂוֹחֵ֑חַ כִּ֤י נִגְזַר֙ מֵאֶ֣רֶץ חַיִּ֔ים מִפֶּ֥שַׁע עַמִּ֖י נֶ֥גַע לָֽמוֹ׃
וַיִּתֵּ֤ן אֶת־רְשָׁעִים֙ קִבְר֔וֹ וְאֶת־עָשִׁ֖יר בְּמֹתָ֑יו עַ֚ל לֹא־חָמָ֣ס עָשָׂ֔ה וְלֹ֥א מִרְמָ֖ה בְּפִֽיו׃
וַיהֹוָ֞ה חָפֵ֤ץ דַּכְּאוֹ֙ הֶחֱלִ֔י אִם־תָּשִׂ֤ים אָשָׁם֙ נַפְשׁ֔וֹ יִרְאֶ֥ה זֶ֖רַע יַאֲרִ֣יךְ יָמִ֑ים וְחֵ֥פֶץ יְהֹוָ֖ה בְּיָד֥וֹ יִצְלָֽח׃
מֵעֲמַ֤ל נַפְשׁוֹ֙ יִרְאֶ֣ה יִשְׂבָּ֔ע בְּדַעְתּ֗וֹ יַצְדִּ֥יק צַדִּ֛יק עַבְדִּ֖י לָרַבִּ֑ים וַעֲוֺנֹתָ֖ם ה֥וּא יִסְבֹּֽל׃
לָכֵ֞ן אֲחַלֶּק־ל֣וֹ בָרַבִּ֗ים וְאֶת־עֲצוּמִים֮ יְחַלֵּ֣ק שָׁלָל֒ תַּ֗חַת אֲשֶׁ֨ר הֶעֱרָ֤ה לַמָּ֙וֶת֙ נַפְשׁ֔וֹ וְאֶת־פֹּשְׁעִ֖ים נִמְנָ֑ה וְהוּא֙ חֵטְא־רַבִּ֣ים נָשָׂ֔א וְלַפֹּשְׁעִ֖ים יַפְגִּֽיעַ׃"""


def consonnes(v):
    """Retire voyelles/accents ; maqaf → espace ; sof pasouq supprimé."""
    v = v.replace("\u05BE", " ").replace("\u05C3", "")
    v = "".join(c for c in unicodedata.normalize("NFD", v) if not ("\u0591" <= c <= "\u05C7"))
    return re.sub(r"\s+", " ", v).strip()


VERSETS = [consonnes(v) for v in ESAIE_53.splitlines()]


def parchemin(w, h, ton=(1.0, 1.0, 1.0), sombre=0.0):
    base = Image.open(PARCH).convert("RGB")
    # on retire les bords abîmés de la photo puis on assemble des copies en miroir
    bw, bh = base.size
    base = base.crop((int(bw * .06), int(bh * .08), int(bw * .94), int(bh * .92)))
    th = h
    tw = int(base.size[0] * th / base.size[1])
    tile = base.resize((tw, th), Image.LANCZOS)
    out = Image.new("RGB", (w, h))
    x, flip = 0, False
    while x < w:
        out.paste(ImageOps.mirror(tile) if flip else tile, (x, 0))
        x += tw; flip = not flip
    r, g, b = out.split()
    out = Image.merge("RGB", (r.point(lambda v: v * ton[0]), g.point(lambda v: v * ton[1]), b.point(lambda v: v * ton[2])))
    if sombre:
        out = Image.blend(out, Image.new("RGB", out.size, (60, 42, 24)), sombre)
    return out


def taches(img, n=40, amp=.18, seed=1):
    rnd = random.Random(seed)
    w, h = img.size
    m = Image.new("L", (w // 8, h // 8), 0)
    d = ImageDraw.Draw(m)
    for _ in range(n):
        x, y, r = rnd.randrange(m.size[0]), rnd.randrange(m.size[1]), rnd.randrange(4, 30)
        d.ellipse((x - r, y - r * .7, x + r, y + r * .7), fill=rnd.randrange(30, 120))
    m = m.filter(ImageFilter.GaussianBlur(9)).resize((w, h), Image.BICUBIC)
    dark = ImageChops.multiply(img, Image.new("RGB", (w, h), (int(255 * (1 - amp)), int(255 * (1 - amp * 1.3)), int(255 * (1 - amp * 1.8)))))
    return Image.composite(dark, img, m)


def encre(size, draw_fn, couleur=(34, 24, 16), flou=0.6, seed=2):
    """Dessine un masque de texte, ajoute des irrégularités d'encre et renvoie (couleur, masque)."""
    mask = Image.new("L", size, 0)
    draw_fn(ImageDraw.Draw(mask))
    rnd = Image.effect_noise((size[0] // 4, size[1] // 4), 60).resize(size, Image.BICUBIC)
    mask = ImageChops.multiply(mask, rnd.point(lambda v: 150 + v * 0.42 if v < 250 else 255))
    mask = mask.filter(ImageFilter.GaussianBlur(flou))
    return Image.new("RGB", size, couleur), mask


# ---------------------------------------------------------------- rouleau d'Ésaïe 53
def colonnes(font, largeur):
    lignes, ref = [], []          # ref[i] = numéro du verset où commence la ligne i
    cur, cur_v = "", None
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    for vi, v in enumerate(VERSETS, 1):
        for mot in v.split():
            essai = (cur + " " + mot).strip()
            if d.textlength(essai, font=font, direction="rtl") <= largeur:
                if not cur: cur_v = vi
                cur = essai
            else:
                lignes.append(cur); ref.append(cur_v); cur, cur_v = mot, vi
    lignes.append(cur); ref.append(cur_v)
    return lignes, ref


def rouleau():
    W, H = 4096, 1024
    img = parchemin(W, H, ton=(.93, .82, .66), sombre=.10)
    img = taches(img, 120, .22, seed=7)
    font = ImageFont.truetype(F_HEB, 40)
    font.set_variation_by_name("Medium")
    col_w, gap, top, lh, nl = 430, 130, 175, 56, 12
    lignes, ref = colonnes(font, col_w)
    ncol = -(-len(lignes) // nl)
    total = ncol * col_w + (ncol - 1) * gap
    x0 = (W - total) // 2
    cols_info = []

    def draw(d):
        for c in range(ncol):
            xr = W - (x0 + c * (col_w + gap))           # l'hébreu se lit de droite à gauche : colonne 1 à droite
            for i, txt in enumerate(lignes[c * nl:(c + 1) * nl]):
                d.text((xr, top + i * lh), txt, font=font, fill=255, anchor="ra", direction="rtl")
    col, mask = encre((W, H), draw, seed=3)
    # lignes réglées à la pointe sèche (le texte « pend » sous la ligne)
    regl = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(regl)
    for c in range(ncol):
        xr = W - (x0 + c * (col_w + gap))
        for i in range(nl + 1):
            y = top + i * lh - 4
            dr.line((xr - col_w - 10, y, xr + 10, y), fill=26, width=1)
        dr.line((xr + 14, top - 10, xr + 14, top + nl * lh), fill=18)
        dr.line((xr - col_w - 14, top - 10, xr - col_w - 14, top + nl * lh), fill=18)
        sl = ref[c * nl:(c + 1) * nl]
        cols_info.append({"col": c + 1, "de": sl[0], "a": max(sl), "x_centre": (xr - col_w / 2) / W})
    img = Image.composite(Image.new("RGB", (W, H), (120, 92, 60)), img, regl)
    # coutures entre feuilles de parchemin
    sew = Image.new("L", (W, H), 0); ds = ImageDraw.Draw(sew)
    for xs in (int(W * .5),):
        ds.line((xs, 0, xs, H), fill=70, width=3)
        for y in range(30, H, 46): ds.line((xs - 7, y, xs + 7, y + 10), fill=140, width=2)
    img = Image.composite(Image.new("RGB", (W, H), (80, 56, 34)), img, sew.filter(ImageFilter.GaussianBlur(1)))
    img = Image.composite(col, img, mask)
    # bords supérieur/inférieur usés
    edge = Image.new("L", (W, H), 0); de = ImageDraw.Draw(edge)
    for x in range(0, W, 6):
        de.line((x, 0, x, random.randint(4, 26)), fill=255); de.line((x, H, x, H - random.randint(4, 30)), fill=255)
    img = Image.composite(Image.new("RGB", (W, H), (52, 36, 22)), img, edge.filter(ImageFilter.GaussianBlur(5)))
    out = ROOT / "assets/img/salles/03/rouleau-esaie53.jpg"
    img.save(out, quality=86, optimize=True, progressive=True)
    return img, cols_info, (x0, col_w, gap, top, lh, nl, ncol)


def fragment(img, geo):
    x0, col_w, gap, top, lh, nl, ncol = geo
    W, H = img.size
    c = ncol - 1                                        # dernière colonne : v. 9-12 (fin du chapitre)
    xr = W - (x0 + c * (col_w + gap))
    crop = img.crop((xr - col_w - 110, 60, xr + 110, H - 60))
    S = 1080 - 120
    crop = crop.resize((int(crop.size[0] * S / crop.size[1]), S), Image.LANCZOS)
    w, h = crop.size
    # silhouette rongée du fragment : distance au bord + bruit à plusieurs échelles
    import numpy as np
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(float)
    def bruit(px, amp):
        n = Image.effect_noise((max(2, w // px), max(2, h // px)), 100).resize((w, h), Image.BICUBIC)
        return (np.asarray(n, float) - 128) / 128 * amp
    champ = dist + bruit(60, 70) + bruit(14, 18) + bruit(4, 5)
    m = Image.fromarray(((champ > 34) * 255).astype("uint8"))
    # quelques petites lacunes internes irrégulières
    lac = bruit(30, 1) + bruit(8, .35)
    m = ImageChops.multiply(m, Image.fromarray(((lac < 1.28) * 255).astype("uint8")))
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    bg = Image.new("RGB", (1920, 1080), (10, 10, 14))
    sh = Image.new("L", (1920, 1080), 0)
    ox, oy = (1920 - w) // 2, 60
    sh.paste(m, (ox + 14, oy + 18)); sh = sh.filter(ImageFilter.GaussianBlur(22))
    bg = Image.composite(Image.new("RGB", bg.size, (0, 0, 0)), bg, sh.point(lambda v: v * .8))
    bg.paste(crop, (ox, oy), m)
    bg.save(ROOT / "assets/img/salles/03/fragment-esaie53.jpg", quality=88, optimize=True, progressive=True)
    bg.resize((960, 540), Image.LANCZOS).save(ROOT / "assets/img/salles/03/fragment-esaie53-960.jpg", quality=84)


# ---------------------------------------------------------------- Codex H : avant / après
# 1 Corinthiens 13:4-7 en onciales, sigma lunaire, sans espaces ni accents, en « lignes de sens »
# (démonstration du principe ; ce passage n'est pas tiré d'une page réelle du Codex H)
STIQUES = ["ΗΑΓΑΠΗΜΑΚΡΟΘΥΜΕΙ", "ΧΡΗϹΤΕΥΕΤΑΙΗΑΓΑΠΗ", "ΟΥΖΗΛΟΙ", "ΗΑΓΑΠΗΟΥΠΕΡΠΕΡΕΥΕΤΑΙ", "ΟΥΦΥϹΙΟΥΤΑΙ",
           "ΟΥΚΑϹΧΗΜΟΝΕΙ", "ΟΥΖΗΤΕΙΤΑΕΑΥΤΗϹ", "ΟΥΠΑΡΟΞΥΝΕΤΑΙ", "ΟΥΛΟΓΙΖΕΤΑΙΤΟΚΑΚΟΝ", "ΟΥΧΑΙΡΕΙΕΠΙΤΗΑΔΙΚΙΑ",
           "ϹΥΝΧΑΙΡΕΙΔΕΤΗΑΛΗΘΕΙΑ", "ΠΑΝΤΑϹΤΕΓΕΙ", "ΠΑΝΤΑΠΙϹΤΕΥΕΙ", "ΠΑΝΤΑΕΛΠΙΖΕΙ", "ΠΑΝΤΑΥΠΟΜΕΝΕΙ"]


def codex_h():
    W, H = 1600, 1100
    font = ImageFont.truetype(F_GRC, 50)
    try: font.set_variation_by_name("Regular")
    except Exception: pass

    def draw(d):
        y = 120
        for i, s in enumerate(STIQUES):
            indent = 0 if i in (0, 3, 5, 8, 11) else 46     # retraits des lignes de sens
            d.text((300 + indent, y), s, font=font, fill=255)
            y += 58
    _, mask = encre((W, H), draw, flou=0.8, seed=9)
    miroir = ImageOps.mirror(mask)                       # l'empreinte (« offset ») est inversée

    leaf = parchemin(W, H, ton=(.97, .9, .78), sombre=.06)
    leaf = taches(leaf, 60, .25, seed=11)
    # trous de couture et pliure de reliure à gauche
    d = ImageDraw.Draw(leaf)
    for y in range(140, H - 120, 120): d.ellipse((118, y, 128, y + 10), fill=(70, 50, 30))
    fold = Image.new("L", (W, H), 0); ImageDraw.Draw(fold).rectangle((0, 0, 150, H), fill=110)
    leaf = Image.composite(Image.new("RGB", (W, H), (120, 92, 58)), leaf, fold.filter(ImageFilter.GaussianBlur(40)))

    # AVANT : empreinte à peine perceptible, diffuse et irrégulière
    blot = Image.effect_noise((W // 16, H // 16), 90).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(20))
    faint = ImageChops.multiply(miroir.filter(ImageFilter.GaussianBlur(1.6)), blot.point(lambda v: min(255, 60 + v * .6)))
    avant = Image.composite(Image.new("RGB", (W, H), (125, 95, 62)), leaf, faint.point(lambda v: min(255, v * .75)))
    avant.save(ROOT / "assets/img/salles/05/codexh-avant.jpg", quality=88, optimize=True, progressive=True)

    # APRÈS : rendu « fausses couleurs » typique d'un traitement multispectral (simulation)
    g = ImageOps.autocontrast(leaf.convert("L"), cutoff=2)
    g = ImageOps.equalize(g).filter(ImageFilter.GaussianBlur(1.5))
    fc = ImageOps.colorize(g, black=(30, 18, 70), mid=(150, 120, 190), white=(236, 226, 246))
    ink = miroir.filter(ImageFilter.GaussianBlur(0.9)).point(lambda v: min(255, v * 1.15))
    apres = Image.composite(Image.new("RGB", (W, H), (14, 8, 34)), fc, ink)
    apres.save(ROOT / "assets/img/salles/05/codexh-apres.jpg", quality=88, optimize=True, progressive=True)


if __name__ == "__main__":
    img, cols, geo = rouleau()
    fragment(img, geo)
    # codex_h()  → remplacé par tools/codexh_photo.py
    (ROOT / "tools/data").mkdir(exist_ok=True)
    (ROOT / "tools/data/rouleau_colonnes.json").write_text(json.dumps(cols, ensure_ascii=False, indent=1), encoding="utf-8")
    print("colonnes :", cols)
