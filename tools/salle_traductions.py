"""
VERBUM — Salle 07 « La Septante et les grandes traductions » (étape E09)
Marqueurs remplacés dans tools/templates/salles/traductions.html :
  {{S07_POLY_NAV}} / {{S07_POLY}}   polyglotte interactive (hébreu · grec · latin · syriaque · français),
                                    segments alignés (survol / focus = mise en évidence dans les 5 colonnes)
  {{S07_NOM}}          le nom divin dans la Septante (démonstration à 3 états)
  {{S07_VULG}}         mille ans de Bible latine (frise)
  {{S07_NT27}}         les 27 livres du Nouveau Testament et le canon de la Peshitta
  {{S07_VERSIONS}}     les versions anciennes (cartes)
  {{S07_TR_LXX}} / {{S07_TR_VUL}}   transcriptions des narrations
Textes : hébreu massorétique (sans cantillation), Septante (Rahlfs), Vulgate (Clémentine),
Peshitta (vérifiés sur tanakh.info). Traductions françaises du musée ; יהוה = « Jéhovah ».
"""
import html

e = html.escape

# --------------------------------------------------------------------------
# Polyglotte : chaque langue = liste de (segment, index d'alignement ou tuple, séparateur après)
# --------------------------------------------------------------------------
POLY = [
    dict(
        key="gn1-1", ref="Genèse 1:1", titre="La création",
        heb=[("בְּרֵאשִׁית", 0), ("בָּרָא", 1), ("אֱלֹהִים", 2), ("אֵת הַשָּׁמַיִם", 3), ("וְאֵת הָאָרֶץ", 4, "׃")],
        heb_tr="Bereshit bara Elohim et hashamayim veet haarets.",
        grc=[("Ἐν ἀρχῇ", 0), ("ἐποίησεν", 1), ("ὁ Θεὸς", 2), ("τὸν οὐρανὸν", 3), ("καὶ τὴν γῆν", 4, ".")],
        lat=[("In principio", 0), ("creavit", 1), ("Deus", 2), ("caelum", 3), ("et terram", 4, ".")],
        syr=[("ܒܪܫܝܬ", 0), ("ܒܪܐ", 1), ("ܐܠܗܐ", 2, "܂"), ("ܝܬ ܫܡܝܐ", 3), ("ܘܝܬ ܐܪܥܐ", 4, "܂")],
        syr_tr="Brishit bra Alaha yat shmayya w-yat ar'a.",
        fr=[("Au commencement,", 0), ("Dieu", 2), ("créa", 1), ("les cieux", 3), ("et la terre.", 4)],
        notes=["Le syriaque ܒܪܐ (bra, « créa ») est de la même racine que l'hébreu בָּרָא (bara, « créa ») : les deux langues sont sœurs.",
               "Le grec dit ἐποίησεν (« fit »), le latin creavit (« créa ») : deux mots différents, un seul sens.",
               "« Les cieux » est un pluriel en hébreu et en syriaque, un singulier en grec et en latin : une différence de langue, pas de message."],
    ),
    dict(
        key="gn1-3", ref="Genèse 1:3", titre="La lumière",
        heb=[("וַיֹּאמֶר", 0), ("אֱלֹהִים", 1), ("יְהִי אוֹר", 2), ("וַיְהִי־אוֹר", 3, "׃")],
        heb_tr="Vayomer Elohim yehi or vayehi or.",
        grc=[("Καὶ εἶπεν", 0), ("ὁ Θεός", 1), ("Γενηθήτω φῶς", 2, "·"), ("καὶ ἐγένετο φῶς", 3, ".")],
        lat=[("Dixitque", 0), ("Deus", 1), ("fiat lux", 2), ("et facta est lux", 3, ".")],
        syr=[("ܘܐܡܼܪ", 0), ("ܐܠܗܐ", 1), ("ܢܗܘܐ ܢܘܗܪܐ", 2, "܂"), ("ܘܗܘܼܐ ܢܘܗܪܐ", 3, "܂")],
        syr_tr="W-emar Alaha nehwe nuhra w-hwa nuhra.",
        fr=[("Dieu", 1), ("dit :", 0), ("« Que la lumière soit ! »", 2), ("Et la lumière fut.", 3)],
        notes=["La traduction latine fiat lux (« que la lumière soit ») est devenue proverbiale dans toute l'Europe.",
               "Dans les quatre langues, le verset garde le même rythme : un ordre, puis son accomplissement immédiat."],
    ),
    dict(
        key="gn2-8", ref="Genèse 2:8", titre="Le jardin d'Éden",
        heb=[("וַיִּטַּע", 0), ("יְהוָה אֱלֹהִים", 1), ("גַּן־", 2, ""), ("בְּעֵדֶן", 3), ("מִקֶּדֶם", 4), ("וַיָּשֶׂם שָׁם אֶת־הָאָדָם", 5), ("אֲשֶׁר יָצָר", 6, "׃")],
        heb_tr="Vayyitta YHWH Elohim gan-beEden miqqedem vayyasem sham et-haadam asher yatsar.",
        grc=[("Καὶ ἐφύτευσεν", 0), ("Κύριος ὁ Θεὸς", 1), ("παράδεισον", 2), ("ἐν Ἐδὲμ", 3), ("κατὰ ἀνατολάς", 4, ","), ("καὶ ἔθετο ἐκεῖ τὸν ἄνθρωπον", 5), ("ὃν ἔπλασεν", 6, ".")],
        lat=[("Plantaverat autem", 0), ("Dominus Deus", 1), ("paradisum", 2), ("voluptatis", 3), ("a principio", 4, ","), ("in quo posuit hominem", 5), ("quem formaverat", 6, ".")],
        syr=[("ܘܢܨܼܒ", 0), ("ܡܪܝܐ ܐܠܗܐ", 1), ("ܦܪܕܝܣܐ", 2), ("ܒܥܕܢ", 3), ("ܡܢ ܩܕܝܡ", 4, "܂"), ("ܘܣܡ ܬܡܢ ܠܐܕܡ", 5), ("ܕܓܒܠ", 6, "܂")],
        syr_tr="W-nṣab Marya Alaha pardaysa b-'Eden men qdim. W-sam tammān l-Adam d-gbal.",
        fr=[("Jéhovah Dieu", 1), ("planta", 0), ("un jardin", 2), ("en Éden,", 3), ("du côté de l'orient,", 4), ("et il y plaça l'homme", 5), ("qu'il avait formé.", 6)],
        notes=["Le nom divin יהוה devient Κύριος en grec, Dominus en latin et ܡܪܝܐ (Marya) en syriaque, trois mots qui signifient « Seigneur ». Ce musée le rend par « Jéhovah ».",
               "Le grec παράδεισον, mot d'origine perse signifiant « jardin clos », a donné notre mot « paradis » ; le syriaque l'a emprunté (ܦܪܕܝܣܐ, pardaysa).",
               "Jérôme traduit le sens du nom Éden (voluptatis, « des délices ») et comprend מִקֶּדֶם au sens de « dès le commencement » (a principio), là où le grec et le syriaque disent « à l'orient ». Les choix varient ; le récit reste le même."],
    ),
]

