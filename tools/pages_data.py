"""VERBUM — Contenus des pages transversales (E14) : textes, bibliographie, crédits."""

# ---------------------------------------------------------------- Audioguide
GUIDE_ACCUEIL = [
    "Bienvenue dans l'audioguide de VERBUM, le Musée virtuel de la Bible. Je serai votre guide tout au long d'un voyage de trois mille cinq cents ans, des tablettes de pierre jusqu'aux écrans d'aujourd'hui.",
    "Le parcours compte douze salles. Dans chacune, des narrations comme celle-ci racontent ce que vous avez sous les yeux : un fragment de papyrus, un rouleau de cuir, une page imprimée, une stèle gravée. Vous pouvez les écouter à la suite, comme une seule grande visite, ou choisir librement un chapitre dans la liste. Le lecteur garde votre place : si vous quittez la page, vous reprendrez exactement là où vous vous étiez arrêté. Et si vous souhaitez lire plutôt qu'écouter, chaque narration possède sa transcription complète, dans la salle correspondante.",
    "Une question guidera toute notre visite : le texte que nous lisons aujourd'hui est-il bien celui qui a été écrit ? Pour y répondre, nous suivrons les témoins eux-mêmes. Les rouleaux d'argent de Ketef Hinnom, les scribes et les massorètes, les grottes de Qumrân, les grands codex grecs, les traducteurs d'Alexandrie et de Bethléem, l'atelier de Gutenberg, puis les archéologues et les chercheurs de notre siècle, et enfin les traducteurs qui ont fait parler la Bible en français.",
    "Au fil des salles, vous verrez deux étiquettes : canonique, pour les livres reconnus dans la Bible, et apocryphe, pour les écrits anciens qui n'y ont pas été retenus. Chaque texte en hébreu ou en grec est accompagné de sa traduction française. Installez-vous confortablement, ouvrez grand les yeux et les oreilles. La visite commence au pied du Sinaï.",
]

GUIDE_EPILOGUE = [
    "Notre visite touche à sa fin. Nous avons parcouru trois mille cinq cents ans en douze salles. Nous avons vu deux minuscules rouleaux d'argent, cachés dans une tombe près de Jérusalem, porter déjà la bénédiction du livre des Nombres. Nous avons suivi les scribes qui comptaient les lettres, et les massorètes qui ont fixé chaque voyelle.",
    "Nous sommes entrés dans les grottes de Qumrân, où le grand rouleau d'Ésaïe a fait reculer d'environ mille ans la plus ancienne copie connue de ce livre. Puis sont venus les papyrus et les grands codex, les traductions en grec, en latin et en syriaque, la presse de Gutenberg, et les pierres gravées qui confirment les noms des rois et des gouverneurs. Nous avons vu des Bibles brûlées, interdites, cachées, et pourtant recopiées. Et nous avons suivi, de Lefèvre d'Étaples à Louis Segond, la Bible devenue française.",
    "Qu'avons-nous appris ? Les manuscrits ne sont pas tous identiques. Les copistes ont parfois hésité, oublié un mot, modifié une orthographe. Mais ces différences sont connues, comptées et étudiées, et elles ne changent pas le message. Plus de cinq mille huit cents manuscrits grecs du Nouveau Testament, des milliers de témoins hébreux, des traductions anciennes dans de nombreuses langues : aucun autre texte de l'Antiquité n'est aussi bien attesté.",
    "Le prophète Ésaïe l'avait écrit : « L'herbe se dessèche, la fleur se fane, mais la parole de notre Dieu subsiste pour toujours. » Merci de votre visite. Les portes de VERBUM restent ouvertes : revenez quand vous le souhaitez, et prenez le temps, à votre tour, de lire ce livre qui a traversé les millénaires.",
]

