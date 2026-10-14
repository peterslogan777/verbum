"""VERBUM — Carte du monde en projection Natural Earth (Šavrič et al.)
Source des contours : Natural Earth 110m land (domaine public).
Produit un tracé SVG compact et des positions de lieux prêtes à l'emploi."""
import json, math
from pathlib import Path

W, H = 1000, 500
LAT_MIN = -58  # on écarte l'Antarctique

def _ne(lon, lat):
    l, p = math.radians(lon), math.radians(lat)
    p2 = p * p; p4 = p2 * p2
    x = l * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = p * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x, y

_XMAX = _ne(180, 0)[0]
_YTOP = _ne(0, 84)[1]
_YBOT = _ne(0, LAT_MIN)[1]
_S = min(W / (2 * _XMAX), H / (_YTOP - _YBOT))
_OX = W / 2
_OY = _YTOP * _S + (H - (_YTOP - _YBOT) * _S) / 2


def proj(lon, lat):
    x, y = _ne(lon, lat)
    return round(_OX + x * _S, 1), round(_OY - y * _S, 1)


def land_path(geojson_path):
    data = json.loads(Path(geojson_path).read_text())
    parts = []
    for f in data["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                if max(pt[1] for pt in ring) < LAT_MIN:
                    continue
                pts = [proj(lon, max(lat, LAT_MIN)) for lon, lat in ring]
                d = "M" + "L".join(f"{x:g} {y:g}" for x, y in pts) + "Z"
                parts.append(d)
    return "".join(parts)


if __name__ == "__main__":
    print(proj(35.23, 31.78), len(land_path("/tmp/land.geojson")))
