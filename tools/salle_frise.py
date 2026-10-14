"""
VERBUM — Salle 11 « La Grande Frise chronologique » (étape E13)
Marqueurs remplacés dans tools/templates/salles/frise.html :
  {{S11_ERAS}}      boutons des 8 époques (navigation dans la frise)
  {{S11_CATS}}      filtres par nature d'événement
  {{S11_MINI}}      mini-carte proportionnelle au temps (repères)
  {{S11_RAIL}}      la frise : un événement par colonne (cartes cliquables)
  {{S11_DATA}}      données JSON des fiches détaillées (dialogue)
  {{S11_EPOQUES}}   cartes des 8 époques
  {{S11_ECART}}     graphique « écart rédaction / plus ancienne copie »
  {{S11_ORDRE}}     jeu « Remettre dans l'ordre »
  {{S11_TR_*}}      transcriptions des narrations
Règles VERBUM : tétragramme rendu « Jéhovah » ; tout texte étranger traduit ; badges canonique / apocryphe ;
aucune croix (les traits verticaux s'arrêtent sur l'axe, sans le traverser).
"""
import html
import json

e = html.escape

ERAS = [
    # n, titre, période, audio, début (s)
    (1, "Les origines", "≈ 1500 – 539 av. J.-C.", "origines", 0),
    (2, "Du retour d'exil à Qumrân", "539 av. J.-C. – Iᵉʳ s. av. J.-C.", "origines", 52.2),
    (3, "Les apôtres et les premiers papyrus", "Iᵉʳ – IIIᵉ siècle", "codex", 0),
    (4, "Les grands codex et les traductions", "IVᵉ – VIᵉ siècle", "codex", 47.7),
    (5, "Massorètes et copistes", "VIIᵉ – XVᵉ siècle", "copistes", 0),
    (6, "L'imprimerie et la Réforme", "1455 – 1611", "copistes", 47.8),
    (7, "Le temps des découvertes", "1800 – 1979", "decouvertes", 0),
    (8, "L'ère numérique", "1981 – 2026", "decouvertes", 53.1),
]

CATS = [
    ("redaction", "Rédaction"),
    ("manuscrit", "Manuscrits"),
    ("traduction", "Traductions"),
    ("imprime", "Imprimé et diffusion"),
    ("temoin", "Témoins archéologiques"),
    ("persecution", "Persécutions"),
    ("decouverte", "Découvertes et recherche"),
]
CAT_L = dict(CATS)

BADGES = {"canon": '<span class="badge badge-canon">Canonique</span>',
          "apo": '<span class="badge badge-apo">Apocryphe</span>',
          "none": ""}

SALLES = {"01": ("01-origines", "Les Origines"), "02": ("02-copistes", "Les Copistes et les Massorètes"),
          "03": ("03-qumran", "Les Manuscrits de la mer Morte"), "04": ("04-codex-grecs", "Les Grands Codex grecs"),
          "05": ("05-codex-h", "Le Codex H"), "06": ("06-apocryphes", "Les Textes apocryphes"),
          "07": ("07-traductions", "La Septante et les grandes traductions"), "08": ("08-gutenberg", "Gutenberg et l'imprimerie"),
          "09": ("09-archeologie", "Les Preuves archéologiques"), "10": ("10-indestructible", "Le Livre indestructible"),
          "12": ("12-bible-francaise", "La Bible en français")}

