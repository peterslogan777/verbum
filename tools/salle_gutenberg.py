"""
VERBUM — Salle 08 « Gutenberg et l'imprimerie » (étape E10)
Marqueurs remplacés dans tools/templates/salles/gutenberg.html :
  {{S08_ETAPES_NAV}} / {{S08_ETAPES}}   de la lettre à la page (4 étapes, onglets)
  {{S08_COMPO}}        jeu « À vous de composer » (données JSON des mots)
  {{S08_FAC}}          page d'inspiration B42 avec points d'intérêt
  {{S08_FAC_INFO}}     textes des points d'intérêt
  {{S08_VIE}}          vie de Gutenberg (frise)
  {{S08_VAGUE}}        « la vague imprimée » : liste des éditions + JSON pour la carte
  {{S08_REFORME}}      cartes « retour aux sources »
  {{S08_LANGUES}}      barre des 7 394 langues (ProgressBible, septembre 2026)
  {{S08_TR_GUT}} / {{S08_TR_DIF}}   transcriptions
Données géographiques : assets/js/salle08-geo.js (Natural Earth 110 m, domaine public).
"""
import html
import json

e = html.escape


def img(name, alt, caption, sizes="(max-width: 1000px) 100vw, 50vw", root="{{ROOT}}"):
    p = f"{root}assets/img/salles/08/{name}"
    return (f'<img src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" data-lightbox data-full="{p}.jpg" data-caption="{e(caption)}">')


# --------------------------------------------------------------------------
# I. De la lettre à la page
# --------------------------------------------------------------------------
ETAPES = [
    ("fondre", "1", "Graver et fondre",
     "fonte", "Un fondeur verse l'alliage en fusion dans un moule à main ; devant lui, des rangées de caractères neufs",
     "Fondre les caractères. Reconstitution numérique.",
     ["Chaque lettre est d'abord gravée en relief, à l'envers, au bout d'une tige d'acier : le <b>poinçon</b>.",
      "Frappé dans un bloc de cuivre plus tendre, il laisse une empreinte en creux : la <b>matrice</b>.",
      "La matrice est placée au fond d'un <b>moule à main</b> ajustable, où l'on verse un alliage de <b>plomb, d'étain et d'antimoine</b> qui fond à basse température et durcit en quelques secondes.",
      "Un ouvrier exercé peut ainsi couler des centaines de caractères identiques par jour."]),
    ("composer", "2", "Composer",
     "casse", "Les mains d'un compositeur placent de minuscules lettres de métal dans un composteur, au-dessus d'une casse",
     "Composer une ligne. Reconstitution numérique.",
     ["Les caractères sont rangés dans une <b>casse</b>, une caisse en bois à compartiments.",
      "Le compositeur les prend un à un et les aligne dans un <b>composteur</b> : les lettres sont à l'envers, et la ligne se lit en miroir.",
      "Les lignes sont réunies en colonnes, puis en pages serrées dans un cadre de fer : la <b>forme</b>.",
      "Pour la Bible, plusieurs compositeurs (six, selon certaines études) travaillent en parallèle : les spécialistes reconnaissent leurs habitudes d'une page à l'autre."]),
    ("presser", "3", "Encrer et presser",
     "presse", "Un ouvrier tire de toutes ses forces sur le levier d'une presse à vis en bois ; derrière lui, un autre tient des balles d'encre",
     "Le coup de barreau. Reconstitution numérique.",
     ["La forme est encrée avec deux <b>balles de cuir</b> rembourrées.",
      "Gutenberg met au point une <b>encre grasse</b>, à base d'huile de lin et de noir de fumée, qui adhère au métal ; elle brille encore aujourd'hui.",
      "Une feuille de papier humide est posée sur la forme. Le pressier tire le barreau : la <b>presse à vis</b>, adaptée des pressoirs à raisin ou à papier, applique une pression égale sur toute la page.",
      "On imprime une face, puis l'autre : deux coups de barreau pour une feuille."]),
    ("secher", "4", "Sécher et assembler",
     "sechage", "Des centaines de grandes feuilles imprimées sèchent sur des cordes sous une charpente, éclairées par un rayon de soleil",
     "Le séchoir de l'atelier. Reconstitution numérique.",
     ["Les feuilles sèchent suspendues sous les toits avant d'être pliées en cahiers.",
      "Les livres sont vendus en feuilles : l'acheteur fait ajouter à ses frais les <b>titres rouges</b>, les <b>initiales peintes</b> et la <b>reliure</b>.",
      "Les caractères, eux, sont défaits, nettoyés et remis dans la casse pour composer la page suivante.",
      "C'est la grande nouveauté : des milliers de pages identiques, sans une seule faute de copie ajoutée."]),
]


