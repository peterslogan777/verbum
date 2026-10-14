"""
VERBUM — Salle 04 « Les Grands Codex grecs » (étape E06)
Marqueurs remplacés dans tools/templates/salles/codex-grecs.html :
  {{S04_P52_RECTO}} / {{S04_P52_VERSO}}   fragment P52 interactif (lettres conservées / restituées)
  {{S04_P64}}          P64 : texte grec intégral des versets conservés + traduction française
  {{S04_CODEX}}        cartes 3D des trois grands codex (+ Évangiles de Garima)
  {{S04_SINAI}}        frise de l'histoire du Codex Sinaiticus
  {{S04_FEUILLETS}}    répartition des feuillets du Sinaiticus
  {{S04_CHART}}        comparaison avec d'autres œuvres antiques
  {{S04_TR_PAPYRUS}} / {{S04_TR_CODEX}}   transcriptions des narrations
Textes grecs : texte standard (Nestle-Aland). Les lettres « conservées » de P52 suivent la
transcription publiée de C. H. Roberts (1935) ; leur découpage est une approximation.
"""
import html

e = html.escape

# --------------------------------------------------------------------------
# P52 — chaque ligne : (partie conservée, partie perdue) ; côté où se trouve la partie conservée
# --------------------------------------------------------------------------
P52_RECTO = [  # recto : début des lignes conservé
    ("ΟΙ ΙΟΥΔΑΙΟΙ ΗΜΕΙΝ", " ΟΥΚ ΕΞΕΣΤΙΝ ΑΠΟΚΤΕΙΝΑΙ"),
    ("ΟΥΔΕΝΑ ΙΝΑ Ο Λ", "ΟΓΟΣ ΤΟΥ ΙΗΣΟΥ ΠΛΗΡΩΘΗ ΟΝ ΕΙ-"),
    ("ΠΕΝ ΣΗΜΑΙΝΩ", "Ν ΠΟΙΩ ΘΑΝΑΤΩ ΗΜΕΛΛΕΝ ΑΠΟ-"),
    ("ΘΝΗΣΚΕΙΝ ΙΣ", "ΗΛΘΕΝ ΟΥΝ ΠΑΛΙΝ ΕΙΣ ΤΟ ΠΡΑΙΤΩ-"),
    ("ΡΙΟΝ Ο Π", "ΙΛΑΤΟΣ ΚΑΙ ΕΦΩΝΗΣΕΝ ΤΟΝ ΙΗΣΟΥΝ"),
    ("ΚΑΙ ΕΙΠ", "ΕΝ ΑΥΤΩ ΣΥ ΕΙ Ο ΒΑΣΙΛΕΥΣ ΤΩΝ ΙΟΥ-"),
    ("ΔΑΙΩΝ", ""),
]
P52_VERSO = [  # verso : fin des lignes conservée (perdu, conservé)
    ("ΒΑΣΙΛΕΥΣ ΕΙΜΙ ΕΓΩ ΕΙΣ ΤΟΥ", "ΤΟ ΓΕΓΕΝΝΗΜΑΙ"),
    ("ΚΑΙ ΕΛΗΛΥΘΑ ΕΙΣ ", "ΤΟΝ ΚΟΣΜΟΝ ΙΝΑ ΜΑΡΤΥ-"),
    ("ΡΗΣΩ ΤΗ ΑΛΗΘΕΙΑ ΠΑΣ Ο ΩΝ ", "ΕΚ ΤΗΣ ΑΛΗ-"),
    ("ΘΕΙΑΣ ΑΚΟΥΕΙ ΜΟΥ ΤΗΣ ΦΩΝΗΣ ", "ΛΕΓΕΙ ΑΥΤΩ"),
    ("Ο ΠΙΛΑΤΟΣ ΤΙ ΕΣΤΙΝ ΑΛΗΘΕΙΑ ", "ΚΑΙ ΤΟΥΤΟ"),
    ("ΕΙΠΩΝ ΠΑΛΙΝ ΕΞΗΛΘΕΝ ΠΡΟΣ ", "ΤΟΥΣ ΙΟΥ-"),
    ("ΔΑΙΟΥΣ ΚΑΙ ΛΕΓΕΙ ΑΥΤΟΙΣ ΕΓΩ ", "ΟΥΔΕΜΙ-"),
    ("ΑΝ ΕΥΡΙΣΚΩ ΕΝ ΑΥΤΩ ΑΙΤΙΑΝ", ""),
]
P52_FR_RECTO = ("Les Juifs lui dirent : « Il ne nous est pas permis de mettre quelqu'un à mort. » "
                "Ainsi s'accomplissait la parole que Jésus avait dite pour indiquer de quelle mort il allait mourir. "
                "Pilate rentra donc dans le prétoire, appela Jésus et lui dit : « Es-tu le roi des Juifs ? »")