# (année pour l'échelle, libellé, titre, époque, catégorie, badge, salle, image "dossier/nom", texte, importance, lien original)
EV = [
    (-1500, "≈ 1500 av. J.-C.", "Moïse consigne la Loi", 1, "redaction", "canon", "01", "01/moise-tables",
     "Selon la Bible elle-même (Exode 24:4 ; Deutéronome 31:9, 24), Moïse met par écrit les paroles de la Loi dans le désert du Sinaï. Les cinq premiers livres de la Bible, la Torah ou Pentateuque, lui sont traditionnellement attribués. Les historiens débattent de la date et des étapes de la rédaction ; la tradition biblique situe l'Exode au IIᵉ millénaire avant notre ère.",
     "Dès l'origine, le texte est présenté comme un écrit à conserver près de l'arche, à lire en public et à recopier (Deutéronome 31:26 ; 17:18).", None),
    (-1208, "≈ 1208 av. J.-C.", "La stèle de Merneptah", 1, "temoin", "none", "01", "01/merneptah",
     "Le pharaon Merneptah, fils de Ramsès II, célèbre ses victoires sur une stèle de granit haute de plus de trois mètres. À la ligne 27, il affirme : « Israël est dévasté, sa semence n'existe plus. » La stèle a été découverte à Thèbes en 1896 par Flinders Petrie et se trouve aujourd'hui au Caire.",
     "C'est la plus ancienne mention connue d'Israël hors de la Bible : un peuple déjà installé en Canaan à la fin du XIIIᵉ siècle avant notre ère.", None),
    (-840, "IXᵉ s. av. J.-C.", "Les stèles de Mésha et de Tel Dan", 1, "temoin", "none", "09", "09/mesha",
     "Vers 840 avant notre ère, Mésha, roi de Moab, fait graver le récit de sa révolte contre Israël : il cite Omri, roi d'Israël, et, à la ligne 18, le nom divin, Jéhovah. Quelques décennies plus tard, un roi araméen, probablement Hazaël, se vante sur la stèle de Tel Dan d'avoir vaincu le « roi d'Israël » et le roi de la « maison de David ».",
     "Des adversaires d'Israël confirment, dans leurs propres inscriptions, des rois et des événements racontés dans les livres des Rois.",
     ("Musée du Louvre", "https://collections.louvre.fr/ark:/53355/cl010120339")),
    (-600, "≈ 600 av. J.-C.", "Les rouleaux d'argent de Ketef Hinnom", 1, "manuscrit", "canon", "01", "01/ketef-amulettes",
     "Deux amulettes d'argent roulées, longues de quelques centimètres, portent, gravée en écriture paléo-hébraïque, la bénédiction de Nombres 6:24-26 : « Que Jéhovah te bénisse et te garde ; que Jéhovah fasse briller sa face sur toi… » Elles ont été retrouvées en 1979 dans une tombe de Jérusalem.",
     "C'est le plus ancien texte biblique connu, antérieur de plusieurs siècles aux manuscrits de la mer Morte.",
     ("Musée d'Israël", "https://www.imj.org.il/en/collections/198069")),
    (-539, "539 av. J.-C.", "Cyrus et le retour des exilés", 1, "temoin", "none", "09", "09/cyrus",
     "Le roi perse Cyrus prend Babylone en 539 avant notre ère. Le cylindre d'argile qui porte son nom, découvert en 1879 et conservé au British Museum, décrit sa politique : rendre aux peuples déportés leurs sanctuaires et leur permettre de rentrer chez eux.",
     "Cette politique correspond au décret rapporté en Esdras 1:1-4, qui autorise les Judéens à rentrer à Jérusalem et à rebâtir le temple.",
     ("British Museum", "https://www.britishmuseum.org/collection/object/W_1880-0617-1941")),
    (-450, "Vᵉ s. av. J.-C.", "Esdras, « copiste habile »", 2, "manuscrit", "canon", "02", "02/esdras-lecture",
     "Le livre d'Esdras présente ce prêtre comme « un copiste habile dans la loi de Moïse » (Esdras 7:6). Selon Néhémie 8, il lit la Loi devant le peuple rassemblé à Jérusalem, de l'aube jusqu'à midi, pendant que des Lévites en expliquent le sens.",
     "La tradition juive voit en lui l'un des grands artisans de la préservation et de la mise en ordre des Écritures.", None),
    (-280, "≈ 280 av. J.-C.", "La Septante", 2, "traduction", "canon", "07", "07/septante",
     "À Alexandrie, sous les rois Ptolémées, des savants juifs traduisent la Torah en grec. La Lettre d'Aristée raconte que 72 traducteurs auraient achevé leur travail en 72 jours, un récit en partie légendaire. Les autres livres de la Bible hébraïque sont traduits au cours des deux siècles suivants.",
     "Première grande traduction de la Bible, la Septante est fréquemment citée par les rédacteurs du Nouveau Testament.", None),
    (-125, "≈ 125 av. J.-C.", "Le grand rouleau d'Ésaïe", 2, "manuscrit", "canon", "03", "03/fragment-esaie53",
     "Le rouleau 1QIsaᵃ mesure environ 7,3 mètres et contient les 66 chapitres du livre d'Ésaïe, sur 17 feuilles de cuir cousues. Retrouvé en 1947 dans la grotte 1 de Qumrân, il est exposé au Sanctuaire du Livre, au Musée d'Israël.",
     "Comparé au Codex de Leningrad, copié plus de mille ans plus tard, il présente surtout des différences d'orthographe et de détail : le texte a été transmis avec une fidélité remarquable.",
     ("Musée d'Israël", "http://dss.collections.imj.org.il/isaiah")),
    (75, "≈ 50 – 100", "La rédaction du Nouveau Testament", 3, "redaction", "canon", "04", "11/redaction-nt",
     "Vers l'an 50, Paul écrit ses premières lettres, sans doute celles aux Thessaloniciens. Les Évangiles, les Actes et les autres lettres suivent ; vers la fin du siècle, l'apôtre Jean écrit son Évangile, ses trois lettres et la Révélation. Les dates précises sont discutées, mais l'ensemble des 27 livres est rédigé en une cinquantaine d'années.",
     "Les 66 livres de la Bible sont achevés : environ 1 600 ans de rédaction, une quarantaine de rédacteurs, trois langues (hébreu, araméen, grec).", None),
    (125, "≈ 100 – 150", "Le papyrus P52", 3, "manuscrit", "canon", "04", "04/p52",
     "Ce fragment de papyrus de 9 cm sur 6 porte, d'un côté, quelques mots de Jean 18:31-33 et, de l'autre, de Jean 18:37-38. Acheté en Égypte en 1920, il est conservé à la John Rylands Library de Manchester.",
     "C'est le plus ancien manuscrit connu du Nouveau Testament : l'Évangile de Jean circulait déjà en Égypte quelques décennies après sa rédaction.", None),
    (200, "≈ 200", "Le papyrus Bodmer II (P66)", 3, "manuscrit", "canon", "04", "04/p66",
     "Ce codex de papyrus contient la plus grande partie de l'Évangile de Jean. Acquis par le collectionneur Martin Bodmer dans les années 1950, il est conservé à la Fondation Bodmer, à Cologny, près de Genève.",
     "Il montre qu'un livre entier du Nouveau Testament était déjà copié avec soin, et relu par son copiste, vers l'an 200.",
     ("Fondation Bodmer", "https://bodmerlab.unige.ch/fr/constellations/papyri")),
    (303, "303", "L'édit de Dioclétien", 4, "persecution", "none", "10", "10/diocletien",
     "En février 303, un édit impérial ordonne de détruire les lieux de culte chrétiens et de livrer les Écritures pour qu'elles soient brûlées. Eusèbe de Césarée affirme avoir vu les livres brûler sur les places publiques.",
     "Moins de trente ans plus tard, Constantin commande 50 exemplaires des Écritures : la persécution n'a pas interrompu la transmission.", None),
    (340, "≈ 325 – 360", "Les codex Vaticanus et Sinaïticus", 4, "manuscrit", "canon", "04", "04/vaticanus",
     "Deux Bibles grecques monumentales sont copiées sur parchemin. Le Vaticanus se trouve à la Bibliothèque vaticane depuis au moins le XVᵉ siècle. Le Sinaïticus, longtemps conservé au monastère Sainte-Catherine du Sinaï, est aujourd'hui partagé entre Londres, Leipzig, le Sinaï et Saint-Pétersbourg.",
     "Le Sinaïticus contient le plus ancien Nouveau Testament complet connu.",
     ("Bibliothèque vaticane", "https://digi.vatlib.it/view/MSS_Vat.gr.1209")),
    (405, "382 – 405", "La Vulgate de Jérôme", 4, "traduction", "canon", "07", "07/jerome",
     "Chargé par l'évêque de Rome Damase de réviser les traductions latines, Jérôme s'installe à Bethléem et traduit l'Ancien Testament directement de l'hébreu, ce qui est alors inédit. Sa traduction, appelée plus tard « Vulgate », c'est-à-dire « répandue », s'impose peu à peu dans tout l'Occident.",
     "Pendant plus de mille ans, la Vulgate sera la Bible de l'Europe occidentale : c'est elle que Gutenberg imprimera.", None),
    (430, "≈ 400 – 440", "Le Codex Alexandrinus", 4, "manuscrit", "canon", "04", "04/alexandrinus",
     "Cette Bible grecque sur parchemin contient l'Ancien et le Nouveau Testament. Offerte au roi d'Angleterre par le patriarche Cyrille Loukaris, elle arrive à Londres en 1627 ; elle est aujourd'hui à la British Library.",
     "C'est l'un des trois grands codex grecs : les savants européens y ont eu accès bien avant le Sinaïticus.",
     ("British Library", "https://www.bl.uk/collection-items/codex-alexandrinus")),
    (464, "Vᵉ s.", "La Peshitta", 4, "traduction", "canon", "07", "07/edesse",
     "Dans la région d'Édesse, la Bible des chrétiens de langue syriaque, une forme de l'araméen, se fixe sous le nom de Peshitta, « la simple ». Le manuscrit Add. 14425 de la British Library, daté de 464, est le plus ancien manuscrit biblique portant une date.",
     "Portée par les communautés syriaques jusqu'en Perse, en Inde et en Chine, elle témoigne de la diffusion précoce de la Bible hors du monde gréco-romain.", None),
    (550, "VIᵉ s.", "Le Codex H est copié", 4, "manuscrit", "canon", "05", "05/codexh-avant",
     "Un copiste grec réalise un manuscrit des Lettres de Paul accompagné de l'appareil dit « euthalien » : prologues, listes de chapitres et notes de lecture. Au XIIIᵉ siècle, au mont Athos, ses feuillets usés sont réutilisés dans des reliures d'autres livres.",
     "Ses pages dispersées entre plusieurs bibliothèques témoignent du soin avec lequel le texte de Paul était édité et étudié.",
     ("Projet Codex H", "https://codexh.arts.gla.ac.uk/")),
    (930, "≈ 930", "Le Codex d'Alep", 5, "manuscrit", "canon", "02", "02/codex-alep",
     "À Tibériade, le massorète Aaron ben Moïse ben Asher vocalise et annote ce manuscrit complet de la Bible hébraïque. Endommagé lors d'émeutes à Alep en 1947, il a perdu environ 40 % de ses feuillets, dont la plus grande partie de la Torah. Il est exposé au Sanctuaire du Livre, à Jérusalem.",
     "Le savant juif Maïmonide le tenait pour le modèle de référence du texte hébreu.",
     ("Aleppo Codex", "https://www.aleppocodex.org/")),
    (1008, "1008", "Le Codex de Leningrad", 5, "manuscrit", "canon", "02", "02/codex-leningrad",
     "Copié au Caire en 1008 ou 1009 par le scribe Samuel ben Jacob, d'après des manuscrits de l'école de Ben Asher, il est conservé à la Bibliothèque nationale de Russie, à Saint-Pétersbourg.",
     "C'est le plus ancien manuscrit complet de la Bible hébraïque : il sert de base aux éditions savantes modernes, comme la Biblia Hebraica Stuttgartensia.",
     ("Bibliothèque nationale de Russie", "https://expositions.nlr.ru/eng/ex_manus/firkovich/catalog.php")),
    (1382, "≈ 1382", "La Bible de Wycliffe", 5, "traduction", "canon", "10", "11/wycliffe",
     "À Oxford, John Wycliffe inspire la première traduction complète de la Bible en anglais, réalisée à partir de la Vulgate latine par lui et ses collaborateurs. Interdite par les constitutions d'Oxford en 1408, elle continue d'être recopiée en secret.",
     "Plus de 250 manuscrits en sont conservés : l'interdiction n'a pas suffi à la faire disparaître.", None),
    (1455, "≈ 1455", "La Bible de Gutenberg", 6, "imprime", "canon", "08", "08/b42",
     "À Mayence, Johannes Gutenberg imprime la Vulgate latine en caractères mobiles de métal, sur deux colonnes de 42 lignes. Environ 180 exemplaires sont tirés, sur papier et sur vélin ; une cinquantaine sont conservés, complets ou partiels.",
     "Le texte peut désormais être reproduit à l'identique et en grand nombre : chaque exemplaire d'un même tirage est semblable aux autres.",
     ("Gutenberg Digital, Göttingen", "https://www.gutenbergdigital.de/")),
    (1516, "1516", "Le Nouveau Testament grec d'Érasme", 6, "imprime", "canon", "08", "08/erasme",
     "À Bâle, chez l'imprimeur Johann Froben, l'humaniste Érasme publie le premier Nouveau Testament grec mis en vente, accompagné d'une nouvelle traduction latine. Préparée en quelques mois à partir d'un petit nombre de manuscrits tardifs, l'édition sera révisée à plusieurs reprises.",
     "Luther et Tyndale traduiront à partir de ce texte grec : le retour aux langues originales est lancé.", None),
    (1522, "1522 – 1534", "La Bible de Luther", 6, "traduction", "canon", "08", "11/luther",
     "Caché au château de la Wartburg, Martin Luther traduit le Nouveau Testament du grec en allemand en onze semaines, durant l'hiver 1521-1522. Publié en septembre 1522, il est suivi en 1534 de la Bible complète, traduite avec une équipe de collaborateurs.",
     "Imprimée à des centaines de milliers d'exemplaires, cette traduction façonne la langue allemande et inspire les traducteurs de toute l'Europe.", None),
    (1526, "1526 – 1536", "Tyndale, traducteur et martyr", 6, "persecution", "canon", "10", "10/vilvorde",
     "William Tyndale fait imprimer à Worms, en 1526, le premier Nouveau Testament anglais traduit du grec. Les exemplaires sont brûlés à Londres ; lui-même est arrêté à Anvers, puis étranglé et brûlé à Vilvorde le 6 octobre 1536.",
     "Trois ans plus tard, la Grande Bible, en grande partie son œuvre, est imprimée pour toutes les églises d'Angleterre.", None),
    (1535, "1535", "La Bible d'Olivétan", 6, "traduction", "canon", "12", "11/olivetan",
     "Pierre Robert Olivétan, cousin de Jean Calvin, traduit la Bible en français à partir de l'hébreu et du grec, à la demande des Vaudois. Elle est imprimée à Serrières, près de Neuchâtel, par Pierre de Vingle, et achevée le 4 juin 1535.",
     "Première Bible protestante en français traduite sur les langues originales, elle est l'ancêtre de la Bible de Genève et de nombreuses révisions.", None),
    (1611, "1611", "La Bible du roi Jacques", 6, "traduction", "canon", "08", "11/kjv",
     "Commandée par le roi Jacques Iᵉʳ en 1604, cette traduction anglaise est préparée par une cinquantaine de savants répartis en six comités, à Westminster, Oxford et Cambridge. Elle est imprimée à Londres par Robert Barker, imprimeur du roi.",
     "Reprenant une large part du travail de Tyndale, elle façonnera la langue anglaise pendant plus de trois siècles.", None),
    (1804, "1800 – 1804", "Mary Jones et les sociétés bibliques", 7, "imprime", "none", "08", "11/mary-jones",
     "En 1800, Mary Jones, une jeune Galloise d'une quinzaine d'années qui a économisé pendant six ans, marche une quarantaine de kilomètres jusqu'à Bala pour acheter une Bible en gallois auprès du pasteur Thomas Charles. Son histoire contribue à la fondation, à Londres, en 1804, de la Société biblique britannique et étrangère.",
     "Le mouvement des sociétés bibliques fera de la Bible le livre le plus traduit et le plus diffusé au monde.", None),
    (1859, "1844 – 1859", "Tischendorf et le Sinaïticus", 7, "decouverte", "canon", "04", "04/tischendorf",
     "Au monastère Sainte-Catherine du Sinaï, le savant allemand Constantin von Tischendorf repère en 1844 des feuillets d'un très ancien manuscrit grec. En 1859, on lui montre le reste du codex, qui est ensuite remis au tsar de Russie. Les conditions de ce transfert restent discutées.",
     "Le monde savant découvre une Bible complète du IVᵉ siècle, qui permet de vérifier le texte du Nouveau Testament.",
     ("Codex Sinaiticus", "https://www.codexsinaiticus.org/en/")),
    (1902, "1902", "Le papyrus Nash", 7, "decouverte", "canon", "02", "11/nash",
     "Acquis en Égypte par Walter Llewellyn Nash et publié en 1903, ce petit feuillet de papyrus des IIᵉ ou Iᵉʳ siècles avant notre ère contient les Dix Paroles et le début du Shema Israël (Deutéronome 6:4-5). Il est conservé à la bibliothèque de l'université de Cambridge.",
     "Jusqu'en 1947, c'était le plus ancien manuscrit biblique en hébreu connu.", None),
    (1945, "1945", "La bibliothèque de Nag Hammadi", 7, "decouverte", "apo", "06", "06/hero-nag",
     "En Haute-Égypte, des paysans découvrent une jarre contenant treize codex de papyrus en copte, copiés au IVᵉ siècle. On y trouve des écrits gnostiques comme l'Évangile de Thomas.",
     "Ces textes apocryphes ne font pas partie de la Bible : ils éclairent les débats des premiers siècles et la manière dont le canon a été reconnu.", None),
    (1947, "1947", "Les manuscrits de la mer Morte", 7, "decouverte", "canon", "03", "03/berger-1947",
     "Un jeune berger bédouin découvre des jarres dans une grotte près de Qumrân. Jusqu'en 1956, onze grottes livrent les restes d'environ 900 manuscrits, dont quelque 230 manuscrits bibliques, copiés entre le IIIᵉ siècle avant notre ère et le Iᵉʳ siècle de notre ère.",
     "Tous les livres de la Bible hébraïque y sont représentés, sauf Esther : un bond de mille ans en arrière dans l'histoire du texte.",
     ("Bibliothèque numérique Leon Levy", "https://www.deadseascrolls.org.il/?locale=fr_FR")),
    (1979, "1979", "La découverte de Ketef Hinnom", 7, "decouverte", "canon", "01", "01/ketef-fouilles",
     "En fouillant des tombes creusées dans le rocher face à la vieille ville de Jérusalem, l'équipe de l'archéologue Gabriel Barkay retrouve deux minuscules rouleaux d'argent. Il faudra trois ans pour les dérouler sans les briser, puis des années pour les déchiffrer.",
     "Ils contiennent le plus ancien texte biblique connu, et le nom divin, Jéhovah, gravé vers 600 avant notre ère.", None),
    (1981, "18 juin 1981", "Le projet Perle", 8, "persecution", "none", "10", "10/plage",
     "Dans la nuit du 18 juin 1981, une barge chargée d'un million de Bibles en chinois approche d'une plage près de Shantou, dans le sud de la Chine. Des centaines de croyants chinois les débarquent en quelques heures.",
     "Même derrière des frontières fermées, la Bible continue d'être recopiée, cachée et transmise.", None),
    (2009, "2009", "Le Codex Sinaïticus en ligne", 8, "decouverte", "canon", "04", "11/numerisation",
     "Après quatre ans de travail, la British Library, l'université de Leipzig, le monastère Sainte-Catherine et la Bibliothèque nationale de Russie publient en ligne l'ensemble des feuillets conservés du Codex Sinaïticus, photographiés en haute définition.",
     "Pour la première fois depuis le XIXᵉ siècle, le manuscrit est réuni, virtuellement, et accessible à tous.",
     ("Codex Sinaiticus", "https://www.codexsinaiticus.org/en/")),
    (2026, "2026", "Les 42 pages restituées du Codex H", 8, "decouverte", "canon", "05", "05/hero-labo",
     "Grâce à l'imagerie multispectrale, l'équipe du professeur Garrick Allen, à l'université de Glasgow, fait réapparaître 42 pages effacées du Codex H. Il ne s'agit pas de textes nouveaux : ce sont des passages des Lettres de Paul déjà connus.",
     "Une fois de plus, une découverte récente confirme le texte que l'on lisait déjà.",
     ("Université de Glasgow", "https://www.gla.ac.uk/news/headline_1263245_en.html")),
    (2026, "Septembre 2026", "La Bible en 807 langues", 8, "traduction", "canon", "08", "08/globe",
     "Selon Wycliffe, la Bible complète existe en 807 langues, le Nouveau Testament dans 1 844 autres et des portions dans 1 519 autres. Au total, au moins une partie de la Bible est disponible dans plus de 4 100 langues.",
     "Environ 6,3 milliards de personnes peuvent lire la Bible complète dans leur langue.", None),
]


