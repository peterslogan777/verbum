"""
VERBUM — Salle 01 « Les Origines » (étape E03)
Données et générateurs HTML propres à la salle :
  {{S01_BENEDICTION}}  bénédiction sacerdotale (Nombres 6:24-26) mot à mot, 3 écritures
  {{S01_KH2}}          lecture restituée de l'amulette KH2 (paléo-hébreu + hébreu carré)
  {{S01_LIVRES}}       les cinq livres de la Torah (cartes à retourner)
  {{S01_ALPHABET}}     de l'image à la lettre : proto-sinaïtique → paléo-hébreu → hébreu → latin
  {{S01_TR_KETEF}} / {{S01_TR_MOISE}}  transcriptions des narrations
Le tétragramme יהוה est toujours rendu « Jéhovah ».
"""
import html
import re
import unicodedata

e = html.escape

# --------------------------------------------------------------------------
# Hébreu carré → paléo-hébreu (bloc Unicode « phénicien », U+10900)
# --------------------------------------------------------------------------
PALEO = {
    "א": "\U00010900", "ב": "\U00010901", "ג": "\U00010902", "ד": "\U00010903", "ה": "\U00010904",
    "ו": "\U00010905", "ז": "\U00010906", "ח": "\U00010907", "ט": "\U00010908", "י": "\U00010909",
    "כ": "\U0001090A", "ך": "\U0001090A", "ל": "\U0001090B", "מ": "\U0001090C", "ם": "\U0001090C",
    "נ": "\U0001090D", "ן": "\U0001090D", "ס": "\U0001090E", "ע": "\U0001090F", "פ": "\U00010910",
    "ף": "\U00010910", "צ": "\U00010911", "ץ": "\U00010911", "ק": "\U00010912", "ר": "\U00010913",
    "ש": "\U00010914", "ת": "\U00010915",
}


def consonnes(mot):
    """Retire voyelles (niqqud) et accents : ne garde que les consonnes."""
    return "".join(c for c in unicodedata.normalize("NFD", mot) if "\u05d0" <= c <= "\u05ea")


def paleo(mot):
    return "".join(PALEO.get(c, c) for c in consonnes(mot))


# --------------------------------------------------------------------------
# Nombres 6:24-26 — (hébreu vocalisé, translittération, glose, présent sur KH2 ?)
# --------------------------------------------------------------------------
BENEDICTION = [
    ("6:24", "Que Jéhovah te bénisse et qu'il te garde.", [
        ("יְבָרֶכְךָ", "yevarekhekha", "qu'il te bénisse", True),
        ("יְהוָה", "YHWH", "Jéhovah", True),
        ("וְיִשְׁמְרֶךָ", "veyishmerekha", "et qu'il te garde", True),
    ]),
    ("6:25", "Que Jéhovah fasse briller sa face vers toi et qu'il te fasse grâce.", [
        ("יָאֵר", "yaʾer", "qu'il fasse briller", True),
        ("יְהוָה", "YHWH", "Jéhovah", True),
        ("פָּנָיו", "panav", "sa face", True),
        ("אֵלֶיךָ", "ʾeleikha", "vers toi", True),
        ("וִיחֻנֶּךָּ", "vikhunnekka", "et qu'il te fasse grâce", False),
    ]),
    ("6:26", "Que Jéhovah lève sa face vers toi et qu'il te donne la paix.", [
        ("יִשָּׂא", "yissaʾ", "qu'il lève", False),
        ("יְהוָה", "YHWH", "Jéhovah", False),
        ("פָּנָיו", "panav", "sa face", False),
        ("אֵלֶיךָ", "ʾeleikha", "vers toi", False),
        ("וְיָשֵׂם", "veyasem", "et qu'il place", True),
        ("לְךָ", "lekha", "pour toi", True),
        ("שָׁלוֹם", "shalom", "la paix", True),
    ]),
]


def benediction():
    out = []
    for ref, fr, mots in BENEDICTION:
        words = []
        for heb, tr, glose, kh in mots:
            tetra = " is-tetra" if tr == "YHWH" else ""
            khc = " is-kh" if kh else ""
            words.append(
                f'<span class="w{tetra}{khc}" tabindex="0" data-gloss="{e(glose)}">'
                f'<span class="w-paleo" lang="hbo-Phnx">{paleo(heb)}</span>'
                f'<span class="w-heb" lang="he">{heb}</span>'
                f'<span class="w-tr" lang="hbo-Latn">{e(tr)}</span>'
                f'<span class="w-fr">{e(glose)}</span></span>')
        out.append(f"""
          <div class="verset" data-reveal>
            <span class="v-ref">Nombres {ref}</span>
            <p class="v-line">{''.join(words)}</p>
            <p class="v-fr">« {e(fr)} »</p>
          </div>""")
    return "".join(out)


# --------------------------------------------------------------------------
# KH2 — lecture restituée (Barkay et al., BASOR 2004). Crochets = lettres restituées
# --------------------------------------------------------------------------
KH2 = "יברך יהוה ישמרך יאר יהוה פניו [אל]יך וישם לך ש[ל]ם"