# ---------------------------------------------------------------- À propos
APROPOS_TR = [
    "VERBUM est un musée virtuel. Il n'a ni murs ni billetterie, mais il poursuit une ambition : raconter, de façon claire et vérifiable, comment la Bible est parvenue jusqu'à nous.",
    "Chaque salle s'appuie sur des sources publiées : catalogues de musées, éditions savantes, rapports de fouilles et bibliothèques numériques. Quand un manuscrit est consultable en ligne, un bouton « Voir l'original » vous y conduit directement : au Musée d'Israël, à la British Library, à la Bibliothèque vaticane, au Louvre ou à l'Université de Glasgow. Les chiffres sont arrondis et datés, et nous signalons les débats chaque fois que les spécialistes ne sont pas d'accord. Notre but n'est pas de vous demander de nous croire sur parole, mais de vous donner les moyens de vérifier par vous-même.",
    "Quelques principes guident notre travail. Les livres reconnus dans le canon biblique portent l'étiquette canonique ; les écrits anciens qui n'y ont pas été retenus portent l'étiquette apocryphe, ou non canonique. Tout texte hébreu, grec, latin ou syriaque est accompagné de sa traduction française. Le nom divin, écrit en hébreu avec quatre lettres, est rendu par Jéhovah.",
    "Les illustrations du musée sont des reconstitutions numériques : elles aident à imaginer les lieux et les objets, mais elles ne remplacent pas les photographies d'archives, vers lesquelles nous renvoyons chaque fois que possible. Enfin, nous distinguons toujours les faits établis des légendes, même lorsque celles-ci sont belles. Bonne visite, et bonne lecture.",
]

PRINCIPES = [
    ("I", "Canonique ou apocryphe : toujours dit",
     'Chaque texte porte son étiquette : <span class="badge badge-canon">Canonique</span> pour les livres reconnus dans le canon biblique, '
     '<span class="badge badge-apo">Apocryphe</span> ou <span class="badge badge-apo">Non canonique</span> pour les écrits anciens qui n\'y ont pas été retenus.'),
    ("II", "Toujours traduit en français",
     "Tout passage en hébreu, en araméen, en grec, en latin ou en syriaque est immédiatement suivi de sa traduction française. "
     "Les textes courts sont donnés en entier, les textes longs sont résumés en détail."),
    ("III", "Le nom divin : Jéhovah",
     "Le Tétragramme hébreu est rendu par « Jéhovah », forme française traditionnelle du nom divin, au lieu d'être remplacé par un titre."),
    ("IV", "Reconstitutions signalées",
     "Les illustrations sont des créations numériques, marquées « Illustration » ou « Reconstitution ». "
     "Pour voir les objets réels, suivez les boutons « Voir l'original »."),
    ("V", "Faits et légendes séparés",
     "Une belle histoire n'est pas une preuve. La salle 10 consacre une vitrine entière au tri entre le vrai et le faux, "
     "par exemple la prétendue prophétie de Voltaire."),
    ("VI", "Des chiffres datés",
     "Le nombre de manuscrits, de langues ou d'exemplaires évolue avec les découvertes. "
     "Chaque chiffre est arrondi, daté et renvoie à sa source."),
]

VIGILANCE = [
    ("Le papyrus P52.", "Il est le plus souvent daté entre 100 et 150 environ ; certains chercheurs proposent une date plus tardive. Nous ne donnons pas d'année précise."),
    ("Le Codex Sinaïticus.", "C'est le plus ancien manuscrit complet du Nouveau Testament (IVe siècle) ; le Vaticanus, aussi ancien, est incomplet à la fin."),
    ("La stèle de Mésha.", "La lecture « maison de David » à la ligne 31 est proposée par André Lemaire et reste débattue ; les mentions d'Omri et de Jéhovah, elles, sont sûres."),
    ("Ebla et Sodome.", "Les rapprochements proposés dans les années 1970 entre les tablettes d'Ebla et les villes de la plaine sont contestés : nous ne les présentons pas comme des preuves."),
    ("Le papyrus Ipuwer.", "Ce texte égyptien n'est pas un récit des plaies d'Égypte ; il n'est pas utilisé comme preuve dans le musée."),
    ("La « prophétie » de Voltaire.", "Elle ne figure dans aucun de ses écrits ; l'histoire de sa maison devenue dépôt de Bibles est une légende, présentée comme telle."),
    ("Trois langues.", "La Bible a été rédigée en hébreu, en araméen et en grec, par une quarantaine de rédacteurs, et non en quarante langues."),
    ("Ésaïe 9:6.", "Ce verset correspond à Ésaïe 9:5 dans la numérotation hébraïque ; nous le précisons quand nous citons le texte hébreu."),
]