def pos(y):
    """Échelle de la mini-carte : l'Antiquité lointaine est compressée."""
    if y <= 0:
        return (y + 1500) / 1500 * 0.30
    if y <= 1500:
        return 0.30 + y / 1500 * 0.38
    return 0.68 + (min(y, 2026) - 1500) / 526 * 0.32


def eras():
    out = []
    for n, t, p, *_ in ERAS:
        out.append(f'<button type="button" role="radio" aria-checked="{"true" if n == 1 else "false"}" data-era="{n}">'
                   f'<b>{n}</b><span>{e(t)}</span></button>')
    return f'<div class="fr-eras seg" role="radiogroup" aria-label="Aller à une époque">{"".join(out)}</div>'


def cats():
    out = [f'<button type="button" class="fr-cat" data-cat="{k}" aria-pressed="true"><i aria-hidden="true"></i>{e(l)}</button>'
           for k, l in CATS]
    return f'<div class="fr-cats" role="group" aria-label="Filtrer par nature d\'événement">{"".join(out)}</div>'


def mini():
    ticks = "".join(f'<button type="button" class="mn-t" data-i="{i}" data-cat="{c}" style="left:{pos(y) * 100:.2f}%" '
                    f'aria-label="{e(lab)} : {e(t)}" tabindex="-1"></button>'
                    for i, (y, lab, t, era, c, *_) in enumerate(EV))
    labels = [(-1500, "1500 av."), (-1000, "1000 av."), (-500, "500 av."), (0, "An 1"), (500, "500"), (1000, "1000"), (1500, "1500"), (1800, "1800"), (2026, "2026")]
    labs = "".join(f'<span class="mn-l" style="left:{pos(y) * 100:.2f}%">{t}</span>' for y, t in labels)
    return f'<div class="fr-mini" aria-hidden="false"><div class="mn-band">{ticks}<span class="mn-win" aria-hidden="true"></span></div><div class="mn-labs">{labs}</div></div>'


