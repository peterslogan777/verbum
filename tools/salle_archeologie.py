"""
VERBUM — Salle 09 « Les Preuves archéologiques » (étape E11)
Marqueurs remplacés dans tools/templates/salles/archeologie.html :
  {{S09_SITES}}        atlas : liste des sites + JSON pour la carte (canvas)
  {{S09_INSC_MESHA}}   lecteur d'inscription : stèle de Mésha (moabite)
  {{S09_INSC_DAN}}     lecteur d'inscription : stèle de Tel Dan (araméen ancien)
  {{S09_INSC_PILATE}}  lecteur d'inscription : pierre de Pilate (latin)
  {{S09_INSC_CAIPHE}}  lecteur d'inscription : ossuaire de Caïphe (araméen)
  {{S09_ELEPH}}        papyrus d'Éléphantine : extraits + réseau de personnages
  {{S09_DELUGE}}       comparateur Gilgamesh XI / Genèse 6-9
  {{S09_REGISTRE}}     registre des personnages confirmés (filtrable)
  {{S09_TR_A}} / {{S09_TR_B}}   transcriptions des narrations
Données géographiques : assets/js/salle09-geo.js (Natural Earth 110 m, domaine public).

Les inscriptions paléo-hébraïques sont affichées en lettres carrées : la lettre taw de l'alphabet
ancien a la forme d'une croix, motif exclu de tout le site.
Règles VERBUM appliquées : tout texte hébreu, araméen, moabite, akkadien ou latin est
suivi de sa traduction française ; le tétragramme יהוה est rendu « Jéhovah ».
"""
import html
import json

e = html.escape

# Correspondance lettres carrées → alphabet phénicien (Unicode U+10900…)
PHEN = dict(zip("אבגדהוזחטיכךלמםנןסעפףצץקרשת",
                ["\U00010900", "\U00010901", "\U00010902", "\U00010903", "\U00010904", "\U00010905", "\U00010906",
                 "\U00010907", "\U00010908", "\U00010909", "\U0001090A", "\U0001090A", "\U0001090B", "\U0001090C",
                 "\U0001090C", "\U0001090D", "\U0001090D", "\U0001090E", "\U0001090F", "\U00010910", "\U00010910",
                 "\U00010911", "\U00010911", "\U00010912", "\U00010913", "\U00010914", "\U00010915"]))


def paleo(s):
    return "".join(PHEN.get(c, c) for c in s)


def img(name, alt, caption, sizes="(max-width: 1000px) 100vw, 50vw", root="{{ROOT}}", extra=""):
    p = f"{root}assets/img/salles/09/{name}"
    return (f'<img src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" data-lightbox data-full="{p}.jpg" data-caption="{e(caption)}"{extra}>')


# --------------------------------------------------------------------------
# I. Atlas des découvertes
# --------------------------------------------------------------------------
SITES = [
    # clé, lieu, lon, lat, année, objet, détail, musée, ancre
    ("nimrud", "Nimrud (Kalhu)", 43.33, 36.10, 1846, "L'Obélisque noir",
     "Austen Henry Layard dégage l'obélisque de Salmanazar III : « Jéhu, fils d'Omri » y apporte son tribut (841 av. J.-C.).",
     "British Museum, Londres", "registre"),
    ("ninive", "Ninive", 43.15, 36.36, 1849, "La bibliothèque d'Assurbanipal",
     "Layard puis Hormuzd Rassam (1853) exhument des dizaines de milliers de tablettes et fragments d'argile.",
     "British Museum, Londres", "ninive"),
    ("dibon", "Dibon (Dhiban)", 35.78, 31.50, 1868, "La stèle de Mésha",
     "Le missionnaire Frederick Klein la remarque ; Charles Clermont-Ganneau en fait prendre l'empreinte avant qu'elle ne soit brisée.",
     "Musée du Louvre, Paris", "mesha"),
    ("babylone", "Babylone", 44.42, 32.54, 1879, "Le cylindre de Cyrus",
     "Hormuzd Rassam le découvre dans les fondations de l'Esagil, le grand temple de Babylone.",
     "British Museum, Londres", "cyrus"),
    ("elephantine", "Éléphantine (Assouan)", 32.89, 24.08, 1893, "Les papyrus d'Éléphantine",
     "Premiers achats de papyrus (Charles Wilbour, 1893), puis fouilles allemandes de 1906 à 1908.",
     "Neues Museum (Berlin), Brooklyn Museum, Le Caire", "elephantine"),
    ("cesaree", "Césarée maritime", 34.89, 32.50, 1961, "La pierre de Pilate",
     "L'équipe italienne d'Antonio Frova la retrouve réemployée comme marche dans le théâtre romain.",
     "Musée d'Israël, Jérusalem (copie sur place)", "evangiles"),
    ("jerusalem", "Jérusalem", 35.23, 31.78, 1990, "L'ossuaire de Caïphe",
     "Des travaux dans la forêt de la Paix mettent au jour une tombe familiale du Ier siècle.",
     "Musée d'Israël, Jérusalem", "evangiles"),
    ("dan", "Tel Dan", 35.65, 33.25, 1993, "La stèle de Tel Dan",
     "Gila Cook, de l'équipe d'Avraham Biran, repère un fragment de basalte inscrit dans un mur ; deux autres suivent en 1994.",
     "Musée d'Israël, Jérusalem", "teldan"),
]


