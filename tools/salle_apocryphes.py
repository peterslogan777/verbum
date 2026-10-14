"""
VERBUM — Salle 06 « Les Textes apocryphes » (étape E08)
Marqueurs remplacés dans tools/templates/salles/apocryphes.html :
  {{S06_DECOUVERTES}}  frise des redécouvertes (1773 → 2006)
  {{S06_TABS}} / {{S06_PANELS}}   dossiers Thomas · Marie · Judas (onglets)
  {{S06_QUIZ}}         jeu « Canonique ou non ? » (données JSON)
  {{S06_JUDE}}         Jude 14-15 (grec + français) face à 1 Hénoch 1:9
  {{S06_HERMAS}}       Pasteur d'Hermas, Précepte 1 (grec intégral + français)
  {{S06_MURATORI}}     Canon de Muratori, lignes 73-80 (latin + français)
  {{S06_COMPARE}}      comparateur canon / apocryphes
  {{S06_CANON}}        frise de la formation du canon
  {{S06_TR_NAG}} / {{S06_TR_CANON}}   transcriptions des narrations
Règle du musée : tout texte non canonique porte un badge rouge, tout texte étranger est
immédiatement suivi de sa traduction française (traductions du musée).
"""
import html
import json

e = html.escape
B = {
    "canon": '<span class="badge badge-canon">Canonique</span>',
    "apo": '<span class="badge badge-apo">Apocryphe</span>',
    "noncanon": '<span class="badge badge-apo">Non canonique</span>',
    "debat": '<span class="badge badge-debat">Débattu</span>',
}

# --------------------------------------------------------------------------
# Frise des redécouvertes
# --------------------------------------------------------------------------
DECOUVERTES = [
    ("1773", "Hénoch revient d'Éthiopie", "L'explorateur écossais James Bruce rapporte en Europe des manuscrits guèzes du Livre d'Hénoch, perdu en Occident depuis l'Antiquité.", "apo"),
    ("1896", "Le Codex de Berlin", "Carl Reinhardt achète au Caire un codex copte du Ve siècle : il contient l'Évangile de Marie. Sa publication n'aura lieu qu'en 1955.", "apo"),
    ("1897 – 1904", "Des « paroles de Jésus » à Oxyrhynque", "Grenfell et Hunt publient trois fragments grecs de paroles attribuées à Jésus. On ne saura qu'après 1945 qu'ils appartiennent à l'Évangile de Thomas.", "apo"),
    ("1938", "Un fragment grec de Marie", "Le papyrus Rylands 463 (IIIe siècle) livre un passage grec de l'Évangile de Marie.", "apo"),
    ("1945", "La jarre de Nag Hammadi", "Douze codex de papyrus et des feuillets d'un treizième : 52 écrits, presque tous inconnus, dont l'Évangile de Thomas.", "apo"),
    ("1952", "Hénoch à Qumrân", "Dans la grotte 4, des fragments araméens du Livre d'Hénoch (4Q201-4Q212) prouvent son ancienneté.", "apo"),
    ("Années 1970", "Un codex dans une tombe", "Près de Maghagha (Moyenne-Égypte), un codex copte est découvert : le futur Codex Tchacos, qui contient l'Évangile de Judas.", "apo"),
    ("2006", "Judas publié", "Après des années chez des marchands, le codex brisé en près de mille fragments est restauré et publié. Il doit rejoindre le Musée copte du Caire.", "apo"),
]


def decouvertes():
    out = []
    for d, t, p, b in DECOUVERTES:
        out.append(f'<li data-reveal><span class="dv-d">{e(d)}</span><div><h4>{e(t)} {B[b]}</h4><p>{e(p)}</p></div></li>')
    return "".join(out)