def thumb(path, alt=""):
    d, n = path.split("/")
    return f'{{{{ROOT}}}}assets/img/salles/{d}/{n}-960.jpg'


def rail():
    cols = []
    prev_era = None
    for i, (y, lab, t, era, c, b, s, im, txt, imp, url) in enumerate(EV):
        start = era != prev_era
        prev_era = era
        side = "up" if i % 2 == 0 else "down"
        era_lab = f'<span class="ev-era"><b>Époque {era}</b>{e(ERAS[era - 1][1])}</span>' if start else ""
        cols.append(f"""
      <li class="ev ev-{side}{' ev-start' if start else ''}" data-i="{i}" data-era="{era}" data-cat="{c}">
        {era_lab}
        <button type="button" class="ev-card" aria-haspopup="dialog" aria-label="{e(lab)} · {e(t)} : ouvrir la fiche">
          <span class="ev-img"><img src="{thumb(im)}" alt="" loading="lazy" decoding="async" width="960" height="540"></span>
          <span class="ev-body">
            <span class="ev-y">{e(lab)}</span>
            <span class="ev-t">{e(t)}</span>
            <span class="ev-meta"><span class="ev-cat"><i aria-hidden="true"></i>{e(CAT_L[c])}</span>{BADGES[b]}</span>
          </span>
        </button>
        <span class="ev-stem" aria-hidden="true"></span>
        <span class="ev-dot" aria-hidden="true"></span>
      </li>""")
    return f'<ol class="fr-rail">{"".join(cols)}\n    </ol>'


