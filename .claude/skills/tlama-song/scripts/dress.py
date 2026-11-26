"""Dress Tlama (B_* and F_* images) in a country costume, no new generations needed.

    .venv/bin/python .claude/skills/tlama-song/scripts/dress.py egypt videos/NNN-language/work/custom

Reads puppets/song_duo/costumes/<country>/sheet.png (transparent: seated robe, standing robe,
hat, left to right) and writes the 10 dressed images; build_song.py picks up custom/ itself.
The clothes go over the body; head, microphone, arms and hands stay on top.
Boxes are in the 752x1344 library images, in costumes/<country>/place.json (copy one and
adjust it for a new sheet).
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

LIB = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../puppets/song_duo"))
country, out = sys.argv[1], sys.argv[2]

sheet = Image.open(f"{LIB}/costumes/{country}/sheet.png").convert("RGBA")
a = np.array(sheet)
# the generator adds a soft glow around the items: keep only the solid shapes, soft 1 px edge
a[..., 3] = np.clip((a[..., 3].astype(int) - 170) * 4, 0, 255)
lab, n = ndimage.label(a[..., 3] > 0)
big = sorted(sorted(range(1, n + 1), key=lambda i: -(lab == i).sum())[:3],
             key=lambda i: np.nonzero(lab == i)[1].min())
items = []
for i in big:
    p = a.copy(); p[..., 3][lab != i] = 0
    im = Image.fromarray(p); items.append(im.crop(im.getbbox()))
seated, standing, hat = items

boxes = json.load(open(f"{LIB}/costumes/{country}/place.json"))     # (left, top, right, bottom)
PLACE = {g: {"robe": (robe, boxes[g]["robe"]), "hat": boxes[g]["hat"]}
         for g, robe in (("B", seated), ("F", standing))}

CHIN = {"B": 990, "F": 1004}

def keep_mask(g):
    """Pixels of the original that stay in front of the robe."""
    S = 4
    m = Image.new("L", (752 * S, 1344 * S), 0); d = ImageDraw.Draw(m)
    def ell(x0, y0, x1, y1): d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), fill=255)
    def box(x0, y0, x1, y1, r): d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), r * S, fill=255)
    def line(pts, w):
        d.line([(x * S, y * S) for x, y in pts], fill=255, width=w * S, joint="curve")
        for x, y in pts: ell(x - w / 2, y - w / 2, x + w / 2, y + w / 2)
    if g == "B":
        ell(229, 695, 531, 991)                                   # head
        box(168, 780, 262, 905, 30); box(500, 780, 584, 910, 30)  # ear cups
        box(345, 998, 408, 1092, 30); box(336, 1044, 416, 1103, 28)  # mic + holder
        box(369, 1090, 383, 1290, 4); ell(331, 1273, 421, 1301)   # stand
        line([(262, 1040), (240, 1062), (218, 1092)], 12)         # arms and hands
        line([(494, 1040), (514, 1066), (532, 1092)], 12)
        ell(193, 1072, 240, 1118); ell(511, 1072, 556, 1118)
    else:
        ell(404, 748, 678, 1005)                                  # head
        box(356, 836, 436, 946, 30); box(654, 836, 730, 946, 30)
        ell(497, 963, 602, 1060); box(513, 1040, 583, 1132, 28)   # pop filter + mic
        box(541, 1120, 556, 1300, 4); ell(508, 1292, 590, 1320)
        line([(446, 1052), (428, 1090), (419, 1150)], 12)
        line([(645, 1052), (667, 1095), (678, 1150)], 12)
        ell(397, 1133, 442, 1180); ell(655, 1133, 701, 1180)
    return m.resize((752, 1344), Image.LANCZOS)

def paste(base, item, box):
    im = item.resize((box[2] - box[0], box[3] - box[1]), Image.LANCZOS)
    layer = Image.new("RGBA", base.size); layer.paste(im, box[:2])
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")

os.makedirs(out, exist_ok=True)
for g, shapes in (("B", "closed half wide o blink"), ("F", "closed half wide o drum")):
    keep = keep_mask(g)
    for s in shapes.split():
        src = Image.open(f"{LIB}/{g}_{s}.png").convert("RGB")
        assert src.size == (752, 1344)
        item, box = PLACE[g]["robe"]
        rgb = np.asarray(src)                    # old white coat inside the keep shapes goes too
        coat = (rgb[..., 0] > 185) & (rgb[..., 2] > 185)
        coat[:CHIN[g]] = False                   # ...but never the teeth above the chin line
        front = np.array(keep); front[coat] = 0
        im = Image.composite(src, paste(src, item, box), Image.fromarray(front))
        paste(im, hat, PLACE[g]["hat"]).save(f"{out}/{g}_{s}.png")
print("dressed 10 images ->", out)