# --------------------------------------------------------------------------
# Dossiers : Thomas · Marie · Judas
# --------------------------------------------------------------------------
DOSSIERS = [
    dict(
        key="thomas", tab="Évangile de Thomas", img="oxy654",
        alt="Un fragment de papyrus grec déchiré, couvert d'une quarantaine de lignes d'écriture, sur fond noir",
        cap="Un fragment grec de papyrus : reconstitution numérique inspirée du papyrus d'Oxyrhynque 654.",
        titre="L'Évangile selon Thomas",
        accroche="114 paroles attribuées à Jésus, sans récit de sa vie, de sa mort ni de sa résurrection.",
        fiche=[("Rédaction", "IIe siècle selon la majorité des spécialistes (vers 120 – 150) ; certains défendent un noyau plus ancien"),
               ("Manuscrits", "1 copie copte complète (Nag Hammadi, codex II, vers 350) et 3 fragments grecs d'Oxyrhynque (vers 200 – 250)"),
               ("Langue d'origine", "Grec, puis traduit en copte"),
               ("Conservation", "Musée copte du Caire · British Library · Bodleian Library · Harvard")],
        debat=True,
        resume=[
            "L'ouvrage se présente comme une suite de « paroles secrètes » introduites par la formule « Jésus dit ». Environ la moitié ont un équivalent, plus ou moins proche, dans Matthieu, Marc ou Luc : paraboles du semeur, de la graine de moutarde, du festin ; le prophète méprisé dans sa patrie ; l'aveugle qui guide un aveugle.",
            "Les autres paroles sont propres à Thomas et souvent énigmatiques. Elles insistent sur la connaissance de soi (« Quand vous vous connaîtrez, vous serez connus »), sur un Royaume déjà présent « au-dedans de vous et au-dehors de vous », sur le retour à l'origine et sur la figure du « solitaire » qui se détache du monde.",
            "Il n'y a ni naissance, ni miracle raconté, ni passion, ni résurrection : le salut vient de la juste interprétation des paroles. La dernière parole (114), sur Marie devenant « mâle » pour entrer dans le Royaume, montre l'écart avec les Évangiles canoniques.",
        ],
        extrait_titre="Le début, dans le papyrus grec d'Oxyrhynque 654 (vers 250)",
        extrait=[
            ("Prologue", "Οὗτοι οἱ λόγοι οἱ [ἀπόκρυφοι οὓς ἐλά]λησεν Ἰη(σοῦ)ς ὁ ζῶν κ[αὶ ἔγραψεν Ἰούδα ὁ] καὶ Θωμᾶ.",
             "Voici les paroles [secrètes] qu'a prononcées Jésus le Vivant, et qu'a écrites [Judas, appelé] aussi Thomas."),
            ("Parole 1", "καὶ εἶπεν· [ὃς ἂν τὴν ἑρμηνεί]αν τῶν λόγων τούτ[ων εὕρῃ, θανάτου] οὐ μὴ γεύσηται.",
             "Et il a dit : « [Celui qui trouvera l'interpré]tation de ces paroles ne goûtera pas [la mort]. »"),
            ("Parole 2", "[λέγει Ἰη(σοῦ)ς· μὴ παυσάσθω ὁ ζη]τῶν τοῦ ζητεῖν ἕως ἂν εὕρῃ, καὶ ὅταν εὕρῃ [θαμβηθήσεται, καὶ θαμ]βηθεὶς βασιλεύσει, κα[ὶ βασιλεύσας ἀναπα]ήσεται.",
             "[Jésus dit : « Que celui qui cher]che ne cesse pas de chercher jusqu'à ce qu'il trouve ; et quand il aura trouvé, [il sera stupéfait ; et, stu]péfait, il régnera ; et, [ayant régné, il trouvera le re]pos. »"),
        ],
        extrait_note="Entre crochets : lettres perdues, restituées d'après la version copte (restitution courante, d'après H. Attridge). Sur le papyrus, le nom de Jésus est abrégé.",
        pourquoi=["Rédaction plus tardive que les écrits des apôtres et de leurs proches",
                  "Aucun auteur chrétien des premiers siècles ne le cite comme Écriture ; Eusèbe de Césarée (vers 325) le range parmi les écrits hérétiques",
                  "Enseignement de type ésotérique : le salut par une connaissance secrète, sans la mort et la résurrection de Jésus"],
        liens=[("Papyrus d'Oxyrhynque 654 · transcription (papyri.info)", "https://papyri.info/dclp/62840"),
               ("Archives photographiques de Nag Hammadi (Claremont)", "https://ccdl.claremont.edu/digital/collection/nha")],
    ),
    dict(
        key="marie", tab="Évangile de Marie", img="berlin",
        alt="Un codex de papyrus copte ancien ouvert sous verre ; la page de gauche n'est plus qu'une suite de lambeaux",
        cap="Un codex copte incomplet : reconstitution numérique inspirée du Codex de Berlin.",
        titre="L'Évangile de Marie",
        accroche="Un dialogue après la résurrection, dont la moitié des pages a disparu.",
        fiche=[("Rédaction", "IIe siècle"),
               ("Manuscrits", "1 copie copte incomplète (Codex de Berlin 8502, Ve siècle) et 2 fragments grecs du IIIe siècle (Rylands 463, Oxyrhynque 3525)"),
               ("État", "Pages 1 à 6 et 11 à 14 perdues : il reste environ la moitié du texte"),
               ("Conservation", "Musée égyptien et Collection de papyrus de Berlin · John Rylands Library · Oxford")],
        debat=False,
        resume=[
            "Le texte s'ouvre au milieu d'un dialogue : le Sauveur répond aux questions des disciples sur la matière et sur le péché, puis les envoie annoncer l'Évangile du Royaume avant de les quitter.",
            "Les disciples sont abattus et ont peur. Marie (que la tradition identifie à Marie-Madeleine, bien que le texte dise seulement « Marie ») les réconforte. Pierre lui demande de leur rapporter les paroles du Sauveur qu'elle seule connaît. Elle raconte alors une vision.",
            "Après une lacune de quatre pages, on lit la montée de l'âme qui franchit quatre « puissances » hostiles (Ténèbres, Désir, Ignorance, Colère) en répondant à leurs questions. André et Pierre contestent vivement ces enseignements ; Lévi prend la défense de Marie. Les disciples partent enfin prêcher.",
            "Les thèmes (âme prisonnière de la matière, ascension à travers des puissances) rattachent ce texte aux courants gnostiques du IIe siècle.",
        ],
        extrait_titre="Un passage (Codex de Berlin, page 8) · traduit du copte",
        extrait=[("Page 8", None, "« Prenez garde que personne ne vous égare en disant : “Le voici !” ou “Le voilà !” Car le Fils de l'homme est au-dedans de vous. Suivez-le ! Ceux qui le cherchent le trouveront. »")],
        extrait_note="L'original est en copte, une langue égyptienne écrite avec un alphabet dérivé du grec. Le passage fait écho à Luc 17:21 et Matthieu 24:23, mais leur donne un sens intérieur.",
        pourquoi=["Texte tardif, connu seulement par trois manuscrits",
                  "Absent de toutes les listes d'écrits reçus dans les Églises",
                  "Enseignement gnostique sur l'âme et les puissances, étranger aux écrits des apôtres"],
        liens=[],
    ),
    dict(
        key="judas", tab="Évangile de Judas", img="tchacos",
        alt="Une restauratrice reconstitue à la pince des centaines de minuscules fragments de papyrus sur une plaque de verre",
        cap="La restauration d'un codex brisé : reconstitution numérique inspirée du Codex Tchacos.",
        titre="L'Évangile de Judas",
        accroche="Un texte connu par Irénée vers 180, retrouvé en un seul exemplaire brisé en près de mille fragments.",
        fiche=[("Rédaction", "IIe siècle (avant 180, date à laquelle Irénée de Lyon le mentionne)"),
               ("Manuscrit", "1 seule copie copte : le Codex Tchacos, daté par le carbone 14 entre 220 et 340"),
               ("Découverte", "Années 1970, près de Maghagha (Égypte) ; publié en 2006"),
               ("Conservation", "Destiné au Musée copte du Caire")],
        debat=True,
        resume=[
            "Le texte se présente comme « le récit secret de la révélation que Jésus a faite à Judas Iscariote » pendant huit jours, trois jours avant la Pâque.",
            "Jésus y rit des disciples qui rendent grâce à Dieu, car pour l'auteur, ce dieu n'est qu'une puissance inférieure. Il révèle à Judas seul un vaste système de mondes célestes, d'éons et d'anges (Barbélo, l'Autogène, Saklas…), typique de la pensée gnostique dite « séthienne ».",
            "Le récit s'achève brutalement : Judas reçoit de l'argent des grands prêtres et leur livre Jésus. Il n'y a ni crucifixion ni résurrection.",
            "Irénée de Lyon, vers 180, signalait déjà ce livre comme une « histoire inventée » par un groupe gnostique (Contre les hérésies, I, 31, 1).",
        ],
        extrait_titre="La phrase la plus discutée (page 56) · traduite du copte",
        extrait=[("Page 56", None, "« Toi, tu les surpasseras tous. Car tu sacrifieras l'homme qui me sert d'enveloppe. »")],
        extrait_note="En 2006, la première publication présentait un Judas « héros », ami privilégié de Jésus. D'autres spécialistes, notamment April DeConick (2007), ont contesté plusieurs traductions : Judas y est appelé « treizième démon » et son destin reste tragique.",
        pourquoi=["Texte rejeté dès le IIe siècle par Irénée, comme invention d'un groupe gnostique",
                  "Rédaction bien postérieure aux événements, sans lien avec les apôtres",
                  "Doctrine opposée aux Écritures hébraïques : le Dieu créateur y est une puissance inférieure"],
        liens=[],
    ),
]


