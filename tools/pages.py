"""
VERBUM — Pages transversales (étape E14).

Construit, après les salles :
  - audioguide.html   : les narrations du musée à la suite (lecteur continu)
  - recherche.html    : la recherche plein texte (+ index assets/js/recherche-index.js)
  - a-propos.html     : mission, principes, méthode, crédits
  - sources.html      : originaux en ligne, bibliographie, statistiques, crédits
  - 404.html          : page introuvable
  - sitemap.xml, robots.txt, site.webmanifest

Appel : pages.build_all(build_module) depuis tools/build.py.
"""
from __future__ import annotations

import html
import json
import re
from collections import OrderedDict
from pathlib import Path

import pages_data as D

B = None          # module build (injecté)
e = html.escape


# --------------------------------------------------------------------------
# Outils
# --------------------------------------------------------------------------
def fmt_duree(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style|svg|canvas|template)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def img_tag(path, alt="", sizes="100vw", cls="", lazy=True, w=1920, h=1080):
    root = "{{ROOT}}"
    p = f"{root}{path}"
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{p}-960.jpg" srcset="{p}-960.jpg 960w, {p}.jpg 1920w" sizes="{sizes}" '
            f'alt="{e(alt)}" width="{w}" height="{h}" decoding="async"{load}>')


def player(pid, src, titre, duree, paras, label="Écouter la narration"):
    """Lecteur audio commun (même balisage que les salles, géré par audio.js)."""
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f"""
    <div class="s-audio" data-audio-zone data-reveal>
      <div class="audio-player" id="audio-{pid}" data-src="{{{{ROOT}}}}{src}">
        <button class="ap-play" type="button" aria-label="{e(label)} : {e(titre)}">
          <svg class="i-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>
          <svg class="i-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>
        </button>
        <div class="ap-body">
          <div class="ap-meta"><b>{e(label)} · {e(titre)}</b><span class="ap-time">0:00 / {fmt_duree(duree)}</span></div>
          <canvas class="ap-viz" aria-hidden="true"></canvas>
          <input class="ap-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="Position de lecture">
        </div>
      </div>
      <details class="transcript">
        <summary>Lire la transcription</summary>
        <div class="transcript-body">{body}</div>
      </details>
    </div>"""


def hero(kicker, titre, lead, img, alt, extra=""):
    return f"""
<section class="salle-hero has-img page-hero" style="--salle-glow:rgba(201,168,76,.28)">
  <div class="bg" aria-hidden="true">{img_tag(img, "", lazy=False).replace('decoding="async"', 'decoding="async" data-parallax="0.15"')}</div>
  <div class="container">
    <span class="kicker" data-reveal>{kicker}</span>
    <h1 data-reveal>{titre}</h1>
    <p class="lead" data-reveal style="margin-top:1rem">{lead}</p>
    {extra}
  </div>
</section>"""


def write_page(path, slug, title, desc, body, css=(), js=(), image=None, image_alt="", jsonld=None, noindex=False):
    root = "" if path.count("/") == 0 else "../" * path.count("/")
    base = None
    if path == "404.html":           # servie à n'importe quelle adresse : chemins absolus
        base, root = B.SITE["base"], ""
    full_title = f"{title} · {B.SITE['titre']}"
    page = (B.head(full_title, desc, root, ["salle", "pages", *css], path=path, image=image, image_alt=image_alt,
                   jsonld=jsonld, noindex=noindex, base=base)
            + f'\n<body class="salle page page-{slug} is-ready">\n' + B.header(root, slug)
            + f'\n<main id="contenu">{body}\n</main>' + B.footer(root) + B.scripts(root, ["audio", *js]))
    body_nb = re.sub(r"«\s", "«\u00a0", re.sub(r"\s»", "\u00a0»", body))
    page = page.replace(body, body_nb)
    page = page.replace("{{ROOT}}", root).replace("{{ARROW}}", B.ARROW).replace("{{PLAY}}", B.PLAY)
    (B.ROOT / path).write_text(B.typo(page), encoding="utf-8")