def etapes_nav():
    return "".join(
        f'<button type="button" role="tab" id="et-tab-{k}" aria-controls="et-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span>{n}</span><b>{e(t)}</b></button>' for i, (k, n, t, *_r) in enumerate(ETAPES))


def etapes():
    out = []
    for i, (k, n, t, im, alt, cap, pts) in enumerate(ETAPES):
        li = "".join(f"<li>{p}</li>" for p in pts)
        out.append(f'''
<div class="et-panel" role="tabpanel" id="et-{k}" aria-labelledby="et-tab-{k}"{"" if i == 0 else " hidden"}>
  <figure class="s08-fig">{img(im, alt, cap)}<figcaption><span class="tag">Reconstitution</span> {e(cap.replace(" Reconstitution numérique.", ""))}</figcaption></figure>
  <div class="et-txt"><span class="et-n">Étape {n}</span><h3>{e(t)}</h3><ol>{li}</ol></div>
</div>''')
    return "".join(out)


# --------------------------------------------------------------------------
# II. Jeu « À vous de composer »
# --------------------------------------------------------------------------
MOTS = [
    dict(mot="LUX", fr="« lumière » — Fiat lux, « Que la lumière soit » (Genèse 1:3)"),
    dict(mot="VERBUM", fr="« parole » — In principio erat Verbum, « Au commencement était la Parole » (Jean 1:1)"),
    dict(mot="BIBLIA", fr="« les livres » — du grec τὰ βιβλία (ta biblia, « les livres »), qui a donné notre mot « Bible »"),
]


def compo():
    data = json.dumps(MOTS, ensure_ascii=False)
    btns = "".join(
        f'<button type="button" role="radio" aria-checked="{"true" if i == 0 else "false"}" data-i="{i}">{e(m["mot"])}</button>'
        for i, m in enumerate(MOTS))
    return f'<div class="seg cp-mots" role="radiogroup" aria-label="Mot à composer">{btns}</div><script type="application/json" id="cp-data">{data}</script>'


# --------------------------------------------------------------------------
# III. Page d'inspiration B42 + points d'intérêt
# --------------------------------------------------------------------------
LATIN = ("n principio creauit deus celum et terram. Terra autem erat inanis et uacua : et tenebre erant super faciem abyssi : "
         "et spiritus dei ferebatur super aquas. Dixitque deus. Fiat lux. Et facta est lux. Et uidit deus lucem quod esset bona : "
         "et diuisit lucem a tenebris. Appellauitque lucem diem et tenebras noctem. Factumque est uespere et mane dies unus. "
         "Dixit quoque deus. Fiat firmamentum in medio aquarum : et diuidat aquas ab aquis. Et fecit deus firmamentum : "
         "diuisitque aquas que erant sub firmamento ab hiis que erant super firmamentum. Et factum est ita. "
         "Uocauitque deus firmamentum celum : et factum est uespere et mane dies secundus.")