P52_FR_VERSO = ("« … Je suis roi. Si je suis né, et si je suis venu dans le monde, c'est pour rendre témoignage à la vérité. "
                "Quiconque est de la vérité écoute ma voix. » Pilate lui dit : « Qu'est-ce que la vérité ? » "
                "Après avoir dit cela, il sortit de nouveau vers les Juifs et leur dit : « Je ne trouve en lui aucun motif de condamnation. »")


def p52_face(lines, cote):
    out = []
    for a, b in lines:
        if cote == "recto":
            kept, lost = a, b
            inner = f'<span class="k">{e(kept)}</span><span class="l">{e(lost)}</span>' if kept else f'<span class="l">{e(lost)}</span>'
        else:
            lost, kept = a, b
            inner = f'<span class="l">{e(lost)}</span><span class="k">{e(kept)}</span>' if kept else f'<span class="l">{e(lost)}</span>'
        out.append(f'<span class="p52-l">{inner}</span>')
    return "".join(out)


# --------------------------------------------------------------------------
# P64 — Matthieu 26 (fragments de Magdalen College, Oxford)
# --------------------------------------------------------------------------
P64 = [
    ("26:7", "προσῆλθεν αὐτῷ γυνὴ ἔχουσα ἀλάβαστρον μύρου βαρυτίμου καὶ κατέχεεν ἐπὶ τῆς κεφαλῆς αὐτοῦ ἀνακειμένου.",
     "Une femme s'approcha de lui avec un flacon d'albâtre contenant un parfum de grand prix, et elle le versa sur sa tête pendant qu'il était à table."),
    ("26:8", "ἰδόντες δὲ οἱ μαθηταὶ ἠγανάκτησαν λέγοντες· εἰς τί ἡ ἀπώλεια αὕτη;",
     "En voyant cela, les disciples s'indignèrent et dirent : « À quoi bon ce gaspillage ? »"),
    ("26:10", "γνοὺς δὲ ὁ Ἰησοῦς εἶπεν αὐτοῖς· τί κόπους παρέχετε τῇ γυναικί; ἔργον γὰρ καλὸν ἠργάσατο εἰς ἐμέ·",
     "Jésus, s'en apercevant, leur dit : « Pourquoi tourmentez-vous cette femme ? C'est une belle action qu'elle a faite envers moi. »"),
    ("26:14", "Τότε πορευθεὶς εἷς τῶν δώδεκα, ὁ λεγόμενος Ἰούδας Ἰσκαριώτης, πρὸς τοὺς ἀρχιερεῖς",
     "Alors l'un des Douze, appelé Judas Iscariote, alla trouver les chefs des prêtres"),
    ("26:15", "εἶπεν· τί θέλετέ μοι δοῦναι, κἀγὼ ὑμῖν παραδώσω αὐτόν; οἱ δὲ ἔστησαν αὐτῷ τριάκοντα ἀργύρια.",
     "et dit : « Que voulez-vous me donner, et je vous le livrerai ? » Ils lui fixèrent trente pièces d'argent."),
    ("26:22", "καὶ λυπούμενοι σφόδρα ἤρξαντο λέγειν αὐτῷ εἷς ἕκαστος· μήτι ἐγώ εἰμι, κύριε;",
     "Profondément attristés, ils se mirent à lui dire, chacun à son tour : « Ce n'est pas moi, Maître ? »"),
    ("26:23", "ὁ δὲ ἀποκριθεὶς εἶπεν· ὁ ἐμβάψας μετ’ ἐμοῦ τὴν χεῖρα ἐν τῷ τρυβλίῳ οὗτός με παραδώσει.",
     "Il répondit : « Celui qui a mis avec moi la main dans le plat, c'est lui qui me livrera. »"),
    ("26:31", "Τότε λέγει αὐτοῖς ὁ Ἰησοῦς· πάντες ὑμεῖς σκανδαλισθήσεσθε ἐν ἐμοὶ ἐν τῇ νυκτὶ ταύτῃ, γέγραπται γάρ· πατάξω τὸν ποιμένα, καὶ διασκορπισθήσονται τὰ πρόβατα τῆς ποίμνης.",
     "Alors Jésus leur dit : « Vous trébucherez tous à cause de moi cette nuit, car il est écrit : Je frapperai le berger, et les brebis du troupeau seront dispersées. »"),
    ("26:32", "μετὰ δὲ τὸ ἐγερθῆναί με προάξω ὑμᾶς εἰς τὴν Γαλιλαίαν.",
     "« Mais après que j'aurai été relevé, je vous précéderai en Galilée. »"),
    ("26:33", "ἀποκριθεὶς δὲ ὁ Πέτρος εἶπεν αὐτῷ· εἰ πάντες σκανδαλισθήσονται ἐν σοί, ἐγὼ οὐδέποτε σκανδαλισθήσομαι.",
     "Pierre prit la parole et lui dit : « Même si tous trébuchent à cause de toi, moi, je ne trébucherai jamais. »"),
]


