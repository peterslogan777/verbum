"""
VERBUM — Salle 02 « Les Copistes et les Massorètes » (étape E04)
Marqueurs remplacés dans tools/templates/salles/copistes.html :
  {{S02_COUCHES}}   Genèse 1:1 en trois couches (consonnes / voyelles / accents)
  {{S02_JEU}}       « Trouvez l'erreur du copiste » (4 manches)
  {{S02_CARTE}}     carte SVG du voyage du Codex d'Alep
  {{S02_FEUILLETS}} 487 feuillets du Codex d'Alep (294 conservés), schéma
  {{S02_TR_SCRIBES}} / {{S02_TR_CODEX}}  transcriptions des narrations
Le tétragramme יהוה est toujours rendu « Jéhovah ».
"""
import html
import json
import math
import unicodedata
from pathlib import Path

e = html.escape
ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Outils hébreu
# --------------------------------------------------------------------------
CANTIL = {chr(c) for c in range(0x0591, 0x05B0)} | {"\u05BD", "\u05C0", "\u05C3", "\u05C6"}
NIQQUD = {chr(c) for c in range(0x05B0, 0x05BD)} | {"\u05BF", "\u05C1", "\u05C2", "\u05C4", "\u05C5", "\u05C7"}


def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if c not in CANTIL)


def consonnes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if c not in CANTIL and c not in NIQQUD)


# --------------------------------------------------------------------------
# Genèse 1:1 — texte massorétique complet (consonnes + niqqud + te'amim)
# --------------------------------------------------------------------------
GEN11 = [
    ("בְּרֵאשִׁ֖ית", "bereshit", "Au commencement"),
    ("בָּרָ֣א", "bara", "créa"),
    ("אֱלֹהִ֑ים", "ʾelohim", "Dieu"),
    ("אֵ֥ת", "ʾet", "(marque du complément)"),
    ("הַשָּׁמַ֖יִם", "hashamayim", "les cieux"),
    ("וְאֵ֥ת", "veʾet", "et"),
    ("הָאָֽרֶץ׃", "haʾarets", "la terre."),
]


def couches():
    out = []
    for full, tr, fr in GEN11:
        out.append(
            f'<span class="cw" tabindex="0"><span class="cw-heb" lang="he">'
            f'<span class="l1">{consonnes(full)}</span><span class="l2">{sans_accents(full)}</span><span class="l3">{full}</span></span>'
            f'<span class="cw-tr">{e(tr)}</span><span class="cw-fr">{e(fr)}</span></span>')
    return "".join(out)


# --------------------------------------------------------------------------
# Jeu : trouvez l'erreur du copiste
# (référence, modèle, index de la lettre fautive dans la copie, lettre fautive, traduction, explication)
# --------------------------------------------------------------------------
JEU = [
    ("Deutéronome 6:4", "שמע ישראל יהוה אלהינו יהוה אחד", "ר",
     "« Écoute, Israël : Jéhovah notre Dieu est un seul Jéhovah. »",
     "Le copiste a écrit אחר (<i>ʾaḥer</i>, « autre ») au lieu de אחד (<i>ʾeḥad</i>, « un ») : le ד et le ר ne diffèrent que par un petit angle. "
     "La phrase deviendrait « Jéhovah est un autre » ! Dans les rouleaux de la Torah, le ד de ce verset est d'ailleurs écrit en grand, "
     "tout comme le ע de שמע, précisément pour empêcher cette confusion.", -1),
    ("Genèse 1:1", "בראשית ברא אלהים את השמים ואת הארץ", "ח",
     "« Au commencement, Dieu créa les cieux et la terre. »",
     "הארץ (« la terre ») est devenu חארץ, un mot qui n'existe pas. Le ה possède une petite ouverture en haut à gauche ; le ח est fermé. "
     "Les règles exigeaient que chaque lettre soit parfaitement formée et entourée de parchemin.", -4),
    ("Ésaïe 40:8", "יבש חציר נבל ציץ ודבר אלהינו יקום לעולם", "כ",
     "« L'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours. »",
     "ודבר (« et la parole ») est devenu ודכר : il suffit d'oublier le petit talon en bas à droite du ב pour obtenir un כ. "
     "Le contrôle lettre par lettre permettait de repérer ce genre de faute.", 15),
    ("Nombres 6:24", "יברכך יהוה וישמרך", "ז",
     "« Que Jéhovah te bénisse et qu'il te garde. »",
     "וישמרך (« et qu'il te garde ») commence maintenant par un ז : la tête du ז déborde des deux côtés, celle du ו d'un seul. "
     "C'est le verset gravé sur les amulettes de Ketef Hinnom (salle 01).", 9),
]


