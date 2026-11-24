# Derive Tlama puppet variants with a prop painted into a layer (phone in hand, nest on head).
# Props baked into the puppet move with it and vanish with it (static props would float).
# Run: .venv/bin/python scripts/puppet_variants.py "$PWD"
import json, shutil, math, random, os, sys
from PIL import Image, ImageDraw
import numpy as np
ROOT = sys.argv[1]
SRC = f"{ROOT}/puppets/main_hero_tlama"
INK = (39, 25, 37, 255)

def fresh(name):
    dst = f"{ROOT}/puppets/{name}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("source*.png", "emotions.png", "*preview.png"))
    rig = json.load(open(f"{dst}/rig.json")); rig["name"] = name
    return dst, rig

# ---------- phone in right hand ----------
def phone_img(s=1.0, ang=0):
    W, H = int(78*s), int(130*s); pad = 12
    im = Image.new("RGBA", (W+2*pad, H+2*pad), (0,0,0,0)); d = ImageDraw.Draw(im)
    lw = max(5, int(8*s))
    d.rounded_rectangle([pad, pad, pad+W, pad+H], radius=int(16*s), fill=(226, 79, 79, 255), outline=INK, width=lw)
    d.rounded_rectangle([pad+int(12*s), pad+int(16*s), pad+W-int(12*s), pad+H-int(30*s)], radius=int(6*s), fill=(150, 220, 255, 255), outline=INK, width=max(3, lw//2))
    d.ellipse([pad+W//2-int(7*s), pad+H-int(23*s), pad+W//2+int(7*s), pad+H-int(9*s)], fill=INK)
    return im.rotate(ang, expand=True, resample=Image.BICUBIC)

dst, rig = fresh("main_hero_tlama_phone")
L = rig["layers"]["armR"]; arm = Image.open(f"{dst}/armR.png").convert("RGBA")
a = np.array(arm)[..., 3] > 40; ys, xs = np.nonzero(a)
low = ys > ys.max() - 40; hx, hy = xs[low].mean(), ys[low].mean()   # hand ball
M = 160
big = Image.new("RGBA", (arm.width + 2*M, arm.height + 2*M), (0,0,0,0)); big.alpha_composite(arm, (M, M))
POSE = -105   # arm pose used in short.json; phone drawn so it is upright then
ph = phone_img(1.6, ang=POSE)   # PIL rotate = ccw; stage +clockwise -> counter-rotate
big.alpha_composite(ph, (int(M+hx-ph.width/2), int(M+hy-ph.height*0.62)))
big.save(f"{dst}/armR.png")
x, y, w, h = L["box"]; L["box"] = [x-M, y-M, w+2*M, h+2*M]
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)

# ---------- nest on head ----------
def draw_nest(im, cx, top, s):
    d = ImageDraw.Draw(im); rnd = random.Random(7)
    w, h = 400*s, 150*s; y0 = top - 70*s
    lw = max(4, int(9*s))
    # twigs behind
    for i in range(9):
        x1 = cx + rnd.uniform(-0.55, 0.55)*w; ang = rnd.uniform(-0.9, 0.9) + (math.pi if x1 < cx else 0)
        ln = rnd.uniform(60, 110)*s; y1 = y0 + rnd.uniform(0.1, 0.4)*h
        d.line([x1, y1, x1 + math.cos(ang)*ln*0.5*(1 if x1>cx else -1)*-1 + (ln*0.6 if x1>cx else -ln*0.6), y1 - abs(math.sin(ang))*ln*0.6], fill=INK, width=lw+6)
        d.line([x1, y1, x1 + math.cos(ang)*ln*0.5*(1 if x1>cx else -1)*-1 + (ln*0.6 if x1>cx else -ln*0.6), y1 - abs(math.sin(ang))*ln*0.6], fill=(122, 82, 48, 255), width=lw)
    # bowl
    d.ellipse([cx-w/2, y0, cx+w/2, y0+h], fill=(150, 101, 58, 255), outline=INK, width=lw)
    d.ellipse([cx-w*0.36, y0+h*0.08, cx+w*0.36, y0+h*0.42], fill=(92, 58, 34, 255), outline=INK, width=max(3, lw//2))
    for i in range(14):   # woven strokes
        yy = y0 + h*rnd.uniform(0.5, 0.85); xx = cx + w*rnd.uniform(-0.4, 0.3)
        d.arc([xx, yy-12*s, xx+w*rnd.uniform(0.12, 0.25), yy+18*s], 200, 340, fill=(96, 62, 36, 255), width=max(3, int(6*s)))
    # two eggs
    for ex in (-0.12, 0.1):
        d.ellipse([cx+w*ex-26*s, y0-14*s, cx+w*ex+26*s, y0+h*0.36], fill=(255, 243, 224, 255), outline=INK, width=max(3, lw//2))

dst, rig = fresh("main_hero_tlama_nest")
UP = 150
H = rig["layers"]["head"]; head = Image.open(f"{dst}/head.png").convert("RGBA")
big = Image.new("RGBA", (head.width, head.height + UP), (0,0,0,0)); big.alpha_composite(head, (0, UP))
hx0, hy0 = H["box"][0], H["box"][1]
cx = rig["head"]["center"][0] - hx0; top = rig["head"]["center"][1] - rig["head"]["diameter"]/2 - hy0 + UP
draw_nest(big, cx, top, 1.0); big.save(f"{dst}/head.png")
x, y, w, h = H["box"]; H["box"] = [x, y-UP, w, h+UP]
for name, F in rig["faces"].items():
    s = F["diameter"] / rig["head"]["diameter"]; up = int(UP*s)
    f = Image.open(f"{dst}/{F['file']}").convert("RGBA")
    big = Image.new("RGBA", (f.width, f.height + up), (0,0,0,0)); big.alpha_composite(f, (0, up))
    draw_nest(big, F["center"][0], F["center"][1] - F["diameter"]/2 + up, s)
    big.save(f"{dst}/{F['file']}")
    F["size"] = [f.width, f.height + up]; F["pivot"][1] += up; F["center"][1] += up
json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)
print("ok")
