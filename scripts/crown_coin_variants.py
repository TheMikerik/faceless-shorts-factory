# Crown + coin props and the puppet variants that go with them (made locally with PIL,
# no Higgsfield). Everything is derived from existing puppets, so the style matches.
#   puppets/prop_crown              the tiny king's gold crown, cut out of dwarf_king (flies, lands)
#   puppets/prop_coin               a gold coin with a star
#   puppets/dwarf_king_nocrown      the tiny king with a bare head (all faces)
#   puppets/orange_tabby_cat_crown  the orange cat wearing the crown
#   puppets/main_hero_tlama_crown   Tlama wearing the crown (all faces)
#   puppets/main_hero_tlama_coin    Tlama holding the coin in the right hand (star upright at armR -100)
# Run: .venv/bin/python scripts/crown_coin_variants.py "$PWD"
import json, shutil, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
PUP = f"{ROOT}/puppets"
INK = (39, 25, 37, 255)


def yellow(a):
    R, G, B, A = (a[..., i].astype(int) for i in range(4))
    return (R > 170) & (G > 120) & (B < 130) & (A > 100) & (R - B > 80)


def crown_mask(a, grow=11):
    """Crown = the yellow blob plus its ink outline (ink pixels close to the yellow, above the head)."""
    y = yellow(a)
    lab, n = ndimage.label(y)
    if n == 0:
        return np.zeros_like(y)
    sizes = ndimage.sum(y, lab, range(1, n + 1))
    y = lab == (1 + int(np.argmax(sizes)))
    near = ndimage.binary_dilation(y, iterations=grow)
    R, G, B, A = (a[..., i].astype(int) for i in range(4))
    dark = (R + G + B < 300) & (A > 60)
    return y | (near & dark) | (near & (A < 250) & ~(R + G + B > 600))


def fit_circle(pts):
    x, y = pts[:, 0].astype(float), pts[:, 1].astype(float)
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    c, *_ = np.linalg.lstsq(A, x * x + y * y, rcond=None)
    cx, cy = c[0], c[1]
    return cx, cy, np.sqrt(c[2] + cx * cx + cy * cy)


def remove_crown(path):
    im = Image.open(path).convert("RGBA"); a = np.array(im)
    m = crown_mask(a)
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # head outline points: top edge of the alpha just left/right of the crown, plus side edges below it
    alpha = a[..., 3] > 128
    pts = []
    for x in list(range(max(0, x0 - 60), x0 - 4, 3)) + list(range(x1 + 4, min(a.shape[1], x1 + 60), 3)):
        col = np.nonzero(alpha[:, x] & ~m[:, x])[0]
        if len(col): pts.append((x, col[0]))
    for yy in range(y1 + 10, y1 + 70, 4):
        row = np.nonzero(alpha[yy])[0]
        if len(row): pts += [(row[0], yy), (row[-1], yy)]
    cx, cy, r = fit_circle(np.array(pts))
    skin = a[min(a.shape[0] - 1, int(y1 + 25)), int((x0 + x1) / 2)].copy()
    inkw = max(6, int(r * 0.045))
    out = a.copy()
    Y, X = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    d = np.hypot(X - cx, Y - cy)
    zone = ndimage.binary_dilation(m, iterations=3)
    out[zone] = 0
    fill = zone & (d < r - inkw)
    ring = zone & (d >= r - inkw) & (d <= r + 0.5)
    out[fill] = skin
    out[ring] = INK
    # thin leftovers of the crown outline above the head
    box = (Y < cy) & (X > x0 - 30) & (X < x1 + 30) & (Y < y1 + 30) & (d > r + 1)
    out[box] = 0
    Image.fromarray(out).save(path)


def fresh(src, name):
    dst = f"{PUP}/{name}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(f"{PUP}/{src}", dst, ignore=shutil.ignore_patterns("source*.png", "emotions.png", "*preview.png"))
    rig = json.load(open(f"{dst}/rig.json")); rig["name"] = name
    return dst, rig


