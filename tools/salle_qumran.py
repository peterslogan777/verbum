"""
VERBUM — Salle 03 « Les Manuscrits de la mer Morte » (étape E05, salle phare)
Marqueurs remplacés dans tools/templates/salles/qumran.html :
  {{S03_GROTTES_SVG}} / {{S03_GROTTES_PANELS}}  plan schématique des 11 grottes + fiches
  {{S03_COMPARATEUR}}   comparateur Qumrân · texte massorétique · traduction
  {{S03_FRISE}}         frise chronologique (de l'installation du site à 2021)
  {{S03_VIEWER_JSON}}   données du visualiseur 3D (colonnes ↔ versets, traduction)
  {{S03_ESAIE53}}       Ésaïe 53 intégral (hébreu consonantique + traduction française)
  {{S03_TR_DECOUVERTE}} / {{S03_TR_ESAIE}}  transcriptions des narrations
Le tétragramme יהוה est toujours rendu « Jéhovah ».
"""
import html
import json
from pathlib import Path

e = html.escape
ROOT = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT / "tools"))
from textures import VERSETS  # Ésaïe 53, texte consonantique (voyelles et accents retirés)  # noqa: E402

ESAIE53_FR = [
    "Qui a cru à ce que nous avons entendu ? Et à qui le bras de Jéhovah a-t-il été révélé ?",
    "Il a grandi devant lui comme une jeune pousse, comme une racine sortant d'une terre desséchée ; il n'avait ni belle apparence ni éclat pour attirer nos regards, ni aspect pour nous plaire.",
    "Il était méprisé et abandonné des hommes, homme de douleurs, familier de la souffrance ; semblable à celui devant qui l'on se voile la face, il était méprisé, et nous n'avons fait de lui aucun cas.",
    "Pourtant, ce sont nos souffrances qu'il a portées, ce sont nos douleurs dont il s'est chargé ; et nous, nous l'avons considéré comme frappé, battu par Dieu et humilié.",
    "Mais il a été transpercé à cause de nos transgressions, écrasé à cause de nos fautes ; le châtiment qui nous donne la paix est tombé sur lui, et c'est par ses blessures que nous sommes guéris.",
    "Nous étions tous errants comme des brebis, chacun suivait sa propre voie ; et Jéhovah a fait retomber sur lui la faute de nous tous.",
    "Il a été maltraité, il s'est humilié et n'a pas ouvert la bouche ; comme un agneau qu'on mène à l'abattoir, comme une brebis muette devant ceux qui la tondent, il n'a pas ouvert la bouche.",
    "Par l'oppression et le jugement il a été emporté ; et parmi ses contemporains, qui s'en est soucié ? Il a été retranché de la terre des vivants, frappé à cause de la transgression de mon peuple.",
    "On a placé sa tombe avec les méchants, et avec le riche dans sa mort, bien qu'il n'ait commis aucune violence et qu'il n'y ait eu aucune tromperie dans sa bouche.",
    "Il a plu à Jéhovah de l'écraser par la souffrance. Si tu fais de sa vie un sacrifice de réparation, il verra une descendance, il prolongera ses jours, et la volonté de Jéhovah réussira par sa main.",
    "À cause de la peine de son âme, il verra et sera rassasié. Par sa connaissance, le juste, mon serviteur, rendra justes beaucoup de gens, et c'est lui qui portera leurs fautes.",
    "C'est pourquoi je lui donnerai sa part parmi les grands ; il partagera le butin avec les puissants, parce qu'il s'est livré lui-même à la mort et qu'il a été compté parmi les transgresseurs ; il a porté le péché de beaucoup et il intercède pour les transgresseurs.",
]


def _jeh(heb):
    return heb.replace("יהוה", '<span class="tetragramme" title="Le nom divin, rendu « Jéhovah »">יהוה</span>')


def esaie53():
    rows = []
    for i, (h, f) in enumerate(zip(VERSETS, ESAIE53_FR), 1):
        rows.append(f'<li><span class="e53-n">{i}</span><p class="e53-he" lang="he" dir="rtl">{_jeh(h)}</p><p class="e53-fr">{e(f)}</p></li>')
    return '<ol class="e53">' + "".join(rows) + "</ol>"


def viewer_json():
    cols = json.loads((ROOT / "tools/data/rouleau_colonnes.json").read_text(encoding="utf-8"))
    return json.dumps({"colonnes": cols, "fr": ESAIE53_FR}, ensure_ascii=False).replace("</", "<\\/")