# --------------------------------------------------------------------------
# 1. Audioguide
# --------------------------------------------------------------------------
RX_PLAYER = re.compile(r'<div class="audio-player" id="([^"]+)" data-src="([^"]+)"(?: data-title="([^"]*)")?>')


def pistes():
    """Toutes les narrations du parcours, dans l'ordre de visite, avec leur transcription."""
    out = [dict(src="assets/audio/guide-accueil.mp3", t="Bienvenue dans l'audioguide", g="Accueil", n="00",
                h="audioguide.html", img="assets/img/pages/guide", tr=D.GUIDE_ACCUEIL)]
    sources = [("index.html", "00", "Hall d'entrée", "assets/img/accueil/hero-jarres-grotte")]
    sources += [(s["href"], s["num"], f"Salle {s['num']} · {s['titre']}", s.get("hero_img")) for s in B.SALLES]
    for href, num, groupe, cover in sources:
        page = (B.ROOT / href).read_text(encoding="utf-8")
        for m in RX_PLAYER.finditer(page):
            pid, src, dtitle = m.group(1), m.group(2), m.group(3)
            src = src.replace("../", "")
            after = page[m.end():m.end() + 6000]
            mt = re.search(r"<b>(.*?)</b>", after, re.S)
            titre = dtitle or strip_tags(mt.group(1) if mt else pid)
            titre = re.sub(r"^Écouter (la narration|le commentaire)\s*·\s*", "", titre)
            mtr = re.search(r'<div class="transcript-body">(.*?)</div>\s*</details>', page[m.end():], re.S)
            paras = re.findall(r"<p[^>]*>(.*?)</p>", mtr.group(1), re.S) if mtr else []
            out.append(dict(src=src, t=titre, g=groupe, n=num, h=f"{href}#{pid}", img=cover,
                            tr=[strip_tags(p) for p in paras]))
    out.append(dict(src="assets/audio/guide-epilogue.mp3", t="Épilogue : la Parole qui traverse les millénaires",
                    g="Sortie du musée", n=f"{len(B.SALLES) + 1:02d}", h="audioguide.html", img="assets/img/salles/11/fin", tr=D.GUIDE_EPILOGUE))
    for p in out:
        p["d"] = B.DUREES.get(Path(p["src"]).name, 0)
    return out