FR = ("Au commencement, Dieu créa les cieux et la terre. La terre était informe et vide ; il y avait des ténèbres à la surface de l'abîme, "
      "et l'esprit de Dieu se mouvait au-dessus des eaux. Dieu dit : « Que la lumière soit ! » Et la lumière fut. "
      "Dieu vit que la lumière était bonne, et Dieu sépara la lumière d'avec les ténèbres. Dieu appela la lumière « jour » "
      "et les ténèbres « nuit ». Il y eut un soir, il y eut un matin : ce fut le premier jour. Dieu dit : « Qu'il y ait une étendue "
      "au milieu des eaux, et qu'elle sépare les eaux d'avec les eaux. » Dieu fit l'étendue et sépara les eaux qui sont au-dessous "
      "de l'étendue d'avec les eaux qui sont au-dessus. Et cela fut ainsi. Dieu appela l'étendue « ciel ». Il y eut un soir, "
      "il y eut un matin : ce fut le deuxième jour. (Genèse 1:1-8)")

POINTS = [
    ("rubrique", "1", "La rubrique rouge",
     "« Incipit liber Bresith quem nos Genesim dicimus » : « Ici commence le livre Bereshit, que nous appelons Genèse ». Gutenberg a d'abord tenté d'imprimer le rouge en un second passage, puis y a renoncé : les titres étaient ajoutés à la main par un <b>rubricateur</b>, guidé par une table imprimée (conservée dans deux exemplaires seulement, à Munich et à Vienne)."),
    ("initiale", "2", "L'initiale peinte",
     "L'imprimeur laissait un espace vide. L'acheteur faisait peindre la grande lettre, ici le I de « In principio », en bleu, rouge et or, selon ses moyens."),
    ("colonnes", "3", "Deux colonnes de 42 lignes",
     "Les premières pages comptent 40 lignes, puis 41, puis 42 par colonne : en serrant le texte, Gutenberg économise du papier et du vélin. D'où le nom savant de l'ouvrage : B42."),
    ("justif", "4", "Une justification parfaite",
     "Toutes les lignes ont exactement la même longueur. Pour y parvenir, Gutenberg dispose de 290 caractères différents : majuscules, minuscules, lettres liées (ligatures), abréviations et variantes de largeur, comme les copistes."),
    ("encre", "5", "L'encre de Mayence",
     "Une encre grasse et dense, riche en particules métalliques selon certaines analyses, d'un noir brillant qui n'a presque pas pâli en près de six siècles."),
    ("marge", "6", "La marge enluminée",
     "Rinceaux, fleurs et oiseaux étaient peints par des ateliers locaux, différents d'une ville à l'autre. C'est pourquoi aucun des 49 exemplaires conservés ne ressemble tout à fait à un autre."),
]


def fac():
    hs = "".join(f'<button type="button" class="hs hs-{k}" data-k="{k}" aria-label="Point {n} : {e(t)}" aria-pressed="false">{n}</button>'
                 for k, n, t, _ in POINTS)
    return f'''
<div class="fac-page" lang="la">
  <div class="fac-marge" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="fac-cols">
    <p class="fac-rub">Incipit liber Bresith quem nos Genesim dicimus</p>
    <p class="fac-txt"><span class="fac-ini" aria-hidden="true">I</span><span class="sr-only">I</span>{e(LATIN)}</p>
  </div>
  {hs}
</div>'''


def fac_info():
    return "".join(
        f'<div class="fi" data-k="{k}"{"" if i == 0 else " hidden"}><span class="fi-n">{n}</span><h4>{e(t)}</h4><p>{p}</p></div>'
        for i, (k, n, t, p) in enumerate(POINTS))


# --------------------------------------------------------------------------
# Vie de Gutenberg
# --------------------------------------------------------------------------
VIE = [
    ("Vers 1400", "Naissance à Mayence", "Johannes Gensfleisch, dit Gutenberg, du nom de la maison familiale."),
    ("1434 – 1444", "Strasbourg", "Il y travaille les métaux précieux et mène des essais tenus secrets, évoqués lors d'un procès en 1439."),
    ("1448 – 1450", "Retour à Mayence", "Il emprunte, notamment au financier Johann Fust, pour monter son atelier."),
    ("Vers 1455", "La Bible achevée", "En novembre 1455, Fust lui intente un procès et récupère une partie du matériel."),
    ("1457", "Le Psautier de Mayence", "Fust et Peter Schöffer publient le premier livre portant une date et le nom de ses imprimeurs."),
    ("1468", "Mort à Mayence", "Le 3 février. Trois ans plus tôt, l'archevêque de Mayence lui avait accordé une pension."),
]