def p64():
    rows = "".join(f'<li><span class="v-n">{e(r)}</span><p class="v-grc" lang="grc">{e(g)}</p><p class="v-fr">{e(f)}</p></li>' for r, g, f in P64)
    return f'<ol class="vv">{rows}</ol>'


# --------------------------------------------------------------------------
# Les grands codex (cartes 3D : recto image, verso fiche)
# --------------------------------------------------------------------------
CODEX = [
    dict(key="vaticanus", sigle="B · 03", nom="Codex Vaticanus", img="vaticanus", date="≈ 300 – 350",
         lieu="Bibliothèque apostolique vaticane, Rome (Vat. gr. 1209)", badge="canon",
         fiche=[("Support", "Parchemin fin, ≈ 759 feuillets conservés"), ("Mise en page", "3 colonnes par page (2 pour les livres poétiques)"),
                ("Contenu", "Bible grecque presque complète ; manquent le début de la Genèse, une partie des Psaumes, la fin d'Hébreux, les lettres à Timothée, Tite, Philémon et la Révélation"),
                ("À retenir", "Son texte est très proche de celui du papyrus P75, copié plus d'un siècle plus tôt.")],
         lien=("https://digi.vatlib.it/view/MSS_Vat.gr.1209", "Voir l'original · DigiVatLib")),
    dict(key="sinaiticus", sigle="01 · « aleph » (première lettre hébraïque)", nom="Codex Sinaiticus", img="tischendorf", date="≈ 330 – 360",
         lieu="Londres, Leipzig, Saint-Pétersbourg et monastère Sainte-Catherine du Sinaï", badge="canon",
         fiche=[("Support", "Parchemin ; ≈ 400 feuillets conservés sur ≈ 730 à l'origine"), ("Mise en page", "4 colonnes par page, 48 lignes par colonne : un format unique"),
                ("Contenu", "Le plus ancien Nouveau Testament complet, avec une grande partie de l'Ancien Testament en grec"),
                ("En annexe", "L'Épître de Barnabé et une partie du Pasteur d'Hermas, deux écrits non canoniques")],
         lien=("https://www.codexsinaiticus.org/en/", "Voir l'original · codexsinaiticus.org")),
    dict(key="alexandrinus", sigle="A · 02", nom="Codex Alexandrinus", img="alexandrinus", date="Ve siècle",
         lieu="British Library, Londres (Royal MS 1 D V–VIII)", badge="canon",
         fiche=[("Support", "Parchemin, 773 feuillets, 4 volumes"), ("Mise en page", "2 colonnes par page"),
                ("Contenu", "Bible grecque presque complète ; il manque la plus grande partie de Matthieu (jusqu'à 25:6), une partie de Jean et de 2 Corinthiens"),
                ("Histoire", "Offert en 1627 par le patriarche Cyrille Loukaris au roi d'Angleterre Charles Ier ; il contient aussi les deux lettres de Clément, non canoniques")],
         lien=("https://www.bl.uk/collection-items/codex-alexandrinus", "Voir la notice · British Library")),
    dict(key="garima", sigle="Garima I et II", nom="Les Évangiles de Garima", img="garima", date="≈ 330 – 650 (radiocarbone)",
         lieu="Monastère d'Abba Garima, près d'Adoua (Tigré, Éthiopie)", badge="canon",
         fiche=[("Support", "Parchemin épais (peau de chèvre), deux volumes"), ("Langue", "Guèze, la langue liturgique éthiopienne, traduite du grec"),
                ("Contenu", "Les quatre Évangiles, avec des pages enluminées"),
                ("À retenir", "Longtemps datés des XIe – XIIe siècles, ils figurent parmi les plus anciens livres des Évangiles enluminés connus")],
         lien=None),
]