def build_audioguide():
    P = pistes()
    total = sum(p["d"] for p in P)
    groupes = OrderedDict()
    for i, p in enumerate(P):
        groupes.setdefault((p["n"], p["g"]), []).append((i, p))
    chap = []
    for (num, g), items in groupes.items():
        lis = "".join(
            f'<li><button class="ag-it" type="button" data-i="{i}"><span class="ag-n">{i + 1:02d}</span>'
            f'<span class="ag-tt">{e(p["t"])}</span><span class="ag-d">{fmt_duree(p["d"])}</span>'
            f'<span class="ag-ok" aria-hidden="true"></span></button></li>' for i, p in items)
        gd = sum(p["d"] for _, p in items)
        chap.append(f'<li class="ag-grp" data-reveal><div class="ag-gh"><span class="ag-gn">{num}</span>'
                    f'<span class="ag-gt">{e(g)}</span><span class="ag-gd">{len(items)} · {fmt_duree(gd)}</span></div>'
                    f'<ol class="ag-list">{lis}</ol></li>')
    data = [dict(src=p["src"], t=p["t"], g=p["g"], h=p["h"], img=p["img"], d=p["d"], tr=p["tr"]) for p in P]
    body = hero("Autour de la visite · Audioguide", "L'audioguide <em>du musée</em>",
                f"{len(P)} narrations, {round(total / 60)} minutes : toute l'histoire de la transmission de la Bible, "
                "à écouter à la suite, de l'accueil jusqu'à la sortie du musée.",
                "assets/img/pages/guide", "Un casque ancien devant une vitrine éclairée",
                extra=f'<div class="badges" data-reveal><span class="badge badge-canon">Narration en français</span>'
                      f'<span class="badge badge-debat">{len(P)} chapitres</span></div>')
    body += f"""
<section class="section ag" id="lecteur" aria-labelledby="ag-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Lecture continue</span>
      <h2 id="ag-title">Écoutez le musée <em>de bout en bout</em></h2>
      <p class="lead">Le lecteur enchaîne les chapitres et garde votre place, même si vous quittez la page. Touches : <kbd>Espace</kbd> lecture ou pause, <kbd>N</kbd> chapitre suivant, <kbd>P</kbd> chapitre précédent.</p>
    </div>
    <div class="ag-grid">
      <div class="ag-player" data-reveal>
        <figure class="ag-cover"><img class="ag-img" src="{{{{ROOT}}}}assets/img/pages/guide-960.jpg" alt="" width="960" height="540"><figcaption class="ag-ill">Illustration · reconstitution numérique</figcaption></figure>
        <div class="ag-info">
          <p class="ag-grp-now">Accueil</p>
          <p class="ag-t-now">Bienvenue dans l'audioguide</p>
          <p class="ag-pos"><span class="ag-cur">1</span> / {len(P)}</p>
        </div>
        <div class="ag-bar"><input class="ag-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="Position dans le chapitre"><div class="ag-times"><span class="ag-tc">0:00</span><span class="ag-td">{fmt_duree(P[0]["d"])}</span></div></div>
        <div class="ag-ctrl">
          <button class="ag-prev" type="button" aria-label="Chapitre précédent"><svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M6 5h2v14H6zM20 5.5v13a1 1 0 0 1-1.5.86L9 12.86a1 1 0 0 1 0-1.72l9.5-6.5A1 1 0 0 1 20 5.5z"/></svg></button>
          <button class="ag-back" type="button" aria-label="Reculer de 15 secondes">−15 s</button>
          <button class="ag-play" type="button" aria-label="Lancer l'audioguide">
            <svg class="i-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>
            <svg class="i-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>
          </button>
          <button class="ag-fwd" type="button" aria-label="Avancer de 15 secondes">+15 s</button>
          <button class="ag-next" type="button" aria-label="Chapitre suivant"><svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M16 5h2v14h-2zM4 5.5v13a1 1 0 0 0 1.5.86L15 12.86a1 1 0 0 0 0-1.72L5.5 4.64A1 1 0 0 0 4 5.5z"/></svg></button>
        </div>
        <div class="ag-opts">
          <button class="ag-rate" type="button" aria-label="Vitesse de lecture">Vitesse 1×</button>
          <label class="ag-auto"><input type="checkbox" checked> Enchaîner les chapitres</label>
          <a class="ag-go" href="{{{{ROOT}}}}index.html">Voir dans la salle {{{{ARROW}}}}</a>
        </div>
        <div class="ag-total"><span class="ag-total-bar"><i></i></span><span class="ag-total-txt">0 chapitre écouté sur {len(P)}</span><button class="ag-reset" type="button">Recommencer</button></div>
      </div>
      <div class="ag-tr" data-reveal="right">
        <p class="ag-tr-h">Transcription du chapitre</p>
        <div class="ag-tr-body" tabindex="0" aria-live="off"></div>
      </div>
    </div>
  </div>
</section>

<section class="section ag-chap" id="chapitres" aria-labelledby="chap-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Sommaire</span>
      <h2 id="chap-title">{len(P)} chapitres, <em>{len(groupes)} étapes</em></h2>
      <p class="lead">Durée totale : environ {round(total / 60)} minutes. Choisissez librement un chapitre : la lecture reprend à partir de celui-ci.</p>
    </div>
    <ol class="ag-groups">{''.join(chap)}</ol>
  </div>
</section>
<script type="application/json" id="ag-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>"""
    write_page("audioguide.html", "audioguide", "Audioguide",
               f"L'audioguide de VERBUM : {len(P)} narrations en français, environ {round(total / 60)} minutes, "
               "pour suivre la transmission de la Bible de Moïse à 2026.",
               body, js=["audioguide"], image="assets/img/pages/guide", image_alt="Un casque ancien devant une vitrine éclairée")
    return P


# --------------------------------------------------------------------------
# 2. Index de recherche + page
# --------------------------------------------------------------------------
RX_SECTION = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S)


