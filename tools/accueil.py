"""VERBUM — Rendu des composants de la page d'accueil (E02)."""
import html, math
from pathlib import Path
from data_accueil import HERO_SLIDES, FRISE, CARTE_EPOQUES, CARTE_LIEUX, IMG
import carte

e = html.escape
ROOT = Path(__file__).resolve().parent.parent

BADGES = {
    "canon": '<span class="badge badge-canon">Canonique</span>',
    "apo": '<span class="badge badge-apo">Apocryphe</span>',
    "debat": '<span class="badge badge-debat">Datation débattue</span>',
    "trad": '<span class="badge badge-debat">Datation traditionnelle</span>',
    "none": "",
}


def hero_slides():
    out = []
    for i, (n, alt) in enumerate(HERO_SLIDES):
        prio = ' fetchpriority="high"' if i == 0 else ' loading="lazy"'
        out.append(
            f'<figure class="slide{" is-active" if i == 0 else ""}" data-caption="{e(alt)}">'
            f'<img src="{IMG}{n}.jpg" srcset="{IMG}{n}-960.jpg 960w, {IMG}{n}.jpg 1920w" sizes="100vw" '
            f'alt="{e(alt)} (illustration numérique)" width="1920" height="1080" decoding="async"{prio}></figure>')
    dots = "".join(f'<button type="button" class="hero-dot{" is-active" if i == 0 else ""}" aria-label="Image {i + 1} : {e(a)}"><i></i></button>'
                   for i, (_, a) in enumerate(HERO_SLIDES))
    return "\n      ".join(out), dots


# --- Frise : échelle par morceaux (l'Antiquité lointaine est compressée) ---
def frise_pos(y):
    if y <= 0:
        return (y + 1500) / 1500 * 0.30
    if y <= 1500:
        return 0.30 + y / 1500 * 0.38
    return 0.68 + (y - 1500) / 526 * 0.32


def frise():
    salles = {"01": "01-origines", "02": "02-copistes", "03": "03-qumran", "04": "04-codex-grecs", "05": "05-codex-h",
              "06": "06-apocryphes", "07": "07-traductions", "08": "08-gutenberg", "09": "09-archeologie", "10": "10-indestructible"}
    cards, dots = [], []
    for i, (y, lab, titre, txt, badge, salle, img) in enumerate(FRISE):
        pos = frise_pos(y)
        main, small = (lab.replace(" av. J.-C.", ""), "av. J.-C.") if "av. J.-C." in lab else (lab, "ap. J.-C." if y < 1000 else "")
        media = (f'<div class="fr-media"><img src="{IMG}{img}-960.jpg" alt="" loading="lazy" decoding="async" width="960" height="540"></div>'
                 if img else '<div class="fr-media fr-media--empty" aria-hidden="true"><span>' + e(main) + '</span></div>')
        cards.append(f"""
        <article class="fr-card{' has-img' if img else ''}" data-i="{i}" data-pos="{pos:.4f}">
          {media}
          <div class="fr-body">
            <p class="fr-year">{e(main)}{f' <small>{small}</small>' if small else ''}</p>
            {BADGES[badge]}
            <h3>{e(titre)}</h3>
            <p>{e(txt)}</p>
            <a class="fr-link" href="salles/{salles[salle]}.html">Salle {salle} <span aria-hidden="true">→</span></a>
          </div>
        </article>""")
        dots.append(f'<button type="button" class="fr-dot" style="left:{pos * 100:.2f}%" data-i="{i}" aria-label="{e(lab)} : {e(titre)}"></button>')
    labels = [(-1500, "1500 av."), (-1000, "1000 av."), (-500, "500 av."), (0, "Notre ère"), (500, "500"), (1000, "1000"), (1500, "1500"), (1800, "1800"), (2026, "2026")]
    def cls(i):
        return " is-first" if i == 0 else (" is-last" if i == len(labels) - 1 else (" is-zero" if labels[i][0] == 0 else ""))
    lab_html = "".join(f'<span class="fr-lab{cls(i)}" style="left:{frise_pos(y) * 100:.2f}%">{t}</span>' for i, (y, t) in enumerate(labels))
    return "".join(cards), "".join(dots), lab_html


# --- Carte ---
def carte_html():
    land = carte.land_path(ROOT / "tools" / "geo" / "ne_110m_land.geojson")
    idx = {n: (lon, lat) for n, lon, lat, *_ in CARTE_LIEUX}
    arcs, pts = [], []
    for n, lon, lat, era, det, src in CARTE_LIEUX:
        x, y = carte.proj(lon, lat)
        if src:
            x1, y1 = carte.proj(*idx[src])
            dx, dy = x - x1, y - y1
            dist = math.hypot(dx, dy) or 1
            k = min(0.35, 12 / dist + 0.18)
            cx, cy = (x1 + x) / 2 - dy * k, (y1 + y) / 2 + dx * k
            if cy > (y1 + y) / 2:  # toujours bomber vers le haut
                cx, cy = (x1 + x) / 2 + dy * k, (y1 + y) / 2 - dx * k
            arcs.append(f'<path class="arc" data-era="{era}" d="M{x1} {y1}Q{cx:.1f} {cy:.1f} {x} {y}"/>')
        pts.append(f'<g class="pt" data-era="{era}" tabindex="0" role="button" transform="translate({x} {y})" '
                   f'data-name="{e(n)}" data-detail="{e(det)}" aria-label="{e(n)} : {e(det)}">'
                   f'<circle class="halo" r="7"/><circle class="core" r="2.6"/></g>')
    tabs, panels = [], []
    for k, (date, titre, desc) in enumerate(CARTE_EPOQUES):
        tabs.append(f'<button type="button" class="ep-tab{" is-active" if k == 0 else ""}" data-era="{k}" role="tab" aria-selected="{"true" if k == 0 else "false"}">'
                    f'<span class="ep-date">{date}</span><span class="ep-title">{e(titre)}</span></button>')
        lieux = "".join(f'<li><b>{e(n)}</b> — {e(det)}</li>' for n, _, _, era, det, _ in CARTE_LIEUX if era == k)
        panels.append(f'<div class="ep-panel{" is-active" if k == 0 else ""}" data-era="{k}" role="tabpanel">'
                      f'<p class="ep-kicker">{date}</p><h3>{e(titre)}</h3><p class="ep-desc">{e(desc)}</p><ul>{lieux}</ul></div>')
    svg = f"""<svg class="carte-svg" viewBox="0 0 {carte.W} {carte.H}" role="img" aria-label="Carte du monde de la diffusion de la Bible">
          <defs>
            <pattern id="dots" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r=".9" fill="#C9A84C" fill-opacity=".38"/></pattern>
            <radialGradient id="glowJ" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E6CC7A" stop-opacity=".55"/><stop offset="1" stop-color="#E6CC7A" stop-opacity="0"/></radialGradient>
          </defs>
          <path class="land" d="{land}"/>
          <circle cx="{carte.proj(35.23, 31.78)[0]}" cy="{carte.proj(35.23, 31.78)[1]}" r="60" fill="url(#glowJ)" class="glow-origin"/>
          <g class="arcs">{''.join(arcs)}</g>
          <g class="pts">{''.join(pts)}</g>
        </svg>"""
    return svg, "".join(tabs), "".join(panels)