def tabs():
    return "".join(
        f'<button type="button" role="tab" id="tab-{d["key"]}" aria-controls="dos-{d["key"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span>{e(d["tab"])}</span><small>Apocryphe</small></button>'
        for i, d in enumerate(DOSSIERS))


def panels():
    out = []
    for i, d in enumerate(DOSSIERS):
        fiche = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in d["fiche"])
        resume = "".join(f"<p>{e(p)}</p>" for p in d["resume"])
        ex = []
        for lab, grc, fr in d["extrait"]:
            g = f'<p class="ex-grc" lang="grc">{e(grc)}</p>' if grc else ""
            ex.append(f'<li><span class="ex-lab">{e(lab)}</span>{g}<p class="ex-fr">{e(fr)}</p></li>')
        pq = "".join(f"<li>{e(p)}</li>" for p in d["pourquoi"])
        liens = "".join(f'<a class="btn btn-ghost btn-sm" href="{u}" target="_blank" rel="noopener">Voir l\'original · {e(t)} {{{{ARROW}}}}</a>' for t, u in d["liens"])
        if not liens:
            liens = '<p class="dos-nolink">Aucune numérisation officielle librement consultable à ce jour.</p>'
        badges = B["apo"] + (B["debat"] if d["debat"] else "")
        im = f'{{{{ROOT}}}}assets/img/salles/06/{d["img"]}'
        out.append(f'''
<div class="dos" role="tabpanel" id="dos-{d["key"]}" aria-labelledby="tab-{d["key"]}"{"" if i == 0 else " hidden"}>
  <div class="dos-top">
    <figure class="dos-fig">
      <img src="{im}-960.jpg" srcset="{im}-960.jpg 960w, {im}.jpg 1920w" sizes="(max-width: 1000px) 100vw, 45vw" alt="{e(d["alt"])}" loading="lazy" decoding="async"
           data-lightbox data-full="{im}.jpg" data-caption="{e(d["cap"])}">
      <figcaption><span class="tag">Reconstitution</span> {e(d["cap"])}</figcaption>
    </figure>
    <div class="dos-id">
      <div class="badges">{badges}</div>
      <h3>{e(d["titre"])}</h3>
      <p class="dos-acc">{e(d["accroche"])}</p>
      <dl class="dos-fiche">{fiche}</dl>
    </div>
  </div>
  <div class="dos-grid">
    <div class="dos-resume"><p class="ch-k">Résumé détaillé du contenu</p>{resume}</div>
    <div class="dos-side">
      <div class="dos-ex"><p class="ch-k">{e(d["extrait_titre"])}</p><ol>{"".join(ex)}</ol><p class="ex-note">{e(d["extrait_note"])}</p></div>
      <div class="dos-pq"><p class="ch-k">Pourquoi n'est-il pas dans la Bible ?</p><ul>{pq}</ul></div>
      <div class="dos-liens">{liens}</div>
    </div>
  </div>
</div>''')
    return "".join(out)