TECHNIQUE = [
    ("Site statique.", "Des pages HTML, CSS et JavaScript, sans serveur d'application ni base de données : le musée fonctionne aussi hors ligne, depuis l'archive ZIP."),
    ("Aucun pistage.", "Pas de cookies, pas de mesure d'audience, aucune ressource tierce chargée : polices, images et sons sont hébergés avec le site."),
    ("Accessibilité.", "Navigation complète au clavier, lien d'évitement, transcription de toutes les narrations, textes alternatifs et respect du réglage « réduire les animations »."),
    ("Narrations.", "Voix de synthèse en français, légère réverbération, MP3 à 192 kb/s, entre une et deux minutes chacune."),
    ("Illustrations.", "Reconstitutions photoréalistes générées numériquement, en JPG haute définition, vérifiées une à une."),
    ("Polices.", "Cormorant Garamond, EB Garamond, Cinzel Decorative, Inter, Noto Sans Hebrew et Frank Ruhl Libre, sous licence libre SIL Open Font License."),
    ("Cartes.", "Contours Natural Earth (domaine public), projetés et simplifiés pour le musée."),
]

SUGGESTIONS = ["Ketef Hinnom", "Jéhovah", "Ésaïe", "Codex H", "Septante", "Gutenberg", "Tyndale", "Mésha", "P52", "massorètes"]