def page_index(href, label):
    page = (B.ROOT / href).read_text(encoding="utf-8")
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    entries = []
    for attrs, inner in RX_SECTION.findall(main):
        mid = re.search(r'\bid="([^"]+)"', attrs)
        mh = re.search(r"<h[12][^>]*>(.*?)</h[12]>", inner, re.S)
        mk = re.search(r'class="kicker"[^>]*>(.*?)</span>', inner, re.S)
        titre = strip_tags(mh.group(1)) if mh else label
        kick = strip_tags(mk.group(1)) if mk else ""
        texte = strip_tags(inner)
        for part in (kick, titre):          # le texte commence souvent par la vitrine et le titre : on les retire
            if part and texte.startswith(part):
                texte = texte[len(part):].lstrip(" ·")
        if len(texte) < 40:
            continue
        entries.append(dict(u=href + (f"#{mid.group(1)}" if mid else ""), p=label, s=titre,
                            k=strip_tags(mk.group(1)) if mk else "", t=texte[:9000]))
    return entries, page


def build_index_recherche(extra_pages):
    idx = []
    labels = [("index.html", "Hall d'entrée")] + [(s["href"], f"Salle {s['num']} · {s['titre']}") for s in B.SALLES] + extra_pages
    for href, label in labels:
        entries, page = page_index(href, label)
        idx += entries
        m = re.search(r'<script[^>]*id="fr-data"[^>]*>(.*?)</script>', page, re.S)
        if m:   # jalons de la Grande Frise : une entrée chacun, ouverture directe de la fiche
            for i, d in enumerate(json.loads(m.group(1))):
                idx.append(dict(u=f"{href}#jalon-{i + 1}", p=label, s=f"{d['lab']} · {d['t']}", k=f"Jalon · {d['eraT']}",
                                t=strip_tags(d.get("txt", "") + " " + d.get("imp", ""))))
    js = ("/* VERBUM — index de recherche (généré par tools/pages.py, ne pas modifier) */\n"
          "window.VERBUM_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (B.ROOT / "assets" / "js" / "recherche-index.js").write_text(js, encoding="utf-8")
    return len(idx)


def build_recherche():
    sugg = "".join(f'<a class="tag sr-sugg" href="?q={e(q)}">{e(q)}</a>' for q in D.SUGGESTIONS)
    body = hero("Autour de la visite · Recherche", "Rechercher <em>dans le musée</em>",
                "Un manuscrit, un personnage, un lieu, une date : toutes les salles, leurs transcriptions et les 36 jalons de la frise.",
                "assets/img/pages/recherche", "Une loupe ancienne posée sur un parchemin")
    body += f"""
<section class="section sr-page" id="resultats" aria-labelledby="sr-title">
  <div class="container">
    <h2 id="sr-title" class="visually-hidden">Résultats de recherche</h2>
    <form class="sr-form" role="search" action="recherche.html" method="get" data-reveal>
      <label class="visually-hidden" for="sr-q">Rechercher</label>
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.4 15.4 20.5 20.5"/></svg>
      <input id="sr-q" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="Par exemple : Ketef Hinnom, Tyndale, Septante…">
      <button class="btn btn-or" type="submit">Rechercher</button>
    </form>
    <div class="sr-sugg-row" data-reveal><span>Suggestions :</span>{sugg}</div>
    <p class="sr-count" aria-live="polite"></p>
    <ol class="sr-results sr-results-page"></ol>
  </div>
</section>"""
    write_page("recherche.html", "recherche", "Recherche",
               "Rechercher dans VERBUM : manuscrits, personnages, lieux et dates de l'histoire de la Bible.",
               body, image="assets/img/pages/recherche", image_alt="Une loupe ancienne posée sur un parchemin")


# --------------------------------------------------------------------------
# 3. À propos
# --------------------------------------------------------------------------
def build_apropos(nb_pistes, nb_liens, nb_index):
    nb_img = len(list((B.ROOT / "assets" / "img").rglob("*.jpg"))) // 2
    duree = round(sum(v for k, v in B.DUREES.items() if k != "apropos.mp3") / 60)
    cpt = [(11, "salles"), (36, "jalons sur la frise"), (nb_pistes, "narrations"), (duree, "minutes d'écoute"),
           (nb_liens, "liens vers les originaux")]
    compteurs = "".join(f'<div class="cpt" data-reveal><span class="cpt-n" data-count="{n}">{n}</span><span class="cpt-l">{e(l)}</span></div>' for n, l in cpt)
    principes = "".join(f'<article class="pr-card" data-reveal><span class="pr-k">{k}</span><h3>{t}</h3><p>{d}</p></article>' for k, t, d in D.PRINCIPES)
    vigil = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in D.VIGILANCE)
    salles = "".join(f'<li><a href="{s["href"]}"><span class="ap-num">{s["num"]}</span><span class="ap-tt">{e(s["titre"])}</span>'
                     f'<span class="ap-sous">{e(s["sous"])}</span></a></li>' for s in B.SALLES)
    tech = "".join(f"<li><b>{t}</b> {d}</li>" for t, d in D.TECHNIQUE)
    body = hero("Autour de la visite · À propos", "Un musée <em>sans murs</em>",
                "VERBUM raconte, de façon claire et vérifiable, comment la Bible est parvenue jusqu'à nous : "
                "trois langues, environ quarante rédacteurs, quelque 1 600 ans de rédaction et 3 500 ans de transmission.",
                "assets/img/pages/apropos", "Le grand hall d'un musée la nuit, avec des vitrines de manuscrits")
    body += f"""
<nav class="s-sommaire" aria-label="Sommaire de la page">
  <div class="container">
    <a href="#mission"><span>I</span>La mission</a>
    <a href="#principes"><span>II</span>Nos principes</a>
    <a href="#methode"><span>III</span>La méthode</a>
    <a href="#parcours-salles"><span>IV</span>Les douze salles</a>
    <a href="#technique"><span>V</span>Technique et crédits</a>
  </div>
</nav>

<section class="section" id="mission" aria-labelledby="mission-title">
  <div class="container ap-mission">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine I · La mission</span>
      <h2 id="mission-title">Montrer, pièces à l'appui, <em>comment le texte a traversé le temps</em></h2>
      <p class="lead">Ni murs ni billetterie, mais une ambition : vous donner les moyens de vérifier par vous-même que la Bible nous est parvenue pour l'essentiel intacte, malgré les siècles, les copies, les traductions et les destructions.</p>
    </div>
    {player("apropos", "assets/audio/apropos.mp3", "Qui sommes-nous ?", B.DUREES.get("apropos.mp3", 85), D.APROPOS_TR)}
    <div class="compteurs ap-cpt">{compteurs}</div>
  </div>
</section>

<section class="section" id="principes" aria-labelledby="principes-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine II · Nos principes</span>
      <h2 id="principes-title">Six règles, <em>appliquées dans chaque salle</em></h2>
    </div>
    <div class="pr-grid">{principes}</div>
    <blockquote class="q-heb ap-nom" data-reveal>
      <p class="qh" lang="he" dir="rtl">יהוה</p>
      <p class="qf">Les quatre lettres hébraïques du nom divin, Yod, Hé, Waw, Hé, que VERBUM rend partout par <b>« Jéhovah »</b>, et non par un titre comme « Seigneur ».</p>
      <cite>Le Tétragramme · près de 7 000 occurrences dans la Bible hébraïque</cite>
    </blockquote>
  </div>
</section>

<section class="section" id="methode" aria-labelledby="methode-title">
  <div class="container ap-methode">
    <figure class="ap-fig" data-reveal>{img_tag("assets/img/pages/methode", "Des mains gantées tiennent une loupe au-dessus d'un fragment de papyrus", "(max-width: 900px) 100vw, 46vw")}<figcaption><span class="tag">Illustration</span> Reconstitution numérique.</figcaption></figure>
    <div data-reveal="right">
      <span class="kicker">Vitrine III · La méthode</span>
      <h2 id="methode-title">Des sources publiées, <em>des débats signalés</em></h2>
      <p>Chaque salle s'appuie sur des sources publiées : catalogues de musées, éditions savantes, rapports de fouilles et bibliothèques numériques. Quand un manuscrit est consultable en ligne, un bouton « Voir l'original » y conduit directement. Les chiffres sont arrondis, datés et sourcés : par exemple, les statistiques de traduction de la Bible sont celles de septembre 2026.</p>
      <p>Lorsque les spécialistes ne sont pas d'accord, nous le disons, avec l'étiquette <span class="badge badge-debat">Datation débattue</span> et un encadré qui expose les positions en présence.</p>
      <h3 class="sub-title">Points de vigilance</h3>
      <ul class="ap-vigil">{vigil}</ul>
      <p style="margin-top:1.2rem"><a class="btn btn-ghost" href="sources.html">Consulter les sources {{{{ARROW}}}}</a></p>
    </div>
  </div>
</section>

<section class="section" id="parcours-salles" aria-labelledby="ps-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine IV · Le parcours</span>
      <h2 id="ps-title">Douze salles, <em>un seul fil</em></h2>
      <p class="lead">Chaque salle se visite seule, mais l'ordre suit le fil de la transmission, de l'écriture au Sinaï jusqu'aux laboratoires de 2026.</p>
    </div>
    <ol class="ap-salles" data-reveal>{salles}</ol>
  </div>
</section>

<section class="section" id="technique" aria-labelledby="tech-title">
  <div class="container ap-tech">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine V · Technique et crédits</span>
      <h2 id="tech-title">Un site léger, <em>ouvert à tous</em></h2>
    </div>
    <ul class="ap-tech-list" data-reveal>{tech}</ul>
    <div class="ap-cta" data-reveal>
      <a class="btn btn-or" href="salles/01-origines.html">Commencer la visite {{{{ARROW}}}}</a>
      <a class="btn btn-ghost" href="audioguide.html">Lancer l'audioguide</a>
      <a class="btn btn-ghost" href="recherche.html">Rechercher</a>
    </div>
  </div>
</section>"""
    write_page("a-propos.html", "a-propos", "À propos",
               "VERBUM, Musée Virtuel de la Bible : mission, principes (canonique et apocryphe, traduction française, nom divin Jéhovah), méthode et crédits.",
               body, js=["pages"], image="assets/img/pages/apropos", image_alt="Le grand hall d'un musée la nuit")