COLS = [("heb", "Hébreu", "Texte massorétique", "he", "rtl"),
        ("grc", "Grec", "Septante", "grc", "ltr"),
        ("lat", "Latin", "Vulgate", "la", "ltr"),
        ("syr", "Syriaque", "Peshitta", "syc", "rtl")]


def _segs(items):
    out = []
    for it in items:
        txt, idx = it[0], it[1]
        sep = it[2] if len(it) > 2 else None
        ids = " ".join(str(i) for i in idx) if isinstance(idx, tuple) else str(idx)
        out.append(f'<span class="pg-s" data-i="{ids}" tabindex="0">{e(txt)}</span>{e(sep) if sep else ""}')
    # séparateur : espace, sauf si le séparateur explicite est "" (maqaf)
    html_ = ""
    for i, (it, s) in enumerate(zip(items, out)):
        html_ += s
        if i < len(items) - 1 and not (len(it) > 2 and it[2] == ""):
            html_ += " "
    return html_


def poly_nav():
    return "".join(
        f'<button type="button" role="tab" id="pg-tab-{v["key"]}" aria-controls="pg-{v["key"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<b>{e(v["ref"])}</b><small>{e(v["titre"])}</small></button>' for i, v in enumerate(POLY))


def poly():
    out = []
    for i, v in enumerate(POLY):
        cols = []
        for k, nom, src, lang, d in COLS:
            tr = v.get(f"{k}_tr")
            trl = f'<p class="pg-tr">Prononciation approchée : {e(tr)}</p>' if tr else ""
            cols.append(f'<div class="pg-col pg-{k}"><p class="pg-h"><b>{nom}</b><small>{src}</small></p>'
                        f'<p class="pg-t" lang="{lang}" dir="{d}">{_segs(v[k])}</p>{trl}</div>')
        fr = " ".join(f'<span class="pg-s" data-i="{n}" tabindex="0">{e(t)}</span>' for t, n in v["fr"])
        notes = "".join(f"<li>{e(n)}</li>" for n in v["notes"])
        out.append(f'''
<div class="pg-panel" role="tabpanel" id="pg-{v["key"]}" aria-labelledby="pg-tab-{v["key"]}"{"" if i == 0 else " hidden"}>
  <div class="pg-grid">{"".join(cols)}</div>
  <div class="pg-fr"><p class="pg-h"><b>Français</b><small>traduction du musée</small></p><p class="pg-t">{fr}</p></div>
  <ul class="pg-notes">{notes}</ul>
</div>''')
    return "".join(out)


