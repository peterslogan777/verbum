"""
VERBUM — Salle 10 « Le Livre indestructible » (étape E12)
Marqueurs remplacés dans tools/templates/salles/indestructible.html :
  {{S10_CIRTA}}       procès-verbal de Cirta (19 mai 303), extraits
  {{S10_BUCHER}}      page du Nouveau Testament de Tyndale (1526) à livrer au feu + Grande Bible (1539)
  {{S10_INTERDITS}}   frise de cartes recto/verso « tentative / ce qui a suivi »
  {{S10_ROUTES}}      routes clandestines : boutons + données JSON pour la carte (canvas)
  {{S10_QUIZ}}        « Vrai ou légende ? »
  {{S10_TR_A}} / {{S10_TR_B}}   transcriptions des narrations
  {{IMG_*}}           images de la salle (assets/img/salles/10)
Données géographiques : assets/js/salle10-geo.js (Natural Earth 110 m, domaine public).

Règles VERBUM appliquées : tout texte étranger (latin, anglais ancien, hébreu, grec) est suivi de sa
traduction française ; le tétragramme est rendu « Jéhovah » ; aucune croix, ni dans les images ni dans
le décor ; les récits invérifiables sont signalés comme légendes.
"""
import html
import json

e = html.escape


def img(name, alt, caption, sizes="(max-width: 1000px) 100vw, 50vw", root="{{ROOT}}", extra=""):
    p = f"{root}assets/img/salles/10/{name}"
    return (f'<img src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" data-lightbox data-full="{p}.jpg" data-caption="{e(caption)}"{extra}>')


# --------------------------------------------------------------------------
# I. Cirta, 19 mai 303 — procès-verbal (Gesta apud Zenophilum)
# --------------------------------------------------------------------------
CIRTA = [
    ("Félix, curateur de la cité", "Apportez les Écritures de la loi, et tout ce que vous avez ici, comme il a été ordonné, afin d'obéir à l'édit."),
    ("Paul, évêque", "Les Écritures, ce sont les lecteurs qui les ont. Nous, nous vous donnons ce que nous avons ici."),
    ("Félix", "Montrez-nous les lecteurs, ou envoyez quelqu'un les chercher."),
    ("Paul", "Vous les connaissez tous."),
    ("Le greffier", "On se rend ensuite chez les lecteurs, maison après maison. L'un d'eux remet quatre volumes, un autre cinq, un autre huit…"),
]


def cirta():
    rows = "".join(f'<li><b>{e(w)}</b><span>« {e(t)} »</span></li>' if w != "Le greffier"
                   else f'<li class="ci-note"><b>{e(w)}</b><span>{e(t)}</span></li>' for w, t in CIRTA)
    return f"""
    <ol class="ci-pv">{rows}</ol>"""


# --------------------------------------------------------------------------
# II. Le bûcher interactif — Jean 1:1-5
# --------------------------------------------------------------------------
TYNDALE = ("In the begynnynge was that worde, and that worde was with god: and god was thatt worde. "
           "The same was in the begynnynge wyth god. All thynges were made by it, and with out it, was made "
           "nothinge, that was made. In it was lyfe, and lyfe was the lyght of men, and the lyght shyneth in "
           "the darcknes, and the darcknes comprehended it not.")
GRANDE = ("In the begynnynge was the worde, and the worde was wyth God: and God was the worde. The same was in "
          "the begynnynge wyth God. All thinges were made by it, and wythout it was made nothynge that was made. "
          "In it was lyfe, and the lyfe was the lyght of men, and the lyght shyneth in darcknes, and the darcknes "
          "comprehended it not.")
FR_JEAN = ("« Au commencement était la Parole, et la Parole était avec Dieu, et la Parole était Dieu. Elle était "
           "au commencement avec Dieu. Toutes choses ont été faites par elle, et sans elle rien de ce qui a été fait "
           "n'a été fait. En elle était la vie, et la vie était la lumière des hommes ; la lumière brille dans les "
           "ténèbres, et les ténèbres ne l'ont pas saisie. »")


