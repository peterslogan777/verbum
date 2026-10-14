# Mettre VERBUM en ligne

VERBUM est un **site entièrement statique** : du HTML, du CSS, du JavaScript, des images JPG et des fichiers MP3.
Il ne demande ni base de données, ni serveur d'application, ni compilation. N'importe quel hébergement web convient.

> **Avant toute mise en ligne**, régénérez les pages avec l'adresse définitive du site.
> Les balises Open Graph, l'adresse canonique, le `sitemap.xml` et le `robots.txt` en dépendent.
>
> ```bash
> python3 tools/build.py --url https://www.mon-domaine.fr
> # site placé dans un sous-dossier (ex. https://exemple.org/verbum/) :
> python3 tools/build.py --url https://exemple.org/verbum --base /verbum/
> ```
>
> Seul Python 3.9 ou plus récent est nécessaire, sans aucune bibliothèque à installer.

Fichiers à publier : `index.html`, `404.html`, `a-propos.html`, `audioguide.html`, `recherche.html`, `sources.html`,
`robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon-32.jpg`, `favicon-64.jpg`, `apple-touch-icon.jpg`, et les dossiers `assets/` et `salles/`.
Les dossiers `tools/` et `docs/` ne servent qu'à la fabrication et peuvent rester en local.

---

## 1. Essai sur votre ordinateur

```bash
cd verbum
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

Passez par un petit serveur local plutôt que par un double-clic sur `index.html` : certains navigateurs bloquent
la lecture des MP3 et le chargement de l'index de recherche en `file://`.

## 2. Netlify (le plus simple, gratuit)

1. Créez un compte sur netlify.com.
2. Faites glisser le dossier `verbum/` dans la zone « Deploy manually ».
3. C'est en ligne. Le fichier `netlify.toml` fourni configure déjà la page 404 et la mise en cache.

Pour un nom de domaine personnel : *Domain settings → Add custom domain*, puis relancez
`python3 tools/build.py --url https://votre-domaine` et redéposez le dossier.

## 3. GitHub Pages (gratuit, mise à jour automatique)

1. Créez un dépôt GitHub et poussez-y le contenu du dossier `verbum/`.
2. Dans *Settings → Pages*, choisissez **Source : GitHub Actions**.
3. Le workflow `.github/workflows/pages.yml` régénère les pages avec la bonne adresse
   (`https://utilisateur.github.io/depot/`) puis publie le site à chaque `git push` sur `main`.

GitHub Pages sert automatiquement `404.html` pour les adresses inconnues.

## 4. Vercel

```bash
npm i -g vercel
cd verbum && vercel --prod
```

Aucun réglage de « build » n'est nécessaire : choisissez *Other* et laissez la commande vide.
Le fichier `vercel.json` ajoute les en-têtes de cache. Vercel sert `404.html` automatiquement.

## 5. Cloudflare Pages

*Workers & Pages → Create → Pages → Upload assets*, puis déposez le dossier.
Le fichier `_headers` est pris en compte, et `404.html` est servi automatiquement.

## 6. Hébergement classique (OVH, o2switch, Ionos, etc.)

1. Envoyez les fichiers par FTP/SFTP (FileZilla) dans le dossier `www/` ou `public_html/`.
2. Le fichier `.htaccess` fourni active la page 404, la compression et la mise en cache.
   Si le site est dans un sous-dossier, adaptez la ligne `ErrorDocument 404 /sous-dossier/404.html`.

## 7. Nginx

```nginx
server {
  server_name verbum.exemple.fr;
  root /var/www/verbum;
  index index.html;
  error_page 404 /404.html;
  location /assets/ { expires 30d; add_header Cache-Control "public"; }
  types { application/manifest+json webmanifest; }
  gzip on; gzip_types text/css application/javascript application/json;
}
```

---

## Vérifications après la mise en ligne

- La page d'accueil s'ouvre et l'animation de parchemin démarre.
- La touche `/` ouvre la recherche, et une recherche sur « Qumrân » renvoie des résultats.
- L'audioguide lit les chapitres à la suite.
- Une adresse inexistante (`/essai-404`) affiche la vitrine vide « Cette page s'est perdue ».
- L'aperçu de partage s'affiche correctement, à vérifier avec l'outil de débogage de Facebook ou de LinkedIn
  (la balise `og:image` doit pointer vers votre domaine).
- `https://votre-domaine/sitemap.xml` liste bien 17 adresses (accueil, 12 salles, 4 pages).

## Poids du site

Environ 130 Mo, dont l'essentiel en images (1920 × 1080 et 960 × 540) et en narrations MP3 (192 kbit/s).
Les images sont chargées à la demande (`loading="lazy"`) et pour les MP3, seules les métadonnées sont chargées avant la lecture.