# --------------------------------------------------------------------------
# Le nom divin dans la Septante
# --------------------------------------------------------------------------
def nom():
    return '''
<div class="nd-stage" data-etat="kyrios">
  <p class="nd-line" lang="grc">Καὶ ἐφύτευσεν <span class="nd-nom" aria-live="polite"><span class="nd-k">Κύριος</span><bdi class="nd-h" lang="he" dir="rtl">יהוה</bdi><bdi class="nd-p" lang="he" dir="rtl">𐤉𐤄𐤅𐤄</bdi></span> ὁ Θεὸς παράδεισον ἐν Ἐδὲμ κατὰ ἀνατολάς…</p>
  <p class="nd-fr">« Jéhovah Dieu planta un jardin en Éden, du côté de l'orient… » (Genèse 2:8)</p>
</div>
<div class="seg nd-seg" role="radiogroup" aria-label="Manière d'écrire le nom divin">
  <button type="button" role="radio" aria-checked="false" data-etat="paleo">Lettres paléo-hébraïques<small>Rouleau grec des Douze Prophètes, Naḥal Ḥever · vers le tournant de notre ère</small></button>
  <button type="button" role="radio" aria-checked="false" data-etat="carre">Lettres hébraïques carrées<small>Papyrus Fouad 266 · Ier siècle av. J.-C.</small></button>
  <button type="button" role="radio" aria-checked="true" data-etat="kyrios">Κύριος (« Seigneur »)<small>Grands codex chrétiens · IVe siècle</small></button>
</div>'''