def prop_puppet(name, img):
    dst = f"{PUP}/{name}"
    if os.path.exists(dst): shutil.rmtree(dst)
    os.makedirs(dst)
    w, h = img.size
    img.save(f"{dst}/head.png")
    Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(f"{dst}/body.png")
    rig = {"version": 2, "name": name, "size": [w, h], "feetY": h,
           "head": {"center": [w / 2, h / 2], "diameter": float(w)}, "skin": "#f4f1e8",
           "layers": {"body": {"file": "body.png", "box": [w // 2, h - 1, 1, 1], "pivot": [w / 2, h]},
                      "head": {"file": "head.png", "box": [0, 0, w, h], "pivot": [w / 2, h]}},
           "order": ["body", "head"], "faces": {}}
    json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)


# ---------- crown prop (cut from the king's head) ----------
head = np.array(Image.open(f"{PUP}/dwarf_king/head.png").convert("RGBA"))
m = crown_mask(head)
cr = head.copy(); cr[~m] = 0
ys, xs = np.nonzero(m)
CROWN = Image.fromarray(cr[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
CROWN = CROWN.rotate(-8, expand=True, resample=Image.BICUBIC)        # level it (it sits tilted on the king)
bb = CROWN.getbbox(); CROWN = CROWN.crop(bb)
pad = 6; c2 = Image.new("RGBA", (CROWN.width + 2 * pad, CROWN.height + 2 * pad)); c2.alpha_composite(CROWN, (pad, pad)); CROWN = c2
prop_puppet("prop_crown", CROWN)

# ---------- coin prop ----------
def coin_img(D=300):
    im = Image.new("RGBA", (D + 24, D + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lw = max(5, D // 22); o = 12
    d.ellipse([o, o, o + D, o + D], fill=(245, 196, 60, 255), outline=INK, width=lw)
    d.ellipse([o + D * .16, o + D * .16, o + D * .84, o + D * .84], fill=(255, 216, 96, 255), outline=(201, 140, 40, 255), width=max(3, lw // 2))
    import math
    cx = cy = o + D / 2; R1, R2 = D * .24, D * .1
    star = [(cx + (R1 if i % 2 == 0 else R2) * math.sin(i * math.pi / 5), cy - (R1 if i % 2 == 0 else R2) * math.cos(i * math.pi / 5)) for i in range(10)]
    d.polygon(star, fill=(255, 246, 200, 255), outline=INK, width=max(3, lw // 2))
    d.arc([o + D * .1, o + D * .1, o + D * .9, o + D * .9], 200, 250, fill=(255, 246, 200, 255), width=max(4, lw // 2))
    return im
COIN = coin_img()
prop_puppet("prop_coin", COIN)

# ---------- king without crown ----------
dst, rig = fresh("dwarf_king", "dwarf_king_nocrown")
remove_crown(f"{dst}/head.png")
for F in rig["faces"].values():
    remove_crown(f"{dst}/{F['file']}")
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)


# ---------- paste the crown on top of a head layer (canvas grows upward) ----------
def put_crown(img_path, cx, top, width, tilt=0, sink=0.32):
    im = Image.open(img_path).convert("RGBA")
    c = CROWN.resize((int(width), int(width * CROWN.height / CROWN.width)), Image.LANCZOS)
    if tilt: c = c.rotate(tilt, expand=True, resample=Image.BICUBIC)
    y = int(top - c.height * (1 - sink)); up = max(0, -y)
    big = Image.new("RGBA", (im.width, im.height + up), (0, 0, 0, 0)); big.alpha_composite(im, (0, up))
    big.alpha_composite(c, (int(cx - c.width / 2), y + up))
    big.save(img_path)
    return up


# Tlama with crown (head + every face)
dst, rig = fresh("main_hero_tlama", "main_hero_tlama_crown")
H = rig["layers"]["head"]
hx0, hy0 = H["box"][0], H["box"][1]
D = rig["head"]["diameter"]
cx = rig["head"]["center"][0] - hx0; top = rig["head"]["center"][1] - D / 2 - hy0
up = put_crown(f"{dst}/head.png", cx + D * 0.04, top + D * 0.02, D * 0.42, tilt=-6)
x, y, w, h = H["box"]; H["box"] = [x, y - up, w, h + up]
for F in rig["faces"].values():
    s = F["diameter"] / D
    up = put_crown(f"{dst}/{F['file']}", F["center"][0] + D * 0.04 * s, F["center"][1] - F["diameter"] / 2 + D * 0.02 * s, D * 0.42 * s, tilt=-6)
    F["size"] = [F["size"][0], F["size"][1] + up]; F["pivot"][1] += up; F["center"][1] += up
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)

# cat with crown (head layer only, cats have no faces)
dst, rig = fresh("orange_tabby_cat", "orange_tabby_cat_crown")
H = rig["layers"]["head"]
hx0, hy0 = H["box"][0], H["box"][1]
D = rig["head"]["diameter"]
cx = rig["head"]["center"][0] - hx0 - D * 0.05; top = rig["head"]["center"][1] - D / 2 - hy0 + D * 0.06
up = put_crown(f"{dst}/head.png", cx, top, D * 0.5, tilt=-10, sink=0.25)
x, y, w, h = H["box"]; H["box"] = [x, y - up, w, h + up]
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)

# Tlama holding the coin (armR)
dst, rig = fresh("main_hero_tlama", "main_hero_tlama_coin")
L = rig["layers"]["armR"]; arm = Image.open(f"{dst}/armR.png").convert("RGBA")
al = np.array(arm)[..., 3] > 40; ys, xs = np.nonzero(al)
low = ys > ys.max() - 40; hx, hy = xs[low].mean(), ys[low].mean()
M = 160
big = Image.new("RGBA", (arm.width + 2 * M, arm.height + 2 * M), (0, 0, 0, 0)); big.alpha_composite(arm, (M, M))
POSE = -100   # arm pose used in short.json; PIL rotate(POSE) keeps the star upright at that pose
c = COIN.resize((170, 170), Image.LANCZOS).rotate(POSE, resample=Image.BICUBIC)
big.alpha_composite(c, (int(M + hx - 85), int(M + hy - 95)))
big.save(f"{dst}/armR.png")
x, y, w, h = L["box"]; L["box"] = [x - M, y - M, w + 2 * M, h + 2 * M]
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)
print("ok: prop_crown prop_coin dwarf_king_nocrown main_hero_tlama_crown orange_tabby_cat_crown main_hero_tlama_coin")
