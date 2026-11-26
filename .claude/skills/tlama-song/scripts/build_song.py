"""Render a --cvs video (dialogue + rap finale) from work/song.json.

    cd V/work && ../../../.venv/bin/python ../../../.claude/skills/tlama-song/scripts/build_song.py --stills
    cd V/work && ../../../.venv/bin/python ../../../.claude/skills/tlama-song/scripts/build_song.py

Reads song.json (from analyze_song.py) and audio/voice.mp3. Images: custom/<name>.png if present,
else puppets/song_duo/<name>.png (A = producer, B = Tlama, F = finale with drums).
Look: plain beige, static frames, hard cuts to whoever speaks, mouth patches pasted from the
variants onto the base image (outlines never jitter), blinks, A gestures on long lines,
B with closed eyes in the pause before the drop, finale: drum pose and camera jump on the beat.
Frame 0 is the thumbnail (the only image in the video folder): IG/TikTok cover.
Output: out.mp4 (h264_videotoolbox, light on the fanless Mac) or out_stills/*.jpg.
"""
import json, os, random, re, subprocess, sys
import numpy as np
from scipy.ndimage import median_filter
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30
INK = (39, 25, 37)                                  # plum black #271925
FONT = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 60, index=2)  # Demi Bold
# Languages with their own script: original on top, latin in brackets below.
UNI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"     # raqm shapes Arabic, Hebrew...
ORIG_FONT = ImageFont.truetype(UNI, 72)
LATIN_FONT = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 46, index=2)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
LIB = os.path.join(ROOT, "puppets/song_duo")

song = json.load(open("song.json", encoding="utf-8"))
DUR = song["duration"]; N = int(DUR * FPS)
FINALE, BEAT0, BEAT = song["finale"], song["drop"], 60 / song["bpm"]
lines = song["lines"]; talk = [l for l in lines if l["who"] != "RAP"]; rap = lines[-1]
if any("඀" <= c <= "෿" for c in rap.get("orig", "")):   # Sinhala: not in Arial Unicode
    ORIG_FONT = ImageFont.truetype("/System/Library/Fonts/Sinhala Sangam MN.ttc", 72, index=1)
    RAP_ORIG_Y = 0.17                                             # 5 rows: clear of the tall hat
else:
    RAP_ORIG_Y = 0.20
def t0(l): return l["words"][0][1]
def t1(l): return l["words"][-1][2]

# ---- audio: 100 analysis frames per second, voice band ------------------------
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "audio/voice.mp3", "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
fr = np.fft.rfftfreq(1024, 1 / 16000); band = (fr >= 300) & (fr <= 3400); win = np.hanning(1024)

# ---- images -----------------------------------------------------------------
def load(name):
    p = f"custom/{name}.png"
    im = Image.open(p if os.path.exists(p) else f"{LIB}/{name}.png").convert("RGB")
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    top = (im.height - H) // 2
    return im.crop((0, top, W, top + H))

def sx(v): return round(v * W / 752)
def sy(v): return round(v * H / 1344)
FACE = {"A": (sx(230), sy(740), sx(520), sy(990)), "B": (sx(220), sy(700), sx(530), sy(1000)),
        "F": (sx(400), sy(760), sx(735), sy(1015))}
IMG, MASK = {}, {}
for g, shapes in (("A", "closed half wide o blink hand"), ("B", "closed half wide o blink"),
                  ("F", "closed half wide o drum")):
    for s in shapes.split():
        IMG[f"{g}_{s}"] = load(f"{g}_{s}")