def _letters(s):
    return [c for c in s]


def jeu():
    rounds = []
    for i, (ref, modele, faux, fr, expl, pos) in enumerate(JEU):
        chars = _letters(modele)
        idxs = [k for k, c in enumerate(chars) if c != " "]
        k = idxs[pos] if pos < 0 else idxs[pos]
        copie = chars[:]
        copie[k] = faux
        words, cur = [], []
        for j, c in enumerate(copie + [" "]):
            if c == " ":
                if cur:
                    words.append('<span class="wd">' + "".join(cur) + "</span>")
                cur = []
            else:
                ok = ' data-faute="1"' if j == k else ""
                cur.append(f'<button type="button" class="lt"{ok} aria-label="Lettre {c}">{c}</button>')
        btns = [" ".join(words)]
        rounds.append(f"""
          <div class="jeu-round{' is-active' if i == 0 else ''}" data-round="{i}">
            <p class="jr-ref">Manche {i + 1} sur {len(JEU)} · {e(ref)}</p>
            <div class="jr-line"><span class="jr-lab">Modèle</span><p class="jr-heb" lang="he" dir="rtl">{modele}</p></div>
            <div class="jr-line is-copie"><span class="jr-lab">Copie à vérifier</span><p class="jr-heb" lang="he" dir="rtl">{''.join(btns)}</p></div>
            <p class="jr-fr">{e(fr)}</p>
            <div class="jr-expl" hidden><b>Bien vu !</b> {expl}</div>
          </div>""")
    return "".join(rounds)


# --------------------------------------------------------------------------
# Carte du voyage du Codex d'Alep (projection équirectangulaire locale)
# --------------------------------------------------------------------------
LON0, LON1, LAT0, LAT1 = 29.4, 39.6, 28.8, 37.2
K = 64.0
COS = math.cos(math.radians(33))
VW = round((LON1 - LON0) * COS * K)
VH = round((LAT1 - LAT0) * K)


def _p(lon, lat):
    return round((lon - LON0) * COS * K, 1), round((LAT1 - lat) * K, 1)


ETAPES_ALEP = [
    ("tiberiade", "Tibériade", 35.53, 32.79, "≈ 930", "Copié par Shlomo ben Bouya'a, vocalisé et annoté par Aaron ben Asher."),
    ("jerusalem", "Jérusalem", 35.23, 31.78, "XIe s.", "Acquis par la communauté juive (karaïte) de Jérusalem."),
    ("caire", "Le Caire (Fustat)", 31.23, 30.03, "après 1099", "Emporté lors de la prise de Jérusalem, racheté par les Juifs d'Égypte. Maïmonide le consulte."),
    ("alep", "Alep", 37.16, 36.20, "fin XIVe s.", "Gardé cinq siècles dans la « grotte d'Élie », sous l'ancienne synagogue."),
    ("jerusalem2", "Jérusalem", 35.23, 31.78, "1958", "Arrive en Israël après dix ans de cachette ; 294 feuillets sur 487."),
]


CURVE = [0.35, -0.22, -0.38, -0.3]


