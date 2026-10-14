"""
VERBUM — Salle 12 « La Bible en français » (étape E15)
Marqueurs remplacés dans tools/templates/salles/bible-francaise.html :
  {{S12_MOYEN_AGE}}   frise des Bibles françaises avant 1500
  {{S12_OLIVETAN}}    Jean 1:1-5 dans la Bible d'Olivétan (1535) : orthographe d'origine / modernisée + glossaire
  {{S12_COMPARATEUR}} Jean 1:1 dans onze versions, de la Vulgate à 2018 (curseur + vue d'ensemble)
  {{S12_NOM}}         tableau : comment les Bibles françaises ont rendu le nom divin יהוה
  {{S12_FOYERS}}      frise 1588 – 1910
  {{S12_AUJOURDHUI}}  les grandes traductions depuis 1956
  {{S12_QUIZ}}        « Qui a traduit ? »
  {{S12_TR_A}} / {{S12_TR_B}}   transcriptions des narrations
  {{IMG_*}}           images de la salle (assets/img/salles/12)

Règles VERBUM appliquées : tout texte étranger (latin, grec, hébreu) est suivi de sa traduction
française ; le tétragramme est rendu « Jéhovah » dans le texte du musée (les autres rendus ne sont
cités que comme faits historiques) ; aucune croix, ni dans les images ni dans le décor.

Sources principales : olivetan.eglises-protestantes.org (2026) ; fac-similé de la Bible d'Olivétan,
Bibliothèque de Genève, e-rara (doi:10.3931/e-rara-5690) ; Wikisource (Segond 1910, Sacy, Crampon 1923) ;
P.-M. Bogaert (dir.), Les Bibles en français, Brepols, 1991.
"""
import html

e = html.escape


def img(name, alt, caption, sizes="(max-width: 1000px) 100vw, 50vw", root="{{ROOT}}"):
    p = f"{root}assets/img/salles/12/{name}"
    return (f'<img src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" data-lightbox data-full="{p}.jpg" data-caption="{e(caption)}">')


# --------------------------------------------------------------------------
# I. Avant l'imprimerie
# --------------------------------------------------------------------------
MOYEN_AGE = [
    ("XIIe siècle", "Le Psautier d'Oxford",
     "Les Psaumes en anglo-normand, l'une des plus anciennes traductions bibliques en langue française. "
     "Au même siècle paraissent aussi les « Quatre Livres des Rois »."),
    ("Vers 1230 – 1260", "La Bible française du XIIIe siècle",
     "À Paris, des traducteurs anonymes donnent la première Bible presque complète en français. "
     "Ce travail inégal, longtemps inachevé, circule peu."),
    ("1291 – 1295", "La Bible historiale",
     "Guyart des Moulins, chanoine d'Aire-sur-la-Lys, adapte l'Histoire scolastique de Pierre le Mangeur : "
     "les récits bibliques, accompagnés de commentaires. Complétée par la Bible du XIIIe siècle, elle devient "
     "la Bible des princes, souvent somptueusement enluminée."),
    ("Vers 1476", "Le premier Nouveau Testament imprimé",
     "À Lyon, l'imprimeur Barthélemy Buyer publie un Nouveau Testament en français, préparé par deux religieux, "
     "Julien Macho et Pierre Farget. Le livre sort enfin des bibliothèques royales."),
    ("Vers 1498", "La première Bible imprimée",
     "À Paris, Antoine Vérard imprime une Bible historiale revue par Jean de Rély, confesseur du roi Charles VIII. "
     "C'est encore une adaptation, et non une traduction complète."),
]


def moyen_age():
    items = "".join(f"""
      <li class="ma-it" data-reveal>
        <span class="ma-d">{e(d)}</span>
        <h3>{e(t)}</h3>
        <p>{e(txt)}</p>
      </li>""" for d, t, txt in MOYEN_AGE)
    return f'<ol class="ma-list">{items}\n    </ol>'