BADGES = {"canon": '<span class="badge badge-canon">Canonique</span>'}


def codex():
    out = []
    for i, c in enumerate(CODEX):
        dl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in c["fiche"])
        lien = (f'<a class="btn btn-or btn-sm" href="{c["lien"][0]}" target="_blank" rel="noopener">{e(c["lien"][1])} {{{{ARROW}}}}</a>'
                if c["lien"] else '<p class="cx-nolink">Pas d\'édition numérique publique à ce jour : les manuscrits restent au monastère.</p>')
        out.append(f"""
      <article class="cx" data-reveal style="--d:{i * 80}ms">
        <div class="cx-in">
          <div class="cx-face cx-front">
            <img src="{{{{ROOT}}}}assets/img/salles/04/{c['img']}-960.jpg" alt="" loading="lazy" decoding="async">
            <div class="cx-cap"><span class="cx-sigle">{e(c['sigle'])}</span><h3>{e(c['nom'])}</h3><p>{e(c['date'])}</p></div>
            <button type="button" class="cx-btn" aria-expanded="false" aria-label="Retourner la carte : fiche du {e(c['nom'])}">Fiche <span aria-hidden="true">↻</span></button>
          </div>
          <div class="cx-face cx-back">
            <div class="cx-top">{BADGES[c['badge']]}<span class="cx-sigle">{e(c['sigle'])}</span></div>
            <h3>{e(c['nom'])}</h3>
            <p class="cx-lieu">{e(c['lieu'])}</p>
            <dl>{dl}</dl>
            <div class="cx-actions">{lien}<button type="button" class="cx-btn cx-back-btn" aria-label="Revenir à l'image">↺ Retour</button></div>
          </div>
        </div>
      </article>""")
    return "".join(out)


# --------------------------------------------------------------------------
# Histoire du Sinaiticus
# --------------------------------------------------------------------------
SINAI = [
    ("≈ 330 – 360", "La copie", "Plusieurs scribes copient le codex, probablement en Palestine ou en Égypte. Des correcteurs le relisent pendant des siècles."),
    ("1844", "Première visite", "Constantin von Tischendorf voit au monastère Sainte-Catherine 129 feuillets de l'Ancien Testament et en emporte 43, aujourd'hui à Leipzig."),
    ("4 février 1859", "La grande découverte", "Lors de sa troisième visite, sous le patronage du tsar Alexandre II, on lui montre 347 feuillets, dont le Nouveau Testament complet."),
    ("1862", "Le fac-similé", "Tischendorf publie le texte en quatre volumes à Saint-Pétersbourg. Le manuscrit reste en Russie."),
    ("1933", "Londres", "Le gouvernement soviétique vend la partie russe au British Museum pour 100 000 livres sterling."),
    ("1975", "Les « nouvelles trouvailles »", "Des feuillets et des fragments supplémentaires sont découverts dans une salle du monastère."),
    ("2009", "Réuni en ligne", "Les quatre institutions publient ensemble l'intégralité du codex sur codexsinaiticus.org."),
]


