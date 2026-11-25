# Pirate crew made locally (PIL, no Higgsfield) from existing puppets: bandana / hat / eyepatch on the
# head and every face; each also in a *_shovel variant (shovel in the right hand, upright at armR -60).
#   pirate_elder, pirate_king, pirate_noble, pirate_teacher, pirate_kid   (+ _shovel)
#   pirate_captain            green_feather_noble with an eyepatch
# Run from the project root: .venv/bin/python scripts/pirate_variants.py
import json, os, shutil, math
import numpy as np
from PIL import Image, ImageDraw
ROOT = os.getcwd(); PUP = f"{ROOT}/puppets"
INK = (39, 25, 37, 255)
SS = 3                                                          # supersampling for smooth lines


def fresh(src, name):
    dst = f"{PUP}/{name}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(f"{PUP}/{src}", dst, ignore=shutil.ignore_patterns("source*.png", "emotions*.png", "*preview.png"))
    rig = json.load(open(f"{dst}/rig.json")); rig["name"] = name
    return dst, rig


def overlay(im, fn, pad):
    """grow the canvas by pad px on the top/left/right, draw with fn(draw, ox, oy, s), return the new image"""
    W, H = im.width + 2 * pad, im.height + pad
    ov = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); fn(ImageDraw.Draw(ov), ov)
    ov = ov.resize((W, H), Image.LANCZOS)
    big = Image.new("RGBA", (W, H), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad)); big.alpha_composite(ov)
    return big


def ball(path, mode):
    """circle of the round head: (cx, cy, D) measured from the alpha (widest row = diameter)"""
    a = np.array(Image.open(path).convert("RGBA"))[..., 3] > 128
    top = np.nonzero(a.any(1))[0][0]
    if mode == "top":                                           # bare head, bottom may carry a collar: use the upper part
        pts = []
        h = a.shape[0]
        for y in range(top + 4, top + int(0.42 * h), 3):
            r = np.nonzero(a[y])[0]
            if len(r): pts += [(r[0], y), (r[-1], y)]
        p = np.array(pts, float); A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
        c, *_ = np.linalg.lstsq(A, (p ** 2).sum(1), rcond=None)
        return c[0], c[1], 2 * math.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)


def bandana(d, ov, cx, cy, D, col, low):
    cx, cy, R = cx * SS, cy * SS, D * SS / 2 * 1.05
    lw = int(D * SS * 0.024); yb = cy - low * D * SS
    dy = cy - yb; hx = math.sqrt(max(1, R * R - dy * dy)); a0 = math.degrees(math.atan2(-dy, -hx)) % 360; a1 = math.degrees(math.atan2(-dy, hx)) % 360
    # knot on the right
    kx, ky = cx + hx * 0.98, yb - D * SS * 0.01
    for (ex, ey) in ((0.20, 0.20), (0.26, 0.04)):
        d.polygon([(kx, ky - 0.03 * D * SS), (kx + ex * D * SS, ky + (ey - 0.05) * D * SS), (kx + ex * 0.86 * D * SS, ky + (ey + 0.07) * D * SS), (kx - 0.01 * D * SS, ky + 0.05 * D * SS)], fill=col, outline=INK, width=lw)
    pts = [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in np.linspace(a0, a1, 60)]
    band = [(cx + hx * u, yb + 0.05 * D * SS * (1 - u * u)) for u in np.linspace(1, -1, 40)]
    d.polygon(pts + band, fill=col); 
    for (u, v) in ((-0.5, 0.16), (-0.2, 0.28), (0.12, 0.17), (0.42, 0.26), (0.62, 0.1), (-0.74, 0.07), (0.16, 0.4), (-0.3, 0.08)):
        x, y, r = cx + u * hx, yb - v * D * SS * 0.8, 0.03 * D * SS
        if math.hypot(x - cx, y - cy) < R - 1.8 * r: d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 230, 255))
    d.line(pts + band + [pts[0]], fill=INK, width=lw, joint="curve")