# --------------------------------------------------------------------------
# II. Olivétan, Jean 1:1-5 (transcription de lecture du fac-similé de 1535)
# --------------------------------------------------------------------------
# (orthographe de 1535, orthographe modernisée)
OLIVETAN = [
    ("1", "Au commencement estoit la parolle; et la parolle estoit avec Dieu: et Dieu estoit la parolle.",
     "Au commencement était la parole, et la parole était avec Dieu, et Dieu était la parole."),
    ("2", "Icelle estoit au commencement avec Dieu.",
     "Celle-ci était au commencement avec Dieu."),
    ("3", "Toutes choses ont este faictes par icelle: et sans icelle rien na este faict; de ce qui est faict.",
     "Toutes choses ont été faites par elle, et sans elle rien n'a été fait de ce qui est fait."),
    ("4", "En icelle estoit la vie: et la vie estoit la lumiere des hommes;",
     "En elle était la vie, et la vie était la lumière des hommes,"),
    ("5", "& la lumiere luyt es tenebres; et les tenebres ne lont pas comprinse",
     "et la lumière luit dans les ténèbres, et les ténèbres ne l'ont pas saisie."),
]
GLOSSAIRE = [
    ("estoit", "était : le s muet de l'ancien français disparaîtra de l'orthographe au XVIIIe siècle, remplacé par l'accent."),
    ("parolle", "parole : Olivétan rend ainsi le grec logos, « parole, discours ». Les Bibles protestantes garderont « la Parole »."),
    ("icelle", "celle-ci, elle : pronom courant au XVIe siècle, disparu depuis."),
    ("faictes", "faites : le c rappelle le latin factus ; il ne se prononçait déjà plus."),
    ("luyt es tenebres", "luit dans les ténèbres : « es » est la contraction de « en les »."),
    ("comprinse", "comprise, au sens ancien de « saisie, arrêtée »."),
]


def olivetan():
    vv = "".join(f"""
          <p class="ol-v"><sup>{n}</sup><span class="ol-old">{e(a)}</span><span class="ol-new">{e(b)}</span></p>"""
                 for n, a, b in OLIVETAN)
    gl = "".join(f'<li><b>{e(m)}</b> {e(d)}</li>' for m, d in GLOSSAIRE)
    return f"""
    <div class="ol-wrap">
      <div class="ol-page" data-mode="old" data-reveal="left">
        <div class="ol-top">
          <span class="ol-k">Jean 1:1-5 · Neuchâtel, 1535</span>
          <div class="seg ol-seg" role="radiogroup" aria-label="Orthographe">
            <button type="button" role="radio" aria-checked="true" data-mode="old">1535<small>orthographe d'origine</small></button>
            <button type="button" role="radio" aria-checked="false" data-mode="new">Aujourd'hui<small>orthographe modernisée</small></button>
          </div>
        </div>
        <div class="ol-txt" aria-live="polite">{vv}
        </div>
        <p class="ol-src">Transcription de lecture du fac-similé (Bibliothèque de Genève). Dans l'original, les versets ne sont pas numérotés : la division en versets, due à l'imprimeur Robert Estienne, date de 1551. <span class="badge badge-canon">Canonique</span></p>
      </div>
      <div class="ol-gl" data-reveal="right">
        <h3>Petit glossaire de 1535</h3>
        <ul>{gl}</ul>
        <a class="btn btn-ghost btn-sm" href="https://doi.org/10.3931/e-rara-5690" target="_blank" rel="noopener">Voir l'original · Bible d'Olivétan, e-rara {{{{ARROW}}}}</a>
      </div>
    </div>"""