def sites():
    data = [{"k": k, "n": n, "lon": lo, "lat": la, "y": y} for k, n, lo, la, y, *_ in SITES]
    lis = []
    for k, n, lo, la, y, obj, det, mus, anc in SITES:
        lis.append(f"""
        <li class="at-site" data-k="{k}">
          <button type="button" class="at-btn" aria-pressed="false" aria-controls="at-info-{k}">
            <span class="at-y">{y}</span><span class="at-o">{e(obj)}</span><span class="at-l">{e(n)}</span>
          </button>
          <div class="at-info" id="at-info-{k}" hidden>
            <p>{e(det)}</p>
            <p class="at-mus"><span class="tag">Conservé</span>{e(mus)}</p>
            <a class="at-go" href="#{anc}">Voir la vitrine {{{{ARROW}}}}</a>
          </div>
        </li>""")
    return (f'<script type="application/json" id="at-data">{json.dumps(data, ensure_ascii=False)}</script>'
            f'<ol class="at-list">{"".join(lis)}</ol>')


# --------------------------------------------------------------------------
# Lecteurs d'inscriptions
# Chaque mot : (texte, translittération, sens en français[, note])
# --------------------------------------------------------------------------
INSC = {
    "mesha": dict(
        lang="he", dir="rtl", paleo=False, nom="Stèle de Mésha",
        label="Moabite · vers 840 av. J.-C. · transcrit en lettres hébraïques (original en alphabet paléo-hébraïque)",
        lignes=[
            ("1", [("אנך", "ʾnk", "je (suis)"), ("משע", "mšʿ", "Mésha"), ("בן", "bn", "fils de"),
                   ("כמש[ית]", "kmš[yt]", "Kemosh[-yat]", "Nom du père, partiellement restitué."),
                   ("מלך", "mlk", "roi"), ("מאב", "mʾb", "de Moab"), ("הדיבני", "hdybny", "le Dibonite", "Originaire de Dibon, capitale de Mésha.")],
             "« Je suis Mésha, fils de Kemosh[-yat], roi de Moab, le Dibonite. »"),
            ("4-5", [("עמרי", "ʿmry", "Omri", "Roi d'Israël, fondateur de Samarie (1 Rois 16:23-24)."),
                     ("מלך", "mlk", "(était) roi"), ("ישראל", "yśrʾl", "d'Israël"),
                     ("ויענו", "wyʿnw", "et il opprima"), ("את", "ʾt", "(marque du complément)"), ("מאב", "mʾb", "Moab"),
                     ("ימן", "ymn", "des jours"), ("רבן", "rbn", "nombreux")],
             "« Omri était roi d'Israël, et il opprima Moab pendant de longs jours. »"),
            ("17-18", [("ואקח", "wʾqḥ", "et je pris"), ("משם", "mšm", "de là"), ("א[ת]", "ʾ[t]", "(marque du complément)"),
                       ("[כ]לי", "[k]ly", "les objets sacrés", "Littéralement « les ustensiles », ceux du culte."),
                       ("יהוה", "yhwh", "de Jéhovah", "Le tétragramme, nom propre du Dieu d'Israël : l'une des plus anciennes attestations hors de la Bible."),
                       ("ואסחב", "wʾsḥb", "et je (les) traînai"), ("הם", "hm", "eux"), ("לפני", "lpny", "devant"),
                       ("כמש", "kmš", "Kemosh", "Le dieu national de Moab.")],
             "« Et je pris de là les [objets sacrés] de Jéhovah, et je les traînai devant Kemosh. »"),
            ("31", [("וחורנן", "wḥwrnn", "et Horonaïm", "Ville de Moab citée en Ésaïe 15:5 et Jérémie 48:3."),
                    ("ישב", "yšb", "habitait"), ("בה", "bh", "en elle"),
                    ("ב[ת ד]וד", "bt[d]wd", "la maison de [D]avid ?", "Lecture proposée par André Lemaire en 1994 : une lettre est restituée. Lecture débattue (voir ci-dessous).")],
             "« Et à Horonaïm habitait la maison de [D]avid… » (lecture débattue)"),
        ]),
    "dan": dict(
        lang="arc", dir="rtl", paleo=False, nom="Stèle de Tel Dan",
        label="Araméen ancien · IXe siècle av. J.-C. · transcrit en lettres hébraïques (original en alphabet de type phénicien)",
        lignes=[
            ("7", [("[קתלת", "[qtlt", "[j'ai tué", "Restitution de Biran et Naveh (1995)."), ("אית", "ʾyt", "(marque du complément)"),
                   ("יהו]רם", "yhw]rm", "[Jo]ram", "Joram, roi d'Israël (2 Rois 8-9). Le début du nom est restitué."),
                   ("בר", "br", "fils de"), ("[אחאב]", "[ʾḥʾb]", "[d'Achab]", "Nom entièrement restitué.")],
             "« [J'ai tué Jo]ram, fils [d'Achab], »"),
            ("8", [("מלך", "mlk", "roi"), ("ישראל", "yśrʾl", "d'Israël", "La plus ancienne mention connue du titre « roi d'Israël » sur une inscription."),
                   ("וקתל[ת", "wqtl[t", "et j'ai tu[é"), ("אית", "ʾyt", "(marque du complément)"),
                   ("אחז]יהו", "ʾḥz]yhw", "[Achaz]ias", "Achazia, roi de Juda (2 Rois 8:25-29). Le début du nom est restitué."),
                   ("בר", "br", "fils de"), ("[יהורם]", "[yhwrm]", "[Joram]")],
             "« roi d'Israël, et j'ai tu[é Achaz]ias, fils de [Joram], »"),
            ("9", [("[מל]ך", "[ml]k", "[ro]i"),
                   ("ביתדוד", "bytdwd", "de la maison de David", "Écrit en un seul mot, sans point séparateur : un nom de royaume, « la dynastie de David ». C'est la plus ancienne mention de David hors de la Bible."),
                   ("ואשם", "wʾšm", "et je mis…")],
             "« [ro]i de la maison de David. Et je mis… »"),
        ]),
    "pilate": dict(
        lang="la", dir="ltr", paleo=False, nom="Pierre de Pilate",
        label="Latin, capitales romaines · vers 26-36 ap. J.-C.",
        lignes=[
            ("1", [("[…]S", "", "(fin d'un mot perdu)", "Peut-être la fin d'une dédicace « aux dieux Augustes » ; restitution discutée."),
                   ("TIBERIEVM", "Tiberieum", "le Tibérieum", "Un édifice dédié à l'empereur Tibère, qui régna de 14 à 37 (Luc 3:1). Sa nature exacte (temple, portique, phare ?) est discutée.")],
             "« […] le Tibérieum »"),
            ("2", [("[PO]NTIVS", "Pontius", "Ponce"), ("PILATVS", "Pilatus", "Pilate", "Le gouverneur devant qui Jésus comparut (Jean 18-19).")],
             "« [Po]nce Pilate »"),
            ("3", [("[PRAEF]ECTVS", "praefectus", "préfet", "Titre exact de Pilate. Des auteurs plus tardifs, comme Tacite, l'appellent « procurateur »."),
                   ("IVDA[EA]E", "Iudaeae", "de Judée")],
             "« [pré]fet de Jud[é]e »"),
            ("4", [("[…]E[…]", "", "(une seule lettre lisible)", "On restitue souvent « [a fait et] dé[dié] » ; ce n'est qu'une hypothèse.")],
             "« […] »"),
        ]),
    "caiphe": dict(
        lang="arc", dir="rtl", paleo=False, nom="Ossuaire de Caïphe",
        label="Araméen, écriture carrée gravée · Ier siècle ap. J.-C.",
        lignes=[
            ("A", [("יהוסף", "yhwsp", "Joseph", "Selon l'historien Flavius Josèphe, le grand prêtre s'appelait « Joseph, appelé Caïphe » (Antiquités juives 18, 35)."),
                   ("בר", "br", "fils de"), ("קיפא", "qypʾ", "Caïphe", "Nom de famille ou surnom, écrit ici avec un yod.")],
             "« Joseph, fils de Caïphe »"),
            ("B", [("יהוסף", "yhwsp", "Joseph"), ("בר", "br", "fils de"),
                   ("קפא", "qpʾ", "Caïphe", "Même nom, écrit sans yod, sur un autre côté du coffre.")],
             "« Joseph, fils de Caïphe »"),
        ]),
}