def hat(d, ov, cx, cy, D, col, low):
    cx, cy, D = cx * SS, cy * SS, D * SS; lw = int(D * 0.026); y = cy - low * D
    pts = []
    for u in np.linspace(-1, 1, 60):                            # top line: two horns
        pts.append((cx + u * 0.66 * D, y - D * (0.20 + 0.20 * math.cos(u * math.pi / 2) ** 2 + 0.10 * abs(u) ** 3)))
    bot = [(cx + u * 0.66 * D, y + D * (0.05 - 0.17 * u * u) ) for u in np.linspace(1, -1, 60)]
    d.polygon(pts + bot, fill=col); d.line(pts + bot + [pts[0]], fill=INK, width=lw, joint="curve")
    d.line([(x, yy - 0.05 * D) for x, yy in bot[4:-4]], fill=(245, 196, 60, 255), width=int(0.03 * D), joint="curve")
    sx, sy, r = cx, y - 0.20 * D, 0.085 * D                     # skull
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 246, 230, 255)); d.rounded_rectangle([sx - r * .55, sy + r * .4, sx + r * .55, sy + r * 1.45], radius=r * .2, fill=(255, 246, 230, 255))
    for k in (-1, 1): d.ellipse([sx + k * r * .42 - r * .28, sy - r * .2, sx + k * r * .42 + r * .28, sy + r * .4], fill=INK)


def patch(d, ov, ex, ey, r, strap):
    """black eyepatch with a strap through (ex, ey); strap = two end points"""
    for p in strap: d.line([(ex * SS, ey * SS), (p[0] * SS, p[1] * SS)], fill=INK, width=int(r * SS * 0.3))
    d.ellipse([(ex - r) * SS, (ey - r) * SS, (ex + r) * SS, (ey + r * 1.1) * SS], fill=(39, 25, 37, 255))
    d.arc([(ex - r * .6) * SS, (ey - r * .6) * SS, (ex + r * .6) * SS, (ey + r * .6) * SS], 190, 260, fill=(110, 90, 110, 255), width=int(r * SS * 0.16))


def make(src, name, draw_fn, drop=0.0):
    dst, rig = fresh(src, name); H = rig["layers"]["head"]
    pad = int(rig["head"]["diameter"] * 0.35)
    f = f"{dst}/head.png"; im = Image.open(f).convert("RGBA")
    overlay(im, lambda d, ov: draw_fn(d, ov, f, pad), pad).save(f)
    x, y, w, h = H["box"]; H["box"] = [x - pad, y - pad, w + 2 * pad, h + pad]
    for F in rig["faces"].values():
        f = f"{dst}/{F['file']}"; im = Image.open(f).convert("RGBA"); p = int(F["diameter"] * 0.35)
        overlay(im, lambda d, ov: draw_fn(d, ov, f, p), p).save(f)
        F["size"] = [F["size"][0] + 2 * p, F["size"][1] + p]; F["pivot"] = [F["pivot"][0] + p, F["pivot"][1] + p - drop * F["diameter"]]; F["center"] = [F["center"][0] + p, F["center"][1] + p]
    rig.pop("eyes", None)                                       # no painted blink over an eyepatch
    json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)
    return dst