# --------------------------------------------------------------------------
# III. Un verset, cinq siècles : Jean 1:1
# --------------------------------------------------------------------------
# (année affichée, version, tradition, texte, remarque)
VERSIONS = [
    ("v. 400", "Vulgate de Jérôme", "Latin · texte de référence",
     "In principio erat Verbum, et Verbum erat apud Deum, et Deus erat Verbum.",
     "Traduction : « Au commencement était le Verbe, et le Verbe était auprès de Dieu, et Dieu était le Verbe. » "
     "C'est sur ce texte latin que travaillent Lefèvre d'Étaples (1523) et Sacy (1667).", "la"),
    ("1535", "Pierre Robert Olivétan", "Protestante · sur le grec",
     "Au commencement estoit la parolle; et la parolle estoit avec Dieu: et Dieu estoit la parolle.",
     "Le choix de « parolle » pour le grec logos marque toute la tradition protestante. L'ordre des mots suit le grec.", "fr"),
    ("1669", "Bible de Genève", "Protestante · révision",
     "Au commencement estoit la Parole, et la Parole estoit avec Dieu: et cette Parole estoit Dieu.",
     "Héritière d'Olivétan, revue par les pasteurs de Genève (révision de 1588).", "fr"),
    ("1701", "Lemaistre de Sacy · Port-Royal", "Catholique · sur la Vulgate",
     "Au commencement était le Verbe, et le Verbe était avec Dieu; et le Verbe était Dieu.",
     "« Le Verbe », calqué sur le latin Verbum : ce mot restera celui des Bibles catholiques pendant trois siècles.", "fr"),
    ("1744", "David Martin", "Protestante · révision",
     "Au commencement était la Parole, et la Parole était avec Dieu ; et cette parole était Dieu.",
     "Révision de la Bible de Genève publiée par Martin en 1707, ici dans l'édition de 1744.", "fr"),
    ("1881", "Jean-Frédéric Ostervald", "Protestante · révision",
     "Au commencement était la Parole, la Parole était avec Dieu, et la Parole était Dieu.",
     "Ostervald, pasteur à Neuchâtel, révise à son tour le texte en 1744 ; édition revue de 1881.", "fr"),
    ("1885", "John Nelson Darby", "Frères · sur le grec",
     "Au commencement était la Parole; et la Parole était auprès de Dieu; et la Parole était Dieu.",
     "« Auprès de » rend le grec pros, « tourné vers, auprès de ».", "fr"),
    ("1910", "Louis Segond", "Protestante · sur l'hébreu et le grec",
     "Au commencement était la Parole, et la Parole était avec Dieu, et la Parole était Dieu.",
     "La phrase que des millions de lecteurs francophones connaissent par cœur.", "fr"),
    ("1923", "Augustin Crampon", "Catholique · sur l'hébreu et le grec",
     "Au commencement était le Verbe, et le Verbe était en Dieu, et le Verbe était Dieu.",
     "Une des premières Bibles catholiques françaises traduites sur les langues originales.", "fr"),
    ("2000", "Parole de Vie", "Interconfessionnelle · français fondamental",
     "Au commencement, la Parole existait déjà. La Parole était avec Dieu et la Parole était Dieu.",
     "Une traduction en vocabulaire simple, pour les lecteurs dont le français n'est pas la langue maternelle.", "fr"),
    ("2018", "Traduction du monde nouveau", "Témoins de Jéhovah · révision",
     "Au commencement était la Parole, et la Parole était avec Dieu, et la Parole était un dieu.",
     "Le grec theos est ici sans article : la plupart des versions comprennent « était Dieu », la Traduction du monde "
     "nouveau traduit « était un dieu ». C'est la principale divergence d'interprétation de ce verset.", "fr"),
]
GREC_JEAN = "Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος."
GREC_MOT = ("Mot à mot : « Au commencement était le logos (la parole), et le logos était auprès de (pros) "
            "Dieu (ton theon, avec article), et Dieu (theos, sans article) était le logos. »")


