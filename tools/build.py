#!/usr/bin/env python3
"""
VERBUM — Générateur statique minimal.
Source unique de vérité pour : la liste des salles, l'en-tête, le plan du musée
(panneau latéral), le pied de page, la page d'accueil et les pages de salles.

Usage :  python3 tools/build.py      (depuis le dossier verbum/)
Les salles marquées "ouverte": True utilisent leur propre corps de page
(tools/templates/salles/<slug>.html) ; les autres reçoivent une page « en préparation ».
"""
from pathlib import Path
import html, json, re, sys

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "tools" / "templates"
sys.path.insert(0, str(ROOT / "tools"))
from icons import ICONS, ARROW, CHEVRON_R, PLAY  # noqa: E402
import accueil  # noqa: E402

SITE = {
    "nom": "VERBUM",
    "titre": "VERBUM — Musée Virtuel de la Bible",
    "slogan": "La Parole qui traverse les millénaires",
    "description": "Musée virtuel immersif consacré à l'histoire de la Bible : manuscrits, copistes, "
                   "manuscrits de la mer Morte, grands codex, imprimerie et découvertes récentes.",
    # Adresse publique du site (balises canoniques, Open Graph, sitemap) :
    #   python3 tools/build.py --url https://mon-domaine.fr [--base /]
    "url": "https://verbum.example",
    "base": "/",          # chemin du site sur le serveur (page 404)
    "etape": "E14",
    "maj": "2026-10-13",
}
for _i, _a in enumerate(sys.argv):
    if _a == "--url" and _i + 1 < len(sys.argv):
        SITE["url"] = sys.argv[_i + 1].rstrip("/")
    if _a == "--base" and _i + 1 < len(sys.argv):
        SITE["base"] = "/" + sys.argv[_i + 1].strip("/") + ("/" if sys.argv[_i + 1].strip("/") else "")