def shovel_img(L):
    W = int(L * 0.30); im = Image.new("RGBA", (W * SS, L * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = W * SS / 2; w = L * SS * 0.026; lw = int(L * SS * 0.013)
    d.rounded_rectangle([c - w, 8 * SS, c + w, L * SS * 0.72], radius=w, fill=(181, 101, 58, 255), outline=INK, width=lw)
    d.rounded_rectangle([c - w * 4, 4 * SS, c + w * 4, 4 * SS + w * 2.2], radius=w, fill=(181, 101, 58, 255), outline=INK, width=lw)
    b = L * SS * 0.64; e = L * SS * 0.985; hw = W * SS * 0.40
    d.polygon([(c - hw, b), (c + hw, b), (c + hw * .92, b + (e - b) * .6), (c, e), (c - hw * .92, b + (e - b) * .6)], fill=(168, 176, 192, 255))
    d.line([(c - hw, b), (c + hw, b), (c + hw * .92, b + (e - b) * .6), (c, e), (c - hw * .92, b + (e - b) * .6), (c - hw, b)], fill=INK, width=lw, joint="curve")
    d.line([(c - hw * .5, b + (e - b) * .15), (c - hw * .45, b + (e - b) * .55)], fill=(225, 230, 238, 255), width=lw)
    return im.resize((W, L), Image.LANCZOS)


def shovel(src, name, pose=-60, L=640, grip=0.46):
    dst, rig = fresh(src, name); A = rig["layers"]["armR"]; arm = Image.open(f"{dst}/armR.png").convert("RGBA")
    al = np.array(arm)[..., 3] > 40; ys, xs = np.nonzero(al); low = ys > ys.max() - 40; hx, hy = xs[low].mean(), ys[low].mean() - 8
    M = L; big = Image.new("RGBA", (arm.width + 2 * M, arm.height + 2 * M), (0, 0, 0, 0))
    sq = Image.new("RGBA", (2 * L, 2 * L), (0, 0, 0, 0)); s = shovel_img(L); sq.alpha_composite(s, (L - s.width // 2, int(L - grip * L)))
    sq = sq.rotate(pose, resample=Image.BICUBIC)
    big.alpha_composite(sq, (int(M + hx - L), int(M + hy - L)) if M + hx >= L and M + hy >= L else (0, 0)); big.alpha_composite(arm, (M, M))
    big.save(f"{dst}/armR.png"); x, y, w, h = A["box"]; A["box"] = [x - M, y - M, w + 2 * M, h + 2 * M]
    json.dump(rig, open(f"{dst}/rig.json", "w"), indent=1)


if __name__ == "__main__":
    def band(col, low, ep=False):
        def fn(d, ov, f, p):
            cx, cy, D = ball(f, "top"); cx += p; cy += p
            if ep:
                ex, ey = cx - 0.235 * D, cy - 0.06 * D
                patch(d, ov, ex, ey, 0.125 * D, [(cx - 0.47 * D, ey - 0.10 * D), (cx + 0.40 * D, cy - 0.28 * D)])
            bandana(d, ov, cx, cy, D, col, low)
        return fn
    def hatfn(col, low):
        def fn(d, ov, f, p):
            cx, cy, D = ball(f, "top"); hat(d, ov, cx + p, cy + p, D, col, low)
        return fn
    def cap(d, ov, f, p):
        im = Image.open(f); w = im.width
        patch(d, ov, p + 0.325 * w, p + 0.47 * w, 0.082 * w, [(p + 0.20 * w, p + 0.40 * w), (p + 0.66 * w, p + 0.37 * w)])
    RED, BLUE, YEL, GRN, BLK = (214, 60, 66, 255), (62, 116, 190, 255), (240, 176, 56, 255), (70, 150, 96, 255), (58, 48, 66, 255)
    make("maroon_cap_elder_nocap", "pirate_elder", band(RED, 0.27, True))
    make("dwarf_king_nocrown", "pirate_king", hatfn(BLK, 0.30), drop=0.05)
    make("black_hat_noble_nohat", "pirate_noble", band(BLUE, 0.24))
    make("grey_mustache_teacher", "pirate_teacher", band(YEL, 0.27))
    make("yellow_hoodie_kid", "pirate_kid", band(GRN, 0.22), drop=0.06)
    make("green_feather_noble", "pirate_captain", cap)
    for n in ("pirate_elder", "pirate_king", "pirate_noble", "pirate_teacher", "pirate_kid", "pirate_captain"): shovel(n, n + "_shovel")
    print("ok")