def comparateur():
    data, la = [], ' lang="la"'
    for i, (an, nom, trad, txt, note, lang) in enumerate(VERSIONS):
        data.append(f"""
        <article class="cp-card{' is-on' if i == 1 else ''}" data-i="{i}" {'hidden' if i != 1 else ''}>
          <header><span class="cp-an">{e(an)}</span><div><h3>{e(nom)}</h3><span class="cp-trad">{e(trad)}</span></div></header>
          <p class="cp-txt"{la if lang == 'la' else ''}>« {e(txt)} »</p>
          <p class="cp-note">{e(note)}</p>
        </article>""")
    ticks = "".join(f'<button type="button" class="cp-tick{" is-on" if i == 1 else ""}" data-i="{i}" '
                    f'aria-label="{e(v[0])} · {e(v[1])}"><span>{e(v[0])}</span></button>' for i, v in enumerate(VERSIONS))
    la = ' lang="la"'
    rows = "".join(f'<li><span class="cp-an">{e(an)}</span><b>{e(nom)}</b><span class="cp-l"{la if lang == "la" else ""}>« {e(txt)} »</span></li>'
                   for an, nom, trad, txt, note, lang in VERSIONS)
    return f"""
    <div class="cp" data-reveal>
      <div class="cp-grec q-heb q-grc">
        <p class="qh" lang="grc">{GREC_JEAN}</p>
        <p class="qf">{e(GREC_MOT)}</p>
        <cite>Jean 1:1 · grec · <span class="badge badge-canon">Canonique</span></cite>
      </div>
      <div class="cp-ctrl">
        <label class="cp-lab" for="cp-range">Faites glisser le curseur à travers cinq siècles</label>
        <input id="cp-range" class="cp-range" type="range" min="0" max="{len(VERSIONS) - 1}" value="1" step="1"
               aria-valuetext="{e(VERSIONS[1][0])} · {e(VERSIONS[1][1])}">
        <div class="cp-ticks">{ticks}</div>
      </div>
      <div class="cp-stage" aria-live="polite">{"".join(data)}
      </div>
      <div class="cp-mots" aria-hidden="true">
        <span class="cp-m"><i class="m-parole"></i>« Parole » : tradition protestante, depuis Olivétan</span>
        <span class="cp-m"><i class="m-verbe"></i>« Verbe » : tradition catholique, du latin Verbum</span>
      </div>
      <details class="cp-all">
        <summary>Voir les onze versions ensemble</summary>
        <ol class="cp-rows">{rows}</ol>
      </details>
    </div>"""


# --------------------------------------------------------------------------
# IV. Le nom divin dans les Bibles françaises
# --------------------------------------------------------------------------
NOM = [
    ("1535", "Olivétan", "« l'Éternel » ; « Iehouah » dans quelques versets, dont Exode 6:3",
     "Olivétan rattache le nom au verbe hébreu « être » : celui qui est, qui était et qui sera."),
    ("1588 – 1910", "Genève, Martin, Ostervald, Segond", "« l'Éternel »",
     "La « trouvaille d'Olivétan » devient l'usage de la plupart des Bibles protestantes."),
    ("1696", "Sacy · Port-Royal", "« le Seigneur »",
     "Traduit le latin Dominus de la Vulgate, lui-même hérité du grec Kyrios de la Septante."),
    ("1894 – 1904", "Crampon, première édition", "« Jéhovah »",
     "Dans tout l'Ancien Testament. L'édition révisée de 1923 adoptera « Yahweh »."),
    ("1956", "Bible de Jérusalem", "« Yahvé »",
     "Forme reconstituée par les savants du XIXe siècle, reprise par plusieurs Bibles catholiques."),
    ("1975", "Traduction œcuménique (TOB)", "« le SEIGNEUR », en petites capitales",
     "Une note signale que le texte hébreu porte les quatre lettres YHWH."),
    ("1974 · 2018", "Traduction du monde nouveau", "« Jéhovah »",
     "Plus de 7 000 fois, dans l'Ancien comme dans le Nouveau Testament."),
]


def nom_divin():
    rows = "".join(f"""
        <tr{' class="is-jeh"' if 'Jéhovah' in f else ''}><td class="nd-an">{e(a)}</td><th scope="row">{e(v)}</th><td class="nd-f">{e(f)}</td><td class="nd-r">{e(r)}</td></tr>"""
                   for a, v, f, r in NOM)
    return f"""
    <div class="nd-wrap" data-reveal>
      <table class="nd">
        <caption class="sr-only">Comment les Bibles françaises ont rendu le nom divin</caption>
        <thead><tr><th scope="col">Date</th><th scope="col">Version</th><th scope="col">Forme employée</th><th scope="col">Remarque</th></tr></thead>
        <tbody>{rows}
        </tbody>
      </table>
    </div>"""