# --------------------------------------------------------------------------
# 4. Sources
# --------------------------------------------------------------------------
def liens_originaux():
    """Liens externes des salles, dédoublonnés, groupés par salle."""
    vus, groupes = set(), []
    for s in B.SALLES:
        page = (B.ROOT / s["href"]).read_text(encoding="utf-8")
        main = page.split("<main", 1)[1].split("</main>", 1)[0]
        items = []
        for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', main, re.S):
            url, txt = m.group(1), strip_tags(m.group(2))
            if url in vus:
                continue
            vus.add(url)
            txt = re.sub(r"^(Voir (l'original|la notice|les fragments|les collections|l'édition numérique)|Consulter)\s*·?\s*", "", txt).strip() or txt
            items.append((url, txt[:1].upper() + txt[1:]))
        if items:
            groupes.append((s, items))
    return groupes


def build_sources():
    groupes = liens_originaux()
    nb = sum(len(i) for _, i in groupes)
    cartes = []
    for s, items in groupes:
        lis = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener"><span>{e(t)}</span>'
                      f'<small>{e(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</small></a></li>' for u, t in items)
        cartes.append(f'<article class="so-card" data-reveal><a class="so-salle" href="{s["href"]}"><span>{s["num"]}</span>{e(s["titre"])}</a><ul>{lis}</ul></article>')
    biblio = []
    for theme, refs in D.BIBLIO:
        lis = "".join(f'<li><p class="bi-ref">{r}</p><p class="bi-fr">{d}</p></li>' for r, d in refs)
        biblio.append(f'<details class="bi-grp" data-reveal><summary><span>{e(theme)}</span><small>{len(refs)} références</small></summary><ol>{lis}</ol></details>')
    stats = "".join(f'<li><b>{t}</b><span>{d}</span><a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a></li>' for t, d, u, l in D.STATS)
    nb_img = len([f for f in (B.ROOT / "assets" / "img").rglob("*.jpg") if not f.stem.endswith("-960")])
    credits = "".join(f"<li><b>{t}</b><span>{d.replace('{NB_IMG}', str(nb_img)).replace('{NB_AUDIO}', str(len(B.DUREES)))}</span></li>" for t, d in D.CREDITS)
    nb_ref = sum(len(r) for _, r in D.BIBLIO)
    body = hero("Autour de la visite · Sources", "Sources <em>et bibliographie</em>",
                "Les manuscrits originaux consultables en ligne, les ouvrages de référence et les chiffres utilisés dans le musée : tout ce qu'il faut pour vérifier.",
                "assets/img/pages/sources", "Une salle de lecture de bibliothèque ancienne, la nuit")
    body += f"""
<nav class="s-sommaire" aria-label="Sommaire de la page">
  <div class="container">
    <a href="#originaux"><span>I</span>Les originaux en ligne</a>
    <a href="#bibliographie"><span>II</span>Bibliographie</a>
    <a href="#chiffres"><span>III</span>Chiffres et statistiques</a>
    <a href="#credits"><span>IV</span>Crédits</a>
  </div>
</nav>

<section class="section" id="originaux" aria-labelledby="orig-title">
  <div class="container">
    <div class="so-intro">
      <div class="s-head" data-reveal>
        <span class="kicker">Vitrine I · Voir les originaux</span>
        <h2 id="orig-title">{nb} portes ouvertes <em>sur les manuscrits réels</em></h2>
        <p class="lead">Musées, bibliothèques et universités ont numérisé les pièces présentées dans VERBUM. Ces liens ouvrent les sites officiels, dans un nouvel onglet ; la plupart sont en anglais.</p>
      </div>
      <figure class="ap-fig" data-reveal="right">{img_tag("assets/img/pages/numerique", "Un écran affiche la numérisation d'un codex ancien posé devant lui", "(max-width: 900px) 100vw, 40vw")}<figcaption><span class="tag">Illustration</span> Reconstitution numérique.</figcaption></figure>
    </div>
    <div class="so-grid">{''.join(cartes)}</div>
  </div>
</section>

<section class="section" id="bibliographie" aria-labelledby="bib-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine II · Bibliographie</span>
      <h2 id="bib-title">{nb_ref} ouvrages et articles <em>de référence</em></h2>
      <p class="lead">Les titres sont donnés dans leur langue de publication, chacun suivi d'une présentation en français.</p>
    </div>
    <div class="bi-filter" data-reveal><label for="bi-q" class="visually-hidden">Filtrer la bibliographie</label><input id="bi-q" type="search" placeholder="Filtrer : Qumrân, Septante, Tyndale…" autocomplete="off"><span class="bi-n" aria-live="polite"></span></div>
    <div class="bi-list">{''.join(biblio)}</div>
  </div>
</section>

<section class="section" id="chiffres" aria-labelledby="chif-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine III · Chiffres et statistiques</span>
      <h2 id="chif-title">D'où viennent <em>les chiffres du musée</em></h2>
      <p class="lead">Les chiffres sont arrondis et datés. Quand plusieurs estimations existent, nous donnons un ordre de grandeur et nous l'indiquons.</p>
    </div>
    <ul class="so-stats" data-reveal>{stats}</ul>
  </div>
</section>

<section class="section" id="credits" aria-labelledby="cred-title">
  <div class="container">
    <div class="s-head" data-reveal>
      <span class="kicker">Vitrine IV · Crédits</span>
      <h2 id="cred-title">Images, voix, <em>polices et cartes</em></h2>
    </div>
    <ul class="so-credits" data-reveal>{credits}</ul>
  </div>
</section>"""
    write_page("sources.html", "sources", "Sources et bibliographie",
               "Sources de VERBUM : manuscrits originaux consultables en ligne, bibliographie commentée en français, statistiques et crédits.",
               body, js=["pages"], image="assets/img/pages/sources", image_alt="Une salle de lecture de bibliothèque ancienne")
    return nb