# ---------------------------------------------------------------- Bibliographie
# (référence en langue de publication, présentation en français)
BIBLIO = [
    ("Bible hébraïque, scribes et massorètes", [
        ("Emanuel Tov, <i>Textual Criticism of the Hebrew Bible</i>, 3ᵉ éd., Minneapolis, Fortress Press, 2012.",
         "L'ouvrage de référence sur l'histoire du texte de l'Ancien Testament : manuscrits, versions anciennes et méthodes."),
        ("Ernst Würthwein, révisé par Alexander A. Fischer, <i>The Text of the Old Testament</i>, 3ᵉ éd., Grand Rapids, Eerdmans, 2014.",
         "Manuel classique, illustré de planches des principaux manuscrits hébreux."),
        ("David Noel Freedman (dir.), <i>The Leningrad Codex: A Facsimile Edition</i>, Grand Rapids, Eerdmans, 1998.",
         "Fac-similé intégral du Codex de Leningrad (1008), le plus ancien manuscrit complet de la Bible hébraïque."),
        ("Hayim Tawil et Bernard Schneider, <i>Crown of Aleppo</i>, Philadelphie, Jewish Publication Society, 2010.",
         "L'histoire mouvementée du Codex d'Alep, de Tibériade jusqu'à Jérusalem."),
        ("Gabriel Barkay, Andrew G. Vaughn, Marilyn J. Lundberg et Bruce Zuckerman, « The Amulets from Ketef Hinnom: A New Edition and Evaluation », <i>Bulletin of the American Schools of Oriental Research</i> 334, 2004, p. 41-71.",
         "La nouvelle édition des rouleaux d'argent, qui confirme leur datation vers 600 av. J.-C."),
    ]),
    ("Les manuscrits de la mer Morte", [
        ("Katell Berthelot, Thierry Legrand et André Paul (dir.), <i>La Bibliothèque de Qumrân</i>, Paris, Cerf, depuis 2008.",
         "Édition bilingue, en français, des manuscrits de Qumrân, classés selon les livres bibliques."),
        ("André Dupont-Sommer, <i>Les Écrits esséniens découverts près de la mer Morte</i>, Paris, Payot, 1959.",
         "Le classique francophone qui a fait connaître les textes de Qumrân au grand public."),
        ("James C. VanderKam et Peter W. Flint, <i>The Meaning of the Dead Sea Scrolls</i>, San Francisco, HarperSanFrancisco, 2002.",
         "Synthèse sur la découverte, le contenu et la portée des manuscrits pour le texte biblique."),
        ("Martin Abegg Jr., Peter Flint et Eugene Ulrich, <i>The Dead Sea Scrolls Bible</i>, San Francisco, HarperSanFrancisco, 1999.",
         "Traduction des manuscrits bibliques de Qumrân, avec leurs variantes par rapport au texte massorétique."),
        ("Geza Vermes, <i>The Complete Dead Sea Scrolls in English</i>, éd. révisée, Londres, Penguin, 2004.",
         "Traduction des textes non bibliques de Qumrân : Règle de la communauté, Rouleau de la Guerre, Rouleau du Temple."),
    ]),
    ("Le Nouveau Testament et ses manuscrits", [
        ("Léon Vaganay et Christian-Bernard Amphoux, <i>Initiation à la critique textuelle du Nouveau Testament</i>, Paris, Cerf, 1986.",
         "Introduction en français à l'étude des manuscrits du Nouveau Testament."),
        ("Bruce M. Metzger et Bart D. Ehrman, <i>The Text of the New Testament: Its Transmission, Corruption, and Restoration</i>, 4ᵉ éd., New York, Oxford University Press, 2005.",
         "Le manuel de référence sur la transmission du texte grec du Nouveau Testament."),
        ("Kurt Aland et Barbara Aland, <i>The Text of the New Testament</i>, 2ᵉ éd., Grand Rapids, Eerdmans, 1989.",
         "Présentation des catégories de manuscrits par les responsables de l'édition critique de Münster."),
        ("Larry W. Hurtado, <i>The Earliest Christian Artifacts: Manuscripts and Christian Origins</i>, Grand Rapids, Eerdmans, 2006.",
         "Ce que les plus anciens papyrus chrétiens révèlent : préférence pour le codex, abréviations des noms sacrés."),
        ("Brent Nongbri, <i>God's Library: The Archaeology of the Earliest Christian Manuscripts</i>, New Haven, Yale University Press, 2018.",
         "Une réévaluation critique de la datation des premiers papyrus, dont P52."),
        ("David C. Parker, <i>Codex Sinaiticus: The Story of the World's Oldest Bible</i>, Londres, British Library, 2010.",
         "L'histoire du Codex Sinaïticus, de sa copie au IVe siècle à sa numérisation intégrale."),
        ("Université de Glasgow, communiqué d'avril 2026 et édition numérique du Codex H (codexh.arts.gla.ac.uk).",
         "La restitution par imagerie multispectrale de 42 pages perdues des Lettres de Paul (salle 05)."),
    ]),
    ("Canon et textes apocryphes", [
        ("Jean-Pierre Mahé et Paul-Hubert Poirier (dir.), <i>Écrits gnostiques. La bibliothèque de Nag Hammadi</i>, Paris, Gallimard, « Bibliothèque de la Pléiade », 2007.",
         "Traduction française intégrale des codex de Nag Hammadi."),
        ("François Bovon et Pierre Geoltrain (dir.), <i>Écrits apocryphes chrétiens</i>, t. I, Paris, Gallimard, « Bibliothèque de la Pléiade », 1997.",
         "Les principaux apocryphes chrétiens traduits et présentés en français."),
        ("Marvin Meyer (dir.), <i>The Nag Hammadi Scriptures</i>, New York, HarperOne, 2007.",
         "Édition anglaise de référence des textes de Nag Hammadi, avec introductions."),
        ("Bruce M. Metzger, <i>The Canon of the New Testament: Its Origin, Development, and Significance</i>, Oxford, Clarendon Press, 1987.",
         "Comment et selon quels critères les livres du Nouveau Testament ont été reconnus."),
    ]),
    ("Les grandes traductions anciennes", [
        ("Marguerite Harl, Gilles Dorival et Olivier Munnich, <i>La Bible grecque des Septante</i>, Paris, Cerf, 1988.",
         "La synthèse francophone de référence sur la Septante, du judaïsme hellénistique au christianisme ancien."),
        ("Jennifer M. Dines, <i>The Septuagint</i>, Londres, T&amp;T Clark, 2004.",
         "Une introduction claire à l'histoire et aux enjeux de la Bible grecque."),
        ("J. N. D. Kelly, <i>Jerome: His Life, Writings, and Controversies</i>, Londres, Duckworth, 1975.",
         "La biographie de référence de Jérôme, traducteur de la Vulgate à Bethléem."),
        ("Sebastian P. Brock, <i>The Bible in the Syriac Tradition</i>, 2ᵉ éd., Piscataway, Gorgias Press, 2006.",
         "La Peshitta et les autres versions syriaques, par le grand spécialiste du domaine."),
    ]),
    ("La Bible en français", [
        ("Pierre-Maurice Bogaert (dir.), <i>Les Bibles en français. Histoire illustrée du Moyen Âge à nos jours</i>, Turnhout, Brepols, 1991.",
         "La synthèse de référence sur les traductions françaises, des psautiers médiévaux aux versions contemporaines (salle 12)."),
        ("<i>La Bible d'Olivétan, 1535</i>, fac-similé numérique, Bibliothèque de Genève, e-rara (doi:10.3931/e-rara-5690).",
         "L'exemplaire numérisé de la première Bible française traduite sur l'hébreu et le grec."),
        ("Philippe Sellier (éd.), <i>La Bible</i>, traduction de Louis-Isaac Lemaistre de Sacy, Paris, Robert Laffont, « Bouquins », 1990.",
         "Réédition de la Bible de Port-Royal, avec une introduction historique."),
    ]),
    ("Imprimerie, Réforme et diffusion", [
        ("Lucien Febvre et Henri-Jean Martin, <i>L'Apparition du livre</i>, Paris, Albin Michel, 1958.",
         "Le classique français sur la naissance et la diffusion du livre imprimé."),
        ("Elizabeth L. Eisenstein, <i>The Printing Revolution in Early Modern Europe</i>, Cambridge, Cambridge University Press, 1983.",
         "Les effets de l'imprimerie sur la culture européenne (traduction française : <i>La Révolution de l'imprimé</i>)."),
        ("Eric Marshall White, <i>Editio princeps: A History of the Gutenberg Bible</i>, Turnhout, Harvey Miller, 2017.",
         "L'histoire de la Bible à 42 lignes et le recensement de ses exemplaires."),
        ("David Daniell, <i>William Tyndale: A Biography</i>, New Haven, Yale University Press, 1994.",
         "La vie du traducteur anglais exécuté en 1536 pour avoir traduit la Bible."),
    ]),
    ("Archéologie et inscriptions", [
        ("Lawrence J. Mykytiuk, <i>Identifying Biblical Persons in Northwest Semitic Inscriptions of 1200–539 B.C.E.</i>, Atlanta, Society of Biblical Literature, 2004.",
         "La méthode pour identifier avec certitude un personnage biblique dans une inscription."),
        ("Lawrence J. Mykytiuk, « Archaeology Confirms 50 Real People in the Bible », <i>Biblical Archaeology Review</i> 40/2, 2014.",
         "La liste des personnages de l'Ancien Testament attestés par l'archéologie (salle 09)."),
        ("Avraham Biran et Joseph Naveh, « An Aramaic Stele Fragment from Tel Dan », <i>Israel Exploration Journal</i> 43, 1993, p. 81-98.",
         "La publication de la stèle de Tel Dan et de la mention de la « maison de David »."),
        ("André Lemaire, « “House of David” Restored in Moabite Inscription », <i>Biblical Archaeology Review</i> 20/3, 1994.",
         "La lecture proposée de la « maison de David » sur la stèle de Mésha, toujours débattue."),
        ("Irving Finkel (dir.), <i>The Cyrus Cylinder: The Great Persian Edict from Babylon</i>, Londres, I. B. Tauris, 2013.",
         "Le cylindre de Cyrus, sa traduction et son lien avec le retour des exilés."),
        ("Bezalel Porten (dir.), <i>The Elephantine Papyri in English</i>, Leyde, Brill, 1996.",
         "Les papyrus d'Éléphantine traduits, dont la lettre mentionnant Johanan et les fils de Sanballat."),
        ("Irving Finkel, <i>The Ark Before Noah</i>, Londres, Hodder &amp; Stoughton, 2014.",
         "Les récits mésopotamiens du déluge et les tablettes de la bibliothèque d'Assurbanipal."),
    ]),
    ("Persécutions et survie du texte", [
        ("Eusèbe de Césarée, <i>Histoire ecclésiastique</i>, livres VIII-X, trad. Gustave Bardy, Paris, Cerf, « Sources chrétiennes » 55, 1958.",
         "Le témoignage d'un contemporain sur la persécution de Dioclétien et les Écritures livrées au feu."),
        ("Lactance, <i>De la mort des persécuteurs</i>, trad. Jacques Moreau, Paris, Cerf, « Sources chrétiennes » 39, 1954.",
         "Le récit de l'édit de 303 par un témoin de la cour impériale."),
        ("Frère André, avec John et Elizabeth Sherrill, <i>God's Smuggler</i>, 1967 (traduction française : <i>Le Contrebandier de Dieu</i>).",
         "Le récit du passage de Bibles derrière le rideau de fer (salle 10)."),
    ]),
]