def kh2():
    def conv(s, fn):
        return re.sub(r"[^\[\] ]+", lambda m: fn(m.group(0)), s)
    pal = conv(KH2, paleo)
    return (f'<p class="kh-paleo" lang="hbo-Phnx" dir="rtl">{pal}</p>'
            f'<p class="kh-heb" lang="he" dir="rtl">{KH2}</p>')


# --------------------------------------------------------------------------
# Les cinq livres de la Torah
# --------------------------------------------------------------------------
LIVRES = [
    ("בְּרֵאשִׁית", "Bereshit", "Au commencement", "Genèse", "50",
     "De la création à la mort de Joseph en Égypte : les origines du monde, le déluge, puis Abraham, Isaac, Jacob et ses douze fils."),
    ("שְׁמוֹת", "Shemot", "Noms", "Exode", "40",
     "L'esclavage en Égypte, la vocation de Moïse, la sortie d'Égypte, l'alliance au Sinaï, les Dix Paroles et la construction du tabernacle."),
    ("וַיִּקְרָא", "Vayiqra", "Et il appela", "Lévitique", "27",
     "Le manuel des prêtres : sacrifices, pureté, fêtes annuelles et appel à la sainteté. « Tu aimeras ton prochain comme toi-même » (19:18)."),
    ("בְּמִדְבַּר", "Bemidbar", "Dans le désert", "Nombres", "36",
     "Recensements et quarante ans d'errance dans le désert. C'est ici que se trouve la bénédiction sacerdotale gravée sur les amulettes (6:24-26)."),
    ("דְּבָרִים", "Devarim", "Paroles", "Deutéronome", "34",
     "Les derniers discours de Moïse dans les plaines de Moab, le rappel de la Loi, le « Shema Israël » (6:4) et la mort de Moïse."),
]


def livres():
    out = []
    for i, (heb, tr, sens, fr, ch, resume) in enumerate(LIVRES, 1):
        out.append(f"""
        <div class="flip" data-reveal>
          <button class="flip-inner" type="button" aria-label="Retourner la carte : {e(fr)}" aria-pressed="false">
            <span class="flip-face flip-front">
              <span class="fl-num">Livre {i}</span>
              <span class="fl-heb" lang="he">{heb}</span>
              <span class="fl-tr">{e(tr)} · « {e(sens)} »</span>
              <span class="fl-fr">{e(fr)}</span>
              <span class="fl-hint">Retourner</span>
            </span>
            <span class="flip-face flip-back">
              <span class="fl-fr">{e(fr)}</span>
              <span class="fl-meta">{ch} chapitres · en hébreu <i>{e(tr)}</i>, « {e(sens)} »</span>
              <span class="fl-resume">{e(resume)}</span>
            </span>
          </button>
        </div>""")
    return "".join(out)


# --------------------------------------------------------------------------
# De l'image à la lettre (pictogrammes proto-sinaïtiques dessinés en SVG)
# --------------------------------------------------------------------------
_SVG = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ALPHABET = [
    ("ʾalef", "bœuf", '<path d="M7 9c0-4 6-5 7 1h12c1-6 7-5 7-1"/><path d="M14 10c-2 7 0 16 6 21 6-5 8-14 6-21"/><circle cx="17" cy="18" r=".8" fill="currentColor"/><circle cx="23" cy="18" r=".8" fill="currentColor"/>', "א", "A"),
    ("bet", "maison", '<path d="M22 31h10V9H8v22h8v-8"/>', "ב", "B"),
    ("mem", "eau", '<path d="M4 15l5-5 5 5 5-5 5 5 5-5 5 5"/><path d="M4 28l5-5 5 5 5-5 5 5 5-5 5 5"/>', "מ", "M"),
    ("ʿayin", "œil", '<path d="M4 20c6-9 26-9 32 0-6 9-26 9-32 0z"/><circle cx="20" cy="20" r="4.5"/>', "ע", "O"),
    ("resh", "tête", '<path d="M24 7c-8-2-15 3-15 11 0 6 4 10 9 11v5"/><path d="M24 7c3 1 4 4 4 7l3 4-3 1c0 3-1 6-5 6h-2"/><circle cx="23" cy="14" r=".9" fill="currentColor"/>', "ר", "R"),
    ("shin", "dent", '<path d="M5 11c3 17 10 19 15 5 5 14 12 12 15-5"/>', "ש", "S"),
]


def alphabet():
    out = []
    for nom, sens, svg, heb, lat in ALPHABET:
        out.append(f"""
          <li class="ab-row" data-reveal>
            <span class="ab-cell ab-proto" title="Pictogramme proto-sinaïtique">{_SVG.format(svg)}</span>
            <span class="ab-cell ab-paleo" lang="hbo-Phnx">{PALEO[heb]}</span>
            <span class="ab-cell ab-heb" lang="he">{heb}</span>
            <span class="ab-cell ab-lat">{lat}</span>
            <span class="ab-name"><b>{e(nom)}</b> « {e(sens)} »</span>
          </li>""")
    return "".join(out)


