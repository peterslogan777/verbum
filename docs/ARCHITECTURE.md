# VERBUM — Architecture du projet (mise à jour : étapes E05 et E07)

## Arborescence

```
verbum/
├── index.html                  Hall d'entrée (généré)
├── favicon.svg · favicon-32.jpg · apple-touch-icon.jpg (icônes en JPG depuis la restauration)
├── salles/                     11 pages de salles (générées)
│   ├── 01-origines.html        Les Origines — Moïse et les premiers textes      → E03
│   ├── 02-copistes.html        Les Copistes et les Massorètes                   → E04
│   ├── 03-qumran.html          Les Manuscrits de la mer Morte (salle phare)     → E05
│   ├── 04-codex-grecs.html     Les Grands Codex grecs                           → E06
│   ├── 05-codex-h.html         Découverte 2026 : le Codex H                     → E07
│   ├── 06-apocryphes.html      Les Textes apocryphes                            → E08
│   ├── 07-traductions.html     La Septante et les grandes traductions           → E09
│   ├── 08-gutenberg.html       Gutenberg et l'imprimerie                        → E10
│   ├── 09-archeologie.html     Les Preuves archéologiques                       → E11
│   ├── 10-indestructible.html  Le Livre indestructible                          → E12
│   ├── 11-frise.html           La Grande Frise chronologique                    → E13
│   └── 12-bible-francaise.html La Bible en français (ajout après E14)            → E15
├── assets/
│   ├── css/
│   │   ├── fonts.css           @font-face auto-hébergés
│   │   ├── tokens.css          Design tokens (couleurs, typos, espacements, mouvement)
│   │   ├── base.css            Reset, typographie, hébreu/grec, révélations, curseur
│   │   ├── components.css      Loader, en-tête, plan du musée, boutons, badges, cartes, audio, pied de page
│   │   ├── home.css            Hall d'entrée
│   │   └── salle.css           Gabarit commun des salles
│   ├── js/main.js              Comportements interactifs (sans dépendance)
│   ├── fonts/                  29 fichiers WOFF2 (environ 840 Ko)
│   ├── img/                    logo-verbum.svg, icon-512.jpg ; images JPG des étapes suivantes
│   ├── audio/                  Narrations MP3 (à partir de E02)
│   └── data/salles.json        Données des salles (pour la recherche et la frise)
├── tools/
│   ├── build.py                Générateur (données des salles + gabarits)
│   ├── icons.py                Icônes SVG sans croix
│   └── templates/
│       ├── index.body.html     Corps du hall d'entrée
│       └── salles/<slug>.html  Corps propre de chaque salle (créé à son étape)
└── docs/ARCHITECTURE.md
```

## Charte graphique

| Jeton | Hex | Usage |
|---|---|---|
| Or sacré | `#C9A84C` | Titres, accents, bordures |
| Parchemin | `#F5E6C8` | Fonds de cartes de manuscrits |
| Noir profond | `#0A0A0F` | Fond général |
| Bleu nuit | `#0D1B2A` | Sections secondaires |
| Rouge antique | `#8B1A1A` | Apocryphes, accents dramatiques |
| Blanc parchemin | `#F0E8D5` | Texte sur fond sombre |
| Gris pierre | `#4A4A5A` | Métadonnées |
| Vert doré | `#7E9A4E` | Badge canonique |

Typographies : Cinzel Decorative (galeries), Cormorant Garamond (titres), EB Garamond (corps et grec),
Inter (interface), Frank Ruhl Libre et Noto Sans Hebrew (hébreu).

## Composants livrés à l'étape E01

- Loader : calligraphie de דבר (*davar*, « parole ») puis « VERBUM », affiché une fois par session
- Hero : ciel, soleil levant, rayons, paysage en quatre plans en parallaxe (monts de Moab, mer Morte, falaises de Qumrân, dunes), particules dorées en Canvas, titre gravé lettre par lettre avec éclats de ciseau
- En-tête translucide qui se masque au défilement vers le bas, avec barre de progression dorée
- Plan du musée : panneau latéral avec frise verticale des salles
- Cartes de salles : inclinaison 3D et halo doré qui suit le pointeur
- Compteurs animés, épigraphe Ésaïe 40:8 (hébreu, translittération, traduction)
- Badges canonique, apocryphe et datation débattue
- Lecteur audioguide (coquille ; branchement en E02)
- Curseur en forme de plume de scribe (écrans à souris uniquement)
- Gabarit de salle avec navigation précédente / suivante