# --------------------------------------------------------------------------
# Les salles du musée (ordre de visite)
# --------------------------------------------------------------------------
SALLES = [
    dict(num="01", slug="origines", etape="E03", icon="tables", glow="rgba(201,168,76,.30)",
         hero_img="assets/img/salles/01/hero-sinai", hero_alt="Les montagnes du Sinaï au lever du soleil",
         css=["salle01"], js=["salle01"],
         titre="Les Origines", sous="Moïse et les premiers textes", era="≈ 1500 – 500 av. J.-C.",
         desc="Des rouleaux d'argent de Ketef Hinnom à la Torah de Moïse : les plus anciens témoins de l'Écriture.",
         badges=["canon"],
         programme=[("Les rouleaux d'argent de Ketef Hinnom", "Le plus ancien texte biblique connu (fin VIIe – début VIe s. av. J.-C.)."),
                    ("La bénédiction sacerdotale", "Nombres 6:24-26 en hébreu, avec traduction française intégrale."),
                    ("Moïse et la Torah", "Contexte historique, écriture au IIe millénaire av. J.-C."),
                    ("Témoins extrabibliques", "Stèle de Merneptah (≈ 1208 av. J.-C.) et autres documents.")]),
    dict(num="02", slug="copistes", etape="E04", icon="plume", glow="rgba(230,204,122,.24)",
         hero_img="assets/img/salles/02/hero-tiberiade", css=["salle02"], js=["salle02"],
         titre="Les Copistes et les Massorètes", sous="Gardiens de chaque lettre", era="Ve s. av. J.-C. – 1008 ap. J.-C.",
         desc="Esdras, les scribes d'Israël, puis les massorètes de Tibériade : des siècles de vigilance pour fixer chaque lettre.",
         badges=["canon"],
         programme=[("Les scribes d'Israël", "Règles de copie, comptage des lettres, vérification."),
                    ("Esdras le copiste", "Son rôle après le retour d'exil."),
                    ("Les massorètes de Tibériade", "Vocalisation (niqqud), cantillation, notes massorétiques."),
                    ("Codex d'Alep et Codex de Leningrad", "Les deux joyaux du texte massorétique.")]),
    dict(num="03", slug="qumran", etape="E05", icon="jarre", glow="rgba(230,190,110,.38)", phare=True,
         hero_img="assets/img/salles/03/hero-grottes", css=["salle03"], js=["salle03"],
         titre="Les Manuscrits de la mer Morte", sous="La grande découverte de Qumrân", era="IIIe s. av. J.-C. – Ier s. ap. J.-C. · découverts en 1947",
         desc="Onze grottes, des centaines de manuscrits et le Grand Rouleau d'Ésaïe : l'événement archéologique du XXe siècle pour le texte biblique.",
         badges=["canon", "noncanon", "apo"],
         programme=[("1947 : la découverte", "Un jeune berger, une grotte, des jarres scellées."),
                    ("Le Grand Rouleau d'Ésaïe (1QIsaᵃ)", "66 chapitres, environ mille ans plus ancien que les codex massorétiques."),
                    ("Comparateur interactif", "Qumrân · texte massorétique · traduction française."),
                    ("Textes non bibliques de Qumrân", "Rouleau du Temple, Document de Damas, Rouleau de la Guerre."),
                    ("Carte des onze grottes", "Le contenu de chaque grotte.")]),
    dict(num="04", slug="codex-grecs", etape="E06", icon="codex", glow="rgba(160,170,220,.22)",
         hero_img="assets/img/salles/04/hero-codex", css=["salle04"], js=["salle04"],
         titre="Les Grands Codex grecs", sous="Les premiers témoins du Nouveau Testament", era="IIe – Ve siècle ap. J.-C.",
         desc="P52, P66, P75, Vaticanus, Sinaïticus, Alexandrinus et les Évangiles éthiopiens de Garima : les premiers témoins du Nouveau Testament.",
         badges=["canon", "apo", "debat"],
         programme=[("Papyrus P52", "Jean 18 sur un fragment grand comme une carte bancaire."),
                    ("Papyrus Bodmer II (P66)", "L'Évangile de Jean vers 200 ap. J.-C."),
                    ("Codex Vaticanus et Sinaïticus", "Les deux grands témoins du IVe siècle."),
                    ("Codex Alexandrinus", "Le joyau de la British Library."),
                    ("Le débat du papyrus P64 (Magdalen)", "Les positions savantes exposées.")]),
    dict(num="05", slug="codex-h", etape="E07", icon="spectre", glow="rgba(130,100,230,.32)", actu=True,
         hero_img="assets/img/salles/05/hero-labo", css=["salle05"], js=["salle05"],
         titre="Découverte 2026 : le Codex H", sous="Les pages fantômes des Lettres de Paul", era="VIe siècle · restitué en 2026",
         desc="42 pages perdues des Lettres de Paul restituées par imagerie multispectrale (Université de Glasgow, avril 2026).",
         badges=["canon"],
         programme=[("Un manuscrit démantelé", "Grande Laure du mont Athos, XIIIe siècle."),
                    ("Les « traces fantômes »", "Quand l'encre se décalque d'une page à l'autre."),
                    ("L'imagerie multispectrale", "De l'ultraviolet à l'infrarouge."),
                    ("L'appareil euthalien", "Les plus anciennes listes de chapitres des Lettres de Paul.")]),
    dict(num="06", slug="apocryphes", etape="E08", icon="dechire", glow="rgba(139,26,26,.40)",
         hero_img="assets/img/salles/06/hero-nag", css=["salle06"], js=["salle06"],
         titre="Les Textes apocryphes", sous="Ce qui n'est pas dans le canon, et pourquoi", era="IIIe s. av. J.-C. – IVe s. ap. J.-C.",
         desc="Nag Hammadi, Évangiles de Thomas, de Marie et de Judas, Livre d'Hénoch, Pasteur d'Hermas : des textes d'histoire, clairement distingués de l'Écriture.",
         badges=["apo", "noncanon", "debat"],
         programme=[("La bibliothèque de Nag Hammadi", "1945, Haute-Égypte."),
                    ("Évangiles de Thomas, de Marie, de Judas", "Contenu, datation, raisons de l'exclusion."),
                    ("Hénoch et le Pasteur d'Hermas", "Des textes lus, mais non retenus."),
                    ("Canon et apocryphes : les critères", "Comparatif visuel.")]),
    dict(num="07", slug="traductions", etape="E09", icon="langues", glow="rgba(110,160,200,.25)",
         hero_img="assets/img/salles/07/hero-alexandrie", hero_alt="Le port d'Alexandrie et son phare au coucher du soleil",
         css=["salle07"], js=["salle07"],
         titre="La Septante et les grandes traductions", sous="De l'hébreu au grec, au latin, au syriaque", era="IIIe s. av. J.-C. – Ve s. ap. J.-C.",
         desc="Alexandrie, Bethléem, Édesse : comment la Parole a commencé à parler toutes les langues.",
         badges=["canon"],
         programme=[("La Septante (LXX)", "La Bible grecque d'Alexandrie."),
                    ("La Vulgate de Jérôme", "Mille ans de Bible latine."),
                    ("La Peshitta", "La Bible en syriaque."),
                    ("Un verset, quatre langues", "Polyglotte interactive alignée mot à mot.")]),
    dict(num="08", slug="gutenberg", etape="E10", icon="caracteres", glow="rgba(201,140,76,.30)",
         hero_img="assets/img/salles/08/hero-mayence", hero_alt="L'atelier d'imprimerie de Gutenberg à Mayence, baigné de lumière dorée",
         css=["salle08"], js=["salle08-geo", "salle08"],
         titre="Gutenberg et l'imprimerie", sous="La révolution de 1455", era="XVe siècle – aujourd'hui",
         desc="Mayence, la Bible à 42 lignes, puis des milliers de langues : la diffusion qui a changé le monde.",
         badges=["canon"],
         programme=[("L'atelier de Mayence", "Caractères mobiles et presse à vis (animation)."),
                    ("La Bible à 42 lignes", "Environ 180 exemplaires, dont une cinquantaine conservés."),
                    ("Réforme et traductions", "Luther, Tyndale, Olivétan."),
                    ("La vague imprimée", "Carte animée des premières Bibles imprimées, 1455-1611."),
                    ("Le globe des traductions", "Plus de 4 000 langues aujourd'hui.")]),
    dict(num="09", slug="archeologie", etape="E11", icon="stele", glow="rgba(190,150,90,.28)",
         hero_img="assets/img/salles/09/hero", hero_alt="Une fouille archéologique sur un tell au coucher du soleil",
         css=["salle09"], js=["salle09-geo", "salle09"],
         titre="Les Preuves archéologiques", sous="Quand la terre confirme l'Écriture", era="IXe s. av. J.-C. – Ier s. ap. J.-C.",
         desc="Stèles de Mésha et de Tel Dan, cylindre de Cyrus, papyrus d'Éléphantine, Pilate, Caïphe, Ninive : des témoins gravés dans la pierre.",
         badges=["canon", "debat"],
         programme=[("Stèles de Mésha et de Tel Dan", "Omri, Jéhovah et la « maison de David »."),
                    ("Le cylindre de Cyrus", "Le retour des exilés."),
                    ("Les papyrus d'Éléphantine", "Johanan et Sanballat, à l'époque de Néhémie."),
                    ("Pilate et Caïphe", "Deux noms des Évangiles retrouvés."),
                    ("La bibliothèque d'Assurbanipal", "Manassé et les récits mésopotamiens du déluge."),
                    ("Le registre des noms", "17 personnages bibliques attestés par leur époque.")]),
    dict(num="10", slug="indestructible", etape="E12", icon="flamme", glow="rgba(200,90,50,.30)",
         hero_img="assets/img/salles/10/hero", hero_alt="Une Bible ouverte intacte au milieu de pages qui se consument, sur un sol de pierre parsemé de braises",
         css=["salle10"], js=["salle10-geo", "salle10"],
         titre="Le Livre indestructible", sous="La Bible face à ses destructeurs", era="303 ap. J.-C. – XXe siècle",
         desc="De l'édit de Dioclétien aux Bibles recopiées à la main en URSS : un livre que rien n'a pu effacer.",
         badges=["canon"],
         programme=[("L'édit de Dioclétien (303)", "Les Écritures livrées au feu."),
                    ("Le bûcher de Tyndale", "Une page de 1526 à livrer aux flammes."),
                    ("Six interdictions, six échecs", "De Toulouse (1229) à l'Albanie (1967)."),
                    ("Derrière le rideau de fer", "Samizdat, Frère André, le projet Perle."),
                    ("Vrai ou légende ?", "Voltaire, Dioclétien, Constantin : démêler le vrai du faux."),
                    ("Le livre le plus diffusé", "Les chiffres de 2025.")]),
    dict(num="11", slug="frise", etape="E13", icon="frise", glow="rgba(201,168,76,.26)",
         hero_img="assets/img/salles/11/hero", hero_alt="Une longue galerie de musée plongée dans la pénombre, où des vitrines dorées présentent des supports d'écriture de toutes les époques",
         css=["salle11"], js=["salle11"],
         titre="La Grande Frise chronologique", sous="3 500 ans de transmission", era="≈ 1500 av. J.-C. – 2026",
         desc="De Moïse au Codex H : chaque étape de la transmission, cliquable, illustrée et commentée.",
         badges=["canon", "apo"],
         programme=[("Frise horizontale interactive", "36 jalons, de Moïse à 2026, filtrables par époque et par nature."),
                    ("Fiches détaillées", "Image, texte, lien vers la salle et commentaire audio de l'époque."),
                    ("Huit époques racontées", "Quatre narrations audio."),
                    ("Le Nouveau Testament face aux classiques", "Écart entre rédaction et plus ancienne copie."),
                    ("Remettre dans l'ordre", "Un jeu pour tester sa mémoire de la frise.")]),
    dict(num="12", slug="bible-francaise", etape="E15", icon="livre-fr", glow="rgba(110,140,210,.28)",
         hero_img="assets/img/salles/12/hero", hero_alt="Une grande Bible imprimée en caractères gothiques, ouverte sur une table de chêne devant une fenêtre donnant sur le lac de Neuchâtel et les Alpes",
         css=["salle12"], js=["salle12"],
         titre="La Bible en français", sous="D'Olivétan à nos jours", era="XIIe siècle – 2026",
         desc="Bibles historiales, Lefèvre d'Étaples, Olivétan, Port-Royal, Segond, Crampon : huit siècles pour faire parler la Bible en français.",
         badges=["canon"],
         programme=[("Avant l'imprimerie", "Psautiers, Bible historiale, premiers livres imprimés."),
                    ("Olivétan, 1535", "La première Bible française traduite sur l'hébreu et le grec."),
                    ("Un verset, cinq siècles", "Jean 1:1 dans onze versions, de la Vulgate à 2018."),
                    ("Le nom divin en français", "L'Éternel, Yahvé, Jéhovah : qui a choisi quoi."),
                    ("Port-Royal et la Bastille", "Sacy traduit en prison."),
                    ("Qui a traduit ?", "Un jeu pour retrouver les traducteurs.")]),
]