def sinai():
    return "".join(f'<li data-reveal style="--d:{(i % 4) * 60}ms"><span class="sn-d">{e(d)}</span><h4>{e(t)}</h4><p>{e(p)}</p></li>'
                   for i, (d, t, p) in enumerate(SINAI))


FEUILLETS = [("Londres · British Library", 347, "Nouveau Testament complet et une grande partie de l'Ancien"),
             ("Leipzig · Bibliothèque universitaire", 43, "Feuillets emportés en 1844"),
             ("Sinaï · monastère Sainte-Catherine", 12, "12 feuillets et des dizaines de fragments (trouvailles de 1975)"),
             ("Saint-Pétersbourg · Bibliothèque nationale de Russie", 1, "Fragments de quelques feuillets")]


def feuillets():
    out = []
    for lieu, n, note in FEUILLETS:
        dots = "".join("<i></i>" for _ in range(n))
        lab = "fragments" if n == 1 else f"{n} feuillets"
        out.append(f'<li><div class="fe-k"><b>{e(lieu)}</b><span>{lab}</span></div><div class="fe-dots" aria-hidden="true">{dots}</div><p>{e(note)}</p></li>')
    return '<ul class="fe-list">' + "".join(out) + "</ul>"


# --------------------------------------------------------------------------
# Comparaison avec d'autres œuvres antiques (ordres de grandeur couramment cités)
# --------------------------------------------------------------------------
CHART = [  # œuvre, date de composition, nombre de manuscrits (≈), écart (≈ années) entre composition et plus ancien témoin substantiel
    ("Nouveau Testament (grec)", "Ier s. ap. J.-C.", 5800, 50, True),
    ("Homère, Iliade", "VIIIe s. av. J.-C. ?", 1900, 400, False),
    ("César, Guerre des Gaules", "Ier s. av. J.-C.", 250, 900, False),
    ("Tacite, Annales", "≈ 116 ap. J.-C.", 30, 750, False),
    ("Platon, Dialogues", "IVe s. av. J.-C.", 250, 1200, False),
]


def chart():
    mx_n = max(c[2] for c in CHART); mx_g = max(c[3] for c in CHART)
    rows = []
    for nom, date, n, g, nt in CHART:
        rows.append(f'<li class="{"is-nt" if nt else ""}" style="--n:{n / mx_n:.4f};--g:{g / mx_g:.4f}">'
                    f'<span class="ch-nom"><b>{e(nom)}</b><small>{e(date)}</small></span>'
                    f'<span class="ch-bar"><i></i></span>'
                    f'<span class="ch-val"><span class="v-n">≈ {f"{n:,}".replace(",", "\u202f")}</span><span class="v-g">≈ {g} ans</span></span></li>')
    return '<ul class="chart-l">' + "".join(rows) + "</ul>"