# ---------------------------------------------------------------- Chiffres
STATS = [
    ("Traductions de la Bible (septembre 2026).",
     "7 394 langues dans le monde ; Bible complète dans 807 langues, Nouveau Testament dans 1 844, portions dans 1 519.",
     "https://wycliffe.org.uk/statistics/", "Wycliffe Bible Translators"),
    ("Diffusion en 2025.",
     "148,3 millions de publications bibliques imprimées, dont 22,4 millions de Bibles complètes ; 32,2 milliards de chapitres consultés en ligne.",
     "https://www.unitedbiblesocieties.org/", "Alliance biblique universelle"),
    ("Manuscrits grecs du Nouveau Testament.",
     "Plus de 5 800 manuscrits grecs catalogués : papyrus, onciaux, minuscules et lectionnaires.",
     "https://ntvmr.uni-muenster.de/liste", "INTF, Université de Münster"),
    ("Manuscrits de la mer Morte.",
     "Environ 900 manuscrits retrouvés dans les onze grottes de Qumrân, dont plus de 200 copies de livres bibliques.",
     "https://www.deadseascrolls.org.il/?locale=fr_FR", "Bibliothèque numérique Leon Levy"),
    ("Le projet Perle (1981).",
     "Un million de Bibles chinoises débarquées en une nuit, le 18 juin 1981, sur une plage près de Shantou.",
     "https://www.opendoorscanada.org/project-pearl", "Portes Ouvertes"),
    ("Le Codex H (2026).",
     "42 pages perdues des Lettres de Paul, déjà connues par ailleurs, restituées par imagerie multispectrale.",
     "https://www.gla.ac.uk/news/headline_1263245_en.html", "Université de Glasgow"),
]

CREDITS = [
    ("Illustrations.", "{NB_IMG} reconstitutions photoréalistes générées numériquement (JPG 1920 × 1080 et 960 × 540), signalées « Illustration » ou « Reconstitution ». Ce ne sont pas des documents d'archive."),
    ("Narrations.", "{NB_AUDIO} narrations en français réalisées par synthèse vocale, avec une légère réverbération (MP3, 192 kb/s)."),
    ("Textes anciens.", "Texte massorétique (Codex de Leningrad), manuscrits de Qumrân et éditions critiques du Nouveau Testament ; traductions françaises établies pour le musée."),
    ("Polices.", "Cormorant Garamond, EB Garamond, Cinzel Decorative, Cinzel, Inter, Noto Sans Hebrew, Frank Ruhl Libre, Noto Sans Phoenician, Noto Sans Syriac et UnifrakturMaguntia, sous licence SIL Open Font License 1.1."),
    ("Cartes.", "Contours Natural Earth (domaine public)."),
    ("Institutions citées.", "Les liens vers les musées, bibliothèques et universités n'impliquent aucun partenariat : VERBUM est un projet indépendant."),
]