for s in SALLES:
    s["href"] = f"salles/{s['num']}-{s['slug']}.html"

DUREES = json.loads((ROOT / "tools" / "data" / "audio_durees.json").read_text(encoding="utf-8"))
NB_PISTES = len([k for k in DUREES if k != "apropos.mp3"])   # narrations de l'audioguide

ETAPES = ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14", "E15"]
ETAPES_FAITES = set(ETAPES)

BADGE = {
    "canon": '<span class="badge badge-canon">Canonique</span>',
    "apo": '<span class="badge badge-apo">Apocryphe</span>',
    "debat": '<span class="badge badge-debat">Datation débattue</span>',
    "noncanon": '<span class="badge badge-apo">Non canonique</span>',
}

e = html.escape


def typo(page):
    """Siècles en petites capitales françaises : Ier → Iᵉʳ, IIIe → IIIᵉ (hors balises)."""
    parts = re.split(r"(<[^>]+>)", page)
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            part = re.sub(r"\b([IVX]*I)er\b", r"\1ᵉʳ", part)
            parts[i] = re.sub(r"\b([IVX]+)e\b", r"\1ᵉ", part)
    return "".join(parts)

# --------------------------------------------------------------------------
# Fragments communs
# --------------------------------------------------------------------------
def head(title, desc, root, extra_css=(), path="index.html", image=None, image_alt="", jsonld=None, noindex=False, base=None):
    """En-tête HTML : SEO, Open Graph, Twitter, manifeste, données structurées."""
    css = ["fonts", "tokens", "base", "components", *extra_css]
    links = "\n  ".join(f'<link rel="stylesheet" href="{root}assets/css/{c}.css">' for c in css)
    url = SITE["url"] + "/" + ("" if path == "index.html" else path)
    img = SITE["url"] + "/" + (image or "assets/img/accueil/hero-jarres-grotte") + ".jpg"
    alt = image_alt or "VERBUM — Musée Virtuel de la Bible"
    ld = ""
    if jsonld:
        ld = '\n  <script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    base_tag = f'\n  <base href="{base}">' if base else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">{base_tag}
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  {robots}
  <link rel="canonical" href="{e(url)}">
  <meta name="theme-color" content="#0A0A0F">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="{e(SITE['titre'])}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:image" content="{e(img)}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1920">
  <meta property="og:image:height" content="1080">
  <meta property="og:image:alt" content="{e(alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{e(img)}">
  <link rel="icon" href="{root}favicon-64.jpg" sizes="64x64" type="image/jpeg">
  <link rel="icon" href="{root}favicon-32.jpg" sizes="32x32" type="image/jpeg">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.jpg">
  <link rel="manifest" href="{root}site.webmanifest">
  <link rel="preload" href="{root}assets/fonts/cinzel-decorative-5.woff2" as="font" type="font/woff2" crossorigin>
  {links}{ld}