def insc(key):
    d = INSC[key]
    rows = []
    for n, mots, fr in d["lignes"]:
        ws = []
        for i, m in enumerate(mots):
            txt, tr, sens = m[:3]
            note = m[3] if len(m) > 3 else ""
            pal = f'<span class="w-p" aria-hidden="true">{e(paleo(txt))}</span>' if d["paleo"] else ""
            ws.append(f'<button type="button" class="w" data-tr="{e(tr)}" data-fr="{e(sens)}" data-note="{e(note)}" '
                      f'aria-label="{e(txt)} : {e(sens)}"><span class="w-c">{e(txt)}</span>{pal}</button>')
        sep = '<span class="w-sep" aria-hidden="true">·</span>' if d["dir"] == "rtl" else " "
        rows.append(f"""
          <div class="in-l">
            <span class="in-n">l. {n}</span>
            <p class="in-o" lang="{d['lang']}" dir="{d['dir']}">{sep.join(ws)}</p>
            <p class="in-f">{e(fr)}</p>
          </div>""")
    toggle = ""
    if d["paleo"]:
        toggle = f"""
        <div class="seg in-seg" role="radiogroup" aria-label="Écriture affichée">
          <button type="button" role="radio" aria-checked="true" data-s="p">Écriture d'origine<small>alphabet paléo-hébraïque</small></button>
          <button type="button" role="radio" aria-checked="false" data-s="c">Lettres hébraïques<small>transcription moderne</small></button>
        </div>"""
    return f"""
      <div class="insc{' is-paleo' if d['paleo'] else ''} insc-{d['dir']}" data-insc="{key}">
        <div class="in-head">
          <div><h4 class="in-t">{e(d['nom'])}</h4><p class="in-lab">{e(d['label'])}</p></div>{toggle}
        </div>
        <div class="in-body">{''.join(rows)}</div>
        <div class="in-info" aria-live="polite">
          <p class="in-hint">Touchez un mot pour afficher sa lecture et son sens.</p>
          <div class="in-sel" hidden><span class="in-w"></span><span class="in-tr"></span><b class="in-fr"></b><p class="in-note"></p></div>
        </div>
      </div>"""