# --------------------------------------------------------------------------
# Plan schématique des grottes (nord en haut ; distances non à l'échelle)
# --------------------------------------------------------------------------
GROTTES = [
    # n, x, y, année, découvreurs, titre, contenu, chiffre
    (1, 318, 170, "1947", "Bergers bédouins · fouillée en 1949", "La grotte des sept rouleaux",
     "Le Grand Rouleau d'Ésaïe (1QIsaᵃ), un second Ésaïe (1QIsaᵇ), la Règle de la communauté, le Rouleau de la Guerre, les Hymnes, le Commentaire (pesher) d'Habacuc et l'Apocryphe de la Genèse.",
     "7 grands rouleaux et de nombreux fragments"),
    (2, 300, 205, "1952", "Bergers bédouins", "Une poignée de livres",
     "Fragments d'Exode, de Jérémie, de Ruth, des Psaumes, du Livre des Jubilés…", "≈ 33 manuscrits fragmentaires"),
    (3, 262, 64, "1952", "Archéologues (École biblique et ASOR)", "Le Rouleau de cuivre",
     "Une liste de trésors cachés, gravée sur des feuilles de cuivre (3Q15) : un document unique, toujours énigmatique.", "≈ 15 manuscrits"),
    (4, 440, 392, "1952", "Bergers bédouins, puis archéologues", "Le trésor des trésors",
     "Creusée dans la terrasse de marne, face au site. Elle a livré des fragments de presque tous les livres bibliques, et de nombreux écrits non bibliques.",
     "≈ 15 000 fragments, plus de 500 manuscrits"),
    (5, 424, 364, "1952", "Archéologues", "Voisine de la grotte 4",
     "Fragments de Deutéronome, des Rois, d'Ésaïe, des Psaumes, de Lamentations…", "≈ 25 manuscrits"),
    (6, 352, 410, "1952", "Bergers bédouins", "La grotte des papyrus",
     "Ouverte au pied de la falaise, dans le ravin du Qumrân. Plusieurs textes sur papyrus, dont un fragment de Daniel.", "≈ 30 manuscrits"),
    (7, 506, 404, "1955", "Archéologues", "Une grotte grecque",
     "Uniquement des papyrus en grec, dont un fragment d'Exode (7Q1) et de la Lettre de Jérémie (7Q2).", "19 fragments grecs"),
    (8, 522, 412, "1955", "Archéologues", "Phylactères et mezouza",
     "Fragments de Genèse et des Psaumes, un phylactère et une mezouza.", "5 manuscrits"),
    (9, 538, 404, "1955", "Archéologues", "Un seul témoin",
     "Un unique petit fragment de papyrus.", "1 fragment"),
    (10, 456, 410, "1955", "Archéologues", "Un tesson inscrit",
     "Un ostracon (tesson de poterie portant quelques lettres).", "1 ostracon"),
    (11, 292, 100, "1956", "Bergers bédouins", "La dernière grande grotte",
     "Le Rouleau du Temple (11Q19), le grand Rouleau des Psaumes (11QPsᵃ), un Targum araméen de Job et un Lévitique écrit en paléo-hébreu.",
     "≈ 30 manuscrits"),
]