</head>"""


def header(root, current=""):
    def cur(k):
        return ' aria-current="page"' if k == current else ""
    return f"""
<a class="skip-link" href="#contenu">Aller au contenu</a>
<div class="scroll-progress" aria-hidden="true"></div>
<header class="site-header" id="top">
  <a class="brand" href="{root}index.html" aria-label="VERBUM — retour au hall d'entrée">
    <img class="brand-mark" src="{root}assets/img/logo-verbum.jpg" alt="" width="40" height="40">
    <span class="brand-text"><span class="brand-name">VERBUM</span><span class="brand-tag">Musée Virtuel de la Bible</span></span>
  </a>
  <nav class="main-nav" aria-label="Navigation principale">
    <a class="hide-sm" href="{root}index.html#parcours"{cur('parcours')}>Le parcours</a>
    <a class="hide-md" href="{root}salles/03-qumran.html"{cur('qumran')}>Qumrân</a>
    <a class="hide-md" href="{root}salles/05-codex-h.html"{cur('codex-h')}>Codex H · 2026</a>
    <a class="hide-sm" href="{root}salles/11-frise.html"{cur('frise')}>Frise</a>
    <a class="hide-sm" href="{root}audioguide.html"{cur('audioguide')}>Audioguide</a>
    <button class="search-btn" type="button" data-search-open aria-label="Rechercher dans le musée" title="Rechercher (touche /)">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.4 15.4 20.5 20.5"/></svg>
      <span class="sb-lbl">Rechercher</span><kbd class="sb-kbd">/</kbd>
    </button>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="plan-musee" data-drawer-open>
      <span class="lbl">Plan du musée</span><span class="bars" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
  </nav>