# --------------------------------------------------------------------------
# 5. 404
# --------------------------------------------------------------------------
def build_404():
    body = f"""
<section class="nf" aria-labelledby="nf-title">
  <div class="nf-bg" aria-hidden="true">{img_tag("assets/img/pages/404", "", lazy=False)}</div>
  <div class="container nf-in">
    <span class="kicker">Erreur 404 · vitrine vide</span>
    <h1 id="nf-title">Cette page <em>s'est perdue</em></h1>
    <p class="lead">Comme les 42 pages du Codex H, elle a quitté sa vitrine. Mais, comme elles, le texte que vous cherchez existe encore quelque part dans le musée.</p>
    <form class="sr-form nf-form" role="search" action="recherche.html" method="get">
      <label class="visually-hidden" for="nf-q">Rechercher</label>
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.4 15.4 20.5 20.5"/></svg>
      <input id="nf-q" name="q" type="search" placeholder="Rechercher dans le musée…">
      <button class="btn btn-or" type="submit">Rechercher</button>
    </form>
    <div class="nf-links">
      <a class="btn btn-ghost" href="index.html">Retour au hall d'entrée {{{{ARROW}}}}</a>
      <a class="btn btn-ghost" href="salles/11-frise.html">La Grande Frise</a>
      <a class="btn btn-ghost" href="audioguide.html">L'audioguide</a>
    </div>
  </div>
</section>"""
    write_page("404.html", "404", "Page introuvable", "Cette page n'existe pas ou a été déplacée.", body,
               image="assets/img/pages/404", noindex=True)


