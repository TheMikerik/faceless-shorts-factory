# Draws the doodle skeletons (local, no Higgsfield) and Tlama with a sleeping / hungry face into puppets/.
#   .venv/bin/python scripts/skeleton_puppets.py
# puppets/skeleton            round skull, ribs, bone limbs
# puppets/skeleton_old        the same with a striped nightcap and a grey beard (the "old skeleton")
# puppets/main_hero_tlama_sleep   main_hero_tlama + extra faces "sleep" and "hungry" (drool)
# Faces: neutral, happy, nervous, shocked, shouting, confused, sleep, hungry
import json, math, os, shutil
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = (39, 25, 37, 255); BONE = (250, 243, 222, 255); SHADE = (219, 203, 200, 255); DARK = (58, 38, 66, 255); SS = 3
W, TOP, H0 = 560, 200, 1000            # canvas; TOP = room for the nightcap
def canvas(w=W, h=TOP + H0):
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def S(p): return [(x * SS, (y + TOP) * SS) for x, y in p]
def ell(d, cx, cy, rx, ry, fill, lw=0):
    if lw: d.ellipse([(cx - rx - lw / 2) * SS, (cy - ry - lw / 2 + TOP) * SS, (cx + rx + lw / 2) * SS, (cy + ry + lw / 2 + TOP) * SS], fill=INK); rx -= lw / 2; ry -= lw / 2
    d.ellipse([(cx - rx) * SS, (cy - ry + TOP) * SS, (cx + rx) * SS, (cy + ry + TOP) * SS], fill=fill)
def rr(d, x0, y0, x1, y1, r, fill, lw=0):
    if lw: d.rounded_rectangle([(x0 - lw / 2) * SS, (y0 - lw / 2 + TOP) * SS, (x1 + lw / 2) * SS, (y1 + lw / 2 + TOP) * SS], radius=(r + lw / 2) * SS, fill=INK); x0 += lw / 2; y0 += lw / 2; x1 -= lw / 2; y1 -= lw / 2
    d.rounded_rectangle([x0 * SS, (y0 + TOP) * SS, x1 * SS, (y1 + TOP) * SS], radius=max(1, r) * SS, fill=fill)
def stroke(d, pts, w, fill):
    d.line(S(pts), fill=fill, width=int(w * SS), joint="curve")
    for x, y in (pts[0], pts[-1]): ell(d, x, y, w / 2, w / 2, fill)
def poly(d, pts, fill, lw=12):
    d.polygon(S(pts), fill=fill); stroke(d, pts + [pts[0], pts[1]], lw, INK)
def down(im): return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
def bone(d, pts, w=30, knobs=(1, 1), kr=21):
    for lw, col in ((13, INK), (0, BONE)):
        stroke(d, pts, w + lw - (0 if lw else 0), col)
        for (x, y), on in ((pts[0], knobs[0]), (pts[-1], knobs[1])):
            if on: ell(d, x, y, kr + lw / 2, kr + lw / 2, col)