# --------------------------------------------------------------------------
# V. Éléphantine
# --------------------------------------------------------------------------
ELEPH_EXTRAITS = [
    ("Ligne 1 (adresse)", "אל מראן בגוהי פחת יהוד עבדיך ידניה וכנותה כהניא זי ביב בירתא",
     "« À notre seigneur Bagohi, gouverneur de Juda, tes serviteurs Yedania et ses collègues, les prêtres qui sont à Yeb, la forteresse. »"),
    ("Ligne 18", "יהוחנן כהנא רבא וכנותה כהניא זי בירושלם",
     "« …Yehohanan le grand prêtre et ses collègues, les prêtres qui sont à Jérusalem… »"),
    ("Ligne 29", "דליה ושלמיה בני סנאבלט פחת שמרין",
     "« …Delaïa et Shélémia, fils de Sanballat, gouverneur de Samarie. »"),
]

ELEPH_NOEUDS = [
    # clé, nom, rôle, référence biblique, x%, y%
    ("papyrus", "La lettre de 407 av. J.-C.", "Pétition des Judéens d'Éléphantine (TAD A4.7)", "Datée du 20 marheshvan, an 17 de Darius", 25, 50),
    ("johanan", "Yehohanan", "Grand prêtre à Jérusalem", "Néhémie 12:22 : « Johanan », dans la liste des grands prêtres", 74, 12),
    ("sanballat", "Sanballat", "Gouverneur de Samarie, père de Delaïa et Shélémia", "Néhémie 2:10, 19 ; 4:1 : l'adversaire de Néhémie", 74, 37),
    ("darius", "Darius II", "Roi de Perse (424-404 av. J.-C.)", "Néhémie 12:22 : « Darius le Perse »", 74, 63),
    ("bagohi", "Bagohi", "Gouverneur perse de Juda, successeur de Néhémie", "Non cité dans la Bible ; connu aussi par Flavius Josèphe", 74, 88),
]