# --------------------------------------------------------------------------
# VI. La Bible de tous les foyers (1588 – 1910)
# --------------------------------------------------------------------------
FOYERS = [
    ("1588", "La Bible de Genève", "Les pasteurs de Genève, avec Théodore de Bèze, révisent la traduction d'Olivétan. "
     "Elle accompagnera les protestants français, y compris dans l'exil après 1685."),
    ("1707", "David Martin", "Pasteur réfugié aux Pays-Bas, il modernise la Bible de Genève pour une génération qui ne lit plus le français du XVIe siècle."),
    ("1744", "Jean-Frédéric Ostervald", "Pasteur à Neuchâtel, il révise à son tour le texte. Sa Bible sera rééditée pendant plus d'un siècle."),
    ("1818", "Les sociétés bibliques", "Fondation de la Société biblique protestante de Paris. Avec la Société biblique britannique et étrangère "
     "(1804), elle soutient les colporteurs qui vendent des Bibles à bas prix dans les campagnes."),
    ("1880", "Louis Segond", "À la demande des pasteurs de Genève, il traduit l'Ancien Testament sur l'hébreu (paru en 1874), "
     "puis publie le Nouveau Testament en 1880. La révision de 1910 devient la Bible protestante de référence."),
    ("1885", "John Nelson Darby", "Traduction très littérale, achevée après la mort de son auteur, utilisée par les assemblées de Frères."),
    ("1904", "Augustin Crampon", "Chanoine d'Amiens, il traduit sur l'hébreu et le grec ; sa Bible, achevée après sa mort, "
     "rend le nom divin par « Jéhovah »."),
]


def foyers():
    items = "".join(f"""
      <li class="fo-it" data-reveal><span class="fo-an">{e(a)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>""" for a, t, d in FOYERS)
    return f'<ol class="fo-list">{items}\n    </ol>'


# --------------------------------------------------------------------------
# VII. Aujourd'hui
# --------------------------------------------------------------------------
AUJOURDHUI = [
    ("1956", "Bible de Jérusalem", "Catholique", "Préparée par l'École biblique et archéologique française de Jérusalem, célèbre pour ses notes."),
    ("1975", "Traduction œcuménique de la Bible", "Catholiques et protestants", "Pour la première fois, des biblistes des deux confessions traduisent ensemble."),
    ("1982", "Bible en français courant", "Alliance biblique", "Un français simple et actuel, pour une lecture suivie."),
    ("1992", "Bible du Semeur", "Évangélique", "Une traduction fluide, révisée en 2000 et en 2015."),
    ("2002", "Nouvelle Bible Segond", "Protestante", "La Segond revue sur les éditions critiques modernes, avec notes."),
    ("2007", "Segond 21", "Protestante", "La Segond dans un français du XXIe siècle."),
    ("2013", "Traduction officielle liturgique", "Catholique", "Le texte lu dans la liturgie catholique francophone."),
    ("2018", "Traduction du monde nouveau, révisée", "Témoins de Jéhovah", "Révision en français courant, avec le nom Jéhovah dans tout le texte."),
    ("2019", "Nouvelle Français courant", "Alliance biblique", "Révision complète de la Bible en français courant."),
]


def aujourdhui():
    items = "".join(f"""
      <li class="aj-it" data-reveal><span class="aj-an">{e(a)}</span><h3>{e(t)}</h3><span class="aj-c">{e(c)}</span><p>{e(d)}</p></li>"""
                    for a, t, c, d in AUJOURDHUI)
    return f'<ul class="aj-list">{items}\n    </ul>'


