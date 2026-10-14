"""
VERBUM — Salle 05 « Découverte 2026 : le Codex H » (Lettres de Paul, VIe siècle)
Marqueurs remplacés dans tools/templates/salles/codex-h.html :
  {{S05_CARTE}} / {{S05_LIEUX}}  carte des feuillets dispersés + fiches des bibliothèques
  {{S05_TR}}                     transcription de la narration
Sources : Université de Glasgow, communiqué du 24 avril 2026 ; site du projet https://codexh.arts.gla.ac.uk/
"""
import html
import json
import math
from pathlib import Path

e = html.escape
ROOT = Path(__file__).resolve().parent.parent

LON0, LON1, LAT0, LAT1 = -11.0, 46.0, 34.5, 62.5
K = math.cos(math.radians(49))
VW = 760
VH = round(VW * (LAT1 - LAT0) / ((LON1 - LON0) * K))


def _p(lon, lat):
    return round((lon - LON0) / (LON1 - LON0) * VW, 1), round((LAT1 - lat) / (LAT1 - LAT0) * VH, 1)


ATHOS = (24.38, 40.17)
LIEUX = [
    # clé, ville, lon, lat, feuillets, institution, note, ancre
    ("paris", "Paris", 2.35, 48.85, 22, "Bibliothèque nationale de France (fonds Coislin 202)",
     "Le plus grand ensemble : c'est lui qui a donné au manuscrit son autre nom, « Coislinianus ».", "end"),
    ("athos", "Mont Athos", 24.38, 40.17, 8, "Monastère de la Grande Laure",
     "Le lieu où le codex fut démonté au XIIIe siècle. La communauté a ouvert ses feuillets aux chercheurs pour les imager à plusieurs reprises.", "start"),
    ("turin", "Turin", 7.69, 45.07, 2, "Bibliothèque nationale universitaire de Turin",
     "Deux feuillets, abîmés lors de l'incendie de la bibliothèque en 1904. La bibliothèque est partenaire du projet.", "end"),
    ("kyiv", "Kyiv", 30.52, 50.45, 3, "Bibliothèque nationale d'Ukraine Vernadsky",
     "Trois feuillets conservés en Ukraine.", "start"),
    ("moscou", "Moscou", 37.62, 55.75, 3, "Collections russes",
     "Trois feuillets conservés à Moscou.", "start"),
    ("spb", "Saint-Pétersbourg", 30.31, 59.94, 3, "Bibliothèque nationale de Russie",
     "Trois feuillets conservés à Saint-Pétersbourg.", "start"),
]
GLASGOW = ("glasgow", "Glasgow", -4.25, 55.86)