def carte():
    data = json.loads((ROOT / "tools" / "geo" / "ne_110m_land.geojson").read_text())
    paths = []
    for f in data["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                lons = [pt[0] for pt in ring]; lats = [pt[1] for pt in ring]
                if max(lons) < LON0 - 5 or min(lons) > LON1 + 5 or max(lats) < LAT0 - 5 or min(lats) > LAT1 + 5:
                    continue
                pts = [_p(lon, lat) for lon, lat in ring]
                paths.append("M" + "L".join(f"{x:g} {y:g}" for x, y in pts) + "Z")
    land = "".join(paths)
    pts = [_p(lon, lat) for _, _, lon, lat, _, _ in ETAPES_ALEP]
    # trajet en courbes douces
    segs = []
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        f = CURVE[i - 1]  # courbures choisies pour qu'aucun trajet n'en croise un autre
        cx, cy = mx - dy * f, my + dx * f
        segs.append(f'<path class="cv-seg" data-seg="{i}" d="M{x0} {y0}Q{cx:.1f} {cy:.1f} {x1} {y1}"/>')
    marks = []
    seen = set()
    for i, (key, nom, lon, lat, date, _) in enumerate(ETAPES_ALEP):
        x, y = _p(lon, lat)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        anchor = "start"
        dx = -12 if anchor == "end" else 12
        dy = 18 if key in ("jerusalem", "caire") else (-8 if key == "tiberiade" else 5)
        marks.append(f'<g class="cv-pt" data-key="{key}"><circle class="halo" cx="{x}" cy="{y}" r="11"/><circle class="core" cx="{x}" cy="{y}" r="5"/>'
                     f'<text x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{e(nom)}</text></g>')
    seas = (f'<text class="cv-sea" x="{_p(31.6, 33.6)[0]}" y="{_p(31.6, 33.6)[1]}">Mer Méditerranée</text>'
            f'<text class="cv-sea" x="{_p(36.4, 29.2)[0]}" y="{_p(36.4, 29.2)[1]}">Arabie</text>'
            f'<text class="cv-sea" x="{_p(31.0, 29.3)[0]}" y="{_p(31.0, 29.3)[1]}">Égypte</text>'
            f'<text class="cv-sea" x="{_p(37.9, 34.9)[0]}" y="{_p(37.9, 34.9)[1]}">Syrie</text>')
    svg = (f'<svg class="cv-map" viewBox="0 0 {VW} {VH}" role="img" aria-label="Carte du voyage du Codex d\'Alep : Tibériade, Jérusalem, Le Caire, Alep, puis Jérusalem">'
           f'<defs><clipPath id="cv-clip"><rect width="{VW}" height="{VH}" rx="18"/></clipPath>'
           f'<radialGradient id="cv-sea" cx="35%" cy="40%" r="80%"><stop offset="0" stop-color="#13263A"/><stop offset="1" stop-color="#0A0A0F"/></radialGradient></defs>'
           f'<g clip-path="url(#cv-clip)"><rect width="{VW}" height="{VH}" fill="url(#cv-sea)"/>'
           f'<path class="cv-land" d="{land}"/>{seas}{"".join(segs)}{"".join(marks)}</g></svg>')
    steps = "".join(
        f'<li data-step="{i}"><button type="button"><b>{e(date)}</b><span>{e(nom)}</span></button><p>{e(txt)}</p></li>'
        for i, (_, nom, _, _, date, txt) in enumerate(ETAPES_ALEP))
    return svg, steps


# --------------------------------------------------------------------------
# Feuillets du Codex d'Alep : 487 à l'origine, 294 conservés (schéma)
# --------------------------------------------------------------------------
def feuillets():
    total, gardes = 487, 294
    etat = ["l"] * 109 + ["k"] * 11            # Torah : seules les dernières pages du Deutéronome subsistent
    milieu = 487 - 120 - 54                    # Prophètes et Écrits
    perdus_milieu = 193 - 109 - 54             # pertes éparses
    # pertes éparses regroupées en quelques lacunes continues (cahiers arrachés)
    runs = [6, 8, 5, 7, 4]
    assert sum(runs) == perdus_milieu
    m = ["k"] * milieu
    pas = milieu // len(runs)
    for i, n in enumerate(runs):
        start = i * pas + pas // 3
        for j in range(n):
            m[start + j] = "l"
    etat += m + ["l"] * 54                     # fin des Écrits perdue
    assert len(etat) == total and etat.count("k") == gardes, (len(etat), etat.count("k"))
    cells = []
    for i, s in enumerate(etat):
        zone = "t" if i < 120 else ("p" if i < 120 + 205 else "e")
        cells.append(f'<i class="{s} z{zone}"></i>')
    return "".join(cells)


# --------------------------------------------------------------------------
# Transcriptions
# --------------------------------------------------------------------------
TR_SCRIBES = [
    "Comment un texte peut-il traverser des siècles sans s'altérer ? Pour le comprendre, il faut entrer dans l'atelier des copistes d'Israël.",
    "Au Ve siècle avant notre ère, après le retour de l'exil, un homme incarne cette mission : Esdras, que la Bible appelle « un copiste habile dans la loi de Moïse ». Devant tout le peuple rassemblé à Jérusalem, il lit le livre de la Loi, du matin jusqu'à midi. Après lui, des générations de scribes, les soferim, vont recopier le texte avec un soin presque inimaginable.",
    "Leurs règles sont strictes. Le parchemin doit être préparé selon la tradition, les lignes tracées à la pointe. Le copiste n'écrit jamais de mémoire : il regarde son modèle, prononce chaque mot, puis l'écrit. Avant de tracer le nom divin, il s'arrête et se concentre. Une copie trop fautive n'est pas corrigée indéfiniment : elle est retirée de l'usage, et déposée dans une genizah.",
    "Puis, entre le VIIe et le Xe siècle de notre ère, viennent les Massorètes, les « gardiens de la tradition ». À Tibériade, au bord du lac de Galilée, des familles de savants, dont la plus célèbre est celle de Ben Asher, se donnent une tâche immense.",
    "L'hébreu biblique s'écrivait sans voyelles. La prononciation se transmettait de bouche à oreille… et risquait de se perdre. Les Massorètes inventent alors un système de petits points et de traits, placés autour des lettres, sans jamais modifier une seule consonne. Ils ajoutent des signes de cantillation pour la lecture chantée, et remplissent les marges de notes : combien de fois tel mot apparaît, quelle orthographe est rare, où se trouve le milieu d'un livre.",
    "Ils comptent les versets, les mots, et même les lettres. Grâce à eux, une erreur ne pouvait plus passer inaperçue. Le texte était désormais protégé par une véritable forteresse de chiffres.",
]
TR_CODEX = [
    "Vers l'an 930, à Tibériade, le scribe Shlomo ben Bouya'a copie l'ensemble des Écritures hébraïques sur près de cinq cents feuillets de parchemin. Puis le plus grand des Massorètes, Aaron ben Asher, y ajoute lui-même les voyelles, les accents et les notes. Ce manuscrit deviendra la référence absolue : on l'appellera la Couronne, le Codex d'Alep.",
    "Son voyage est une épopée. Acheté par la communauté juive de Jérusalem, il est emporté lors de la prise de la ville en 1099, puis racheté et conduit au Caire. Là, le grand savant Maïmonide le consulte et déclare que tous s'y fient. À la fin du XIVe siècle, le Codex gagne Alep, en Syrie, où il est gardé pendant cinq siècles dans une crypte de l'ancienne synagogue.",
    "En décembre 1947, des émeutes éclatent ; la synagogue est incendiée. Le Codex survit, mais à son arrivée à Jérusalem, en 1958, il ne compte plus que 294 feuillets sur 487. La plus grande partie de la Torah a disparu.",
    "Heureusement, un autre manuscrit a traversé les siècles. En 1008, au Caire, le scribe Samuel ben Jacob achève une Bible hébraïque complète, copiée d'après des manuscrits corrigés par Aaron ben Asher. Il en écrit seul les lettres, les voyelles et les notes massorétiques.",
    "Ce volume de 491 feuillets est aujourd'hui conservé à Saint-Pétersbourg, à la Bibliothèque nationale de Russie : c'est le Codex de Leningrad, le plus ancien manuscrit complet de la Bible hébraïque. C'est lui qui sert de base aux éditions savantes modernes, la Biblia Hebraica, et donc à la plupart des traductions actuelles des Écritures hébraïques.",
    "Pendant longtemps, ces codex du Xe et du XIe siècle ont été nos plus anciens témoins complets. Une question restait posée : le texte avait-il changé au cours du millénaire précédent ? La réponse viendra, en 1947, d'une grotte près de la mer Morte… C'est la prochaine salle de notre musée.",
]


def render(page):
    svg, steps = carte()
    rep = {
        "{{S02_COUCHES}}": couches(),
        "{{S02_JEU}}": jeu(),
        "{{S02_CARTE}}": svg,
        "{{S02_ETAPES}}": steps,
        "{{S02_FEUILLETS}}": feuillets(),
        "{{S02_TR_SCRIBES}}": "".join(f"<p>{e(p)}</p>" for p in TR_SCRIBES),
        "{{S02_TR_CODEX}}": "".join(f"<p>{e(p)}</p>" for p in TR_CODEX),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    return page