def eleph():
    ex = "".join(f"""
          <blockquote class="q-heb el-q">
            <p class="qh" lang="arc" dir="rtl">{e(a)}</p>
            <p class="qf">{e(f)}</p>
            <cite>{e(l)}</cite>
          </blockquote>""" for l, a, f in ELEPH_EXTRAITS)
    nodes = []
    for k, n, r, ref, x, y in ELEPH_NOEUDS:
        cls = " el-c" if k == "papyrus" else ""
        nodes.append(f'<button type="button" class="el-n{cls}" data-k="{k}" style="--x:{x}%;--y:{y}%" aria-pressed="false">'
                     f'<b>{e(n)}</b><small>{e(r)}</small><span class="el-ref">{e(ref)}</span></button>')
    lines = "".join(f'<line x1="38" y1="50" x2="{x - 12}" y2="{y}" data-k="{k}"/>' for k, _, _, _, x, y in ELEPH_NOEUDS if k != "papyrus")
    return ex, f"""
        <div class="el-net" role="group" aria-label="Les personnages nommés dans la lettre">
          <svg class="el-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{lines}</svg>
          {''.join(nodes)}
        </div>"""


# --------------------------------------------------------------------------
# VII. Déluge : Gilgamesh XI / Genèse
# --------------------------------------------------------------------------
DELUGE = [
    ("Qui décide ?", "L'assemblée des grands dieux, menée par Enlil.", "Jéhovah seul (Genèse 6:5-7).", "diff"),
    ("Pourquoi ?", "La tablette XI ne donne pas de raison ; un autre récit (Atrahasis) évoque le bruit des humains qui dérange les dieux.",
     "La violence et la corruption morale qui remplissent la terre (Genèse 6:11-13).", "diff"),
    ("Le héros", "Uta-napishti, averti en secret par le dieu Ea, qui parle à travers un mur de roseaux.",
     "Noé, « homme juste », averti directement par Dieu (Genèse 6:9, 13).", "proche"),
    ("Le bateau", "Un cube aux côtés égaux, sur sept niveaux, enduit de bitume.",
     "Une arche de 300 × 50 × 30 coudées (≈ 135 × 22 × 13 m), sur trois niveaux, enduite de bitume (Genèse 6:14-16).", "proche"),
    ("Les passagers", "Sa famille, des artisans, du bétail et des animaux sauvages.", "Huit personnes et les animaux, par couples (Genèse 7:7-9).", "proche"),
    ("La durée", "Six jours et sept nuits de tempête.", "Quarante jours de pluie ; près d'un an dans l'arche (Genèse 7:12 ; 8:13-14).", "diff"),
    ("L'échouage", "Le mont Nimush.", "Les montagnes d'Ararat (Genèse 8:4).", "proche"),
    ("Les oiseaux", "Une colombe, une hirondelle, puis un corbeau qui ne revient pas.", "Un corbeau, puis une colombe envoyée trois fois (Genèse 8:6-12).", "proche"),
    ("Après le déluge", "Un sacrifice ; les dieux affamés « s'assemblent comme des mouches ».",
     "Un sacrifice, puis une alliance avec toute la vie, signée par l'arc-en-ciel (Genèse 8:20 – 9:17).", "diff"),
    ("Le destin du héros", "Uta-napishti reçoit l'immortalité des dieux.", "Noé vit encore 350 ans, puis meurt (Genèse 9:28-29).", "diff"),
]