def carte():
    data = json.loads((ROOT / "tools" / "geo" / "ne_110m_land.geojson").read_text())
    paths = []
    for f in data["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                lons = [pt[0] for pt in ring]; lats = [pt[1] for pt in ring]
                if max(lons) < LON0 - 5 or min(lons) > LON1 + 5 or max(lats) < LAT0 - 5 or min(lats) > LAT1 + 5:
                    continue
                paths.append("M" + "L".join("{:g} {:g}".format(*_p(lon, lat)) for lon, lat in ring) + "Z")
    ax, ay = _p(*ATHOS)
    rays, marks = [], []
    for key, ville, lon, lat, n, inst, note, anchor in LIEUX:
        x, y = _p(lon, lat)
        if key != "athos":   # rayons de dispersion depuis l'Athos (des droites issues d'un même point ne se croisent jamais)
            rays.append(f'<path class="ch-ray" data-key="{key}" d="M{ax} {ay}L{x} {y}"/>')
        r = 6 + n * .55
        dx = -14 if anchor == "end" else 14
        marks.append(f'<g class="ch-pt{" is-origine" if key == "athos" else ""}" data-key="{key}" tabindex="0" role="button" aria-label="{e(ville)} : {n} feuillets">'
                     f'<circle class="halo" cx="{x}" cy="{y}" r="{r + 8:.1f}"/><circle class="core" cx="{x}" cy="{y}" r="{r:.1f}"/>'
                     f'<text class="n" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>'
                     f'<text class="v" x="{x + dx + (r - 6) * (1 if anchor == "start" else -1):.1f}" y="{y + 4}" text-anchor="{anchor}">{e(ville)}</text></g>')
    gx, gy = _p(GLASGOW[2], GLASGOW[3])
    marks.append(f'<g class="ch-lab" data-key="glasgow" tabindex="0" role="button" aria-label="Glasgow : l\'équipe de recherche">'
                 f'<rect x="{gx - 7}" y="{gy - 7}" width="14" height="14" rx="3"/><text x="{gx + 14}" y="{gy + 4}">Glasgow · l\'équipe</text></g>')
    svg = (f'<svg class="ch-map" viewBox="0 0 {VW} {VH}" role="img" aria-label="Carte des feuillets du Codex H dispersés en Europe depuis le mont Athos">'
           f'<defs><radialGradient id="ch-sea" cx="60%" cy="70%" r="85%"><stop offset="0" stop-color="#16123a"/><stop offset="1" stop-color="#0A0A0F"/></radialGradient></defs>'
           f'<rect width="{VW}" height="{VH}" fill="url(#ch-sea)"/><path class="ch-land" d="{"".join(paths)}"/>'
           f'{"".join(rays)}{"".join(marks)}</svg>')
    panels = []
    for key, ville, lon, lat, n, inst, note, anchor in LIEUX:
        panels.append(f'<article class="ch-panel" data-key="{key}"{"" if key == "athos" else " hidden"}>'
                      f'<p class="ch-k">{e(ville)}</p><h4>{n} feuillet{"s" if n > 1 else ""}</h4>'
                      f'<p class="ch-inst">{e(inst)}</p><p>{e(note)}</p></article>')
    panels.append('<article class="ch-panel" data-key="glasgow" hidden><p class="ch-k">Glasgow</p><h4>Le laboratoire du projet</h4>'
                  '<p class="ch-inst">Université de Glasgow · avec l\'Université de Groningue, l\'Early Manuscripts Electronic Library (EMEL) et le laboratoire des manuscrits de l\'Université d\'Athènes</p>'
                  '<p>C\'est ici qu\'est dirigé le projet du professeur Garrick Allen, qui a rassemblé virtuellement les feuillets dispersés et leurs pages fantômes.</p></article>')
    return svg, "".join(panels)


TR = """<p>Au sixième siècle, un scribe copie avec soin les lettres de l'apôtre Paul, en grandes lettres onciales, disposées en lignes de sens pour faciliter la lecture à voix haute. Ce manuscrit, les spécialistes l'appellent aujourd'hui le Codex H. Au treizième siècle, au monastère de la Grande Laure, sur le mont Athos, le livre usé est démonté. Son texte avait été repassé à l'encre ; ses feuilles servent désormais de reliure et de pages de garde pour d'autres volumes. Dispersées, les feuilles survivantes se trouvent aujourd'hui en France, en Grèce, en Italie, en Russie et en Ukraine.</p>
<p>C'est cette encre qui a trahi le secret. Ses composés chimiques ont laissé, sur les pages en vis-à-vis, une empreinte en miroir du texte, parfois sur plusieurs feuillets d'épaisseur. Presque invisible à l'œil nu, ce texte fantôme apparaît clairement sous l'imagerie multispectrale. L'équipe internationale dirigée par le professeur Garrick Allen, de l'Université de Glasgow, a ainsi récupéré quarante-deux pages perdues, annoncées le 24 avril 2026, et une datation au radiocarbone, réalisée à Paris, a confirmé le sixième siècle. Le texte retrouvé est celui des lettres de Paul que nous connaissons déjà. La découverte ne change pas la Bible : elle la confirme, et révèle comment des mains anciennes lisaient, corrigeaient et annotaient les Écritures.</p>"""


def render(inner):
    svg, panels = carte()
    return inner.replace("{{S05_CARTE}}", svg).replace("{{S05_LIEUX}}", panels).replace("{{S05_TR}}", TR)


if __name__ == "__main__":
    s, p = carte()
    print(VW, VH, len(s))