def vie():
    return "".join(f'<li data-reveal><span class="vie-d">{e(d)}</span><h4>{e(t)}</h4><p>{e(p)}</p></li>' for d, t, p in VIE)


# --------------------------------------------------------------------------
# IV. La vague imprimée
# --------------------------------------------------------------------------
VAGUE = [
    (1455, "Mayence", 8.27, 50.0, "Latin", "La Bible de Gutenberg, dans la traduction de Jérôme (salle 07)."),
    (1466, "Strasbourg", 7.75, 48.58, "Allemand", "La Bible de Johann Mentelin, première Bible imprimée en langue vivante."),
    (1471, "Venise", 12.33, 45.44, "Italien", "La Bible de Nicolò Malermi."),
    (1477, "Delft", 4.36, 52.01, "Néerlandais", "L'Ancien Testament en néerlandais."),
    (1478, "Valence", -0.38, 39.47, "Catalan", "La Bible valencienne de Bonifaci Ferrer."),
    (1488, "Soncino", 9.87, 45.40, "Hébreu", "La première Bible hébraïque complète imprimée, avec voyelles et accents."),
    (1488, "Prague", 14.43, 50.08, "Tchèque", "La Bible de Prague."),
    (1516, "Bâle", 7.59, 47.56, "Grec", "Le Nouveau Testament grec d'Érasme."),
    (1517, "Alcalá de Henares", -3.36, 40.48, "Hébreu · grec · latin · araméen", "La Polyglotte complutense, imprimée de 1514 à 1517."),
    (1522, "Wittenberg", 12.65, 51.87, "Allemand", "Le Nouveau Testament de Luther, puis la Bible complète en 1534."),
    (1526, "Worms", 8.36, 49.63, "Anglais", "Le Nouveau Testament de William Tyndale, introduit clandestinement en Angleterre."),
    (1530, "Anvers", 4.40, 51.22, "Français", "La Bible de Lefèvre d'Étaples, traduite de la Vulgate."),
    (1535, "Neuchâtel", 6.93, 46.99, "Français", "La Bible d'Olivétan, traduite de l'hébreu et du grec."),
    (1541, "Uppsala", 17.64, 59.86, "Suédois", "La Bible de Gustave Vasa."),
    (1550, "Copenhague", 12.57, 55.68, "Danois", "La Bible de Christian III."),
    (1551, "Genève", 6.15, 46.20, "Grec et latin", "Robert Estienne publie le premier Nouveau Testament découpé en versets numérotés."),
    (1561, "Cracovie", 19.94, 50.06, "Polonais", "La Bible de Leopolita."),
    (1569, "Bâle", 7.59, 47.56, "Espagnol", "La « Bible de l'Ours » de Casiodoro de Reina."),
    (1581, "Ostrog", 26.52, 50.33, "Slavon", "La Bible d'Ostrog, première Bible slavonne complète imprimée."),
    (1588, "Londres", -0.13, 51.51, "Gallois", "La Bible de William Morgan."),
    (1590, "Vizsoly", 21.22, 48.38, "Hongrois", "La Bible de Gáspár Károli."),
    (1611, "Londres", -0.13, 51.51, "Anglais", "La version du roi Jacques (King James Version)."),
]


def vague():
    data = json.dumps([dict(a=a, v=v, x=x, y=y, l=l, t=t) for a, v, x, y, l, t in VAGUE], ensure_ascii=False)
    lis = "".join(f'<li data-a="{a}"><span class="vq-a">{a}</span><span class="vq-v">{e(v)}</span><span class="vq-l">{e(l)}</span><span class="vq-t">{e(t)}</span></li>'
                  for a, v, x, y, l, t in VAGUE)
    return f'<script type="application/json" id="vq-data">{data}</script><ol class="vq-list" aria-live="polite">{lis}</ol>'