def deluge():
    rows = "".join(f"""
          <div class="dl-row" data-t="{t}" role="row">
            <span class="dl-k" role="rowheader">{e(k)}</span>
            <span class="dl-g" role="cell">{e(g)}</span>
            <span class="dl-b" role="cell">{e(b)}</span>
            <span class="dl-tag" role="cell">{'Ressemblance' if t == 'proche' else 'Différence'}</span>
          </div>""" for k, g, b, t in DELUGE)
    return f"""
        <div class="dl-tab" role="table" aria-label="Comparaison des récits du déluge">
          <div class="dl-row dl-hd" role="row">
            <span role="columnheader">Élément</span>
            <span role="columnheader">Épopée de Gilgamesh, tablette XI<small>copie de Ninive, VIIe s. av. J.-C.</small></span>
            <span role="columnheader">Genèse 6-9 <span class="badge badge-canon">Canonique</span></span>
            <span role="columnheader" class="sr-only">Type</span>
          </div>{rows}
        </div>"""


# --------------------------------------------------------------------------
# VIII. Registre des personnages
# --------------------------------------------------------------------------
REGISTRE = [
    # nom, rôle, réf. biblique, témoin archéologique, date du témoin, lieu de conservation, catégories
    ("Omri", "Roi d'Israël", "1 Rois 16:16-28", "Stèle de Mésha ; annales assyriennes (« maison d'Omri »)", "IXe s. av. J.-C.", "Louvre, Paris", "at roi"),
    ("Achab", "Roi d'Israël", "1 Rois 16:29 – 22:40", "Monolithe de Kurkh, de Salmanazar III (bataille de Qarqar, 853 av. J.-C.)", "853 av. J.-C.", "British Museum, Londres", "at roi"),
    ("Jéhu", "Roi d'Israël", "2 Rois 9-10", "Obélisque noir de Salmanazar III : Jéhu, prosterné, apporte son tribut", "841 av. J.-C.", "British Museum, Londres", "at roi"),
    ("Mésha", "Roi de Moab", "2 Rois 3:4-5", "Sa propre stèle, à Dibon", "Vers 840 av. J.-C.", "Louvre, Paris", "at nations"),
    ("Hazaël", "Roi d'Aram-Damas", "1 Rois 19:15 ; 2 Rois 8:7-15", "Annales de Salmanazar III ; ivoires inscrits à son nom", "IXe s. av. J.-C.", "British Museum ; musées d'Iraq et d'Israël", "at nations"),
    ("Ézéchias", "Roi de Juda", "2 Rois 18-20", "Prisme de Sennachérib (« enfermé dans Jérusalem comme un oiseau en cage ») ; empreinte de sceau royal (Ophel, 2015)", "VIIIe – VIIe s. av. J.-C.", "British Museum ; Oriental Institute, Chicago ; Jérusalem", "at roi"),
    ("Sennachérib", "Roi d'Assyrie", "2 Rois 18:13 – 19:37", "Ses propres annales ; reliefs du siège de Lakish", "Vers 700 av. J.-C.", "British Museum, Londres", "at nations"),
    ("Manassé", "Roi de Juda", "2 Rois 21 ; 2 Chroniques 33", "Prisme d'Assarhaddon ; prisme C d'Assurbanipal (liste de 22 rois vassaux)", "VIIe s. av. J.-C.", "British Museum, Londres", "at roi"),
    ("Joïakin", "Roi de Juda", "2 Rois 24:8-15 ; 25:27-30", "Tablettes de rations de Babylone : « Ia'ukinu, roi de Juda »", "Vers 592 av. J.-C.", "Musée de Pergame, Berlin", "at roi"),
    ("Nabuchodonosor II", "Roi de Babylone", "2 Rois 24-25 ; Daniel 1-4", "Chronique babylonienne : prise de Jérusalem en 597 av. J.-C.", "VIe s. av. J.-C.", "British Museum, Londres", "at nations"),
    ("Cyrus II", "Roi de Perse", "Esdras 1:1-4 ; Ésaïe 45:1", "Cylindre de Cyrus", "Vers 539 av. J.-C.", "British Museum, Londres", "at nations"),
    ("Sanballat", "Gouverneur de Samarie", "Néhémie 2:10, 19", "Papyrus d'Éléphantine (TAD A4.7)", "407 av. J.-C.", "Neues Museum, Berlin", "at nations"),
    ("Johanan", "Grand prêtre", "Néhémie 12:22", "Papyrus d'Éléphantine (TAD A4.7)", "407 av. J.-C.", "Neues Museum, Berlin", "at"),
    ("Hérode le Grand", "Roi de Judée", "Matthieu 2:1-19 ; Luc 1:5", "Amphores de vin de Massada adressées « au roi Hérode de Judée »", "19 av. J.-C.", "Massada, Israël", "nt roi"),
    ("Ponce Pilate", "Préfet de Judée", "Luc 3:1 ; Jean 18-19", "Pierre de Césarée", "26-36 ap. J.-C.", "Musée d'Israël, Jérusalem", "nt nations"),
    ("Caïphe", "Grand prêtre", "Matthieu 26:57 ; Jean 18:13-14", "Ossuaire de « Joseph, fils de Caïphe » (identification admise par la majorité des spécialistes)", "Ier s. ap. J.-C.", "Musée d'Israël, Jérusalem", "nt"),
    ("Gallion", "Proconsul d'Achaïe", "Actes 18:12-17", "Inscription de Delphes (lettre de l'empereur Claude), qui permet de dater le séjour de Paul à Corinthe", "Vers 52 ap. J.-C.", "Musée de Delphes, Grèce", "nt nations"),
]