# --------------------------------------------------------------------------
# Mille ans de Bible latine
# --------------------------------------------------------------------------
VULG = [
    ("382", "La commande", "À Rome, l'évêque Damase demande à Jérôme de réviser les vieilles traductions latines des Évangiles."),
    ("386", "Bethléem", "Jérôme s'installe à Bethléem, perfectionne son hébreu auprès de maîtres juifs et rassemble des manuscrits."),
    ("390 – 405", "La « vérité hébraïque »", "Il traduit l'Ancien Testament directement de l'hébreu, et non plus de la Septante."),
    ("Vers 700", "Le Codex Amiatinus", "À Wearmouth-Jarrow, en Northumbrie, des moines copient trois Bibles géantes. L'une d'elles est le plus ancien exemplaire complet de la Vulgate conservé."),
    ("Vers 1455", "Le premier grand livre imprimé", "Gutenberg imprime à Mayence la Vulgate : c'est la Bible à 42 lignes (salle 08)."),
    ("1546", "Le concile de Trente", "La Vulgate est déclarée « authentique » pour l'usage public de l'Église catholique."),
    ("1592", "L'édition clémentine", "Une édition révisée devient la référence pendant près de quatre siècles."),
    ("1979", "La Nova Vulgata", "Une révision moderne, corrigée sur les textes hébreu et grec, est publiée."),
]


def vulg():
    return "".join(f'<li data-reveal><span class="vg-d">{e(d)}</span><h4>{e(t)}</h4><p>{e(p)}</p></li>' for d, t, p in VULG)


# --------------------------------------------------------------------------
# Nouveau Testament et canon de la Peshitta
# --------------------------------------------------------------------------
NT = ["Matthieu", "Marc", "Luc", "Jean", "Actes", "Romains", "1 Corinthiens", "2 Corinthiens", "Galates", "Éphésiens",
      "Philippiens", "Colossiens", "1 Thessaloniciens", "2 Thessaloniciens", "1 Timothée", "2 Timothée", "Tite", "Philémon",
      "Hébreux", "Jacques", "1 Pierre", "2 Pierre", "1 Jean", "2 Jean", "3 Jean", "Jude", "Révélation"]
ABSENTS = {"2 Pierre", "2 Jean", "3 Jean", "Jude", "Révélation"}


def nt27():
    return "".join(f'<li class="{"is-abs" if b in ABSENTS else ""}">{e(b)}</li>' for b in NT)


# --------------------------------------------------------------------------
# Versions anciennes
# --------------------------------------------------------------------------
VERSIONS = [
    ("IIIe – Ier s. av. J.-C.", "Grec", "La Septante", "Alexandrie", "Plus ancien témoin : le papyrus Rylands 458 (IIe siècle av. J.-C.), quelques versets du Deutéronome."),
    ("IIe siècle", "Latin", "Les vieilles versions latines", "Afrique du Nord, Gaule, Italie", "Traductions multiples et inégales, connues par des manuscrits et par les citations de Tertullien ou de Cyprien."),
    ("IIe – Ve siècle", "Syriaque", "La Peshitta", "Édesse (Mésopotamie)", "Manuscrit daté de 464 (British Library, Add. 14425) ; Ancien Testament complet dans le Codex Ambrosianus (Milan)."),
    ("IIIe – IVe siècle", "Copte", "Les versions coptes", "Égypte", "En dialectes sahidique puis bohaïrique : la langue des paysans et des moines d'Égypte."),
    ("Vers 350 – 380", "Gotique", "La Bible de Wulfila", "Bords du Danube", "Wulfila invente un alphabet pour les Goths. Le Codex Argenteus (VIe siècle), en lettres d'argent et d'or sur parchemin pourpre, en conserve 188 feuillets sur 336, à Uppsala."),
    ("382 – 405", "Latin", "La Vulgate de Jérôme", "Bethléem", "Le Codex Amiatinus (vers 700) en est le plus ancien exemplaire complet."),
    ("Vers 405 – 435", "Arménien", "La version arménienne", "Arménie", "Mesrop Machtots crée l'alphabet arménien vers 405 pour traduire la Bible. Sa précision lui vaut le surnom de « reine des versions »."),
    ("IVe – VIe siècle", "Guèze et géorgien", "Éthiopie et Caucase", "Aksoum · Ibérie du Caucase", "Les Évangiles de Garima (salle 04) comptent parmi les plus anciens livres des Évangiles illustrés."),
]