def bucher():
    data = json.dumps({"titre": "The Gospell of S. Jhon. The fyrst Chapter.", "texte": TYNDALE,
                       "pied": "Worms, Peter Schöffer, 1526"}, ensure_ascii=False)
    return f"""
    <div class="bu-scene">
      <div class="bu-under" aria-hidden="false">
        <p class="bu-u-k">Trois ans plus tard · 1539</p>
        <p class="bu-u-t">The Byble in Englyshe</p>
        <p class="bu-u-v" lang="en">{e(GRANDE)}</p>
        <p class="bu-u-f">La « Grande Bible », imprimée par ordre du roi Henri VIII pour toutes les églises d'Angleterre. Son Nouveau Testament reprend pour l'essentiel la traduction de Tyndale.</p>
      </div>
      <canvas class="bu-canvas" role="img" aria-label="Page du Nouveau Testament de Tyndale de 1526, évangile de Jean, chapitre 1. Le bouton permet de la livrer au feu."></canvas>
      <canvas class="bu-fx" aria-hidden="true"></canvas>
      <script type="application/json" id="bu-data">{data}</script>
    </div>
    <div class="bu-bar">
      <button type="button" class="btn btn-or bu-go">Livrer au feu (1526)</button>
      <button type="button" class="btn btn-ghost bu-reset" hidden>Recommencer</button>
      <span class="bu-msg" aria-live="polite">Londres, octobre 1526 : l'évêque de Londres fait brûler les exemplaires saisis.</span>
    </div>
    <details class="bu-trad" open>
      <summary>Traduction française du passage (Jean 1:1-5)</summary>
      <p class="bu-en" lang="en">{e(TYNDALE)}</p>
      <p>{e(FR_JEAN)}</p>
      <p class="bu-note">Orthographe anglaise du XVIe siècle, conservée telle quelle. <span class="badge badge-canon">Canonique</span></p>
    </details>"""


# --------------------------------------------------------------------------
# III. Interdire la Bible — cartes recto (tentative) / verso (suite)
# --------------------------------------------------------------------------
INTERDITS = [
    ("1229", "Toulouse", "Le concile de Toulouse",
     "Son canon 14 interdit aux laïcs de posséder les livres de l'Ancien et du Nouveau Testament, à l'exception du psautier et de quelques livres de prière, et proscrit toute traduction en langue courante.",
     "Les traductions continuent pourtant de circuler en langue d'oc et en français. En 1535, la Bible d'Olivétan, première Bible protestante française traduite sur l'hébreu et le grec, sort des presses de Serrières, près de Neuchâtel."),
    ("1408", "Oxford", "Les constitutions d'Oxford",
     "L'archevêque Thomas Arundel interdit de traduire ou de lire sans autorisation toute traduction anglaise de la Bible, visant la Bible des disciples de John Wycliffe, les « lollards ».",
     "Plus de 250 manuscrits de la Bible de Wycliffe nous sont parvenus : c'est le texte anglais médiéval le mieux conservé. On les recopiait en secret et on les lisait à voix basse, dans des granges ou des maisons."),
    ("1428", "Lutterworth", "Les os de Wycliffe",
     "Condamné à titre posthume par le concile de Constance (1415), John Wycliffe, mort en 1384, est exhumé 44 ans après sa mort. Ses os sont brûlés et ses cendres jetées dans la Swift, une petite rivière.",
     "Au XVIIe siècle, l'historien Thomas Fuller en tire une image restée célèbre : la Swift a porté les cendres à l'Avon, l'Avon à la Severn, la Severn à la mer, comme sa doctrine s'est répandue dans le monde entier."),
    ("1562", "Séville", "Reina brûlé en effigie",
     "Le moine Casiodoro de Reina a fui l'Espagne, où l'Inquisition interdit les Bibles en langue courante. Ne pouvant le saisir, le tribunal de Séville le fait brûler en effigie lors d'un autodafé.",
     "Sa traduction complète paraît à Bâle en 1569 : la « Bible de l'Ours », ainsi nommée pour sa gravure de titre. Révisée par Cipriano de Valera en 1602, la Reina-Valera reste aujourd'hui la Bible la plus lue du monde hispanophone."),
    ("1835", "Madagascar", "L'édit de Ranavalona Ire",
     "La reine interdit le christianisme le 1er mars 1835, l'année même où s'achève l'impression de la Bible en malgache. Les livres sont confisqués ; en 1837, une jeune femme, Rasalama, est exécutée pour sa foi.",
     "Pendant 26 ans, des croyants cachent leurs exemplaires, selon les récits de l'époque jusque dans des grottes, et les recopient. À la mort de la reine, en 1861, les chrétiens sortent de la clandestinité, bien plus nombreux qu'en 1835."),
    ("1967", "Albanie", "Le premier État athée",
     "Le régime d'Enver Hoxha ferme tous les lieux de culte du pays ; la Constitution de 1976 proclame un État athée. Posséder une Bible devient un crime.",
     "En 1990-1991, la liberté religieuse est rétablie. Des Bibles conservées en secret pendant un quart de siècle ressortent des cachettes ; de nouvelles traductions en albanien paraissent dans les années suivantes."),
]