# --------------------------------------------------------------------------
# Jeu « Canonique ou non ? »
# --------------------------------------------------------------------------
QUIZ = [
    dict(q="« Demandez, et l'on vous donnera ; cherchez, et vous trouverez ; frappez, et l'on vous ouvrira. »",
         r="canon", src="Matthieu 7:7", ex="Une parole du Sermon sur la montagne, présente dans Matthieu et dans Luc (11:9)."),
    dict(q="« Fendez le bois : je suis là. Soulevez la pierre, et vous me trouverez là. »",
         r="apo", src="Évangile de Thomas, parole 77", ex="Une parole propre à Thomas, déjà connue en grec par le papyrus d'Oxyrhynque 1 (vers 200)."),
    dict(q="« Vous connaîtrez la vérité, et la vérité vous rendra libres. »",
         r="canon", src="Jean 8:32", ex="Une parole de Jésus rapportée par l'Évangile de Jean."),
    dict(q="« Prenez garde que personne ne vous égare en disant : “Le voici !” ou “Le voilà !” Car le Fils de l'homme est au-dedans de vous. »",
         r="apo", src="Évangile de Marie, page 8", ex="Piège : la phrase reprend Luc 17:21 et Matthieu 24:23, mais le texte est celui de l'Évangile de Marie (IIe siècle)."),
    dict(q="« Avant toute chose, crois qu'il n'y a qu'un seul Dieu, qui a créé et organisé toutes choses. »",
         r="apo", b="Non canonique", src="Pasteur d'Hermas, Précepte 1", ex="Piège : l'enseignement est parfaitement conforme aux Écritures, mais le Pasteur d'Hermas n'a jamais été reçu dans le canon. Une doctrine juste ne suffit pas : il faut aussi une origine apostolique."),
    dict(q="« Voici, Jéhovah est venu avec ses saintes myriades, pour exercer le jugement contre tous. »",
         r="canon", src="Jude 14-15", ex="Piège : la lettre canonique de Jude cite ici une prophétie du Livre d'Hénoch (1:9). Citer un livre ne le rend pas canonique : Paul cite aussi des poètes grecs (Actes 17:28)."),
    dict(q="« Toi, tu les surpasseras tous. Car tu sacrifieras l'homme qui me sert d'enveloppe. »",
         r="apo", src="Évangile de Judas, page 56", ex="Une phrase de l'Évangile de Judas, connue par un seul manuscrit copte (220 – 340)."),
    dict(q="« L'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours. »",
         r="canon", src="Ésaïe 40:8", ex="Le verset qui sert de fil conducteur à ce musée, lu tel quel dans le Grand Rouleau d'Ésaïe de Qumrân."),
]