</header>
{drawer(root, current)}"""


def drawer(root, current=""):
    items = []
    for i, s in enumerate(SALLES):
        star = '<span class="p-star">· salle phare</span>' if s.get("phare") else ('<span class="p-star">· actualité</span>' if s.get("actu") else "")
        cls = ' class="is-current"' if s["slug"] == current else ""
        items.append(f"""      <li{cls} style="transition-delay:{.08 + i * .045:.3f}s"><a href="{root}{s['href']}">
        <span class="p-num">{s['num']}</span><span class="p-title">{e(s['titre'])}{star}</span><span class="p-era">{e(s['era'])}</span></a></li>""")
    items_html = "\n".join(items)
    return f"""<div class="drawer-backdrop" data-drawer-close></div>
<aside class="drawer" id="plan-musee" aria-label="Plan du musée" aria-hidden="true" inert>
  <div class="drawer-head">
    <span class="kicker">Plan du musée</span>
    <button class="drawer-close" type="button" data-drawer-close>Fermer {CHEVRON_R}</button>
  </div>
  <p class="drawer-title">Douze salles, 3 500 ans</p>
  <p class="drawer-sub">Suivez le fil de la transmission, de Moïse à 2026.</p>
  <ol class="plan">
      <li style="transition-delay:.04s"><a href="{root}index.html"><span class="p-num">00</span><span class="p-title">Hall d'entrée</span><span class="p-era">Accueil du musée</span></a></li>
{items_html}
  </ol>
  <p class="drawer-sec">Autour de la visite</p>
  <ul class="plan-plus">
    <li><a href="{root}audioguide.html"{' aria-current="page"' if current == 'audioguide' else ''}><b>Audioguide</b><span>{NB_PISTES} narrations à la suite</span></a></li>
    <li><a href="{root}recherche.html"{' aria-current="page"' if current == 'recherche' else ''}><b>Recherche</b><span>Un nom, un manuscrit, un lieu</span></a></li>
    <li><a href="{root}a-propos.html"{' aria-current="page"' if current == 'a-propos' else ''}><b>À propos</b><span>Mission et principes</span></a></li>
    <li><a href="{root}sources.html"{' aria-current="page"' if current == 'sources' else ''}><b>Sources</b><span>Originaux et bibliographie</span></a></li>
  </ul>