def grottes():
    falaise = ("M210 0 C 250 60 230 120 270 190 C 300 250 280 320 320 380 C 335 410 330 470 360 560 "
               "L 140 560 L 140 0 Z")
    terrasse = "M330 300 C 380 320 440 340 520 360 C 560 372 580 395 560 430 C 520 450 420 440 360 425 C 330 400 320 340 330 300 Z"
    mer = "M640 0 C 615 80 650 150 625 230 C 605 300 640 380 618 450 C 605 500 620 540 610 560 L 800 560 L 800 0 Z"
    svg = [f'<svg class="gr-svg" viewBox="120 0 680 560" role="img" aria-labelledby="gr-svg-t">'
           '<title id="gr-svg-t">Plan schématique des onze grottes de Qumrân autour du site de Khirbet Qumrân et de la mer Morte</title>'
           '<defs><linearGradient id="grMer" x1="0" x2="1"><stop offset="0" stop-color="#16364a"/><stop offset="1" stop-color="#0d2233"/></linearGradient>'
           '<pattern id="grHach" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="8" stroke="rgba(201,168,76,.14)" stroke-width="2"/></pattern></defs>'
           f'<rect x="120" y="0" width="680" height="560" fill="#15120d"/>'
           f'<path d="{falaise}" fill="url(#grHach)" stroke="rgba(201,168,76,.35)"/>'
           f'<path d="{terrasse}" fill="rgba(201,168,76,.07)" stroke="rgba(201,168,76,.22)" stroke-dasharray="4 4"/>'
           f'<path d="{mer}" fill="url(#grMer)"/>'
           '<path class="gr-wadi" d="M140 455 C 230 440 300 420 360 425 C 430 432 520 450 618 455" />'
           '<text class="gr-lab" x="700" y="270" text-anchor="middle">Mer Morte</text>'
           '<text class="gr-lab sm" x="200" y="300" transform="rotate(-72 200 300)">Falaises calcaires</text>'
           '<text class="gr-lab sm" x="470" y="470">Ravin (ouadi) du Qumrân</text>'
           '<g class="gr-site"><rect x="462" y="356" width="30" height="22" rx="2"/><text x="477" y="348" text-anchor="middle">Khirbet Qumrân</text></g>'
           '<g class="gr-nord" transform="translate(770 40)"><path d="M0 -16 L6 6 L0 2 L-6 6 Z"/><text y="22" text-anchor="middle">N</text></g>']
    panels = []
    for n, x, y, an, qui, titre, contenu, chiffre in GROTTES:
        svg.append(f'<g class="gr-pt{" is-major" if n in (1, 4, 11) else ""}" data-g="{n}" tabindex="0" role="button" aria-label="Grotte {n} : {e(titre)}">'
                   f'<circle class="halo" cx="{x}" cy="{y}" r="15"/><circle class="core" cx="{x}" cy="{y}" r="10"/>'
                   f'<text x="{x}" y="{y + 4}" text-anchor="middle">{n}</text></g>')
        panels.append(f'<article class="gr-panel" data-g="{n}"{"" if n == 1 else " hidden"}>'
                      f'<p class="gr-k">Grotte {n} · découverte en {an}</p><h4>{e(titre)}</h4>'
                      f'<p class="gr-qui">{e(qui)}</p><p>{e(contenu)}</p><p class="gr-chiffre">{e(chiffre)}</p></article>')
    svg.append("</svg>")
    return "".join(svg), "".join(panels)


# --------------------------------------------------------------------------
# Comparateur : Qumrân · texte massorétique · traduction
# --------------------------------------------------------------------------
COMP = [
    dict(id="e53", ref="Ésaïe 53:11", ms="1QIsaᵃ (aussi 1QIsaᵇ et 4QIsaᵈ)", type="Un mot en plus",
         q='מעמל נפשו<mark title="orthographe : ה final ajouté">ה</mark> יראה <mark class="mk-sens" title="mot ajouté : « lumière »">אור</mark> <mark title="conjonction « et »">ו</mark>ישבע',
         tm="מעמל נפשו יראה ישבע",
         qfr="« À cause de la peine de son âme, il verra <b>la lumière</b> et sera rassasié. »",
         tmfr="« À cause de la peine de son âme, il verra et sera rassasié. »",
         note="Trois manuscrits de Qumrân ajoutent le mot <i>or</i> (<span lang=\"he\">אור</span>, « lumière »), tout comme la Septante grecque (<span lang=\"el\">φῶς</span>, « lumière »). Plusieurs traductions modernes l'ont adopté. Le sens du verset reste le même : après sa souffrance, le serviteur voit l'issue heureuse de son œuvre."),
    dict(id="ps145", ref="Psaume 145:13", ms="11QPsᵃ (grotte 11)", type="Un verset retrouvé",
         q='<mark class="mk-sens" title="verset absent du texte massorétique">נאמן אלוהים בדבריו וחסיד בכול מעשיו</mark>',
         tm='<span class="cmp-vide">— verset absent —</span>',
         qfr="« Dieu est fidèle dans ses paroles, et bienveillant dans toutes ses œuvres. »",
         tmfr="Le psaume est un acrostiche : chaque verset commence par la lettre suivante de l'alphabet. Dans le texte massorétique, la ligne de la lettre <b>noun</b> (<span lang=\"he\">נ</span>) manque.",
         note="Le rouleau des Psaumes de la grotte 11 contient la ligne en <span lang=\"he\">נ</span> (<i>ne'eman</i>, « fidèle »), déjà connue par la Septante. Le texte de Qumrân confirme ici une ligne que la tradition grecque avait conservée. Aucun enseignement n'en dépend, mais l'acrostiche retrouve sa lettre manquante."),
    dict(id="dt32", ref="Deutéronome 32:8", ms="4QDeutʲ (grotte 4)", type="Une leçon différente",
         q='למספר בני <mark class="mk-sens" title="« fils de Dieu »">אלוהים</mark>',
         tm='למספר בני <mark class="mk-sens" title="« fils d\'Israël »">ישראל</mark>',
         qfr="« … selon le nombre des <b>fils de Dieu</b>. »",
         tmfr="« … selon le nombre des <b>fils d'Israël</b>. »",
         note="C'est l'un des rares écarts où le sens change réellement. La lecture de Qumrân rejoint celle de la Septante (« anges de Dieu »). Les spécialistes en débattent encore : c'est précisément parce que ces différences sont rares qu'elles sont si bien connues et si soigneusement étudiées."),
    dict(id="ortho", ref="L'orthographe de Qumrân", ms="1QIsaᵃ et de nombreux rouleaux", type="Même mot, autre graphie",
         q='כי<mark>א</mark> · ל<mark>ו</mark>א · כ<mark>ו</mark>ל · הוא<mark>ה</mark> · נפשו<mark>ה</mark>',
         tm="כי · לא · כל · הוא · נפשו",
         qfr="« car » · « ne… pas » · « tout » · « lui » · « son âme »",
         tmfr="« car » · « ne… pas » · « tout » · « lui » · « son âme »",
         note="L'immense majorité des différences ressemble à cela : le scribe de Qumrân ajoute des lettres (<span lang=\"he\">א ו ה י</span>) pour aider à prononcer les voyelles. On parle d'<b>orthographe pleine</b>. Le mot, et donc le sens, ne changent pas, comme « clef » et « clé » en français."),
]