## Ajouts de l'étape E02 — Hall d'entrée

| Fichier | Rôle |
|---|---|
| `tools/data_accueil.py` | Données du hall : diapositives du hero, 29 jalons de la frise, foyers de la carte, chiffres clés |
| `tools/accueil.py` | Générateurs HTML (diaporama, frise, carte) appelés par `build.py` |
| `tools/carte.py` + `tools/geo/ne_110m_land.geojson` | Projection de la carte du monde en SVG (Natural Earth) |
| `tools/templates/index.body.html`, `transcription-intro.html` | Corps de la page d'accueil et transcription de l'audioguide |
| `assets/js/accueil.js` | Diaporama Ken Burns, parchemin qui se déroule, frise horizontale, carte interactive |
| `assets/css/home.css` | Styles du hall |
| `assets/img/accueil/*.jpg` | 10 images 1920×1080 (+ versions `-960`) |
| `assets/audio/intro-verbum.mp3` | Narration d'introduction (2 min 25, 192 kb/s) |

## Ajouts de l'étape E03 — Salle 01 « Les Origines »

### Composants communs (réutilisés par toutes les salles suivantes)
| Fichier | Rôle |
|---|---|
| `assets/js/audio.js` | **Audioguide commun** (extrait de `accueil.js`) : lecteur MP3, visualiseur Web Audio, surlignage de la transcription, un seul lecteur actif à la fois. Déclencheur externe : `data-audio-trigger="clé"` → `#audio-clé`. Zone de transcription : `[data-audio-zone]` |
| `assets/js/main.js` §10–12 | `data-parallax` (image d'en-tête), **visionneuse plein écran** `[data-lightbox]` (`data-full`, `data-caption`, molette/double-clic = zoom, glisser, flèches, Échap), **loupe** `[data-loupe="2.6"]` |
| `assets/css/components.css` | Styles visionneuse et loupe ; badges `badge-preuve` (preuve solide) et `badge-debat` (contesté) ; `btn-sm` |
| `assets/css/salle.css` | En-tête de salle avec image (`has-img`), sommaire collant `.s-sommaire`, `.s-head`, `.sub-title`, `.drop`, `.tag` « Reconstitution », et (depuis E04) les composants partagés `.fiche` (fiche d'identité), `.seg` (sélecteur segmenté), `.debat` |
| `assets/fonts/noto-sans-phoenician.woff2` | Police de l'écriture paléo-hébraïque (bloc Unicode phénicien) |

### Mécanique de build
Dans `SALLES` (build.py), une salle peut déclarer `hero_img`, `css` et `js`. Si `tools/templates/salles/<slug>.html` existe, il remplace la page « en préparation » ; si `tools/salle_<slug>.py` existe, sa fonction `render(html)` y remplace les marqueurs `{{…}}` propres à la salle. Les marqueurs `{{ROOT}}`, `{{ARROW}}`, `{{PLAY}}` sont communs. Une salle dont l'étape figure dans `ETAPES_FAITES` affiche « Salle ouverte » dans le parcours.

### Fichiers de la salle 01
| Fichier | Rôle |
|---|---|
| `tools/templates/salles/origines.html` | Corps de la salle : I. Ketef Hinnom · II. Bénédiction · III. Moïse et la Torah · IV. Témoins |
| `tools/salle_origines.py` | Bénédiction mot à mot (conversion automatique hébreu → paléo-hébreu), lecture KH2, 5 livres de la Torah, alphabet, transcriptions |
| `assets/css/salle01.css`, `assets/js/salle01.js` | Styles et interactions (bascule d'écriture, mots de KH2, cartes à retourner, sommaire actif) |
| `assets/img/salles/01/*.jpg` | 10 images 1920×1080 (+ `-960`) |
| `assets/audio/salle01-ketef.mp3`, `salle01-moise.mp3` | Narrations (1 min 40 et 1 min 58, 192 kb/s) |

## Ajouts de l'étape E04 — Salle 02 « Les Copistes et les Massorètes »

| Fichier | Rôle |
|---|---|
| `tools/templates/salles/copistes.html` | I. Les scribes (Esdras, 8 règles, genizah) · II. Les Massorètes (trois couches, « un mot, trois lectures », page massorétique, compteurs) · Jeu du copiste · III. Codex d'Alep · IV. Codex de Leningrad |
| `tools/salle_copistes.py` | Genèse 1:1 découpée automatiquement en consonnes / niqqud / te'amim ; données du jeu (4 manches, lettre fautive calculée) ; carte SVG régionale du voyage du Codex d'Alep (contours Natural Earth, courbes sans croisement) ; schéma des 487 feuillets (294 conservés) ; transcriptions |
| `assets/css/salle02.css`, `assets/js/salle02.js` | Styles et interactions de la salle |
| `assets/img/salles/02/*.jpg` | 10 images 1920×1080 (+ `-960`) ; l'arrière-plan de « Esdras » a été adouci (flou de profondeur) pour supprimer un treillis de porte |
| `assets/audio/salle02-scribes.mp3`, `salle02-codex.mp3` | Narrations (1 min 45 et 2 min 00, 192 kb/s) |

`base.css` contient désormais `[hidden] { display: none !important; }` (les boutons `.btn` en `inline-flex` ignoraient l'attribut).


## Ajouts de l'étape E05 — Salle 03 « Les manuscrits de la mer Morte » (salle phare)

| Fichier | Rôle |
|---|---|
| `tools/salle_qumran.py` | Génère la carte schématique des grottes, les panneaux, les comptes de copies et les colonnes du rouleau (`tools/data/rouleau_colonnes.json`, Ésaïe 53, texte massorétique sans voyelles via Sefaria). |
| `tools/templates/salles/qumran.html` | Gabarit : annonce, visionneuse 3D, comparateur, frise, carte des grottes, fiches des rouleaux (badges canonique / non canonique), audio. |
| `assets/js/salle03.js` | **Visionneuse WebGL du rouleau** : un maillage en bande (L = 4) s'enroule sur deux cylindres (`uR` = 0.15, `uHW` = 0.56) ; on fait glisser le rouleau ou l'on utilise le curseur (`range` rtl, 0–1000) ; le panneau de traduction suit la colonne visible. Les uniformes du vertex shader et du fragment shader portent des noms distincts (sinon erreur de précision à l'édition des liens). Repli sur une image fixe sans WebGL. |
| `assets/css/salle03.css` | Visionneuse, comparateur (`.seg` + panneaux), frise `.qf`, carte `.gr-*`, grille des rouleaux `.r-grid`. Les compteurs utilisent `--f-titre` (chiffres alignés). |

## Ajouts de l'étape E06 — Salle 04 « Les Grands Codex grecs »

| Fichier | Rôle |
|---|---|
| `tools/salle_codex_grecs.py` | Données de la salle : lignes de P52 (`span.k` conservé / `span.l` restitué, d'après Roberts 1935, approché) et traductions, versets de P64 (Mt 26, grec + français), fiches des 4 codex (Vaticanus, Sinaiticus, Alexandrinus, Garima), frise du Sinaiticus (7 étapes), répartition des feuillets (Londres 347, Leipzig 43, Sinaï 12, Saint-Pétersbourg fragments), graphique comparatif, transcriptions. Remplace les `{{S04_*}}`. |
| `tools/templates/salles/codex-grecs.html` | 6 vitrines : papyrus (P66, P75), fragment P52 + débat de datation + P64, « Lire comme un scribe » (Luc 21:33 en 3 étapes), cartes des codex + Bible éthiopienne, odyssée du Sinaiticus, comparaison et liens « Voir l'original ». Pont vers la salle 05. |
| `assets/js/salle04.js` | Retournement recto/verso de P52 et bascule « texte restitué » (`.is-full`), étapes de la scriptio continua, cartes 3D au clic uniquement (`.is-flip`, focus géré), mode du graphique (`data-mode` n / g), délais d'apparition des points de feuillets, sommaire actif. |
| `assets/css/salle04.css` | `.p52*` (fragment en couches CSS « papyrus », rotation 3D), `.p64*`, `.vv`, `.sc*` (page de parchemin), `.cx*` (cartes 3D), `.eth`, `.sn` (frise), `.fe-*`, `.chart*` (barres pilotées par `--n` / `--g`). |

Chiffres du graphique présentés comme « ordres de grandeur ». Datations débattues signalées par `badge-debat` (P52, P64). Hénoch et Jubilés (canon éthiopien) portent le badge « Apocryphe ».

Médias : `assets/img/salles/04/` (9 images × 2 tailles : hero-codex, p52, oxyrhynchus, p66, tischendorf, vaticanus, alexandrinus, garima, scriptorium), `assets/audio/salle04-papyrus.mp3` (1 min 38 s) et `salle04-codex.mp3` (1 min 35 s), 192 kb/s.

## Ajout E15 — Salle 12 « La Bible en français »

- **Données** `tools/salle_bible_francaise.py` : frise médiévale (5 étapes avant 1500), Jean 1:1-5 d'Olivétan (orthographe de 1535 et modernisée, glossaire), comparateur de Jean 1:1 en 11 versions (Vulgate → Traduction du monde nouveau 2018, avec le grec et sa traduction mot à mot), tableau du nom divin (Olivétan « l'Éternel » / « Iehouah », Crampon 1904 « Jéhovah », Bible de Jérusalem « Yahvé », etc.), frise 1588-1910, traductions depuis 1956, jeu « Qui a traduit ? » (6 questions).
- **Gabarit** `tools/templates/salles/bible-francaise.html` : 8 vitrines, 2 narrations, liens « Voir l'original » (e-rara, Wikisource Sacy / Segond 1910 / Crampon 1923).
- **Règle** : VERBUM écrit « Jéhovah » ; les autres rendus du tétragramme ne sont cités que comme faits historiques.
- **Médias** : 8 JPG `assets/img/salles/12/` (hero, moyen-age, vaudois, olivetan, bastille, colporteur, segond, aujourdhui), préparés par `tools/salle12_images.py` à partir des images générées `s12-*.jpg` (non conservées, les JPG finaux font foi) (flou d'arrière-plan sur les éléments pouvant former des lignes croisées, recadrage d'une fenêtre à meneaux). MP3 `salle12-renaissance.mp3` (1 min 15 s) et `salle12-foyers.mp3` (1 min 09 s).
- **Audioguide** : `guide-accueil.mp3` et `guide-epilogue.mp3` réenregistrés (« douze salles »), même voix.
- **Fichiers** : `assets/css/salle12.css`, `assets/js/salle12.js` ; icône `livre-fr` dans `tools/icons.py`.

## Ajouts de l'étape E13 — Salle 11 « La Grande Frise chronologique »

- **Données** `tools/salle_frise.py` : 36 jalons de ≈ 1500 av. J.-C. à 2026, répartis en 8 époques et 7 catégories (rédaction, manuscrits, traductions, imprimé, témoins archéologiques, persécutions, découvertes). Chaque jalon a une date, un texte, une phrase « Pour la transmission », un badge CANONIQUE / APOCRYPHE et un lien vers sa salle, avec parfois un bouton « Voir l'original ». Le module contient aussi les données de l'écart (NT, Homère, Tacite, César) et du jeu « Remettre dans l'ordre ».
- **Gabarit** `tools/templates/salles/frise.html` : 5 vitrines (frise, huit époques, écart, ordre, fin). Les données des fiches sont en JSON dans `#fr-data`.
- **Frise** : rail horizontal à espacement régulier, plus une mini-carte proportionnelle au temps réel avec une fenêtre de visée. On peut la faire glisser à la souris ou au doigt, ou utiliser la molette, les flèches, les boutons précédent/suivant, les pastilles d'époque et les filtres par catégorie. Desktop : rail `--h: 700px`, colonnes de 290 px. Mobile : 650 / 236 px ; pastilles et filtres en bandes défilantes.
- **Fiche** : `<dialog class="fe">` centré. Elle comprend l'image, le texte, un commentaire audio de l'époque (lu dans le MP3 à partir du décalage `at`, arrêté au début de l'époque suivante), la navigation entre jalons au clavier et un bouton « Fermer » en texte, sans icône en X. Le son est exclusif grâce à l'événement `verbum:audio` partagé avec `audio.js`.
- **Écart** : barres animées au défilement. Une note rappelle que ce sont des ordres de grandeur.
- **Médias** : 10 JPG dans `assets/img/salles/11/` et 5 MP3 `salle11-{intro,origines,codex,copistes,decouvertes}.mp3`. Les 4 derniers couvrent chacun deux époques.
- **Fichiers** : `assets/css/salle11.css`, `assets/js/salle11.js`.

## Ajouts de l'étape E12 — Salle 10 « Le Livre indestructible »

- **Source** : `tools/salle_indestructible.py` (données + `render`) et `tools/templates/salles/indestructible.html`.
- **Styles / scripts** : `assets/css/salle10.css`, `assets/js/salle10-geo.js` (38 polygones Natural Earth 110 m, lon −25…135, lat −32…68), `assets/js/salle10.js`.
- **Médias** : `assets/img/salles/10/` (10 JPG × 2 tailles : hero, diocletien, cachette, bucher, vilvorde, lollards, madagascar, samizdat, plage, imprimerie) ; `assets/audio/salle10-flammes.mp3` (1:19) et `salle10-survie.mp3` (1:18), 192 kb/s, réverbération légère.
- **Retouches anti-croix** : ficelles croisées effacées (inpainting OpenCV) sur `cachette` et `samizdat`.
- **Vitrines** :
  1. *L'édit de 303* : Lactance, Eusèbe (HE VIII, 2, 1), procès-verbal de Cirta (19 mai 303), *traditores* → « traître », Constantin et les 50 exemplaires (Vie de Constantin IV, 36).
  2. *Le bûcher* : canvas 2D, page de Jean 1:1-5 du Nouveau Testament de Tyndale (1526) rendue en bitmap, combustion par seuil sur un champ « bruit fbm + distance au foyer » (bords roussis, carbonisés, incandescents) et braises en mode additif ; dessous, la Grande Bible de 1539 (HTML, unités `cqw`). Durée 5,6 s, basée sur l'horloge ; `prefers-reduced-motion` → combustion instantanée. Traduction française du passage.
  3. *Six interdictions, six échecs* : cartes recto/verso au clic (Toulouse 1229, Oxford 1408, Wycliffe 1428, Reina 1562, Madagascar 1835, Albanie 1967).
  4. *Rideau de fer* : URSS, Albanie, Chine, Frère André, projet Perle (18 juin 1981) ; carte canvas de 7 routes clandestines avec tracé animé.
  5. *Vrai ou légende ?* : 6 affirmations (Voltaire et la colonne de Dioclétien = légendes) avec score.
  6. *Les chiffres* : Alliance biblique universelle 2025 (148,3 M d'Écritures, 22,4 M de Bibles, 32,2 milliards de chapitres, 1,1 milliard de Bibles depuis 1946), 807 langues ; Ésaïe 40:8 (hébreu) et Matthieu 24:35 (grec) traduits.
- **Tests** : Playwright 1440 × 900 et 390 × 844, aucune erreur JS, aucun débordement horizontal.

## Ajouts de l'étape E11 — Salle 09 « Les Preuves archéologiques »

- `tools/salle_archeologie.py` (+ gabarit `tools/templates/salles/archeologie.html`) : 8 vitrines — atlas (carte canvas du Proche-Orient + 8 découvertes, 1846-1994), stèle de Mésha (lampe rasante, lecteur mot à mot, débat ligne 31), Tel Dan (jeu de fouille à la brosse, lignes 7-9), cylindre de Cyrus (comparaison avec Esdras 1:2 et Ésaïe 45:1), papyrus d'Éléphantine (extraits TAD A4.7, réseau de personnages de Néhémie), Pilate et Caïphe (lecteurs latin et araméen), Ninive (Gilgamesh XI / Genèse 6-9 filtrable), registre de 17 personnages filtrable.
- Lecteur d'inscription générique (`.insc`) : mots cliquables (translittération, sens français, note), bascule écriture d'origine (Unicode phénicien, police Noto Sans Phoenician) / lettres hébraïques carrées.
- `assets/css/salle09.css`, `assets/js/salle09.js`, `assets/js/salle09-geo.js` (Natural Earth 110 m + fleuves simplifiés).
- 10 JPG `assets/img/salles/09/` (1920×1080 + 960×540) ; l'inscription de `pilate.jpg` a été regravée numériquement avec le texte réel de la pierre ; 2 MP3 `salle09-pierres.mp3`, `salle09-noms.mp3`.

## Ajouts de l'étape E10 — Salle 08 « Gutenberg et l'imprimerie »

- `tools/salle_gutenberg.py` (+ gabarit `tools/templates/salles/gutenberg.html`) : 6 vitrines — atelier (onglets ARIA, 4 étapes), jeu « À vous de composer » (casse → composteur inversé → encrage → presse), Bible à 42 lignes (page reconstituée en textura UnifrakturMaguntia, 6 pastilles), vague imprimée (22 éditions 1455-1611, carte canvas animée), retour aux sources (6 fiches Réforme), globe des traductions (orthographique, glisser pour tourner).
- `assets/css/salle08.css`, `assets/js/salle08.js`, `assets/js/salle08-geo.js` (contours Europe + 2 375 points du globe, générés depuis `tools/data_gutenberg_geo.json`, source Natural Earth domaine public).
- Police ajoutée : `assets/fonts/unifraktur-maguntia.woff2` (OFL).
- 10 JPG `assets/img/salles/08/` (1920×1080 + 960×540) ; 2 MP3 `salle08-gutenberg.mp3`, `salle08-diffusion.mp3`.
- Chiffres mondiaux mis à jour (accueil + salle) : ProgressBible, septembre 2026 via Wycliffe — 807 Bibles complètes, 1 844 NT, 1 519 portions, 3 224 langues sans texte, sur 7 394.

## Ajouts de l'étape E09 — Salle 07 « La Septante et les grandes traductions »

- `tools/salle_traductions.py` + `tools/templates/salles/traductions.html` : marqueurs `{{S07_POLY_NAV}}`, `{{S07_POLY}}`, `{{S07_NOM}}`, `{{S07_VULG}}`, `{{S07_NT27}}`, `{{S07_VERSIONS}}`, `{{S07_TR_LXX}}`, `{{S07_TR_VUL}}`.
- Polyglotte : chaque langue est une liste de segments `(texte, index[, séparateur])` ; le séparateur `""` colle deux segments (maqaf hébreu). Les `.pg-s[data-i]` de même index s'illuminent dans les 5 colonnes (survol, focus clavier, toucher). Textes vérifiés sur tanakh.info (TM, LXX Rahlfs, Vulgate clémentine, Peshitta).
- Police `Noto Sans Syriac` (sous-ensemble syriaque, `assets/fonts/noto-sans-syriac.woff2`) ; classe `.syr` / `[lang="syc"]`. Le latin utilise `--f-titre` (Cormorant), jamais EB Garamond (substitution u → v en `lang="la"`).
- Nom divin : `.nd-stage[data-etat]` = `paleo` (𐤉𐤄𐤅𐤄, Noto Sans Phoenician) · `carre` (יהוה) · `kyrios` ; étiqueté « Illustration » + encadré débat.
- Canon de la Peshitta : `.nt[data-mode="peshitta"]` grise les 5 livres ajoutés en 508 / 616 (tous restent badgés canoniques).
- Médias : 7 JPG (`assets/img/salles/07/`, 1920 + 960 px), 2 MP3 (`salle07-septante.mp3` 1:13, `salle07-vulgate.mp3` 1:19). Une image (scriptorium de Jarrow) a été écartée : ses cadres de séchage formaient des croix.
- Correctif global (`components.css`) : `.ap-body { grid-template-columns: minmax(0, 1fr) }` — un titre de narration long ne déborde plus sur mobile.

## Ajouts de l'étape E08 — Salle 06 « Les Textes apocryphes »

| Fichier | Rôle |
|---|---|
| `tools/salle_apocryphes.py` | Données : frise des redécouvertes (1773 → 2006), 3 dossiers (fiche, résumé détaillé, extrait, « pourquoi pas dans la Bible », liens), 8 questions du jeu (JSON dans `data-quiz`), Jude 14-15 (grec NA27 + français) face à 1 Hénoch 1:9, Précepte 1 d'Hermas (grec intégral + français), Canon de Muratori l. 73-80 (latin + français), comparateur, étapes du canon, transcriptions. Remplace les `{{S06_*}}`. |
| `tools/templates/salles/apocryphes.html` | 6 vitrines : avertissement + repères, Nag Hammadi, dossiers à onglets, jeu, Hénoch et Hermas, critères / comparateur / formation du canon. Pont vers la salle 07. |
| `assets/js/salle06.js` | Onglets ARIA (flèches, Début, Fin), jeu (score, progression, verdict, explication, rejouer), mode du comparateur (`data-crit`), sommaire actif. |
| `assets/css/salle06.css` | `.apo-alerte`, `.def`, `.dv`, `.dos*`, `.quiz` / `.qz-*`, `.hh`, `.jh*`, `.tx-*`, `.crit`, `.cp*` (barres pilotées par `--a`, `--z`, `--m`), `.cn`. |

Règle d'étiquetage : chaque texte non biblique porte un badge rouge (« Apocryphe » ou « Non canonique » pour Hermas) ; chaque citation biblique de comparaison porte le badge « Canonique ». Le latin est composé en Cormorant : EB Garamond applique une variante locale latine (u → v) avec `lang="la"`.

Médias : `assets/img/salles/06/` (9 images × 2 tailles : hero-nag, jarre, codices, oxy654, berlin, tchacos, henoch, hermas, athanase), `assets/audio/salle06-nag.mp3` (1 min 29 s) et `salle06-canon.mp3` (1 min 30 s), 192 kb/s.

## Ajouts de l'étape E07 — Salle 05 « Découverte 2026 : le Codex H »

| Fichier | Rôle |
|---|---|
| `tools/salle_codex_h.py` | Carte de l'Europe (projection lon −11..46) avec les 6 lieux de conservation et leurs feuillets (« selon les inventaires publiés ») ; rayons pointillés depuis le mont Athos ; laboratoire de Glasgow ; transcription de la narration. Remplace `{{S05_CARTE}}`, `{{S05_LIEUX}}`, `{{S05_TR}}`. |
| `tools/templates/salles/codex-h.html` | Annonce et fiche, curseur avant/après, technique en 5 étapes, carte des fragments, encadré de clarification (les 42 pages sont des lettres de Paul déjà connues), apports, audio, pont vers la salle 06. |
| `assets/js/salle05.js` | Curseur avant/après (souris, toucher, clavier), choix de la bande de lumière (`aria-checked`), bouton « remettre le texte à l'endroit » (affiche `.aa-lecture` : 1 Co 13:4 en onciales et en français), clic sur la carte (`.ch-panel`, `.ch-ray.is-on`). |
| `assets/css/salle05.css` | `.aa*` : l'image de gauche est filtrée selon `[data-bande]` (visible / UV / IR), l'image de droite est découpée par `clip-path` sur `--pos` ; `.is-flip` retourne l'empreinte (scaleX(−1)). `.etapes-h`, `.ch-*`, `.clarif`, `.apports`, `.q-pont`. |

Le curseur avant/après est une **simulation pédagogique** signalée comme telle : ce n'est pas une page réelle du Codex H. Les liens « Voir l'édition numérique » renvoient vers codexh.arts.gla.ac.uk et le communiqué de l'Université de Glasgow (24 avril 2026).

Médias : `assets/img/salles/03/` (8 images), `assets/img/salles/05/` (hero-labo, reliure-athos, codexh-avant, codexh-apres), `assets/audio/salle03-*.mp3` et `salle05-codexh.mp3` (1 min 19 s, 192 kb/s).

## Restauration du 13 octobre 2026

Une partie des fichiers des étapes E05 et E07 manquait après une restauration du workspace. Ils ont été reconstruits :

- **Gabarits** `qumran.html` et `codex-h.html` : extraits des pages générées, avec les marqueurs `{{…}}` remis en place ; `tools/data/rouleau_colonnes.json` est régénéré par `tools/textures.py`.
- **CSS et JS** réécrits : `salle03.css`, `salle05.css`, `salle03.js` (rouleau 3D), `salle05.js` et `parchemin-gl.js`. Ce dernier crée lui-même son canevas `.hero-parchemin-gl` dans le hall d'entrée, avec une texture procédurale et sans image à charger.
- **Images régénérées en JPG** :
  - 8 photos des salles 03 et 05 ;
  - la texture `verbum-sources/img/parchemin-vierge.jpg` ;
  - l'emblème source `verbum-sources/img/icone-verbum.jpg`, d'où sont tirés `favicon-32.jpg`, `apple-touch-icon.jpg` et `assets/img/icon-512.jpg`.
- **5 narrations** réassemblées (192 kb/s, légère réverbération). Les fichiers sources intermédiaires ont ensuite été supprimés : `verbum-sources/` ne garde que la texture de parchemin, l'emblème source et deux polices.
- **Composants partagés** : `.compteurs`, `.cpt*`, `.q-heb` et `.q-pont` sont désormais dans `salle.css`.

**Règle de production** : toute nouvelle image est livrée en **JPG** haute qualité (aucun nouveau PNG ni SVG), au maximum 10 images et 10 audios par réponse.

## Ajouts de l'étape E14 — Assemblage final

### Générateur
- `tools/build.py` : paramètres `--url` et `--base`, fonction `head()` commune (adresse canonique, Open Graph, Twitter, JSON-LD, `noindex` pour la 404 et la recherche, balise `<base>` pour la 404), bouton de recherche et lien Audioguide dans l'en-tête, rubrique « Autour de la visite » dans le plan du musée, liens dans le pied de page, cartes « Prolonger la visite » sur l'accueil (`visiter()`, marqueur `{{VISITER}}`).
- `tools/pages.py` construit les pages transversales et les fichiers techniques :
  `audioguide.html`, `recherche.html`, `a-propos.html`, `sources.html`, `404.html`, `sitemap.xml`, `robots.txt`, `site.webmanifest`, ainsi que l'index de recherche `assets/js/recherche-index.js`.
- `tools/pages_data.py` : contenus éditoriaux de ces pages (principes, méthode, points de vigilance, liens vers les originaux, bibliographie `BIBLIO`, chiffres datés, crédits).
- `tools/data/audio_durees.json` : durée des 28 MP3, utilisée pour l'audioguide et les crédits.
- `tools/package.py` : archive ZIP du projet, avec l'option `--site-seul`.

### Index de recherche
`window.VERBUM_INDEX` est une liste d'entrées `{u, p, s, k, t}` : adresse avec ancre, nom de la page, titre de la vitrine, surtitre, texte.
Chaque vitrine (`<section id>`) de l'accueil et des salles fournit une entrée, et chaque jalon de la grande frise en fournit une autre (`salles/11-frise.html#jalon-N`, qui ouvre directement la fiche).
Le fichier, d'environ 290 Ko, n'est chargé qu'à la première ouverture de la recherche.

### JavaScript
- `assets/js/recherche.js` : fenêtre de recherche (touche `/`, `Ctrl/Cmd + K` ou bouton `[data-search-open]`) et mode page (`recherche.html?q=`).
  La recherche ignore les accents ; le score tient compte du titre, du surtitre, du nom de la page, des occurrences dans le texte et de l'expression exacte. Les résultats se parcourent avec ↑ ↓ et s'ouvrent avec Entrée.
- `assets/js/audioguide.js` : lecteur continu de 27 chapitres. Il gère l'enchaînement automatique, la vitesse (1×, 1,25×, 1,5×, 0,85×), les sauts de ±15 s, l'API MediaSession, les chapitres écoutés et la reprise via `localStorage` (clé `verbum-audioguide`), ainsi que la mise en valeur du paragraphe de transcription en cours.
- `assets/js/pages.js` : filtre de la bibliographie (`#bi-q`) et mise en valeur du sommaire des pages.
- `assets/js/salle11.js` : ouverture d'une fiche de la frise depuis l'adresse (`#jalon-N`).

### CSS
- `assets/css/pages.css` : en-tête de page (`.page-hero`), audioguide (`.ag-*`), recherche (`.sr-*`), À propos (`.ap-*`, `.pr-*`), Sources (`.so-*`, `.bi-*`) et 404 (`.nf`).
- `components.css` (bloc E14) : bouton et fenêtre de recherche (`.search-btn`, `.srch`), liens du pied de page, rubriques du plan. Le bouton d'effacement natif des champs de recherche est masqué, car il a la forme d'une croix.
- `base.css` : `overflow-x: clip` et apparitions latérales converties en apparitions verticales sous 900 px, pour qu'aucun défilement horizontal ne soit possible sur mobile.

### Images et icônes
Tous les visuels sont en JPG, y compris le logo (`assets/img/logo-verbum.jpg`), les favicons (`favicon-32.jpg`, `favicon-64.jpg`), `apple-touch-icon.jpg` et l'icône du manifeste (`assets/img/icon-512.jpg`). Le projet ne contient plus aucun fichier SVG ni PNG.

### Déploiement
Le guide se trouve dans `docs/DEPLOIEMENT.md`. Configurations fournies : `netlify.toml`, `_headers`, `vercel.json`, `.htaccess` et `.github/workflows/pages.yml`.

### Codex H : images « avant / après » (après E14)
`tools/codexh_photo.py` calcule les deux images du curseur à partir d'une même photographie de feuillet (`verbum-sources/img/codexh-feuillet-base.jpg`), en 1920 × 1080 avec des variantes en 960 × 540. Comme elles partent de la même photo, les deux images se superposent pixel pour pixel. L'empreinte en miroir reproduit 1 Corinthiens 13:7-10 en onciales et en lignes de sens ; ce passage a été choisi parce qu'il ne contient pas la lettre khi, en forme de X. Le cadre `.aa-stage` passe au format 16 / 9.

### Icônes (JPG uniquement)
`tools/icones.py` produit les icônes à partir de l'emblème `verbum-sources/img/icone-verbum.jpg` (1254 × 1254). Chaque fichier est enregistré en JPG de qualité 95, sans sous-échantillonnage des couleurs :
- `favicon-32.jpg` : icône de l'onglet, cadrée serré sur le V et les rouleaux pour rester lisible à 32 px ;
- `apple-touch-icon.jpg` : icône de l'écran d'accueil iPhone et iPad, en 180 × 180 et plein cadre (iOS arrondit lui-même les coins) ;
- `assets/img/icon-512.jpg` : grand format utilisé par le manifeste et les données structurées, avec l'emblème complet et une marge de sécurité.

L'emblème est posé sur un carré du même bleu nuit, avec un bord fondu, pour qu'aucune couture ne soit visible. Le projet ne contient aucun PNG.