CX = 280
def skull(face, old):
    im, d = canvas()
    # jaw + cranium (one silhouette)
    jaw = {"shouting": 40, "shocked": 34, "hungry": 46}.get(face, 0)
    for lw, col in ((13, INK), (-13, BONE)):
        ell(d, CX, 238, 238 + lw / 2, 226 + lw / 2, col); rr(d, CX - 132 - lw / 2, 360 - lw / 2, CX + 132 + lw / 2, 500 + jaw * .35 + lw / 2, 52, col)
    # shade on the left
    mask = im.split()[3]; sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); ell(sd, CX, 238, 226, 214, SHADE); ell(sd, CX + 38, 232, 218, 214, (0, 0, 0, 0)); im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    def socket(x, y, rx, ry): ell(d, x, y, rx, ry, DARK)
    ex, ey = 96, 232
    if face == "sleep":
        for s in (-1, 1):
            x = CX + s * ex; stroke(d, [(x + 56 * math.cos(t), ey - 6 + 40 * math.sin(t)) for t in [math.pi * i / 14 for i in range(15)]], 17, INK)
    else:
        rx, ry, pr = {"shocked": (74, 82, 13), "shouting": (64, 54, 15), "nervous": (60, 60, 13), "hungry": (72, 74, 24)}.get(face, (64, 66, 18))
        for s in (-1, 1):
            x = CX + s * ex; r2 = ry * (.62 if face == "confused" and s < 0 else 1); socket(x, ey, rx, r2)
            dx = {"nervous": -20, "confused": 18}.get(face, 0); ell(d, x + dx, ey + (4 if face != "hungry" else 2), pr, pr, (255, 250, 235, 255))
        if face == "shouting":
            for s in (-1, 1): stroke(d, [(CX + s * 168, 142), (CX + s * 40, 196)], 24, INK)
        elif face in ("nervous",):
            for s in (-1, 1): stroke(d, [(CX + s * 160, 168), (CX + s * 56, 132)], 19, INK)
        elif face == "confused":
            stroke(d, [(CX - 166, 168), (CX - 46, 172)], 20, INK); stroke(d, [(CX + 46, 128), (CX + 100, 104), (CX + 160, 128)], 20, INK)
        elif face in ("happy", "hungry", "shocked"):
            for s in (-1, 1): stroke(d, [(CX + s * 48, 136), (CX + s * 100, 112), (CX + s * 156, 134)], 19, INK)
    # nose
    for s in (-1, 1): d.polygon(S([(CX + s * 3, 296), (CX + s * 27, 340), (CX + s * 4, 336)]), fill=DARK)
    # mouth
    def teeth(y0, y1, x0, x1, n):
        rr(d, x0, y0, x1, y1, 20, (255, 255, 250, 255), 11)
        for i in range(1, n): x = x0 + (x1 - x0) * i / n; stroke(d, [(x, y0 + 4), (x, y1 - 4)], 8, INK)
        stroke(d, [(x0 + 6, (y0 + y1) / 2), (x1 - 6, (y0 + y1) / 2)], 8, INK)
    if face in ("shouting", "shocked", "hungry"):
        my, ry = 432, {"shouting": 66, "shocked": 56, "hungry": 72}[face]; rx = {"shouting": 108, "shocked": 62, "hungry": 112}[face]
        ell(d, CX, my, rx, ry, (74, 34, 78, 255), 12)
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse([(CX - rx + 7) * SS, (my - ry + 7 + TOP) * SS, (CX + rx - 7) * SS, (my + ry - 7 + TOP) * SS], fill=255)
        ly = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(ly); ell(ld, CX, my + ry, rx * .72, ry * .7, (236, 110, 130, 255))
        ld.rectangle([(CX - rx) * SS, (my - ry + TOP) * SS, (CX + rx) * SS, (my - ry * .52 + TOP) * SS], fill=(255, 255, 250, 255))
        for i in range(-2, 3): ld.line(S([(CX + i * rx * .42, my - ry), (CX + i * rx * .42, my - ry * .52)]), fill=INK, width=8 * SS)
        ld.line(S([(CX - rx, my - ry * .52), (CX + rx, my - ry * .52)]), fill=INK, width=8 * SS); im.paste(ly, (0, 0), Image.composite(ly.split()[3], Image.new("L", im.size, 0), m)); d = ImageDraw.Draw(im)
        if face == "hungry":
            for x, l in ((CX - 70, 64), (CX + 84, 44)):
                stroke(d, [(x, my + 30), (x, my + 30 + l)], 34, INK); stroke(d, [(x, my + 30), (x, my + 30 + l)], 18, (126, 204, 244, 255))
    elif face in ("nervous", "confused"):
        stroke(d, [(CX - 92 + i * 23, 424 + (13 if i % 2 else -13)) for i in range(9)], 14, INK)
    elif face == "sleep":
        stroke(d, [(CX - 70, 420), (CX - 20, 436), (CX + 30, 436), (CX + 74, 418)], 14, INK); ell(d, CX + 60, 470, 24, 24, (170, 222, 250, 255), 9)
    else: teeth(380, 462, CX - 106, CX + 106, 5)
    if face == "nervous":
        poly(d, [(60, 190), (30, 250), (46, 280), (74, 280), (90, 250)], (126, 204, 244, 255), 11)
    if old:
        # beard (grey) around the jaw
        b = [(CX - 160, 372), (CX - 178, 440), (CX - 148, 470), (CX - 150, 520), (CX - 104, 516), (CX - 92, 572), (CX - 44, 540), (CX, 606), (CX + 44, 540), (CX + 92, 572), (CX + 104, 516), (CX + 150, 520), (CX + 148, 470), (CX + 178, 440), (CX + 160, 372), (CX + 128, 420), (CX + 112, 470), (CX + 60, 498), (CX, 506), (CX - 60, 498), (CX - 112, 470), (CX - 128, 420)]
        if face in ("shouting", "hungry", "shocked"): b = [(x, y + (14 if y > 460 else 0)) for x, y in b]
        poly(d, b, (176, 170, 190, 255), 13)
        # nightcap
        cap = [(CX - 226, 150), (CX - 190, 40), (CX - 90, -50), (CX + 40, -96), (CX + 150, -104), (CX + 232, -60), (CX + 252, 40), (CX + 226, 60), (CX + 196, 0), (CX + 150, -10), (CX + 190, 60), (CX + 226, 150)]
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(S(cap), fill=255); lay = Image.new("RGBA", im.size, (86, 108, 200, 255)); ld = ImageDraw.Draw(lay)
        for i in range(-6, 8): ld.line(S([(i * 110 - 80, 200), (i * 110 + 120, -150)]), fill=(244, 238, 250, 255), width=40 * SS)
        im.paste(lay, (0, 0), m); d = ImageDraw.Draw(im); stroke(d, cap + [cap[0], cap[1]], 13, INK)
        rr(d, CX - 246, 116, CX + 246, 178, 30, (250, 246, 252, 255), 13); ell(d, CX + 214, 66, 42, 42, (255, 214, 92, 255), 13)
    return down(im)