def interdits():
    cards = []
    for i, (an, lieu, titre, recto, verso) in enumerate(INTERDITS):
        cards.append(f"""
      <li class="it-item" style="--i:{i}" data-reveal>
        <button type="button" class="it-card" aria-pressed="false" aria-label="{e(an)}, {e(titre)} : retourner la carte">
          <span class="it-in">
            <span class="it-f it-recto">
              <span class="it-y">{an}</span>
              <span class="it-l">{e(lieu)} · la tentative</span>
              <span class="it-t">{e(titre)}</span>
              <span class="it-p">{e(recto)}</span>
              <span class="it-hint">Retourner · ce qui a suivi</span>
            </span>
            <span class="it-f it-verso">
              <span class="it-l">Ce qui a suivi</span>
              <span class="it-p">{e(verso)}</span>
              <span class="it-hint">Revenir à la tentative</span>
            </span>
          </span>
        </button>
      </li>""")
    return f'<ol class="it-list">{"".join(cards)}\n    </ol>'


# --------------------------------------------------------------------------
# IV. Routes clandestines (carte)
# --------------------------------------------------------------------------
ROUTES = [
    ("tyndale", "1526", "Worms → Anvers → Londres", "Les Nouveaux Testaments de Tyndale",
     [[8.36, 49.63], [4.40, 51.22], [-0.12, 51.51]],
     "Imprimés à Worms, les petits volumes passent par les ports flamands, dissimulés parmi des marchandises, puis sont vendus sous le manteau à Londres."),
    ("oso", "1569", "Bâle → Séville", "La Bible de l'Ours",
     [[7.59, 47.56], [4.83, 45.76], [-0.58, 44.84], [-3.70, 40.42], [-5.98, 37.39]],
     "Imprimée à Bâle, la Bible de Casiodoro de Reina est introduite clandestinement en Espagne, où l'Inquisition la recherche et la détruit."),
    ("mada", "1835 – 1861", "Antananarivo", "Les Bibles de Madagascar",
     [[47.52, -18.91]],
     "Pendant 26 ans d'interdiction, des exemplaires de la Bible malgache sont cachés, recopiés et lus en secret sur les hauts plateaux."),
    ("andre", "1955", "Pays-Bas → Varsovie", "Frère André",
     [[4.90, 52.37], [13.40, 52.52], [21.01, 52.23]],
     "Le Néerlandais Andrew van der Bijl, « Frère André », se rend en Pologne en 1955. C'est le début de décennies de voyages pour faire passer des Bibles derrière le rideau de fer."),
    ("samizdat", "1960 – 1980", "Moscou", "Les Bibles recopiées",
     [[37.62, 55.75]],
     "En URSS, des croyants recopient la Bible à la main ou à la machine à écrire, avec plusieurs feuilles de papier carbone, et se transmettent les cahiers."),
    ("tirana", "1967 – 1990", "Tirana", "L'Albanie athée",
     [[19.82, 41.33]],
     "Dans le seul pays officiellement athée du monde, des familles gardent une Bible enterrée ou emmurée pendant près d'un quart de siècle."),
    ("perle", "18 juin 1981", "Manille → Shantou", "Le projet Perle",
     [[120.98, 14.60], [119.50, 19.00], [116.68, 23.35]],
     "Une barge de 232 tonnes de Bibles, tirée par le remorqueur Michael, rejoint de nuit une plage près de Shantou : un million de Bibles en chinois débarquées en quelques heures."),
]