def quiz():
    return e(json.dumps(QUIZ, ensure_ascii=False))


# --------------------------------------------------------------------------
# Hénoch : Jude 14-15 face à 1 Hénoch 1:9
# --------------------------------------------------------------------------
JUDE_GRC = ("Προεφήτευσεν δὲ καὶ τούτοις ἕβδομος ἀπὸ Ἀδὰμ Ἑνὼχ λέγων· ἰδοὺ ἦλθεν κύριος ἐν ἁγίαις μυριάσιν αὐτοῦ "
            "ποιῆσαι κρίσιν κατὰ πάντων καὶ ἐλέγξαι πάντας τοὺς ἀσεβεῖς περὶ πάντων τῶν ἔργων ἀσεβείας αὐτῶν ὧν ἠσέβησαν "
            "καὶ περὶ πάντων τῶν σκληρῶν ὧν ἐλάλησαν κατ᾽ αὐτοῦ ἁμαρτωλοὶ ἀσεβεῖς.")
JUDE_FR = ("« C'est aussi pour eux qu'Hénoch, le septième depuis Adam, a prophétisé en disant : “Voici, Jéhovah est venu avec ses saintes myriades, "
           "pour exercer le jugement contre tous et pour convaincre tous les impies de toutes les œuvres d'impiété qu'ils ont commises, "
           "et de toutes les paroles dures que les pécheurs impies ont prononcées contre lui.” »")