# --------------------------------------------------------------------------
# Transcriptions des narrations
# --------------------------------------------------------------------------
TR_KETEF = [
    "Jérusalem, été 1979. Sur le flanc de la vallée de Hinnom, l'archéologue Gabriel Barkay fouille d'anciennes tombes creusées dans le calcaire, au temps des rois de Juda. Un jeune volontaire de treize ans, en dégageant le sol d'une chambre funéraire, perce par hasard le plafond d'une cavité oubliée : une fosse où l'on déposait autrefois les ossements et les objets des défunts. Les pilleurs ne l'ont jamais trouvée.",
    "Elle contient plus de mille objets : poteries, bijoux, pointes de flèches… et deux minuscules rouleaux d'argent, à peine plus grands qu'un ongle. Les dérouler sans les briser prendra trois ans. Sur la feuille de métal, plus fine que du papier, apparaissent alors des lettres gravées à la pointe, dans l'ancienne écriture paléo-hébraïque.",
    "Et le texte est reconnaissable entre tous. C'est la bénédiction que les prêtres prononçaient sur le peuple, au livre des Nombres, chapitre six : « Que Jéhovah te bénisse et te garde. Que Jéhovah fasse briller sa face vers toi… et qu'il te donne la paix. »",
    "Ces amulettes datent de la fin du VIIe ou du début du VIe siècle avant notre ère, peu avant la destruction de Jérusalem par Babylone. Elles sont donc plus anciennes d'environ quatre siècles que les plus anciens manuscrits de la mer Morte. En 2004, une nouvelle étude, menée avec des techniques d'imagerie de pointe, a confirmé cette datation et révélé des lettres jusque-là invisibles.",
    "Deux petits rouleaux d'argent, portés autour du cou par des habitants de Jérusalem il y a plus de deux mille six cents ans, et qui portent le nom divin, Jéhovah : c'est, à ce jour, le plus ancien témoin connu d'un texte biblique.",
]
TR_MOISE = [
    "« Moïse écrivit toutes les paroles de Jéhovah. » C'est ainsi que le livre de l'Exode, au chapitre 24, décrit la naissance de l'Écriture. Selon la Bible, Moïse a consigné par écrit la loi, les récits et les étapes du voyage d'Israël dans le désert, et la tradition juive comme la tradition chrétienne lui attribuent les cinq premiers livres de la Bible : la Torah, ou Pentateuque.",
    "Moïse, selon le récit biblique, a grandi à la cour d'Égypte. Or l'Égypte de cette époque est un monde de l'écrit : des scribes y rédigent des archives, des lettres et des hymnes, sur papyrus et sur pierre. Dans tout le Proche-Orient, l'écriture cunéiforme sert depuis des siècles à la diplomatie. Et dans les mines de turquoise du Sinaï, à Sérabit el-Khadim, des ouvriers sémites ont gravé, dès le IIe millénaire avant notre ère, quelques-unes des plus anciennes inscriptions alphabétiques connues : l'ancêtre lointain de l'alphabet hébreu… et du nôtre.",
    "Les historiens débattent de la date et de la manière dont la Torah a été rédigée. La tradition situe Moïse vers le XVe siècle avant notre ère ; beaucoup de spécialistes de la critique historique pensent que le texte a été mis en forme bien plus tard, à partir de sources plus anciennes. Ce musée vous présente ces deux lectures, avec les pièces du dossier.",
    "Car certaines pièces parlent d'elles-mêmes. Vers 1208 avant notre ère, le pharaon Merneptah fait graver sur une stèle de granit le récit de ses victoires. Parmi les peuples vaincus figure un nom : Israël. C'est la plus ancienne mention connue d'Israël en dehors de la Bible, et elle montre qu'un peuple de ce nom vivait déjà en Canaan.",
    "D'autres rapprochements, souvent cités, sont plus fragiles : les tablettes d'Ébla, en Syrie, ou le papyrus égyptien d'Ipouer, dont les lamentations évoquent un fleuve changé en sang. Nous les exposons aussi, avec les réserves des spécialistes.",
    "Ainsi commence notre parcours : avec un homme, des tables de pierre, et une parole mise par écrit pour être transmise. Plus de trois mille ans plus tard, elle est toujours lue.",
]


def _tr(paras):
    return "".join(f"<p>{e(p)}</p>" for p in paras)


def render(page):
    rep = {
        "{{S01_BENEDICTION}}": benediction(),
        "{{S01_KH2}}": kh2(),
        "{{S01_LIVRES}}": livres(),
        "{{S01_ALPHABET}}": alphabet(),
        "{{S01_TR_KETEF}}": _tr(TR_KETEF),
        "{{S01_TR_MOISE}}": _tr(TR_MOISE),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    return page