def comparateur():
    tabs, panels = [], []
    for i, c in enumerate(COMP):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button type="button" role="tab" id="cmp-t-{c["id"]}" aria-controls="cmp-p-{c["id"]}" aria-selected="{sel}"'
                    f'{"" if i == 0 else " tabindex=\"-1\""}><b>{e(c["ref"])}</b><small>{e(c["type"])}</small></button>')
        panels.append(f"""
      <div class="cmp-panel" role="tabpanel" id="cmp-p-{c['id']}" aria-labelledby="cmp-t-{c['id']}"{'' if i == 0 else ' hidden'}>
        <div class="cmp-cols">
          <div class="cmp-col is-q"><p class="cmp-k">Qumrân · {e(c['ms'])}</p><p class="cmp-he" lang="he" dir="rtl">{c['q']}</p><p class="cmp-fr">{c['qfr']}</p></div>
          <div class="cmp-col is-tm"><p class="cmp-k">Texte massorétique · Codex de Leningrad (1008)</p><p class="cmp-he" lang="he" dir="rtl">{c['tm']}</p><p class="cmp-fr">{c['tmfr']}</p></div>
        </div>
        <p class="cmp-note"><span class="badge {'badge-debat' if c['id'] == 'dt32' else 'badge-preuve'}">{e(c['type'])}</span> {c['note']}</p>
      </div>""")
    return (f'<div class="cmp-tabs" role="tablist" aria-label="Passages à comparer">{"".join(tabs)}</div>'
            f'<div class="cmp-panels">{"".join(panels)}</div>')


# --------------------------------------------------------------------------
# Frise chronologique
# --------------------------------------------------------------------------
FRISE = [
    ("IIe – Ier s. av. J.-C.", "Un site au bord du désert", "Une communauté s'installe à Khirbet Qumrân. Les spécialistes l'identifient le plus souvent aux Esséniens décrits par Flavius Josèphe et Pline l'Ancien.", "antique"),
    ("≈ 125 av. J.-C.", "Copie du Grand Rouleau d'Ésaïe", "Datation par l'écriture, confirmée par le radiocarbone.", "antique"),
    ("31 av. J.-C.", "Un tremblement de terre", "Les fouilles en ont relevé les traces sur le site.", "antique"),
    ("68 ap. J.-C.", "Les rouleaux sont cachés", "Pendant la guerre contre Rome, le site est détruit par l'armée romaine. Les manuscrits dorment dans les grottes.", "antique"),
    ("Hiver 1946 – 1947", "La pierre du berger", "Muhammad edh-Dhib découvre la grotte 1 et ses jarres.", "moderne"),
    ("29 novembre 1947", "Premier achat", "Eleazar Sukenik, de l'Université hébraïque, acquiert trois rouleaux.", "moderne"),
    ("1949 – 1956", "La course aux grottes", "Roland de Vaux et Gerald Lankester Harding fouillent la grotte 1 puis le site ; bédouins et archéologues explorent les grottes 2 à 11.", "moderne"),
    ("1954", "Une petite annonce", "Quatre rouleaux sont proposés à la vente dans le Wall Street Journal ; Yigael Yadin les fait acheter pour Israël.", "moderne"),
    ("1965", "Le Sanctuaire du Livre", "Le pavillon du musée d'Israël, à Jérusalem, accueille le Grand Rouleau d'Ésaïe.", "moderne"),
    ("1967", "Le Rouleau du Temple", "Yigael Yadin récupère le plus long des rouleaux (8,15 m).", "moderne"),
    ("1991", "Accès libre", "Les photographies de tous les rouleaux deviennent accessibles aux chercheurs du monde entier.", "moderne"),
    ("2011 – 2012", "Les rouleaux en ligne", "Le musée d'Israël, puis la bibliothèque numérique Leon Levy, publient des images haute définition.", "numerique"),
    ("2017", "Une « grotte 12 »", "Des archéologues identifient une nouvelle grotte, pillée : jarres vides et fragment vierge.", "numerique"),
    ("2021", "Nouveaux fragments", "Des fragments grecs des Petits Prophètes (Zacharie, Nahum) sont retrouvés dans la « grotte de l'Horreur », plus au sud.", "numerique"),
]