</aside>"""


def footer(root):
    salles_a = "".join(f'<li><a href="{root}{s["href"]}">{e(s["titre"])}</a></li>' for s in SALLES[:6])
    salles_b = "".join(f'<li><a href="{root}{s["href"]}">{e(s["titre"])}</a></li>' for s in SALLES[6:])
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{root}index.html"><img class="brand-mark" src="{root}assets/img/logo-verbum.jpg" alt="" width="40" height="40"><span class="brand-text"><span class="brand-name">VERBUM</span><span class="brand-tag">Musée Virtuel de la Bible</span></span></a>
        <p class="footer-slogan">« La Parole qui traverse les millénaires »</p>
        <p class="footer-verse">« L'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours. »<br><span class="ref">Ésaïe 40:8</span></p>
      </div>
      <div><h4>Salles</h4><ul>{salles_a}</ul></div>
      <div><h4>Suite du parcours</h4><ul>{salles_b}</ul></div>
      <div><h4>Voir les originaux</h4><ul>
        <li><a href="https://www.codexsinaiticus.org" target="_blank" rel="noopener">Codex Sinaïticus (en ligne)</a></li>
        <li><a href="https://www.deadseascrolls.org.il" target="_blank" rel="noopener">Bibliothèque numérique Leon Levy — manuscrits de la mer Morte</a></li>
        <li><a href="https://codexh.arts.gla.ac.uk/" target="_blank" rel="noopener">Édition numérique du Codex H</a></li>
        <li><a href="https://digi.vatlib.it/view/MSS_Vat.gr.1209" target="_blank" rel="noopener">Codex Vaticanus (Bibliothèque vaticane)</a></li>
        <li><a href="https://gallica.bnf.fr" target="_blank" rel="noopener">Gallica — BnF</a></li>
      </ul></div>
    </div>
    <nav class="footer-links" aria-label="Autour de la visite">
      <a href="{root}audioguide.html">Audioguide</a><a href="{root}recherche.html">Recherche</a><a href="{root}a-propos.html">À propos</a><a href="{root}sources.html">Sources et bibliographie</a><a href="{root}sitemap.xml">Plan du site</a>
    </nav>
    <div class="footer-legende" role="note" aria-label="Légende des étiquettes">
      <span class="fl-titre">Légende</span>
      <span><span class="badge badge-canon">Canonique</span> livre ou passage reconnu dans le canon biblique</span>
      <span><span class="badge badge-apo">Apocryphe</span> <span class="badge badge-apo">Non canonique</span> écrit ancien non retenu dans le canon biblique</span>
      <span><span class="badge badge-debat">Débat</span> datation ou interprétation discutée par les spécialistes</span>
    </div>
    <div class="footer-bottom">
      <span>© 2026 {SITE['titre']} · « {SITE['slogan']} » · Mise à jour : octobre 2026</span>
      <span>Les illustrations signalées « reconstitution » sont des créations numériques, non des documents d'archive.</span>
    </div>
  </div>
</footer>"""


def scripts(root, extra=()):
    tags = "".join(f'\n<script src="{root}assets/js/{x}.js" defer></script>' for x in extra)
    return f'<script src="{root}assets/js/main.js" defer></script>\n<script src="{root}assets/js/recherche.js" defer></script>{tags}\n</body>\n</html>\n'


# --------------------------------------------------------------------------
# Page d'accueil
# --------------------------------------------------------------------------
def salle_card(s):
    cls = "salle-card" + (" is-featured" if s.get("phare") else "")
    span = {"01": 6, "02": 6, "03": 8, "04": 4, "05": 6, "06": 6, "07": 4, "08": 4, "09": 4, "10": 4, "11": 4, "12": 4}[s["num"]]
    badges = "".join(BADGE[b] for b in s["badges"][:1])
    status = '<span class="badge badge-canon">Salle ouverte</span>' if s["etape"] in ETAPES_FAITES else '<span class="badge badge-live">Actualité 2026</span>' if s.get("actu") else (
        '<span class="badge badge-live">Salle phare</span>' if s.get("phare") else f'<span class="badge badge-soon">Ouverture · étape {s["etape"]}</span>')
    return f"""
      <article class="{cls}" style="--span:{span}" data-tilt data-reveal>
        <div class="salle-top"><span class="salle-num">{s['num']}</span><span class="salle-icon">{ICONS[s['icon']]}</span></div>
        <p class="salle-era">{e(s['era'])}</p>
        <h3 class="salle-title">{e(s['titre'])}</h3>
        <p class="salle-desc">{e(s['desc'])}</p>
        <div class="salle-foot">{status}<span class="salle-go">Entrer {ARROW[:-6].replace('<svg', '<svg width="14" height="14"')}</svg></span></div>
        <a class="stretched" href="{s['href']}" aria-label="Entrer dans la salle {s['num']} : {e(s['titre'])}"></a>
      </article>"""