HENOCH_FR = ("« Et voici, il vient avec des myriades de saints pour exercer le jugement contre tous, pour faire périr les impies "
             "et convaincre toute chair de toutes les œuvres d'impiété qu'ils ont commises, et de toutes les paroles dures "
             "que les pécheurs impies ont prononcées contre lui. »")


def jude():
    return f'''
<div class="jh-col is-canon">
  <div class="jh-head">{B["canon"]}<b>Jude 14-15</b><small>Nouveau Testament · texte grec (Nestle-Aland 27)</small></div>
  <p class="jh-grc" lang="grc">{e(JUDE_GRC)}</p>
  <p class="jh-fr">{e(JUDE_FR)}</p>
  <p class="jh-note">Le titre grec κύριος (« Seigneur ») désigne ici Dieu : le musée rend le nom divin par « Jéhovah », selon sa convention.</p>
</div>
<div class="jh-col is-apo">
  <div class="jh-head">{B["apo"]}<b>1 Hénoch 1:9</b><small>Traduit d'après les versions guèze et grecque</small></div>
  <p class="jh-fr">{e(HENOCH_FR)}</p>
  <p class="jh-note">Un fragment araméen de ce passage a été retrouvé à Qumrân (4Q204). Jude cite une prophétie qu'il juge vraie, sans faire pour autant du livre entier une Écriture.</p>
</div>'''


# --------------------------------------------------------------------------
# Hermas & Muratori
# --------------------------------------------------------------------------
HERMAS_GRC = ("Πρῶτον πάντων πίστευσον, ὅτι εἷς ἐστὶν ὁ θεός, ὁ τὰ πάντα κτίσας καὶ καταρτίσας, καὶ ποιήσας ἐκ τοῦ μὴ ὄντος "
              "εἰς τὸ εἶναι τὰ πάντα, καὶ πάντα χωρῶν, μόνος δὲ ἀχώρητος ὤν. Πίστευσον οὖν αὐτῷ καὶ φοβήθητι αὐτόν, "
              "φοβηθεὶς δὲ ἐγκράτευσαι. Ταῦτα φύλασσε, καὶ ἀποβαλεῖς πᾶσαν πονηρίαν ἀπὸ σεαυτοῦ καὶ ἐνδύσῃ πᾶσαν ἀρετὴν "
              "δικαιοσύνης καὶ ζήσῃ τῷ θεῷ, ἐὰν φυλάξῃς τὴν ἐντολὴν ταύτην.")
HERMAS_FR = ("« Avant toute chose, crois qu'il n'y a qu'un seul Dieu, qui a créé et organisé toutes choses, qui a fait passer "
             "toutes choses du néant à l'existence, qui contient tout et que seul rien ne peut contenir. Crois donc en lui et crains-le, "
             "et, le craignant, maîtrise-toi. Observe ces choses : tu rejetteras loin de toi toute méchanceté, tu revêtiras toute vertu "
             "de justice et tu vivras pour Dieu, si tu gardes ce commandement. »")
MURATORI_LAT = ("Pastorem vero nuperrime temporibus nostris in urbe Roma Hermas conscripsit, sedente cathedra urbis Romae ecclesiae "
                "Pio episcopo fratre eius; et ideo legi eum quidem oportet, se publicare vero in ecclesia populo neque inter prophetas, "
                "completo numero, neque inter apostolos in finem temporum potest.")
MURATORI_FR = ("« Quant au Pasteur, Hermas l'a écrit tout récemment, de notre temps, dans la ville de Rome, alors que son frère, l'évêque Pie, "
               "occupait le siège de l'Église de Rome. C'est pourquoi il convient certes de le lire, mais on ne peut pas le lire publiquement "
               "à l'assemblée, ni parmi les prophètes, dont le nombre est complet, ni parmi les apôtres, jusqu'à la fin des temps. »")