TR_PAPYRUS = """<p>Égypte, 1920. Dans un lot de papyrus acheté par le papyrologue Bernard Grenfell se cache un fragment pas plus grand qu'une carte de crédit. Il faudra attendre 1934 pour qu'un jeune chercheur d'Oxford, Colin Roberts, en reconnaisse le texte : quelques lignes de l'Évangile de Jean, au chapitre dix-huit. Jésus se tient devant Pilate. Sur une face, on lit : « Es-tu le roi des Juifs ? » Sur l'autre, la question du gouverneur : « Qu'est-ce que la vérité ? » Ce fragment, le papyrus Rylands 52, est généralement daté de la première moitié du deuxième siècle, entre cent et cent cinquante environ, même si certains spécialistes élargissent cette fourchette. Il est écrit des deux côtés : il ne provient donc pas d'un rouleau, mais d'un codex, l'ancêtre de nos livres. Quelques décennies seulement après la rédaction de l'Évangile, celui-ci était déjà copié et lu dans une ville de province égyptienne.</p>
<p>D'autres témoins ont suivi. Vers l'an deux cent, le papyrus Bodmer II, que les spécialistes appellent P66, conserve presque entièrement les quatorze premiers chapitres de Jean. Son copiste s'est relu et corrigé des centaines de fois : on voit, ligne après ligne, le souci d'exactitude. Le papyrus Bodmer XIV-XV, P75, contient une grande partie de Luc et de Jean. Or son texte est remarquablement proche de celui du Codex Vaticanus, copié plus d'un siècle plus tard. Entre ces deux témoins, le texte n'a pas dérivé : il a été transmis avec soin. Aujourd'hui, on recense plus de cent quarante papyrus du Nouveau Testament, et plus de cinq mille huit cents manuscrits grecs au total. Aucune autre œuvre de l'Antiquité n'approche une telle documentation.</p>"""

TR_CODEX = """<p>Au quatrième siècle, l'Empire romain cesse de persécuter les chrétiens. Les copistes peuvent désormais produire de grands volumes sur parchemin, contenant toute la Bible grecque. Trois de ces géants nous sont parvenus. Le Codex Vaticanus, conservé à la Bibliothèque vaticane depuis au moins le quinzième siècle, date du milieu du quatrième siècle. Il est copié sur trois colonnes, d'une écriture onciale élégante. Le Codex Sinaiticus, presque contemporain, est le plus ancien manuscrit contenant le Nouveau Testament complet. Il a été retrouvé au monastère Sainte-Catherine, au pied du mont Sinaï, par le savant allemand Constantin von Tischendorf, en 1844 puis en 1859. Ses feuillets sont aujourd'hui partagés entre Londres, Leipzig, Saint-Pétersbourg et le Sinaï, mais ils sont réunis virtuellement en ligne depuis 2009.</p>
<p>Le Codex Alexandrinus, copié au cinquième siècle, fut offert en 1627 au roi d'Angleterre Charles Ier par le patriarche Cyrille Loukaris. Il est aujourd'hui conservé à la British Library, à Londres. Plus au sud, sur les hauts plateaux d'Éthiopie, le monastère d'Abba Garima conserve deux livres des Évangiles en langue guèze. Longtemps crus médiévaux, ils ont été datés par le carbone 14 entre le quatrième et le septième siècle. Ces manuscrits ont été copiés sur des continents différents, dans des langues différentes, par des scribes qui ne se connaissaient pas. Et pourtant, ils transmettent le même message, avec les mêmes paroles. Comme l'annonçait Jésus lui-même : le ciel et la terre passeront, mais mes paroles ne passeront pas.</p>"""


def render(inner):
    rep = {
        "{{S04_P52_RECTO}}": p52_face(P52_RECTO, "recto"), "{{S04_P52_VERSO}}": p52_face(P52_VERSO, "verso"),
        "{{S04_P52_FR_RECTO}}": e(P52_FR_RECTO), "{{S04_P52_FR_VERSO}}": e(P52_FR_VERSO),
        "{{S04_P64}}": p64(), "{{S04_CODEX}}": codex(), "{{S04_SINAI}}": sinai(),
        "{{S04_FEUILLETS}}": feuillets(), "{{S04_CHART}}": chart(),
        "{{S04_TR_PAPYRUS}}": TR_PAPYRUS, "{{S04_TR_CODEX}}": TR_CODEX,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S04_P52_RECTO}}{{S04_P64}}{{S04_CODEX}}{{S04_CHART}}{{S04_FEUILLETS}}")
    print(len(out), "{{S04" in out)