def data():
    out = []
    for i, (y, lab, t, era, c, b, s, im, txt, imp, url) in enumerate(EV):
        d, n = im.split("/")
        out.append({"lab": lab, "t": t, "era": era, "eraT": ERAS[era - 1][1], "eraP": ERAS[era - 1][2],
                    "cat": CAT_L[c], "c": c, "b": b, "s": s, "sT": SALLES[s][1], "sU": f"{SALLES[s][0]}.html",
                    "img": f"assets/img/salles/{d}/{n}", "txt": txt, "imp": imp,
                    "url": url[1] if url else None, "urlT": url[0] if url else None,
                    "au": ERAS[era - 1][3], "at": ERAS[era - 1][4]})
    js = json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="fr-data">{js}</script>'


def epoques():
    out = []
    for n, t, p, au, at in ERAS:
        nb = sum(1 for ev in EV if ev[3] == n)
        first = next(i for i, ev in enumerate(EV) if ev[3] == n)
        img = EV[first][7]
        d, nm = img.split("/")
        out.append(f"""
      <li class="ep" data-reveal style="--i:{n}">
        <button type="button" class="ep-btn" data-era="{n}">
          <span class="ep-img"><img src="{{{{ROOT}}}}assets/img/salles/{d}/{nm}-960.jpg" alt="" loading="lazy" decoding="async"></span>
          <span class="ep-n">Époque {n}</span>
          <span class="ep-t">{e(t)}</span>
          <span class="ep-p">{e(p)} · {nb} jalon{'s' if nb > 1 else ''}</span>
          <span class="ep-go">Voir dans la frise</span>
        </button>
      </li>""")
    return f'<ol class="ep-list">{"".join(out)}\n    </ol>'