def versions():
    return "".join(
        f'<article class="vs" data-reveal><span class="vs-d">{e(d)}</span><span class="vs-l">{e(l)}</span>'
        f'<h4>{e(t)}</h4><p class="vs-lieu">{e(lieu)}</p><p>{e(p)}</p></article>'
        for d, l, t, lieu, p in VERSIONS)


# --------------------------------------------------------------------------
TR_LXX = """<p>Alexandrie, troisième siècle avant notre ère. La plus grande ville du monde grec abrite une importante communauté juive, qui parle désormais le grec bien mieux que l'hébreu. Pour qu'elle puisse continuer à lire la Loi de Moïse, les cinq premiers livres de la Bible sont traduits en grec. Un écrit ancien, la Lettre d'Aristée, embellit le récit : le roi Ptolémée aurait fait venir de Jérusalem soixante-douze savants, six par tribu, qui auraient achevé leur travail en soixante-douze jours. De ce chiffre vient le nom de la traduction : la Septante, « les soixante-dix ». La légende est tardive, mais le fait est sûr : vers 250 avant notre ère, la Torah parle grec.</p>
<p>Les autres livres suivent, jusqu'au premier siècle avant notre ère. Pour la première fois, les Écritures hébraïques peuvent être lues par des non-Juifs, dans la langue internationale de l'époque. Plus tard, les rédacteurs du Nouveau Testament citeront très souvent cette version. Les plus anciennes copies de la Septante, retrouvées en Égypte et dans le désert de Judée, réservent une surprise : certaines conservent le nom divin, écrit en lettres hébraïques au milieu du texte grec. Plus tard, les copistes le remplaceront par Kyrios, « Seigneur ». Ce musée, lui, rend ce nom par Jéhovah.</p>"""

TR_VUL = """<p>Rome, 382. L'évêque Damase confie à un savant exigeant, Jérôme, la révision des vieilles traductions latines, devenues confuses à force de copies. Jérôme va beaucoup plus loin. Installé à Bethléem, il apprend l'hébreu auprès de maîtres juifs et traduit l'Ancien Testament directement depuis l'original : c'est ce qu'il appelle la vérité hébraïque. Son œuvre, achevée vers 405, deviendra la Vulgate, c'est-à-dire la version « répandue ». Pendant plus de mille ans, elle sera la Bible de l'Occident. Le plus ancien exemplaire complet qui nous soit parvenu, le Codex Amiatinus, a été copié en Angleterre vers l'an 700. Il pèse plus de trente kilos.</p>
<p>Plus à l'Est, à Édesse, aux confins de l'Empire romain, on parle le syriaque, un dialecte araméen, cousin de la langue que parlait Jésus. Dès le deuxième siècle, les Écritures hébraïques y sont traduites ; le Nouveau Testament suit. Cette version prend le nom de Peshitta, « la simple ». L'un de ses manuscrits, copié en 464 à Amid, est l'un des plus anciens manuscrits bibliques portant une date précise. Grec, latin, syriaque, mais aussi copte, gotique, arménien, guèze : en quelques siècles, la Parole a commencé à parler toutes les langues. Et d'une traduction à l'autre, le message est resté le même.</p>"""


def render(inner):
    rep = {
        "{{S07_POLY_NAV}}": poly_nav(), "{{S07_POLY}}": poly(), "{{S07_NOM}}": nom(), "{{S07_VULG}}": vulg(),
        "{{S07_NT27}}": nt27(), "{{S07_VERSIONS}}": versions(),
        "{{S07_TR_LXX}}": TR_LXX, "{{S07_TR_VUL}}": TR_VUL,
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S07_POLY_NAV}}{{S07_POLY}}{{S07_NOM}}{{S07_VULG}}{{S07_NT27}}{{S07_VERSIONS}}")
    print(len(out), "{{S07" in out)
