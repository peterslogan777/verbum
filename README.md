# VERBUM — Le Musée Virtuel de la Bible
> « La Parole qui traverse les millénaires »

Site statique, immersif et entièrement en français, consacré à l'histoire de la transmission de la Bible.

## État du chantier

| Étape | Contenu | Statut |
|---|---|---|
| **E01** | Architecture, charte graphique, navigation, logo, hall d'entrée animé | ✅ Terminé |
| **E02** | Page d'accueil épique : diaporama, parchemin, audioguide, frise, carte du monde | ✅ Terminé |
| **E03** | Salle 01 — Les Origines : Ketef Hinnom, bénédiction interactive, Moïse et la Torah, témoins | ✅ Terminé |
| **E04** | Salle 02 — Copistes, Massorètes, jeu du copiste, Codex d'Alep et de Leningrad | ✅ Terminé |
| **E05** | Salle 03 — Les manuscrits de la mer Morte (salle phare) : rouleau 3D WebGL, carte des grottes, comparateur, frise, loupe | ✅ Terminé |
| **E06** | Salle 04 — Les grands Codex grecs : papyrus P52 interactif (recto/verso, texte restitué), P66, P75, débat P64, scriptio continua, cartes 3D des codex, Bible éthiopienne, odyssée du Sinaiticus, comparaison avec les textes antiques | ✅ Terminé |
| **E07** | Salle 05 — Découverte 2026 : le Codex H (curseur avant/après, technique, carte des fragments) | ✅ Terminé (réalisé avec E05) |
| **E08** | Salle 06 — Les Textes apocryphes : avertissement et repères canonique / apocryphe, jarre de Nag Hammadi, frise des redécouvertes, dossiers Thomas · Marie · Judas (onglets), jeu « Canonique ou non ? », Hénoch (Jude 14-15) et Hermas (Précepte 1, Canon de Muratori), comparateur, formation du canon | ✅ Terminé |
| **E09** | Salle 07 — La Septante et les grandes traductions : Alexandrie (légende d'Aristée / histoire), P. Rylands 458, deutérocanoniques, le nom divin dans la Septante (démonstration 3 états + débat), Jérôme et la Vulgate (frise 382 → 1979, Codex Amiatinus), Peshitta (Add. 14425, canon de 22 livres), polyglotte interactive alignée hébreu · grec · latin · syriaque · français (Gn 1:1, 1:3, 2:8), versions anciennes et Codex Argenteus | ✅ Terminé |
| E10 | Salle 08 — Gutenberg et l'imprimerie | ✅ |
| E11 | Salle 09 — Les preuves archéologiques | ✅ |
| E12 | Salle 10 — La Bible face aux destructions | ✅ |
| E13 | Salle 11 — La Grande Frise chronologique | ✅ |
| **E14** | Assemblage final : recherche plein texte, audioguide continu (27 chapitres), pages À propos et Sources, page 404, Open Graph et données structurées, sitemap, robots, manifeste, fichiers de déploiement, archive ZIP | ✅ Terminé |

**Avancement : 14 / 14, soit 100 %.**

## Contenu du musée

- **Hall d'entrée** (`index.html`) et **12 salles** (`salles/01-origines.html` à `salles/12-bible-francaise.html`).
- **Audioguide** (`audioguide.html`) : 29 narrations, soit environ 44 minutes. Lecture enchaînée, reprise là où vous vous étiez arrêté, vitesse réglable, raccourcis `Espace`, `N` et `P`.
- **Recherche** : touche `/` ou `Ctrl + K` sur toutes les pages, ou bien `recherche.html?q=…`. Elle porte sur 132 vitrines et jalons, sans tenir compte des accents.
- **À propos** (`a-propos.html`) : mission, principes, méthode, points de vigilance et crédits techniques.
- **Sources** (`sources.html`) : liens vers les originaux numérisés, bibliographie filtrable (39 références), chiffres datés et crédits.
- **Page 404** : une vitrine vide, avec un champ de recherche.

## Lancer le site en local

```bash
cd verbum
python3 -m http.server 8080      # puis ouvrir http://localhost:8080
```

## Régénérer les pages

Les fichiers HTML sont produits par un petit générateur en Python, sans aucune dépendance.
Ne les modifiez pas à la main : modifiez les modules de `tools/`, puis relancez la commande.

```bash
python3 tools/build.py                                          # adresse par défaut (https://verbum.example)
python3 tools/build.py --url https://www.mon-domaine.fr         # adresse définitive (Open Graph, sitemap, canonique)
python3 tools/build.py --url https://ex.org/verbum --base /verbum/   # site placé dans un sous-dossier
```

## Mettre en ligne

Le guide complet est dans `docs/DEPLOIEMENT.md` : Netlify, GitHub Pages (workflow fourni), Vercel, Cloudflare Pages, Apache et Nginx.
Les fichiers de configuration sont déjà prêts : `netlify.toml`, `_headers`, `vercel.json`, `.htaccess` et `.github/workflows/pages.yml`.

## Fabriquer l'archive ZIP

```bash
python3 tools/package.py              # projet complet → ../dist/verbum-musee-virtuel-de-la-bible.zip
python3 tools/package.py --site-seul  # uniquement les fichiers à publier
```

## Choix techniques

- **HTML5, CSS3 et JavaScript natif, sans aucune dépendance** : le site se charge vite, fonctionne hors ligne et se déploie tel quel sur GitHub Pages, Netlify ou Vercel.
- **Polices auto-hébergées** (licence SIL OFL) : Cinzel Decorative, Cinzel, Cormorant Garamond, EB Garamond (grec polytonique), Inter, Frank Ruhl Libre et Noto Sans Hebrew. Aucun appel à Google Fonts.
- **Animations** : IntersectionObserver pour les révélations au défilement, Canvas 2D pour les particules dorées, transformations CSS 3D pour la parallaxe et les cartes. WebGL natif pour le parchemin du hall et le rouleau 3D de Qumrân. Aucune bibliothèque externe : ni GSAP, ni Three.js, ni Leaflet, ni D3.
- **Générateur minimal** (`tools/build.py`) : une seule source de vérité pour les salles, l'en-tête, le plan du musée et le pied de page.
- **Référencement** : balises Open Graph et Twitter, adresse canonique, données structurées JSON-LD (`WebSite` avec recherche intégrée, `Museum`, et `WebPage` avec fil d'Ariane pour chaque salle), `sitemap.xml`, `robots.txt` et manifeste web.
- **Accessibilité** : lien d'évitement, navigation au clavier, touche Échap pour fermer le plan, respect de `prefers-reduced-motion`, curseur-plume désactivé sur écran tactile.

## Règles éditoriales (appliquées partout)

1. Aucune croix : ni dans les visuels, ni dans les icônes, ni dans les ornements (pas même un « + »). Les ornements sont des losanges.
2. Tout texte en hébreu, en araméen ou en grec est suivi de sa traduction française.
3. Le tétragramme יהוה est rendu par **Jéhovah**.
4. Badges **CANONIQUE** (vert doré), **APOCRYPHE** (rouge antique) et **DATATION DÉBATTUE**.
5. Images exclusivement en JPG photoréaliste haute qualité, 1920 × 1080 avec une variante 960 × 540 (10 au maximum par étape). Aucun fichier SVG ni PNG : le logo et les icônes sont eux aussi en JPG. Audios en MP3 à 192 kbit/s (10 au maximum par étape).
6. Les illustrations générées sont signalées comme « reconstitution ».

Voir `docs/ARCHITECTURE.md` pour l'arborescence complète.
