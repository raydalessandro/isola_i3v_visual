"""
Utility per l'autrice/autore delle storie.

Input: id di una location (anche alias), coordinate locali (east, north) in metri,
o coordinate geografiche (lon, lat).
Output: cosa c'e' a quel punto secondo la cartografia — vincoli geografici,
sotto-tratto del Fiume (se applicabile), luoghi vicini.

Supporta alias backward-compat con il grafo storie.

Uso:
    python3 verifica_luogo.py --id due_massi
    python3 verifica_luogo.py --id villaggio_centrale       # alias -> piazza_villaggio
    python3 verifica_luogo.py --id fiume_che_gira           # feature aggregato
    python3 verifica_luogo.py --coord 4000 3500
    python3 verifica_luogo.py --geo 18.0 34.5
"""
import json
import math
import sys
import argparse

LAT_ORIGIN = 34.4685
LON_ORIGIN = 17.956
M_PER_DEG_LAT = 111000
M_PER_DEG_LON = 91400

def to_local(lon, lat):
    return ((lon - LON_ORIGIN) * M_PER_DEG_LON,
            (lat - LAT_ORIGIN) * M_PER_DEG_LAT)

def dist_pp(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def dist_pl(p, line):
    """Distanza minima punto-linestring (coord locali)."""
    min_d = float('inf')
    for i in range(len(line)-1):
        a, b = line[i], line[i+1]
        dx, dy = b[0]-a[0], b[1]-a[1]
        if dx == 0 and dy == 0:
            d = dist_pp(p, a)
        else:
            t = ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / (dx*dx + dy*dy)
            t = max(0, min(1, t))
            proj = (a[0] + t*dx, a[1] + t*dy)
            d = dist_pp(p, proj)
        if d < min_d:
            min_d = d
    return min_d

def resolve_id(data, query_id):
    """
    Trova la feature con id = query_id.
    Se non esiste, cerca nei campi aliases di tutte le feature.
    Ritorna (feature, used_alias) oppure (None, None).
    """
    # Cerca id diretto
    for feat in data['features']:
        if feat['properties']['id'] == query_id:
            return feat, None
    # Cerca in aliases
    for feat in data['features']:
        aliases = feat['properties'].get('aliases', [])
        if query_id in aliases:
            return feat, feat['properties']['id']
    return None, None

def geom_centroid(g):
    pts = []
    def collect(c):
        if isinstance(c[0], (int, float)):
            pts.append(c)
        else:
            for x in c: collect(x)
    collect(g['coordinates'])
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return cx, cy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='ID luogo (anche alias backward-compat)')
    parser.add_argument('--coord', nargs=2, type=float,
                        help='Coord locali (east, north) metri')
    parser.add_argument('--geo', nargs=2, type=float,
                        help='Coord geografiche (lon, lat)')
    parser.add_argument('--geojson', default='geo/island.geojson')
    parser.add_argument('--radius', type=float, default=300,
                        help='Raggio vicinanza in metri (default 300)')
    args = parser.parse_args()

    with open(args.geojson) as f:
        data = json.load(f)

    target_feat = None
    used_alias = None

    if args.id:
        target_feat, used_alias = resolve_id(data, args.id)
        if target_feat is None:
            print(f"Errore: id '{args.id}' non trovato (nemmeno come alias)",
                  file=sys.stderr)
            sys.exit(1)
        g = target_feat['geometry']
        if g['type'] == 'Point':
            lon, lat = g['coordinates']
            qp = to_local(lon, lat)
        else:
            cx, cy = geom_centroid(g)
            qp = to_local(cx, cy)
        resolved_id = target_feat['properties']['id']
        if used_alias:
            print(f"=== VERIFICA: '{args.id}' [alias -> {resolved_id}] ===")
            print(f"Nome: {target_feat['properties'].get('name', resolved_id)}")
        else:
            print(f"=== VERIFICA: {resolved_id} ({target_feat['properties'].get('name', resolved_id)}) ===")
    elif args.coord:
        qp = (args.coord[0], args.coord[1])
        print(f"=== VERIFICA PUNTO locale ({qp[0]:.0f}, {qp[1]:.0f}) ===")
    elif args.geo:
        qp = to_local(args.geo[0], args.geo[1])
        print(f"=== VERIFICA PUNTO geo ({args.geo[0]}, {args.geo[1]}) "
              f"-> locale ({qp[0]:.0f}, {qp[1]:.0f}) ===")
    else:
        parser.print_help()
        sys.exit(1)

    print()

    # Se e' feature aggregata (fiume_che_gira, montagne_gemelle), mostra children
    if target_feat and target_feat['properties'].get('aggregate'):
        children = target_feat['properties'].get('children', [])
        print(f"--- Feature AGGREGATA. Children ({len(children)}) ---")
        for ch in children:
            print(f"  - {ch}")
        print()

    # Luoghi entro radius (solo Point, non aggregate)
    print(f"--- Luoghi entro {args.radius}m ---")
    nearby = []
    for feat in data['features']:
        if feat['geometry']['type'] != 'Point':
            continue
        if feat['properties'].get('aggregate'):
            continue
        lon, lat = feat['geometry']['coordinates']
        p = to_local(lon, lat)
        d = dist_pp(qp, p)
        if d <= args.radius:
            nearby.append((d, feat))
    nearby.sort()
    for d, feat in nearby[:15]:
        p = feat['properties']
        if target_feat and p['id'] == target_feat['properties']['id']:
            print(f"  [SELF]  {p['id']:40s}  [{p.get('type','?')}]")
        else:
            print(f"  {d:6.0f}m  {p['id']:40s}  {p.get('name','?')[:30]:30s}  [{p.get('type','?')}]")

    # Distanza tratti Fiume
    print()
    print("--- Tratti d'acqua e loro distanza ---")
    water_types = ['river', 'stream', 'seasonal_streambed']
    water_feats = [f for f in data['features']
                   if f['properties']['type'] in water_types
                   and f['geometry']['type'] == 'LineString']
    river_dists = []
    for feat in water_feats:
        line_local = [to_local(lon, lat) for lon, lat in feat['geometry']['coordinates']]
        d = dist_pl(qp, line_local)
        river_dists.append((d, feat['properties']['id'],
                           feat['properties'].get('name', '?')))
    river_dists.sort()
    for d, fid, name in river_dists[:6]:
        print(f"  {d:6.0f}m  {fid:35s}  {name}")

    # Sentieri vicini
    print()
    print("--- Sentieri vicini (entro 200m) ---")
    path_feats = [f for f in data['features']
                  if f['properties']['type'] == 'path']
    path_near = []
    for feat in path_feats:
        line_local = [to_local(lon, lat) for lon, lat in feat['geometry']['coordinates']]
        d = dist_pl(qp, line_local)
        if d <= 200:
            path_near.append((d, feat['properties']['id'],
                              feat['properties'].get('name', '?')))
    path_near.sort()
    if path_near:
        for d, fid, name in path_near[:8]:
            print(f"  {d:6.0f}m  {fid:40s}  {name}")
    else:
        print("  (nessuno entro 200m)")

    # Quartiere
    print()
    if nearby:
        qrt = nearby[0][1]['properties'].get('quarter', 'sconosciuto')
        print(f"--- Quartiere probabile: {qrt} ---")

if __name__ == '__main__':
    main()