# --------------------------------------------------------------------------
# VIII. Qui a traduit ?
# --------------------------------------------------------------------------
QUIZ = [
    ("Il a traduit une grande partie de l'Ancien Testament dans une cellule de la Bastille.",
     ["Olivétan", "Lemaistre de Sacy", "Louis Segond"], 1,
     "Louis-Isaac Lemaistre de Sacy, prêtre de Port-Royal, est emprisonné du 13 mai 1666 à la fin de 1668."),
    ("Sa Bible, achevée d'imprimer le 4 juin 1535 à Neuchâtel, est la première traduite en français sur l'hébreu et le grec.",
     ["Lefèvre d'Étaples", "Olivétan", "David Martin"], 1,
     "Pierre Robert, dit Olivétan, financé par les Vaudois réunis à Chanforan en 1532."),
    ("Son Nouveau Testament de 1523 est condamné deux ans plus tard par le Parlement et la Sorbonne.",
     ["Lefèvre d'Étaples", "Jean Calvin", "Augustin Crampon"], 0,
     "Jacques Lefèvre d'Étaples traduit sur la Vulgate en tenant compte du grec ; sa Bible complète paraît à Anvers en 1530."),
    ("Pasteur genevois, sa traduction révisée en 1910 reste l'une des plus lues en français.",
     ["Ostervald", "Louis Segond", "John Nelson Darby"], 1,
     "Louis Segond (1810-1885) : Ancien Testament en 1874, Nouveau Testament en 1880."),
    ("Prêtre catholique, sa Bible achevée en 1904 rend le nom divin par « Jéhovah ».",
     ["Augustin Crampon", "Lemaistre de Sacy", "Lefèvre d'Étaples"], 0,
     "Le chanoine Augustin Crampon meurt en 1894 ; des jésuites achèvent son œuvre."),
    ("Vers 1291-1295, ce chanoine adapte en français les récits bibliques avec leurs commentaires.",
     ["Guyart des Moulins", "Olivétan", "David Martin"], 0,
     "Sa Bible historiale sera la Bible française la plus copiée jusqu'à la fin du Moyen Âge."),
]


def quiz():
    items = []
    for i, (q, opts, ok, expl) in enumerate(QUIZ):
        btns = "".join(f'<button type="button" class="qt-b" data-a="{j}">{e(o)}</button>' for j, o in enumerate(opts))
        items.append(f"""
      <li class="qt-q" data-ok="{ok}" data-reveal>
        <span class="qt-n">Question {i + 1} / {len(QUIZ)}</span>
        <p class="qt-t">{e(q)}</p>
        <div class="qt-btns">{btns}</div>
        <div class="qt-r" hidden>
          <p class="qt-verdict"><span class="badge badge-canon">{e(opts[ok])}</span> <b class="qt-you"></b></p>
          <p>{e(expl)}</p>
        </div>
      </li>""")
    return f"""
    <div class="qt-score" aria-live="polite">Score : <b class="qt-s">0</b> / {len(QUIZ)} <span class="qt-done"></span></div>
    <ol class="qt-list">{"".join(items)}
    </ol>"""


# --------------------------------------------------------------------------
# Transcriptions (texte exact des narrations)
# --------------------------------------------------------------------------
TR_A = """<p>Paris, 1523. Jacques Lefèvre d'Étaples, humaniste et bibliothécaire de l'abbaye de Saint-Germain-des-Prés, publie le Nouveau Testament en français. Pour la première fois, un texte complet, sans coupure ni paraphrase, s'offre aux lecteurs de langue française. Deux ans plus tard, le Parlement et la Sorbonne le condamnent. Lefèvre poursuit pourtant son œuvre : sa Bible complète paraît à Anvers en 1530.</p>
<p>Septembre 1532. Dans les Alpes du Piémont, au hameau de Chanforan, les Vaudois tiennent synode. Ces croyants des montagnes décident de financer une Bible française traduite directement sur l'hébreu et sur le grec. La tâche revient à un jeune érudit picard, Pierre Robert, dit Olivétan, cousin de Jean Calvin.</p>
<p>Le 4 juin 1535, à Neuchâtel, l'imprimeur Pierre de Vingle achève l'impression. Un grand in-folio, en caractères gothiques, sur deux colonnes. Pour rendre le nom divin, les quatre lettres hébraïques, Olivétan écrit le plus souvent « l'Éternel », et dans quelques versets, « Iehouah », c'est-à-dire Jéhovah. De révision en révision, sa traduction deviendra la Bible de Genève, l'ancêtre de la plupart des Bibles protestantes de langue française.</p>"""