def chantier():
    out = []
    for et in ETAPES:
        cls = "done" if et in ETAPES_FAITES else ("next" if et == next((x for x in ETAPES if x not in ETAPES_FAITES), None) else "")
        out.append(f'<span class="{cls}">{et}{" ✓" if cls == "done" else ""}</span>')
    return "".join(out)


def visiter():
    """Bloc « Visiter autrement » en bas de l'accueil (remplace le suivi de chantier)."""
    cartes = [("audioguide.html", "Audioguide", f"{NB_PISTES} narrations, {round(sum(v for k, v in DUREES.items() if k != 'apropos.mp3') / 60)} minutes, à écouter à la suite."),
              ("salles/11-frise.html", "La Grande Frise", "36 jalons, de Moïse au Codex H, sur une seule ligne."),
              ("recherche.html", "Recherche", "Un nom, un manuscrit, un lieu : retrouvez-le dans les salles."),
              ("sources.html", "Sources", "Les originaux en ligne et la bibliographie du musée.")]
    items = "".join(f'<a class="vis-card" href="{h}" data-reveal><span class="vis-t">{e(t)}</span><span class="vis-d">{e(d)}</span>'
                    f'<span class="vis-go">{ARROW}</span></a>' for h, t, d in cartes)
    return f'<span class="kicker" data-reveal>Visiter autrement</span><div class="visiter">{items}</div>'


def build_index():
    body = (TPL / "index.body.html").read_text(encoding="utf-8")
    body = (body.replace("{{SALLES}}", "".join(salle_card(s) for s in SALLES))
                .replace("{{CHANTIER}}", chantier())
                .replace("{{ARROW}}", ARROW).replace("{{PLAY}}", PLAY).replace("{{PLAY_SM}}", PLAY)
                .replace("{{ICON_JARRE}}", ICONS["jarre"]).replace("{{ICON_SPECTRE}}", ICONS["spectre"]))
    slides, dots = accueil.hero_slides()
    fr_cards, fr_dots, fr_labels = accueil.frise()
    svg, tabs, panels = accueil.carte_html()
    transcript = (TPL / "transcription-intro.html").read_text(encoding="utf-8")
    for k, v in {"{{HERO_SLIDES}}": slides, "{{HERO_DOTS}}": dots, "{{FRISE_CARDS}}": fr_cards, "{{FRISE_DOTS}}": fr_dots,
                 "{{FRISE_LABELS}}": fr_labels, "{{CARTE_SVG}}": svg, "{{CARTE_TABS}}": tabs, "{{CARTE_PANELS}}": panels,
                 "{{TRANSCRIPTION}}": transcript}.items():
        body = body.replace(k, v)
    jsonld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["titre"], "alternateName": "VERBUM",
               "url": SITE["url"] + "/", "inLanguage": "fr", "description": SITE["description"],
               "potentialAction": {"@type": "SearchAction", "target": SITE["url"] + "/recherche.html?q={search_term_string}",
                                   "query-input": "required name=search_term_string"}},
              {"@context": "https://schema.org", "@type": "Museum", "name": SITE["titre"], "slogan": SITE["slogan"],
               "url": SITE["url"] + "/", "image": SITE["url"] + "/assets/img/icon-512.jpg",
               "isAccessibleForFree": True, "publicAccess": True}]
    body = body.replace("{{VISITER}}", visiter())
    page = (head(SITE["titre"], SITE["description"], "", ["home"], path="index.html",
                 image="assets/img/accueil/hero-jarres-grotte", image_alt="Des jarres anciennes dans une grotte au-dessus de la mer Morte", jsonld=jsonld)
            + '\n<body class="is-loading home">\n' + header("", "") + body + footer("") + scripts("", ["audio", "accueil", "parchemin-gl"]))
    (ROOT / "index.html").write_text(typo(page), encoding="utf-8")