def part(fn):
    im, d = canvas(); fn(d); return down(im)
def body(d):
    rr(d, 172, 520, 388, 790, 78, DARK, 13)
    for lw, col in ((11, INK), (0, BONE)): stroke(d, [(CX, 500), (CX, 800)], 30 + lw, col)
    for k, (y, w) in enumerate(((566, 92), (622, 100), (678, 88))):
        for s in (-1, 1):
            pts = [(CX + s * 14, y - 8), (CX + s * w * .6, y - 14), (CX + s * w, y + 12), (CX + s * w * .86, y + 22)]
            stroke(d, pts, 38, INK); stroke(d, pts, 25, BONE)
        stroke(d, [(CX, y - 12), (CX, y + 4)], 28, BONE)
    rr(d, 190, 744, 370, 820, 36, BONE, 13)
    for s in (-1, 1): ell(d, CX + s * 46, 782, 19, 15, DARK)
def legs(s):
    def f(d):
        x = CX + s * 64; bone(d, [(x, 818), (x + s * 4, 950)], 24, (0, 0)); ell(d, x + s * 3, 884, 17, 17, BONE, 9)
        for lw, col in ((12, INK), (0, BONE)): stroke(d, [(x + s * 2, 966), (x + s * 46, 970)], 32 + lw, col)
    return f
def arm(s):
    def f(d):
        bone(d, [(CX + s * 108, 560), (CX + s * 156, 650), (CX + s * 172, 752)], 24, (1, 0), 16)
        x, y = CX + s * 174, 766; ell(d, x, y, 27, 27, BONE, 12)
        for a in (-38, 0, 38):
            t = math.radians(90 + a); stroke(d, [(x, y), (x + 40 * math.cos(t), y + 40 * math.sin(t))], 23, INK)
        for a in (-38, 0, 38):
            t = math.radians(90 + a); stroke(d, [(x, y), (x + 40 * math.cos(t), y + 40 * math.sin(t))], 11, BONE)
    return f