def frise():
    out = []
    for i, (date, titre, txt, era) in enumerate(FRISE):
        out.append(f'<li class="qf-item is-{era}" data-reveal style="--d:{(i % 4) * 60}ms"><span class="qf-date">{e(date)}</span>'
                   f'<h4>{e(titre)}</h4><p>{e(txt)}</p></li>')
    return "".join(out)


TR_DECOUVERTE = """<p>Hiver 1946-1947. Sur les falaises qui dominent la rive nord-ouest de la mer Morte, un jeune berger bédouin de la tribu des Ta'amireh, Muhammad edh-Dhib, cherche une chèvre égarée. Il lance une pierre dans une ouverture étroite de la roche… et entend un bruit de poterie brisée. À l'intérieur : de hautes jarres d'argile. Dans l'une d'elles, des rouleaux de cuir enveloppés de lin. Sept manuscrits sortent ainsi de l'ombre, après près de deux mille ans de silence. Parmi eux, un rouleau long de plus de sept mètres : le livre entier du prophète Ésaïe.</p>
<p>Le 29 novembre 1947, le jour même où l'ONU vote le partage de la Palestine, le professeur Eleazar Sukenik achète trois de ces rouleaux. Les quatre autres seront acquis en 1954 par son fils, Yigael Yadin. Puis commence une véritable course aux grottes : entre 1949 et 1956, bédouins et archéologues explorent onze cavités. La grotte 4, à elle seule, livre des milliers de fragments. Au total, environ neuf cent cinquante manuscrits, dont plus de deux cent trente copies de livres bibliques. Tous les livres de la Bible hébraïque y sont représentés, à l'exception d'Esther. Pour la première fois, on pouvait tenir entre ses mains le texte de l'Écriture tel qu'on le lisait avant notre ère.</p>"""

TR_ESAIE = """<p>Avant 1947, les plus anciens manuscrits hébreux complets du livre d'Ésaïe dataient du dixième siècle de notre ère : le Codex d'Alep, puis le Codex de Leningrad. Entre le prophète et ces codex, plus de quinze siècles de copies successives. Beaucoup se demandaient : le texte avait-il dérivé, comme une rumeur que l'on se transmet de bouche à oreille ? Le Grand Rouleau d'Ésaïe a apporté la réponse. Copié vers 125 avant notre ère, sur dix-sept feuilles de parchemin cousues bout à bout, il contient les soixante-six chapitres du livre, en cinquante-quatre colonnes.</p>
<p>Placé à côté du texte massorétique, plus jeune de mille ans, il concorde dans l'immense majorité des versets. La plupart des écarts tiennent à l'orthographe : le scribe de Qumrân ajoute volontiers des lettres pour indiquer les voyelles. Quelques différences touchent le sens, comme au chapitre 53, verset 11, où le rouleau lit : « il verra la lumière », une leçon que l'on retrouve aussi dans la Septante. Mais aucune ne modifie un enseignement. Comme l'écrit le prophète lui-même : l'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours.</p>"""


def render(inner):
    svg, panels = grottes()
    rep = {
        "{{S03_GROTTES_SVG}}": svg, "{{S03_GROTTES_PANELS}}": panels,
        "{{S03_COMPARATEUR}}": comparateur(), "{{S03_FRISE}}": frise(),
        "{{S03_VIEWER_JSON}}": viewer_json(), "{{S03_ESAIE53}}": esaie53(),
        "{{S03_TR_DECOUVERTE}}": TR_DECOUVERTE, "{{S03_TR_ESAIE}}": TR_ESAIE,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S03_GROTTES_SVG}}{{S03_COMPARATEUR}}{{S03_FRISE}}{{S03_VIEWER_JSON}}{{S03_ESAIE53}}")
    print(len(out), "{{" in out)