# --------------------------------------------------------------------------
# Pages de salles
# --------------------------------------------------------------------------
def build_salle(i, s):
    root = "../"
    prev_s = SALLES[i - 1] if i > 0 else None
    next_s = SALLES[i + 1] if i < len(SALLES) - 1 else None
    custom = TPL / "salles" / f"{s['slug']}.html"
    badges = "".join(BADGE[b] for b in s["badges"])
    if custom.exists():
        inner = custom.read_text(encoding="utf-8")
        # module optionnel tools/salle_<slug>.py : render(html) remplace les {{…}} propres à la salle
        mod_path = ROOT / "tools" / f"salle_{s['slug'].replace('-', '_')}.py"
        if mod_path.exists():
            import importlib
            inner = importlib.import_module(mod_path.stem).render(inner)
        inner = inner.replace("{{ROOT}}", root).replace("{{ARROW}}", ARROW).replace("{{PLAY}}", PLAY)
    else:
        prog = "".join(f"<li><b>{e(t)}</b>{e(d)}</li>" for t, d in s["programme"])
        inner = f"""
<section class="section">
  <div class="container programme">
    <div data-reveal>
      <span class="kicker">Au programme de la salle</span>
      <h2>Ce que vous découvrirez ici</h2>
      <ol>{prog}</ol>
    </div>
    <div data-reveal="right">
      <div class="atelier">
        <span class="badge badge-soon">Salle en préparation · étape {s['etape']}</span>
        <p>Les conservateurs installent actuellement cette salle : textes originaux en hébreu ou en grec avec leur traduction française, reconstitutions photoréalistes, commentaires audio et éléments interactifs.</p>
        <p>Elle ouvrira ses portes à l'étape <b>{s['etape']}</b> du chantier.</p>
        <div style="margin-top:1.6rem"><a class="btn btn-ghost" href="{root}index.html#parcours">Retour au parcours {ARROW}</a></div>
      </div>
    </div>
  </div>
</section>"""
    nav_prev = f'<a href="{root}{prev_s["href"]}"><small>Salle précédente</small><span>{prev_s["num"]} · {e(prev_s["titre"])}</span></a>' if prev_s else f'<a href="{root}index.html"><small>Retour</small><span>Hall d\'entrée</span></a>'
    nav_next = f'<a href="{root}{next_s["href"]}"><small>Salle suivante</small><span>{next_s["num"]} · {e(next_s["titre"])}</span></a>' if next_s else ""
    hero_img = ""
    if s.get("hero_img"):
        hi = root + s["hero_img"]
        hero_img = (f'<img src="{hi}.jpg" srcset="{hi}-960.jpg 960w, {hi}.jpg 1920w" sizes="100vw" '
                    f'alt="" fetchpriority="high" decoding="async" data-parallax="0.15">')
    hero_cls = " has-img" if hero_img else ""
    body = f"""
<main id="contenu">
<section class="salle-hero{hero_cls}" style="--salle-glow:{s['glow']}">
  <div class="bg" aria-hidden="true">{hero_img}</div>
  <span class="bg-num" aria-hidden="true">{s['num']}</span>
  <div class="container">
    <div class="icon-xl" data-reveal>{ICONS[s['icon']]}</div>
    <span class="kicker" data-reveal>Salle {s['num']} · {e(s['sous'])}</span>
    <h1 data-reveal>{e(s['titre'])}</h1>
    <p class="era" data-reveal>{e(s['era'])}</p>
    <p class="lead" data-reveal style="margin-top:1rem">{e(s['desc'])}</p>
    <div class="badges" data-reveal>{badges}</div>
  </div>
</section>
{inner}
<div class="container"><nav class="salle-nav" aria-label="Parcours">{nav_prev}{nav_next}</nav></div>
</main>"""
    title = f"Salle {s['num']} · {s['titre']} · {SITE['titre']}"
    jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": s["desc"], "inLanguage": "fr",
              "url": SITE["url"] + "/" + s["href"], "isPartOf": {"@type": "WebSite", "name": SITE["titre"], "url": SITE["url"] + "/"},
              "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Hall d'entrée", "item": SITE["url"] + "/"},
                  {"@type": "ListItem", "position": 2, "name": f"Salle {s['num']} · {s['titre']}", "item": SITE["url"] + "/" + s["href"]}]}}
    page = (head(title, s["desc"], root, ["salle", *s.get("css", [])], path=s["href"], image=s.get("hero_img"),
                 image_alt=s.get("hero_alt", ""), jsonld=jsonld) + f'\n<body class="salle salle-{s["slug"]} is-ready">\n'
            + header(root, s["slug"]) + body + footer(root) + scripts(root, ["audio", *s.get("js", [])]))
    out = ROOT / s["href"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(typo(page), encoding="utf-8")


def build_data():
    data = [{k: s[k] for k in ("num", "slug", "titre", "sous", "era", "etape", "href")} for s in SALLES]
    (ROOT / "assets" / "data" / "salles.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build_index()
    for i, s in enumerate(SALLES):
        build_salle(i, s)
    build_data()
    import pages
    n = pages.build_all(sys.modules[__name__])
    print(f"VERBUM : index + {len(SALLES)} salles + {n} pages générées.")