for g in "ABF":
    base = np.asarray(IMG[f"{g}_closed"].convert("L"), np.int16)
    for s in ("half", "wide", "o", "blink"):
        if f"{g}_{s}" not in IMG: continue
        d = np.zeros(base.shape, bool); x0, y0, x1, y1 = FACE[g]
        d[y0:y1, x0:x1] = np.abs(np.asarray(IMG[f"{g}_{s}"].convert("L"), np.int16) - base)[y0:y1, x0:x1] > 35
        m = Image.fromarray((d * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(25))
        MASK[f"{g}_{s}"] = m.filter(ImageFilter.GaussianBlur(6))

def compose(g, base, face):
    im = IMG[f"{g}_{base}"]
    return im if face == "closed" else Image.composite(IMG[f"{g}_{face}"], im, MASK[f"{g}_{face}"])

# ---- mouths: one opening per syllable, shape from its vowel ------------------
# Loudness alone kept the mouth open through whole words (and followed the drums in the rap).
# Syllable borders snap to dips in the harmonic part of the voice band (drum hits filtered out).
spec = np.array([np.abs(np.fft.rfft(x[i:i + 1024] * win)) for i in range(0, len(x) - 1024, 160)])
hm = median_filter(spec, (17, 1)) ** 2; pm = median_filter(spec, (1, 31)) ** 2
tonal = np.sqrt(np.mean((spec * hm / (hm + pm + 1e-12))[:, band] ** 2, axis=1))
def dip(a, b):                      # time of the quietest moment between a and b
    i0 = max(int((a - 0.032) * 100), 0); i1 = max(int((b - 0.032) * 100), i0 + 1)
    return (i0 + int(np.argmin(tonal[i0:i1]))) / 100 + 0.032 if i0 < len(tonal) else a

ENGLISH = {"ice": "a", "showers": "ae", "their": "e"}   # spelling that fools the vowel count
def vowels(word, english):
    w = re.sub(r"[^\w]", "", word.lower())
    if english:
        if w in ENGLISH: return list(ENGLISH[w])
        if len(w) > 2 and w.endswith("e") and w != "the": w = w[:-1]
    groups = re.findall(r"[aeiouyàâéèêëîïìíóòôöúùûüœ]+", w)
    return [next((v for v in "aàâoóòôöœuúùûüeéèêëiíìîïy" if v in g), "e") for g in groups] or ["e"]
def shape_of(v):
    return "wide" if v in "aàâ" else ("o" if v in "oóòôöœuúùûü" else "half")

def mouth_track(words):
    out, talking = ["closed"] * N, set()
    for text, s, e, english in words:
        syl = vowels(text, english); n = len(syl); step = (e - s) / n
        cuts = [s] + [dip(s + (k - 0.35) * step, s + (k + 0.35) * step) for k in range(1, n)] + [e]
        talking.update(range(int(s * FPS), min(int(e * FPS) + 1, N)))
        for k, v in enumerate(syl):
            f0, f1 = round(cuts[k] * FPS), min(round(cuts[k + 1] * FPS), N)
            m = f1 - f0
            if m <= 0: continue
            seq = ([shape_of(v)] if m == 1 else [shape_of(v), "closed"] if m == 2 else
                   [shape_of(v)] * (m - 1) + ["closed"] if m == 3 else
                   ["half"] + [shape_of(v)] * (m - 3) + ["half", "closed"])
            out[f0:f1] = seq
    return out, talking
MOUTH, TALKING = {}, {}
for g, ls in (("A", [l for l in talk if l["who"] == "A"]), ("B", [l for l in lines if l["who"] != "A"])):
    MOUTH[g], TALKING[g] = mouth_track([(*w, l["who"] == "A") for l in ls for w in l["words"]])
rng = random.Random(len(lines))
def blink_frames():
    b, t = set(), rng.uniform(1.5, 2.5)
    while t < DUR:
        b.update(range(int(t * FPS), int(t * FPS) + 4)); t += rng.uniform(2.2, 3.8)
    return b
BLINK = {"A": blink_frames(), "B": blink_frames()}

# ---- captions: one per word for short lines, phrases of <= 4 words for long ones --
CAPS = []  # (who, start, end, text)
for l in talk:
    ws = l["words"]
    if len(ws) <= 7 and l is not talk[-1]:
        CAPS.append((l["who"], ws[0][1], ws[-1][2], l["text"].rstrip("."))); continue
    chunk = []
    for i, w in enumerate(ws):
        chunk.append(w)
        if len(chunk) == 3 or i == len(ws) - 1:
            CAPS.append((l["who"], chunk[0][1], chunk[-1][2], " ".join(c[0] for c in chunk))); chunk = []
def wrap(text, width=W * 0.8, max_words=4, font=FONT):
    words, out, cur = text.split(), [], []
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for w in words:
        if cur and (len(cur) == max_words or d.textlength(" ".join(cur + [w]), font=font) > width):
            out.append(" ".join(cur)); cur = []
        cur.append(w)
    return out + [" ".join(cur)]
def rows_for(text, orig, max_words):
    if not orig:
        return [(r, FONT) for r in wrap(text, max_words=max_words)]
    return ([(r, ORIG_FONT) for r in wrap(orig.rstrip(".!"), W * 0.86, max_words + 1, ORIG_FONT)] +
            [(r, LATIN_FONT) for r in wrap(f"({text})", W * 0.86, max_words + 1, LATIN_FONT)])
RAP_LINES = rows_for(rap["text"].rstrip(".!"), rap.get("orig"), 4)
ORIG = {t0(l): l["orig"] for l in talk if l.get("orig")}          # short lines, keyed by start

def caption_at(t):
    if t >= FINALE:        # above the costume hats, also in the closest camera
        if rap.get("orig"): return RAP_LINES, RAP_ORIG_Y
        return RAP_LINES, (430 - 74 * len(RAP_LINES) / 2) / H      # bottom edge at y = 430
    for i, (_, s, e, c) in enumerate(CAPS):
        nxt = CAPS[i + 1][1] if i + 1 < len(CAPS) else FINALE
        last = i == len(CAPS) - 1
        if s - 0.05 <= t < (FINALE if last else min(e + 0.5, nxt - 0.05)):
            return rows_for(c, ORIG.get(s), 99), 0.33      # above tall hats
    return None, 0

def draw_caption(im, rows, yc):
    d = ImageDraw.Draw(im)
    hs = [{FONT: 74, ORIG_FONT: 96, LATIN_FONT: 62}[f] for _, f in rows]
    y = yc * H - sum(hs) / 2
    for (r, font), h in zip(rows, hs):
        d.text((W / 2, y), r, font=font, fill=INK, anchor="ma"); y += h

# ---- shots ------------------------------------------------------------------
SHOTS = [("A" if talk[0]["who"] == "A" else "B", 0.0)]
if len(talk) > 1 and t0(talk[1]) - t1(talk[0]) > 1.0:          # silent reaction of the other one
    other = "B" if talk[0]["who"] == "A" else "A"
    SHOTS += [(other, t1(talk[0]) + 0.25), (talk[1]["who"], t0(talk[1]) - 0.25)]
prev = CAPS[0]
for c in CAPS[1:]:
    if c[0] != prev[0]:
        SHOTS.append((c[0], max(prev[2] + 0.08, c[1] - 0.25)))
    prev = c
if FINALE - t1(talk[-1]) > 0.8:
    SHOTS.append(("Bpause", t1(talk[-1]) + 0.12))              # eyes closed, waiting for the drop
SHOTS.append(("F", FINALE)); SHOTS.sort(key=lambda s: s[1])
def shot_at(t):
    cur = SHOTS[0][0]
    for g, s in SHOTS:
        if t >= s: cur = g
    return cur

HAND = []                     # A gestures on long lines (and on a short A line right before one)
for i, l in enumerate(talk):
    if l["who"] != "A" or len(l["words"]) < 6: continue
    s = t0(l) - 0.3
    p = talk[i - 1] if i else None    # "Try this." right before the long line joins the gesture
    if p and p["who"] == "A" and len(p["words"]) <= 3 and t0(l) - t1(p) < 2.0: s = t0(p) - 0.3
    HAND.append((s, t1(l) + 0.4))

beats = [BEAT0 + k * BEAT for k in range(int((DUR - BEAT0) / BEAT) + 1)]
CAMS = [(1.0, 0.5), (1.35, 0.74), (1.0, 0.5), (1.3, 0.28), (1.18, 0.5)]  # (zoom, centre x)
def finale_frame(f, t):
    nb = sum(1 for b in beats if b <= t)
    im = compose("F", "drum" if nb % 2 else "closed", MOUTH["B"][f])
    z, cx = CAMS[(nb // 2) % len(CAMS)] if t >= BEAT0 else CAMS[0]
    if z == 1.0: return im
    w, h = W / z, H / z; x0 = min(max(cx * W - w / 2, 0), W - w)
    return im.crop((round(x0), round(H - h), round(x0 + w), H)).resize((W, H), Image.LANCZOS)

def frame(f):
    t = f / FPS; g = shot_at(t)
    if g == "F": im = finale_frame(f, t)
    elif g == "Bpause": im = IMG["B_blink"]
    else:
        face = MOUTH[g][f]
        if face == "closed" and f in BLINK[g] and f not in TALKING[g]: face = "blink"
        base = "hand" if g == "A" and any(s <= t < e for s, e in HAND) else "closed"
        im = compose(g, base, face)
    im = im.copy(); rows, yc = caption_at(t)
    if rows: draw_caption(im, rows, yc)
    return im

def thumbnail():             # the user's cover image: the only picture in the video folder
    found = [f for f in sorted(os.listdir("..")) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    if len(found) != 1:
        sys.exit(f"Need exactly one thumbnail image in the video folder, found: {found or 'none'}")
    im = Image.open(f"../{found[0]}").convert("RGB")
    h = round(im.height * 1140 / im.width)
    if h >= H:
        return ImageOps.fit(im, (W, H), Image.LANCZOS)
    # wider than 9:16 (generators often give 2:3): crop the sides only a little, so the text
    # survives, keep the bottom edge, and stretch the top pixel row over the missing height
    im = im.resize((1140, h), Image.LANCZOS).crop((30, 0, 1110, h))
    out = Image.new("RGB", (W, H))
    out.paste(im.crop((0, 0, W, 1)).resize((W, H - h)), (0, 0)); out.paste(im, (0, H - h))
    return out

if __name__ == "__main__":
    if "--stills" in sys.argv:
        os.makedirs("out_stills", exist_ok=True)
        ts = [0.3] + [(s + e) / 2 for _, s, e, _ in CAPS] + [(t1(talk[-1]) + FINALE) / 2, FINALE + 0.1] \
             + [b + 0.05 for b in beats[1::2]][:6]
        try:
            thumbnail().save("out_stills/thumbnail_frame0.jpg", quality=88)
        except SystemExit as e:
            print("NOTE:", e)
        for t in ts:
            frame(min(int(t * FPS), N - 1)).save(f"out_stills/{t:05.2f}.jpg", quality=88)
        print("shots:", [(g, round(s, 2)) for g, s in SHOTS])
        print("stills:", len(ts), "-> out_stills/"); sys.exit()
    # --no-cover: only for re-rendering an old video that never had a thumbnail
    cover = frame(0) if "--no-cover" in sys.argv else thumbnail()   # fails before ffmpeg starts
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "audio/voice.mp3",
                          "-c:v", "h264_videotoolbox", "-b:v", "8M", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          "out.mp4"], stdin=subprocess.PIPE)
    for f in range(N):
        p.stdin.write((cover if f == 0 else frame(f)).tobytes())   # frame 0 only, audio unchanged
    p.stdin.close(); p.wait(); print(f"done out.mp4 ({N} frames, {DUR}s)")