# --------------------------------------------------------------------------
# 6. Fichiers pour les moteurs et l'installation
# --------------------------------------------------------------------------
def build_meta_files(extra):
    url, maj = B.SITE["url"], B.SITE["maj"]
    pages = [("", "1.0", "monthly")] + [(s["href"], "0.9" if s.get("phare") or s.get("actu") else "0.8", "monthly") for s in B.SALLES]
    pages += [(p, "0.6", "monthly") for p in extra]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    imgs = {s["href"]: s.get("hero_img") for s in B.SALLES}
    imgs[""] = "assets/img/accueil/hero-jarres-grotte"
    for p in extra:
        imgs[p] = {"audioguide.html": "assets/img/pages/guide", "recherche.html": "assets/img/pages/recherche",
                   "a-propos.html": "assets/img/pages/apropos", "sources.html": "assets/img/pages/sources"}.get(p)
    for p, prio, freq in pages:
        im = f"\n    <image:image><image:loc>{url}/{imgs[p]}.jpg</image:loc></image:image>" if imgs.get(p) else ""
        xml.append(f"  <url>\n    <loc>{url}/{p}</loc>\n    <lastmod>{maj}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>{im}\n  </url>")
    xml.append("</urlset>\n")
    (B.ROOT / "sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
    (B.ROOT / "robots.txt").write_text(
        "# VERBUM — Musée Virtuel de la Bible\nUser-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /docs/\n\n"
        f"Sitemap: {url}/sitemap.xml\n", encoding="utf-8")
    manifest = {
        "name": B.SITE["titre"], "short_name": "VERBUM", "description": B.SITE["description"], "lang": "fr",
        "start_url": "./index.html", "scope": "./", "display": "standalone",
        "background_color": "#0A0A0F", "theme_color": "#0A0A0F",
        "icons": [{"src": "apple-touch-icon.jpg", "sizes": "180x180", "type": "image/jpeg"},
                  {"src": "assets/img/icon-512.jpg", "sizes": "512x512", "type": "image/jpeg", "purpose": "any"}],
    }
    (B.ROOT / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------
def build_all(build_module) -> int:
    global B
    B = build_module
    P = build_audioguide()
    nb_liens = build_sources()
    build_recherche()
    # l'index lit les pages déjà écrites ; À propos est indexée après sa première écriture
    build_apropos(len(P), nb_liens, 0)
    extra = [("audioguide.html", "Audioguide"), ("a-propos.html", "À propos"), ("sources.html", "Sources et bibliographie")]
    n_idx = build_index_recherche(extra)
    build_404()
    build_meta_files(["audioguide.html", "recherche.html", "a-propos.html", "sources.html"])
    B.NB_INDEX = n_idx
    return 5