FACES = ["neutral", "happy", "nervous", "shocked", "shouting", "confused", "sleep", "hungry"]
def build(name, old):
    out = f"{ROOT}/puppets/{name}"; os.makedirs(out + "/faces", exist_ok=True)
    layers = {}
    for n, im, piv in (("body", part(body), (CX, 806)), ("legL", part(legs(-1)), (CX - 64, 818)), ("legR", part(legs(1)), (CX + 64, 818)), ("armL", part(arm(-1)), (CX - 108, 560)), ("armR", part(arm(1)), (CX + 108, 560))):
        bb = im.getbbox(); im.crop(bb).save(f"{out}/{n}.png"); layers[n] = {"file": n + ".png", "box": [bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]], "pivot": [piv[0], piv[1] + TOP]}
    faces = {}; neck = (CX, 500 + TOP)
    for f in FACES:
        im = skull(f, old); bb = (0, 0, W, 640 + TOP); c = im.crop(bb); c.save(f"{out}/faces/{f}.png")
        faces[f] = {"file": f"faces/{f}.png", "size": list(c.size), "pivot": list(neck), "center": [CX, 250 + TOP], "diameter": 480.0}
        if f == "neutral": c.save(f"{out}/head.png"); layers["head"] = {"file": "head.png", "box": [0, 0, c.width, c.height], "pivot": list(neck)}
    json.dump({"version": 2, "name": name, "size": [W, TOP + H0], "feetY": 988 + TOP, "head": {"center": [CX, 250 + TOP], "diameter": 480.0}, "skin": "#faf3de", "layers": layers, "order": ["legL", "legR", "armL", "armR", "body", "head"], "faces": faces}, open(f"{out}/rig.json", "w"), indent=1)
def tlama_sleep():
    src, dst = f"{ROOT}/puppets/main_hero_tlama", f"{ROOT}/puppets/main_hero_tlama_sleep"
    shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst, ignore=shutil.ignore_patterns("source*", "emotions*", "*preview*")); r = json.load(open(dst + "/rig.json"))
    im = Image.open(f"{src}/faces/neutral.png").convert("RGBA"); im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS); d = ImageDraw.Draw(im); pink = im.getpixel((210 * 3, 130 * 3))
    k = 3 * 417 / 420
    for x, y in ((158, 181), (297, 176)):
        d.ellipse([(x - 22) * k, (y - 24) * k, (x + 22) * k, (y + 24) * k], fill=pink)
        pts = [((x + 30 * math.cos(t)) * k, (y - 10 + 22 * math.sin(t)) * k) for t in [math.pi * i / 16 for i in range(17)]]; d.line(pts, fill=INK, width=int(11 * k), joint="curve")
        for p in (pts[0], pts[-1]): d.ellipse([p[0] - 5.5 * k, p[1] - 5.5 * k, p[0] + 5.5 * k, p[1] + 5.5 * k], fill=INK)
    im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(dst + "/faces/sleep.png"); r["faces"]["sleep"] = {**r["faces"]["neutral"], "file": "faces/sleep.png"}
    im = Image.open(f"{src}/faces/shouting.png").convert("RGBA"); im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS); d = ImageDraw.Draw(im)
    for x, y0, l in ((122, 350, 46), (300, 352, 30)):
        for w, c in ((26, INK), (14, (126, 204, 244, 255))):
            d.line([(x * 3, y0 * 3), (x * 3, (y0 + l) * 3)], fill=c, width=w * 3)
            for y in (y0, y0 + l): d.ellipse([(x - w / 2) * 3, (y - w / 2) * 3, (x + w / 2) * 3, (y + w / 2) * 3], fill=c)
    im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(dst + "/faces/hungry.png"); r["faces"]["hungry"] = {**r["faces"]["shouting"], "file": "faces/hungry.png"}
    r["name"] = "main_hero_tlama_sleep"; json.dump(r, open(dst + "/rig.json", "w"), indent=1)
if __name__ == "__main__":
    build("skeleton", False); build("skeleton_old", True); tlama_sleep(); print("ok")