def routes():
    data = [{"k": k, "pts": pts, "y": y} for k, y, _, _, pts, _ in ROUTES]
    lis = []
    for k, y, lieu, titre, pts, det in ROUTES:
        lis.append(f"""
        <li class="rt-item" data-k="{k}">
          <button type="button" class="rt-btn" aria-pressed="false">
            <span class="rt-y">{e(y)}</span><span class="rt-t">{e(titre)}</span><span class="rt-l">{e(lieu)}</span>
          </button>
          <p class="rt-info" hidden>{e(det)}</p>
        </li>""")
    return (f'<ul class="rt-list">{"".join(lis)}\n        </ul>\n'
            f'        <script type="application/json" id="rt-data">{json.dumps(data, separators=(",", ":"))}</script>')


# --------------------------------------------------------------------------
# V. Vrai ou légende ?
# --------------------------------------------------------------------------
QUIZ = [
    ("Voltaire aurait prédit que, cent ans après lui, la Bible serait un livre oublié ; et sa maison serait ensuite devenue un dépôt de Bibles.",
     False,
     "Aucune phrase de ce genre n'a été retrouvée dans les écrits de Voltaire. Theodore Besterman, directeur de l'Institut et Musée Voltaire de Genève, affirmait qu'aucune de ses maisons n'a jamais été liée à une société biblique. L'histoire, répandue au début du XXe siècle, provient sans doute d'une mauvaise lecture d'un rapport de 1849. Seule nuance : un récit anglais de 1836 évoque des Bibles entreposées un temps aux Délices, ancienne demeure du philosophe."),
    ("Dioclétien aurait fait graver une colonne proclamant le nom des chrétiens « effacé » pour toujours.",
     False,
     "L'inscription latine « nomine christianorum deleto », « le nom des chrétiens ayant été effacé », n'est connue que par des recueils de la Renaissance. Aucun original n'a jamais été vu, et les épigraphistes la classent parmi les inscriptions fausses. L'édit de 303, lui, est bien réel."),
    ("En 331 environ, l'empereur Constantin commande 50 exemplaires des Écritures.",
     True,
     "Eusèbe de Césarée cite la lettre de l'empereur : 50 exemplaires sur parchemin, lisibles et faciles à transporter, pour les églises de Constantinople (Vie de Constantin, IV, 36). Certains chercheurs se sont demandé si les codex Vaticanus et Sinaïticus en sont proches ; c'est une simple hypothèse."),
    ("Il ne reste que trois exemplaires du Nouveau Testament de Tyndale imprimé à Worms en 1526.",
     True,
     "Sur plusieurs milliers d'exemplaires imprimés, trois seulement sont connus : celui de la British Library à Londres (il lui manque la page de titre), celui de la Bibliothèque régionale de Stuttgart, le seul complet, identifié en 1996, et un exemplaire très incomplet à la bibliothèque de la cathédrale Saint-Paul de Londres."),
    ("Les os de John Wycliffe ont été brûlés 44 ans après sa mort.",
     True,
     "Mort en 1384, Wycliffe est exhumé en 1428 à Lutterworth sur ordre du pape Martin V, en application d'une décision du concile de Constance. Ses restes sont brûlés et ses cendres jetées dans la rivière Swift."),
    ("Un million de Bibles ont été débarquées en une seule nuit sur une plage de Chine.",
     True,
     "C'est le « projet Perle », dans la nuit du 18 juin 1981, près de Shantou. Les croyants chinois les ont appelées les « Bibles de l'eau ». Une partie des colis fut saisie par les autorités, mais une grande partie fut distribuée dans tout le pays."),
]