# Écart entre rédaction et plus ancienne copie conservée (ordres de grandeur couramment cités)
ECART = [
    ("Nouveau Testament", "rédigé ≈ 50 – 100", "≈ 50 ans", 50, "plus de 5 800", 5800, "en grec, sans compter plus de 10 000 manuscrits latins", True),
    ("Homère, l'Iliade", "composée ≈ VIIIᵉ s. av. J.-C.", "≈ 400 ans", 400, "≈ 1 900", 1900, "papyrus et manuscrits", False),
    ("Tacite, les Annales", "rédigées ≈ 116", "≈ 750 ans", 750, "2", 2, "manuscrits principaux (livres I-VI et XI-XVI)", False),
    ("Jules César, la Guerre des Gaules", "rédigée ≈ 50 av. J.-C.", "≈ 900 ans", 900, "≈ 250", 250, "manuscrits", False),
]


def ecart():
    rows = []
    for name, date, gap_l, gap, nb_l, nb, nb_s, bible in ECART:
        w1 = max(1.5, gap / 1000 * 100)
        w2 = max(0.6, nb / 5800 * 100)
        rows.append(f"""
      <li class="ec-row{' is-bible' if bible else ''}" data-reveal>
        <div class="ec-name"><b>{e(name)}</b><span>{e(date)}</span></div>
        <div class="ec-bars">
          <div class="ec-bar ec-gap"><span class="ec-fill" style="--w:{w1:.1f}%"></span><span class="ec-v">{e(gap_l)}</span></div>
          <div class="ec-bar ec-nb"><span class="ec-fill" style="--w:{w2:.1f}%"></span><span class="ec-v">{e(nb_l)} <small>{e(nb_s)}</small></span></div>
        </div>
      </li>""")
    return f"""
    <div class="ec-legend"><span class="ec-k ec-k-gap"><i></i>Écart entre la rédaction et la plus ancienne copie conservée</span><span class="ec-k ec-k-nb"><i></i>Nombre de manuscrits anciens connus</span></div>
    <ol class="ec-list">{"".join(rows)}
    </ol>"""


ORDRE = [  # (titre, date affichée, année)
    ("La Bible de Gutenberg", "≈ 1455", 1455),
    ("La Septante", "≈ 280 av. J.-C.", -280),
    ("Le Codex d'Alep", "≈ 930", 930),
    ("Le papyrus P52", "≈ 100 – 150", 125),
    ("Les rouleaux de Ketef Hinnom", "≈ 600 av. J.-C.", -600),
    ("La Vulgate de Jérôme", "405", 405),
]


def ordre():
    items = "".join(f"""
        <li class="or-it" data-y="{y}">
          <span class="or-n"></span>
          <span class="or-t">{e(t)}</span>
          <span class="or-d" hidden>{e(d)}</span>
          <span class="or-btns"><button type="button" class="or-up" aria-label="Monter : {e(t)}">↑</button><button type="button" class="or-dn" aria-label="Descendre : {e(t)}">↓</button></span>
        </li>""" for t, d, y in ORDRE)
    return f"""
      <ol class="or-list" aria-label="Événements à classer">{items}
      </ol>
      <div class="or-bar">
        <button type="button" class="btn btn-or or-check">Vérifier</button>
        <button type="button" class="btn btn-ghost or-mix">Mélanger</button>
        <span class="or-msg" aria-live="polite">Utilisez les flèches pour classer du plus ancien au plus récent.</span>
      </div>"""