TR_B = """<p>Paris, 13 mai 1666. Louis-Isaac Lemaistre de Sacy, prêtre de Port-Royal, est arrêté et enfermé à la Bastille. Il y restera plus de deux ans. Dans sa cellule, il poursuit la traduction de l'Ancien Testament. L'année suivante, son Nouveau Testament, imprimé à Mons, se vend par milliers malgré l'interdiction. La Bible de Port-Royal, achevée en 1696, sera pendant deux siècles la Bible des lecteurs catholiques de langue française.</p>
<p>Au dix-neuvième siècle, les sociétés bibliques et leurs colporteurs portent le livre jusque dans les villages les plus reculés. À Genève, le pasteur Louis Segond traduit l'Ancien Testament sur l'hébreu, puis le Nouveau Testament sur le grec. Sa Bible, révisée en 1910, reste l'une des plus lues aujourd'hui. Du côté catholique, la Bible de l'abbé Augustin Crampon, achevée en 1904, rend le nom divin par Jéhovah.</p>
<p>Le vingtième siècle ouvre une ère nouvelle : la Bible de Jérusalem, la Traduction œcuménique, puis des versions en français courant pour les lecteurs d'aujourd'hui. En cinq siècles, l'orthographe a changé, les mots ont vieilli. Mais d'Olivétan à nos jours, le message, lui, est resté le même.</p>"""


def render(inner):
    rep = {
        "{{S12_MOYEN_AGE}}": moyen_age(),
        "{{S12_OLIVETAN}}": olivetan(),
        "{{S12_COMPARATEUR}}": comparateur(),
        "{{S12_NOM}}": nom_divin(),
        "{{S12_FOYERS}}": foyers(),
        "{{S12_AUJOURDHUI}}": aujourdhui(),
        "{{S12_QUIZ}}": quiz(),
        "{{S12_TR_A}}": TR_A,
        "{{S12_TR_B}}": TR_B,
        "{{IMG_MOYEN_AGE}}": img("moyen-age", "Un manuscrit enluminé ouvert sur un pupitre de bois, ses deux colonnes d'écriture gothique encadrées de rinceaux dorés et de petites peintures",
                                 "Une Bible historiale du XIVe siècle. Reconstitution numérique."),
        "{{IMG_VAUDOIS}}": img("vaudois", "Une soixantaine de montagnards assis dans un alpage écoutent un homme qui lit un livre ouvert, devant des sommets enneigés",
                               "Chanforan, septembre 1532 : le synode vaudois décide de financer une Bible française. Reconstitution numérique."),
        "{{IMG_OLIVETAN}}": img("olivetan", "Un jeune érudit coiffé d'une toque noire écrit à la plume, à la lueur d'une bougie, devant des livres hébreux et grecs ouverts",
                                "Olivétan au travail, vers 1534. Reconstitution numérique."),
        "{{IMG_BASTILLE}}": img("bastille", "Un prêtre aux cheveux gris écrit à la plume dans une salle de pierre, éclairée par une bougie et un étroit jour dans le mur",
                                "Lemaistre de Sacy à la Bastille, 1666-1668. Reconstitution numérique."),
        "{{IMG_COLPORTEUR}}": img("colporteur", "Un colporteur portant sur le dos une caisse de livres marche sur un sentier de montagne au lever du soleil, au-dessus d'un village de pierre",
                                  "Un colporteur biblique dans les Cévennes, vers 1850. Reconstitution numérique."),
        "{{IMG_SEGOND}}": img("segond", "Un vieil homme à barbe blanche écrit à son bureau, devant une fenêtre ouverte sur le lac Léman et les Alpes",
                              "Louis Segond à Genève, vers 1875. Reconstitution numérique."),
        "{{IMG_AUJOURDHUI}}": img("aujourdhui", "Une jeune femme lit une Bible ouverte dans une bibliothèque lumineuse, un téléphone posé à côté, devant les toits de Paris",
                                  "Lire la Bible en français aujourd'hui. Reconstitution numérique.", sizes="100vw"),
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S12_MOYEN_AGE}}{{S12_OLIVETAN}}{{S12_COMPARATEUR}}{{S12_NOM}}{{S12_FOYERS}}{{S12_AUJOURDHUI}}{{S12_QUIZ}}")
    assert "{{S12" not in out
    print("ok", len(out))