def quiz():
    items = []
    for i, (q, vrai, expl) in enumerate(QUIZ, 1):
        items.append(f"""
      <li class="vl-q" data-ok="{'vrai' if vrai else 'legende'}" data-reveal>
        <p class="vl-n">Affirmation {i} / {len(QUIZ)}</p>
        <p class="vl-t">{e(q)}</p>
        <div class="vl-btns" role="group" aria-label="Votre réponse">
          <button type="button" class="vl-b" data-a="vrai">Vrai</button>
          <button type="button" class="vl-b" data-a="legende">Légende</button>
        </div>
        <div class="vl-r" hidden>
          <p class="vl-verdict"><span class="badge {'badge-canon' if vrai else 'badge-apo'}">{'Vrai' if vrai else 'Légende'}</span> <b class="vl-you"></b></p>
          <p>{e(expl)}</p>
        </div>
      </li>""")
    return f"""
    <div class="vl-score" aria-live="polite">Score : <b class="vl-s">0</b> / {len(QUIZ)} <span class="vl-done"></span></div>
    <ol class="vl-list">{"".join(items)}
    </ol>"""


# --------------------------------------------------------------------------
# Transcriptions
# --------------------------------------------------------------------------
TR_A = """<p>Nicomédie, février de l'an trois cent trois. L'empereur Dioclétien fait afficher un édit : les lieux de réunion des chrétiens seront rasés, et leurs Écritures livrées aux flammes. L'historien Eusèbe de Césarée écrit qu'il a vu, de ses propres yeux, les saintes Écritures brûler au milieu des places publiques. En Afrique, à Cirta, les magistrats fouillent maison après maison pour saisir les livres. Certains les livrent. D'autres les cachent, au péril de leur vie. Moins de trente ans plus tard, l'empereur Constantin commande cinquante exemplaires des Écritures pour les églises de sa nouvelle capitale. Le livre que l'on voulait effacer est recopié avec un soin nouveau.</p>
<p>Londres, octobre 1526. Devant la cathédrale Saint-Paul, l'évêque Cuthbert Tunstall fait brûler des Nouveaux Testaments en anglais, imprimés à Worms et entrés en secret dans le royaume. Leur traducteur, William Tyndale, est traqué. Arrêté à Anvers, enfermé au château de Vilvorde, il réclame dans une lettre sa Bible hébraïque, sa grammaire et son dictionnaire, pour continuer à traduire. Le 6 octobre 1536, il est étranglé, puis brûlé. Trois ans plus tard, une Bible anglaise, en grande partie son œuvre, est imprimée par ordre du roi pour toutes les églises d'Angleterre. Le feu a détruit des exemplaires. Il n'a pas détruit le texte.</p>"""