def registre():
    cards = []
    for nom, role, ref, tem, date, lieu, cats in REGISTRE:
        test = "Nouveau Testament" if "nt" in cats.split() else "Ancien Testament"
        cards.append(f"""
          <article class="rg-c" data-cats="{cats}">
            <header><span class="rg-test">{test}</span><h4>{e(nom)}</h4><p class="rg-role">{e(role)}</p></header>
            <p class="rg-ref"><span class="badge badge-canon">Canonique</span> {e(ref)}</p>
            <dl>
              <div><dt>Témoin</dt><dd>{e(tem)}</dd></div>
              <div><dt>Date</dt><dd>{e(date)}</dd></div>
              <div><dt>Conservé</dt><dd>{e(lieu)}</dd></div>
            </dl>
          </article>""")
    return "".join(cards)


# --------------------------------------------------------------------------
# Transcriptions
# --------------------------------------------------------------------------
TR_A = """<p>Dibon, dans l'ancien pays de Moab, 1868. Un missionnaire aperçoit dans le sable une pierre noire couverte d'écriture. C'est la stèle du roi Mésha. Le roi y raconte qu'Omri, roi d'Israël, a opprimé Moab pendant de longues années, exactement comme le deuxième livre des Rois présente Mésha, tributaire d'Israël. À la ligne dix-huit, Mésha se vante d'avoir emporté les objets sacrés de Jéhovah. C'est l'une des plus anciennes mentions connues du nom divin hors de la Bible, gravée neuf siècles avant notre ère. Brisée peu après sa découverte, la pierre fut sauvée grâce à une empreinte prise juste à temps, puis reconstituée. Elle est aujourd'hui au musée du Louvre.</p>
<p>Tel Dan, au nord d'Israël, 1993. Dans un mur écroulé, une archéologue remarque un fragment de basalte. Un roi araméen y célèbre sa victoire sur le roi d'Israël et sur le roi de la maison de David. Pour la première fois, le nom de David apparaît hors de la Bible, environ un siècle et demi après son règne. Babylone, 1879. Le cylindre de Cyrus révèle la politique du roi perse : il rend aux villes les statues de leurs dieux et laisse rentrer chez eux les peuples déplacés. Le livre d'Esdras décrit la même politique en faveur des Judéens, autorisés à rentrer d'exil et à rebâtir le temple de Jéhovah à Jérusalem.</p>"""

TR_B = """<p>Sur une île du Nil, à Éléphantine, vivait au cinquième siècle avant notre ère une colonie de soldats judéens. Leurs papyrus, écrits en araméen, nomment le grand prêtre Johanan et les fils de Sanballat, gouverneur de Samarie : des personnages que l'on retrouve dans le livre de Néhémie. Césarée, au bord de la Méditerranée, 1961. Des archéologues italiens dégagent une pierre réemployée dans le théâtre romain. On y lit le nom de Ponce Pilate, préfet de Judée, le gouverneur devant qui Jésus comparut. Jusque-là, Pilate n'était connu que par les Évangiles et quelques auteurs anciens.</p>
<p>Jérusalem, 1990. Des ouvriers mettent au jour une tombe familiale. Sur un ossuaire richement sculpté, une inscription araméenne : Joseph, fils de Caïphe. Le grand prêtre qui présida le procès de Jésus sort à son tour de l'ombre. Et à Ninive, dans les ruines de la bibliothèque du roi Assurbanipal, on a retrouvé des milliers de tablettes d'argile. Les annales de ce roi nomment Manassé, roi de Juda. Ses scribes ont aussi copié un récit mésopotamien du déluge, qui permet de mesurer combien la Genèse s'en distingue. La pierre, l'argile et le papyrus ne remplacent pas la foi. Mais ils montrent que la Bible parle de lieux, de rois et de peuples bien réels.</p>"""