# --------------------------------------------------------------------------
# V. Retour aux sources
# --------------------------------------------------------------------------
REFORME = [
    ("1488 · 1524", "Soncino · Venise", "La Bible hébraïque imprimée",
     "En 1488, la famille Soncino imprime la première Bible hébraïque complète. En 1524-1525, à Venise, Daniel Bomberg publie la grande Bible rabbinique éditée par Jacob ben Hayyim, avec les notes des Massorètes (salle 02) : elle servira de référence pendant quatre siècles."),
    ("1516", "Bâle", "Érasme et le grec original",
     "« Retour aux sources » : l'humaniste Érasme publie chez Froben le premier Nouveau Testament grec mis en vente, avec sa propre traduction latine. Luther et Tyndale traduiront à partir de ses éditions."),
    ("1522 · 1534", "Wittenberg", "La Bible de Luther",
     "Réfugié au château de la Wartburg, Martin Luther traduit le Nouveau Testament en onze semaines. Paru en septembre 1522, il se vend par milliers. La Bible complète suit en 1534 ; sa langue contribue à unifier l'allemand."),
    ("1526 · 1530", "Worms · Anvers", "William Tyndale",
     "Selon le martyrologe de John Foxe, Tyndale aurait lancé à un clerc : « Si Dieu me prête vie, je ferai qu'un garçon qui pousse la charrue connaisse les Écritures mieux que vous. » Dans son Pentateuque de 1530, il écrit le nom divin « Iehouah » (Exode 6:3), l'une des premières apparitions de cette forme dans une Bible anglaise. Arrêté près d'Anvers, il est exécuté à Vilvorde en 1536."),
    ("1523 · 1530", "Paris · Anvers", "Lefèvre d'Étaples",
     "Le savant Jacques Lefèvre d'Étaples publie le Nouveau Testament en français en 1523, puis la Bible entière en 1530, traduite de la Vulgate, pour que les gens simples puissent la lire."),
    ("1535", "Neuchâtel", "La Bible d'Olivétan",
     "Pierre Robert, dit Olivétan, cousin de Calvin, donne la première Bible française traduite directement de l'hébreu et du grec. Pour rendre le nom divin, il choisit « l'Éternel » et s'en explique dans sa préface : c'est un nom propre, distinct du titre « Seigneur »."),
]


def reforme():
    return "".join(
        f'<article class="rf" data-reveal><span class="rf-d">{e(d)}</span><span class="rf-v">{e(v)}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>'
        for d, v, t, p in REFORME)


# --------------------------------------------------------------------------
# VI. Les 7 394 langues
# --------------------------------------------------------------------------
LANGUES = [
    ("bible", 807, "Bible complète", "807 langues"),
    ("nt", 1844, "Nouveau Testament", "1 844 langues"),
    ("portions", 1519, "Portions des Écritures", "1 519 langues"),
    ("aucune", 3224, "Aucun texte biblique", "3 224 langues"),
]


def langues():
    tot = sum(n for _, n, _, _ in LANGUES)
    bars = "".join(f'<button type="button" class="lg-seg lg-{k}" style="--w:{n / tot * 100:.2f}%" data-k="{k}" aria-label="{e(t)} : {e(lbl)}"><span>{n / tot * 100:.0f} %</span></button>'
                   for k, n, t, lbl in LANGUES)
    leg = "".join(f'<li class="lg-{k}" data-k="{k}"><i></i><b>{e(lbl)}</b><span>{e(t)}</span></li>' for k, n, t, lbl in LANGUES)
    tot_s = f"{tot:,}".replace(",", "\u202f")
    return f'<div class="lg-bar" role="group" aria-label="Répartition des {tot_s} langues du monde">{bars}</div><ul class="lg-leg">{leg}</ul>'