def hermas():
    return (f'<p class="ch-k">Texte intégral du Précepte 1 · grec, puis traduction française</p>'
            f'<p class="tx-orig" lang="grc">{e(HERMAS_GRC)}</p><p class="tx-fr">{e(HERMAS_FR)}</p>')


def muratori():
    return (f'<p class="ch-k">Canon de Muratori, lignes 73 à 80 · latin (orthographe normalisée), puis traduction française</p>'
            f'<p class="tx-orig tx-lat" lang="la">{e(MURATORI_LAT)}</p><p class="tx-fr">{e(MURATORI_FR)}</p>')


# --------------------------------------------------------------------------
# Comparateur
# --------------------------------------------------------------------------
# nom, badge, rédaction (texte), fourchette de rédaction en années ap. J.-C. [min, max], manuscrits avant 400 (≈), texte
COMPARE = [
    ("Les 4 Évangiles canoniques", "canon", "≈ 60 – 100", (60, 100), 40, "Plusieurs dizaines de papyrus (P52, P66, P75…), puis les grands codex"),
    ("Évangile de Thomas", "apo", "≈ 120 – 150 (débattu)", (120, 150), 4, "3 fragments grecs et 1 copie copte"),
    ("Évangile de Marie", "apo", "IIe siècle", (100, 200), 2, "2 fragments grecs ; la copie copte date du Ve siècle"),
    ("Évangile de Judas", "apo", "≈ 130 – 170", (130, 170), 1, "1 seule copie copte"),
]


def compare():
    mx = 200; mxn = 40
    rows = []
    for nom, b, red, (a, z), n, ms in COMPARE:
        rows.append(f'<li class="{"is-canon" if b == "canon" else "is-apo"}" style="--a:{a / mx:.3f};--z:{z / mx:.3f};--m:{n / mxn:.3f}">'
                    f'<div class="cp-nom"><b>{e(nom)}</b>{B[b]}</div>'
                    f'<div class="cp-g" data-crit="ecart"><span class="cp-track"><i></i></span><span class="cp-v">{e(red)} ap. J.-C.</span></div>'
                    f'<div class="cp-g" data-crit="mss"><span class="cp-track"><i></i></span><span class="cp-v">{"≈ " if n > 4 else ""}{n} · {e(ms)}</span></div></li>')
    return '<ul class="cp-l">' + "".join(rows) + "</ul>"


# --------------------------------------------------------------------------
# Formation du canon
# --------------------------------------------------------------------------
CANON = [
    ("≈ 180", "Irénée de Lyon", "Il affirme qu'il y a quatre Évangiles, « ni plus, ni moins », et dénonce l'Évangile de Judas comme une invention.", None),
    ("Fin du IIe s.", "Le Canon de Muratori", "La plus ancienne liste connue des écrits lus à Rome : elle écarte le Pasteur d'Hermas, « écrit récemment ».", "debat"),
    ("≈ 250", "Origène", "Il distingue les écrits reconnus partout de ceux qui sont discutés.", None),
    ("≈ 325", "Eusèbe de Césarée", "Il classe les livres : reconnus, discutés, inauthentiques (dont Hermas) et hérétiques (dont Thomas).", None),
    ("367", "Athanase d'Alexandrie", "Sa 39e Lettre festale énumère les 27 livres du Nouveau Testament et range Hermas parmi les livres utiles aux débutants.", None),
    ("397", "Synode de Carthage", "Il reprend la même liste de 27 livres : il confirme un usage déjà établi, il ne l'invente pas.", None),
]


def canon():
    out = []
    for d, t, p, b in CANON:
        badge = ' <span class="badge badge-debat">Date débattue</span>' if b else ""
        out.append(f'<li data-reveal><span class="cn-d">{e(d)}</span><h4>{e(t)}{badge}</h4><p>{e(p)}</p></li>')
    return "".join(out)