def render(inner):
    ex, net = eleph()
    rep = {
        "{{S09_SITES}}": sites(),
        "{{S09_INSC_MESHA}}": insc("mesha"),
        "{{S09_INSC_DAN}}": insc("dan"),
        "{{S09_INSC_PILATE}}": insc("pilate"),
        "{{S09_INSC_CAIPHE}}": insc("caiphe"),
        "{{S09_ELEPH_EX}}": ex,
        "{{S09_ELEPH_NET}}": net,
        "{{S09_DELUGE}}": deluge(),
        "{{S09_REGISTRE}}": registre(),
        "{{S09_NB_REG}}": str(len(REGISTRE)),
        "{{S09_TR_A}}": TR_A,
        "{{IMG_MESHA}}": img("mesha", "La stèle de Mésha, haute pierre de basalte noir au sommet arrondi couverte de lignes d'écriture, sous un projecteur dans une galerie sombre",
                             "La stèle de Mésha (Louvre, AO 5066). Reconstitution numérique.", extra=' class="lampe-base"'),
        "{{IMG_LABO}}": img("labo", "Dans un laboratoire sombre, une pierre inscrite sous un dôme de petites lampes ; un chercheur observe sur un écran le relief des lettres",
                            "Imagerie par transformation de réflectance (RTI). Reconstitution numérique."),
        "{{IMG_TELDAN}}": img("teldan", "Fragment triangulaire de basalte gravé de lignes d'écriture araméenne, à demi pris dans la terre d'une fouille, avec une brosse et une truelle",
                              "Le fragment A de la stèle de Tel Dan au moment de sa découverte. Reconstitution numérique.", extra=' class="fouille-img"'),
        "{{IMG_CYRUS}}": img("cyrus", "Cylindre d'argile en forme de baril couvert de fines lignes cunéiformes, posé dans une vitrine sombre",
                             "Le cylindre de Cyrus (British Museum). Reconstitution numérique.", sizes="100vw"),
        "{{IMG_PILATE}}": img("pilate", "Bloc de calcaire portant une inscription latine en capitales, devant les gradins d'un théâtre romain au bord de la mer au coucher du soleil",
                              "La pierre de Pilate à Césarée maritime. Reconstitution numérique."),
        "{{IMG_CAIPHE}}": img("caiphe", "Coffre funéraire en calcaire orné de deux grandes rosaces, dans une grotte funéraire éclairée par un rayon de lumière",
                              "Un ossuaire orné du Ier siècle, comme celui de Caïphe. Reconstitution numérique."),
        "{{IMG_NINIVE}}": img("ninive", "Un scribe assyrien barbu lit une tablette dans une longue salle remplie d'étagères de tablettes d'argile, éclairée par des lampes à huile",
                              "La bibliothèque d'Assurbanipal à Ninive. Reconstitution numérique."),
        "{{IMG_TABLETTE}}": img("tablette", "Tablette d'argile brisée couverte de signes cunéiformes, sous une lumière rasante, à côté d'une loupe",
                                "La tablette XI de l'Épopée de Gilgamesh, dite « tablette du déluge ». Reconstitution numérique."),
        "{{S09_TR_B}}": TR_B,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("".join(["{{S09_SITES}}", "{{S09_INSC_MESHA}}", "{{S09_INSC_DAN}}", "{{S09_INSC_PILATE}}",
                          "{{S09_INSC_CAIPHE}}", "{{S09_ELEPH_EX}}", "{{S09_ELEPH_NET}}", "{{S09_DELUGE}}", "{{S09_REGISTRE}}"]))
    assert "{{S09" not in out
    assert "Seigneur" not in out and "LORD" not in out
    assert "יהוה" in out and "Jéhovah" in out
    print("salle_archeologie OK :", len(out), "caractères ;", len(SITES), "sites ;", len(REGISTRE), "personnages")
