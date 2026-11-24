"""Fast set dressing: fill a location with many props from props/<pack>/ in a few lines.

Import from a build script (scripts/ is next to it):

    import sys; sys.path.insert(0, 'scripts')
    from set_dressing import M, scatter, line, ring

    G = 'kenney_graveyard-kit_5'
    props  = line(M(G, 'iron-fence', 2.6), (X-10, -8), (X+10, -8))              # fence/wall row
    props += scatter([M(G, 'pine', 3), M(G, 'pine-crooked', 3.3)], 14, ring=(X, 0, 16, 32), seed=1)   # far trees
    props += scatter([M(G, 'rocks', 2), M(G, 'gravestone-round', 3)], 20, rect=(X, 0, 30, 18), keep_out=[(X+0.5, 1.5, 3)], seed=2)

M(pack, name, scale)   one model; scale is a number or (min, max) range; add y=, rotY= (fixed) or rot=False (no random yaw)
scatter(items, n, rect=(cx,cz,w,d) | ring=(cx,cz,r_min,r_max), keep_out=[(x,z,r)], seed, min_dist)
line(item, (x0,z0), (x1,z1), step=None)   evenly spaced row (fence, wall, trees along a road)
ring(...) is scatter(ring=...) shortcut.  All return a list of short.json prop dicts.
"""
import math, random


def M(pack, name, scale=1.0, y=0.0, rotY=None, rot=True, **extra):
    return {'pack': pack, 'name': name, 'scale': scale, 'y': y, 'rotY': rotY, 'rot': rot, 'extra': extra}


def _prop(item, x, z, rng, yaw=None):
    sc = item['scale']
    sc = rng.uniform(*sc) if isinstance(sc, (tuple, list)) else sc * rng.uniform(0.85, 1.2)
    ry = item['rotY'] if item['rotY'] is not None else (rng.uniform(0, 360) if item['rot'] else 0)
    if yaw is not None:
        ry = yaw
    p = {'type': 'model', 'file': f"props/{item['pack']}/{item['name']}.glb", 'pos': [round(x, 2), item['y'], round(z, 2)], 'scale': round(sc, 2), 'rotY': round(ry, 1)}
    p.update(item['extra'])
    return p


def scatter(items, n, rect=None, ring=None, keep_out=(), seed=0, min_dist=1.2):
    """n props at random places in a rectangle (cx, cz, width, depth) or ring (cx, cz, r_min, r_max)."""
    rng = random.Random(seed)
    out, pts, tries = [], [], 0
    while len(out) < n and tries < n * 60:
        tries += 1
        if rect:
            cx, cz, w, d = rect
            x, z = cx + rng.uniform(-w / 2, w / 2), cz + rng.uniform(-d / 2, d / 2)
        else:
            cx, cz, r0, r1 = ring
            a, r = rng.uniform(0, 2 * math.pi), rng.uniform(r0, r1)
            x, z = cx + r * math.cos(a), cz + r * math.sin(a)
        if any(math.hypot(x - kx, z - kz) < kr for kx, kz, kr in keep_out):
            continue
        if any(math.hypot(x - px, z - pz) < min_dist for px, pz in pts):
            continue
        pts.append((x, z))
        out.append(_prop(rng.choice(items), x, z, rng))
    return out


def ring(items, n, center, r_min, r_max, **kw):
    return scatter(items, n, ring=(center[0], center[1], r_min, r_max), **kw)


def line(item, p0, p1, step=None, seed=0, yaw=None):
    """Row of the same model from p0 to p1 (x, z). step defaults to the model's scale (tiles of ~1 unit)."""
    rng = random.Random(seed)
    if not step:
        step = 2.0 if isinstance(item['scale'], (tuple, list)) else item['scale']
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    dist = math.hypot(dx, dz)
    n = max(1, round(dist / step))
    ang = math.degrees(math.atan2(-dz, dx)) if yaw is None else yaw
    return [_prop({**item, 'rot': False, 'rotY': None}, p0[0] + dx * i / n, p0[1] + dz * i / n, rng, yaw=ang) for i in range(n + 1)]


def clear_zone(hero, radius=5.5, reach=34.0, width=3.5, fan=(-55, -28, 0, 28, 55)):
    """keep_out circles around the hero plus corridors toward the camera side (+z), fanned left/right.

    The camera orbits the hero (yaw up to ~55 deg, wide shots far away), so a single straight
    corridor is not enough. Pass the result to keep_out= of every scatter() that places BIG props
    (trees, rocks, crypts), otherwise you get the stage flag CAMERA_INSIDE_PROP.
    Small ground clutter can use keep_out=[(hx, hz, 2.5)] to be allowed close to the hero.
    """
    hx, hz = hero
    zone = [(hx, hz, radius)]
    for deg in fan:
        a = math.radians(deg)
        d = radius
        while d < reach:
            zone.append((hx + d * math.sin(a), hz + d * math.cos(a), width)); d += width
    return zone