# --------------------------------------------------------------------------
TR_NAG = """<p>Décembre 1945. Au pied des falaises du Djebel el-Tarif, près de Nag Hammadi, en Haute-Égypte, des paysans creusent la terre pour y chercher un engrais naturel. Leur pioche heurte une grande jarre de terre cuite, scellée. À l'intérieur : une douzaine de livres de papyrus reliés de cuir, enfouis depuis plus de quinze siècles. Ce sont des traductions coptes de textes grecs plus anciens, copiées au quatrième siècle. Parmi eux, un écrit va faire le tour du monde : l'Évangile selon Thomas. Il ne raconte ni la naissance, ni les miracles, ni la mort de Jésus. C'est un recueil de cent quatorze paroles, souvent énigmatiques, qui lui sont attribuées. Trois fragments grecs en avaient déjà été retrouvés à Oxyrhynque, sans que personne ne sache encore à quel livre ils appartenaient.</p>
<p>D'autres textes ont resurgi de la même façon. L'Évangile de Marie, acheté au Caire en 1896, ne nous est parvenu qu'à moitié : dix pages sur dix-neuf. L'Évangile de Judas, découvert dans les années 1970 et publié en 2006, n'existe qu'en un seul exemplaire, brisé en près de mille fragments. Ces écrits sont précieux pour l'historien. Ils montrent la diversité des courants qui se réclamaient du christianisme aux deuxième et troisième siècles, en particulier les courants gnostiques. Mais ils ne sont pas restés en dehors de la Bible par accident. Ils sont plus tardifs que les écrits des apôtres, leur enseignement s'en écarte, et ils n'ont jamais été reçus par l'ensemble des communautés. L'apocryphe éclaire l'histoire. Il ne remplace pas le canon.</p>"""

TR_CANON = """<p>Certains textes non canoniques n'ont rien de secret. Le Livre d'Hénoch, attribué à l'arrière-grand-père de Noé, raconte la chute des anges veilleurs et des visions du jugement. Il était lu au tournant de notre ère : une dizaine de manuscrits araméens en ont été retrouvés dans la quatrième grotte de Qumrân. La lettre de Jude en cite même une phrase. Pourtant, ni le canon hébreu ni la grande majorité des Églises ne l'ont reçu comme Écriture. Seule l'Église éthiopienne l'a conservé dans sa Bible, en langue guèze, et c'est grâce à elle que le livre nous est parvenu en entier. Le Pasteur d'Hermas, écrit à Rome au deuxième siècle, était si apprécié qu'on l'a recopié à la fin du Codex Sinaiticus, après le Nouveau Testament.</p>
<p>Mais une liste romaine, le Canon de Muratori, généralement datée de la fin du deuxième siècle, précise qu'on peut le lire en privé, et non dans l'assemblée, car il a été écrit récemment. Le critère est clair : ce qui fait autorité, c'est ce qui remonte aux apôtres et à leurs proches. En 367, Athanase, évêque d'Alexandrie, dresse la liste des vingt-sept livres du Nouveau Testament que nous connaissons, et il range Hermas parmi les livres utiles aux débutants, non parmi les Écritures. Le canon ne s'est donc pas décidé lors d'un concile tardif. Il s'est formé par l'usage, dans les communautés, autour des textes reconnus depuis les origines. Ce qui n'y est pas entré reste un témoignage d'histoire, que ce musée vous invite à découvrir, en le distinguant clairement de l'Écriture.</p>"""


def render(inner):
    rep = {
        "{{S06_DECOUVERTES}}": decouvertes(), "{{S06_TABS}}": tabs(), "{{S06_PANELS}}": panels(),
        "{{S06_QUIZ}}": quiz(), "{{S06_JUDE}}": jude(), "{{S06_HERMAS}}": hermas(), "{{S06_MURATORI}}": muratori(),
        "{{S06_COMPARE}}": compare(), "{{S06_CANON}}": canon(),
        "{{S06_TR_NAG}}": TR_NAG, "{{S06_TR_CANON}}": TR_CANON,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S06_DECOUVERTES}}{{S06_TABS}}{{S06_PANELS}}{{S06_QUIZ}}{{S06_JUDE}}{{S06_COMPARE}}{{S06_CANON}}")
    print(len(out), "{{S06" in out)