TR_INTRO = """<p>Bienvenue dans la grande frise de VERBUM. Devant vous s'étendent trois mille cinq cents ans d'histoire : de Moïse, dans le désert du Sinaï, jusqu'aux laboratoires d'imagerie de 2026. Chaque point lumineux est un jalon de la transmission de la Bible : un texte rédigé, un manuscrit copié, une traduction, une impression, une découverte. Faites défiler la frise, choisissez une époque, ouvrez une fiche. Vous verrez se dessiner un fil continu. Des scribes aux imprimeurs, des copistes aux archéologues, des milliers de mains se sont transmis le même texte, génération après génération. Et chaque fois que l'on a pu comparer les copies anciennes et les copies récentes, le constat a été le même : malgré les siècles, les guerres et les bûchers, le message est parvenu jusqu'à nous, pour l'essentiel intact. Bonne traversée des millénaires.</p>
<p>Pour vous guider, la frise est divisée en huit époques, des origines à l'ère numérique. Les couleurs distinguent la nature de chaque jalon : la rédaction des livres, les manuscrits, les traductions, l'imprimerie, les persécutions et les découvertes. Les badges signalent clairement les textes canoniques, et les rares textes apocryphes qui apparaissent sur ce parcours. Un dernier conseil : regardez les écarts. Entre la rédaction d'un livre et la plus ancienne copie conservée, il s'écoule parfois moins d'un siècle pour le Nouveau Testament, quand il faut souvent attendre près de mille ans pour les grands auteurs grecs et latins.</p>"""