TR_GUT = """<p>Mayence, vers 1450. Un orfèvre nommé Johannes Gutenberg poursuit une idée qui l'obsède depuis des années : écrire sans plume. Il découpe chaque lettre dans l'acier, la frappe dans le cuivre, puis coule des milliers de petits caractères dans un alliage de plomb, d'étain et d'antimoine. Ces lettres mobiles, assemblées ligne après ligne, peuvent servir, être défaites, puis resservir à l'infini. Il invente une encre grasse qui accroche le métal et adapte la presse à vis des vignerons. Le premier grand livre qu'il choisit d'imprimer n'est pas un roman ni une chronique : c'est la Bible, dans la traduction latine de Jérôme.</p>
<p>Pendant plusieurs années, une vingtaine d'ouvriers composent, encrent et pressent. Deux cent quatre-vingt-dix caractères différents, deux colonnes de quarante-deux lignes, mille deux cent quatre-vingt-deux pages. Vers 1455, environ cent quatre-vingts exemplaires sont achevés. Un témoin, le futur pape Pie II, s'émerveille : on peut lire ces pages sans lunettes. Les rubriques rouges et les enluminures sont ajoutées à la main, si bien qu'aucun exemplaire ne ressemble tout à fait à un autre. Quarante-neuf d'entre eux existent encore. En quelques années, ce qu'un copiste mettait des mois à écrire sort de la presse par centaines. La Bible ne dépendra plus jamais de quelques mains.</p>"""

TR_DIF = """<p>L'imprimerie se répand comme une traînée de poudre. En 1466, Strasbourg imprime une Bible en allemand ; en 1471, Venise en imprime une en italien ; en 1488, à Soncino, paraît la première Bible hébraïque complète imprimée. En 1516, à Bâle, Érasme publie le Nouveau Testament dans son grec original. Alors les traducteurs se mettent au travail. Luther à Wittenberg, Lefèvre d'Étaples en France, Olivétan à Neuchâtel, qui traduit depuis l'hébreu et le grec. En Angleterre, William Tyndale veut qu'un simple garçon de ferme connaisse les Écritures. Ses Nouveaux Testaments, imprimés sur le continent, traversent la mer cachés dans des ballots de tissu. Il paiera ce travail de sa vie, en 1536.</p>
<p>Cinq siècles plus tard, le mouvement ne s'est jamais arrêté. En 2026, la Bible complète existe dans plus de huit cents langues, le Nouveau Testament dans plus de mille huit cents autres, et des portions des Écritures dans plus de quatre mille langues au total. Plus de six milliards de personnes peuvent lire la Bible entière dans leur propre langue. Aujourd'hui, des équipes de traducteurs travaillent dans plus de quatre mille langues, sous un manguier, devant un ordinateur, avec des anciens du village. Le plomb de Mayence a cédé la place aux écrans, mais le but reste le même que celui des scribes, des copistes et des traducteurs d'autrefois : transmettre fidèlement la Parole.</p>"""


def render(inner):
    rep = {
        "{{S08_ETAPES_NAV}}": etapes_nav(), "{{S08_ETAPES}}": etapes(), "{{S08_COMPO}}": compo(),
        "{{S08_FAC}}": fac(), "{{S08_FAC_INFO}}": fac_info(), "{{S08_FAC_FR}}": e(FR), "{{S08_VIE}}": vie(),
        "{{S08_VAGUE}}": vague(), "{{S08_REFORME}}": reforme(), "{{S08_LANGUES}}": langues(),
        "{{S08_TR_GUT}}": TR_GUT, "{{S08_TR_DIF}}": TR_DIF,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("".join(["{{S08_ETAPES_NAV}}", "{{S08_ETAPES}}", "{{S08_COMPO}}", "{{S08_FAC}}", "{{S08_FAC_INFO}}", "{{S08_VIE}}", "{{S08_VAGUE}}", "{{S08_REFORME}}", "{{S08_LANGUES}}"]))
    print(len(out), "{{S08" in out)
    print(langues()[:300])