TR_B = """<p>Pendant des siècles, des pouvoirs ont tenté d'empêcher la lecture de la Bible dans la langue du peuple. En Angleterre, en 1408, les constitutions d'Oxford interdisent toute traduction anglaise non autorisée. Pourtant, plus de deux cent cinquante manuscrits de la Bible de Wycliffe nous sont parvenus. À Madagascar, la reine Ranavalona interdit le christianisme en 1835, l'année même où s'achève l'impression de la Bible malgache. Pendant vingt-six ans, des croyants cachent leurs exemplaires et les lisent en secret, parfois au fond des grottes. Quand l'interdiction est levée, en 1861, la Bible est toujours là.</p>
<p>Au XXe siècle, en Union soviétique, des croyants recopient la Bible à la main ou à la machine à écrire, page après page, pendant des nuits entières. En Albanie, l'État se proclame athée. En Chine, pendant la Révolution culturelle, des Bibles sont brûlées en public. Puis, dans la nuit du 18 juin 1981, sur une plage proche de Shantou, des centaines de croyants chinois tirent des vagues un million de Bibles, en une seule nuit. Aujourd'hui, la Bible est le livre le plus diffusé de l'histoire, traduite en entier dans plus de huit cents langues. « L'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours. »</p>"""


def render(inner):
    rep = {
        "{{S10_CIRTA}}": cirta(),
        "{{S10_BUCHER}}": bucher(),
        "{{S10_INTERDITS}}": interdits(),
        "{{S10_ROUTES}}": routes(),
        "{{S10_QUIZ}}": quiz(),
        "{{S10_TR_A}}": TR_A,
        "{{S10_TR_B}}": TR_B,
        "{{IMG_DIOCLETIEN}}": img("diocletien", "Deux fonctionnaires romains en toge inventorient des rouleaux dans un coffre, devant un vieil homme et un jeune lecteur inquiets, dans une maison de pierre",
                                  "La saisie des Écritures en 303. Reconstitution numérique."),
        "{{IMG_CACHETTE}}": img("cachette", "Une femme agenouillée, à la lueur d'une lampe à huile, glisse un paquet enveloppé de lin dans une grande jarre d'argile",
                                "Cacher les livres pour les sauver. Reconstitution numérique."),
        "{{IMG_BUCHER}}": img("bucher", "Un grand feu de livres sur une place pavée bordée de maisons à colombages, au crépuscule, devant une foule silencieuse",
                              "Londres, octobre 1526 : des Nouveaux Testaments de Tyndale livrés au feu. Reconstitution numérique."),
        "{{IMG_VILVORDE}}": img("vilvorde", "Un homme barbu écrit à la lueur d'une bougie dans une cellule de pierre, des livres ouverts devant lui, la lune visible par une étroite fenêtre",
                                "Tyndale dans sa cellule de Vilvorde, hiver 1535. Reconstitution numérique."),
        "{{IMG_LOLLARDS}}": img("lollards", "Des paysans réunis dans une grange, autour d'une lanterne, écoutent un jeune homme lire un manuscrit",
                                "Une lecture clandestine de la Bible de Wycliffe. Reconstitution numérique."),
        "{{IMG_MADAGASCAR}}": img("madagascar", "Deux hommes drapés de blanc, assis à l'entrée d'une grotte, tiennent un livre caché ; derrière eux, des rizières en terrasses au coucher du soleil",
                                  "Madagascar, entre 1835 et 1861. Reconstitution numérique."),
        "{{IMG_SAMIZDAT}}": img("samizdat", "Une femme âgée en fichu recopie un texte à la main près d'une fenêtre givrée, à côté d'une machine à écrire et de cahiers ficelés",
                                "Recopier la Bible en Union soviétique. Reconstitution numérique."),
        "{{IMG_PLAGE}}": img("plage", "La nuit, sous la lune, des dizaines de personnes portent des colis enveloppés de plastique hors des vagues ; au large, une barge et un remorqueur",
                             "Le projet Perle, 18 juin 1981. Reconstitution numérique."),
        "{{IMG_IMPRIMERIE}}": img("imprimerie", "Une immense imprimerie moderne où des Bibles reliées de noir aux tranches dorées avancent sur des tapis roulants",
                                  "Une imprimerie biblique aujourd'hui. Reconstitution numérique.", sizes="100vw"),
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S10_CIRTA}}{{S10_BUCHER}}{{S10_INTERDITS}}{{S10_ROUTES}}{{S10_QUIZ}}")
    assert "{{S10" not in out
    print("ok", len(out))