TR = {
    "origines": """<p><b>Époque 1.</b> Tout commence, selon la tradition biblique, dans le désert du Sinaï, vers 1500 ans avant notre ère, lorsque Moïse consigne la Loi. Les siècles suivants laissent des traces dans la pierre. Vers 1208 avant notre ère, le pharaon Merneptah fait graver le nom d'Israël sur une stèle : c'est la plus ancienne mention connue de ce peuple hors de la Bible. Au IXᵉ siècle avant notre ère, la stèle de Mésha, roi de Moab, cite Omri, roi d'Israël, et le nom divin, Jéhovah. La stèle de Tel Dan évoque la maison de David. Vers 600 avant notre ère, à Jérusalem, deux minuscules rouleaux d'argent sont gravés de la bénédiction du livre des Nombres : « Que Jéhovah te bénisse et te garde. » C'est le plus ancien texte biblique connu. Puis vient l'exil à Babylone, et, en 539, la victoire de Cyrus, roi de Perse, qui laisse les déportés rentrer chez eux.</p>
<p><b>Époque 2.</b> De retour à Jérusalem, le prêtre Esdras, que la Bible appelle un copiste habile, lit publiquement la Loi devant le peuple rassemblé. La tradition juive lui attribue un rôle central dans la préservation des Écritures. Vers 280 avant notre ère, à Alexandrie, des savants juifs traduisent la Torah en grec : c'est la Septante. Elle sera ensuite étendue à toute la Bible hébraïque, et deviendra la Bible des premiers chrétiens de langue grecque. Vers 125 avant notre ère, près de la mer Morte, un copiste recopie les 66 chapitres d'Ésaïe sur 17 feuilles de cuir cousues bout à bout. Ce grand rouleau, retrouvé en 1947, a permis une comparaison saisissante : plus ancien de mille ans que les manuscrits connus jusque-là, il transmet, pour l'essentiel, le même texte.</p>""",
    "codex": """<p><b>Époque 3.</b> Au Iᵉʳ siècle de notre ère, une nouvelle série d'écrits voit le jour. Vers l'an 50, l'apôtre Paul envoie ses premières lettres aux communautés de Grèce et d'Asie Mineure. Les Évangiles sont rédigés au cours des décennies suivantes, et vers la fin du siècle, l'apôtre Jean achève son Évangile, ses lettres et la Révélation. La rédaction de la Bible est terminée. Très vite, les textes sont recopiés sur papyrus, sous une forme nouvelle : le codex, le livre à pages. Le papyrus P52, un fragment de l'Évangile de Jean pas plus grand qu'une carte bancaire, est daté entre 100 et 150 environ. Il circulait déjà en Égypte, loin de l'endroit où l'Évangile fut écrit. Vers l'an 200, le papyrus P66 contient presque tout l'Évangile de Jean. Le texte est déjà là, copié et diffusé, à peine quelques générations après sa rédaction.</p>
<p><b>Époque 4.</b> En 303, l'empereur Dioclétien ordonne de brûler les Écritures. Mais moins de trente ans plus tard, l'empereur Constantin en commande cinquante exemplaires. C'est l'époque des grandes Bibles sur parchemin : le Codex Vaticanus, le Codex Sinaïticus, qui contient le plus ancien Nouveau Testament complet connu, puis, au Vᵉ siècle, le Codex Alexandrinus. La Bible est traduite dans les langues de l'Empire, et au-delà. À Bethléem, entre 382 et 405, Jérôme traduit la Bible en latin à partir de l'hébreu et du grec : sa Vulgate sera lue pendant plus de mille ans en Occident. En syriaque, la Peshitta se répand depuis Édesse jusqu'en Perse et en Inde. Au VIᵉ siècle enfin, un copiste grec réalise le Codex H des lettres de Paul, dont 42 pages effacées ont été restituées en 2026.</p>""",
    "copistes": """<p><b>Époque 5.</b> Pendant près de mille ans, la Bible est transmise à la main. À Tibériade, au bord du lac de Galilée, des familles de savants juifs, les massorètes, ajoutent au texte hébreu des voyelles, des accents et des milliers de notes de contrôle. Ils comptent les lettres, les mots et les versets, et repèrent le milieu de chaque livre, pour qu'aucune erreur ne se glisse dans les copies. Vers 930, Aaron ben Asher annote le Codex d'Alep. En 1008, le Codex de Leningrad devient le plus ancien manuscrit complet de la Bible hébraïque qui nous soit parvenu. Dans le monde grec et latin, les copistes multiplient les manuscrits. Au XIVᵉ siècle, en Angleterre, John Wycliffe et ses disciples traduisent la Bible en anglais à partir du latin. Interdite en 1408, leur traduction est pourtant recopiée en secret : plus de 250 manuscrits nous sont parvenus.</p>
<p><b>Époque 6.</b> Vers 1455, à Mayence, Johannes Gutenberg imprime la première Bible en caractères mobiles. En quelques décennies, le livre devient moins rare et moins cher. En 1516, à Bâle, Érasme publie le Nouveau Testament grec, et ouvre la voie à des traductions faites directement sur les langues originales. Caché au château de la Wartburg, Martin Luther traduit le Nouveau Testament en allemand en onze semaines ; il paraît en 1522, et la Bible complète en 1534. William Tyndale fait de même pour l'anglais, au prix de sa vie. En 1535, près de Neuchâtel, Pierre Robert Olivétan publie la première Bible protestante en français traduite sur l'hébreu et le grec. Enfin, en 1611, la Bible du roi Jacques paraît à Londres. Elle façonnera la langue anglaise pendant des siècles.</p>""",
    "decouvertes": """<p><b>Époque 7.</b> En 1800, au pays de Galles, une jeune fille de quinze ans, Mary Jones, marche une quarantaine de kilomètres pour acheter une Bible dans sa langue. Son histoire contribue à la naissance, en 1804, de la Société biblique britannique et étrangère, la première d'une longue série. Au même siècle, les savants partent à la recherche des manuscrits anciens. Au monastère Sainte-Catherine du Sinaï, Constantin von Tischendorf fait connaître le Codex Sinaïticus. En 1902, le papyrus Nash, qui contient les Dix Paroles en hébreu, devient le plus ancien texte biblique hébreu connu. Puis le XXᵉ siècle multiplie les découvertes : la bibliothèque de Nag Hammadi en 1945, faite de textes non canoniques ; les manuscrits de la mer Morte, à partir de 1947 ; et, en 1979, les rouleaux d'argent de Ketef Hinnom, à Jérusalem.</p>
<p><b>Époque 8.</b> À la fin du XXᵉ siècle, la Bible franchit encore des frontières fermées : en 1981, un million de Bibles sont débarquées en une seule nuit sur une plage de Chine. Puis vient l'ère numérique. En 2009, les feuillets du Codex Sinaïticus, dispersés entre Londres, Leipzig, le Sinaï et Saint-Pétersbourg, sont réunis et publiés en ligne. Chacun peut désormais consulter, depuis chez lui, un manuscrit du IVᵉ siècle. Les manuscrits de la mer Morte, les grands codex et des milliers de papyrus sont photographiés en haute résolution. En 2026, grâce à l'imagerie multispectrale, l'équipe du professeur Garrick Allen, à l'université de Glasgow, restitue 42 pages effacées du Codex H : des lettres de Paul déjà connues, qui confirment le texte transmis. Aujourd'hui, la Bible complète existe en 807 langues. Le fil n'a jamais été rompu.</p>""",
}


def img(name, alt, caption, sizes="100vw", root="{{ROOT}}", extra=""):
    p = f"{root}assets/img/salles/11/{name}"
    return (f'<img src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" data-lightbox data-full="{p}.jpg" data-caption="{e(caption)}"{extra}>')


def render(inner):
    rep = {
        "{{S11_ERAS}}": eras(),
        "{{S11_CATS}}": cats(),
        "{{S11_MINI}}": mini(),
        "{{S11_RAIL}}": rail(),
        "{{S11_DATA}}": data(),
        "{{S11_NB}}": str(len(EV)),
        "{{S11_EPOQUES}}": epoques(),
        "{{S11_ECART}}": ecart(),
        "{{S11_ORDRE}}": ordre(),
        "{{S11_TR_INTRO}}": TR_INTRO,
        "{{S11_TR_ORIGINES}}": TR["origines"],
        "{{S11_TR_CODEX}}": TR["codex"],
        "{{S11_TR_COPISTES}}": TR["copistes"],
        "{{S11_TR_DECOUVERTES}}": TR["decouvertes"],
        "{{IMG_FIN}}": img("fin", "Un rouleau de parchemin se prolonge en un livre imprimé puis en une tablette numérique, d'où s'élève une rivière de lumière dorée",
                           "Trois mille ans de transmission d'un même texte. Reconstitution numérique."),
    }
    for k, v in rep.items():
        inner = inner.replace(k, v)
    return inner


if __name__ == "__main__":
    out = render("{{S11_ERAS}}{{S11_CATS}}{{S11_MINI}}{{S11_RAIL}}{{S11_DATA}}{{S11_EPOQUES}}{{S11_ECART}}{{S11_ORDRE}}")
    assert "{{S11" not in out
    print("ok", len(EV), "événements", len(out))
