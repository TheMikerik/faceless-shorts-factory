"""Analyze a Suno track for a --cvs video and write work/song.json.

    .venv/bin/python .claude/skills/tlama-song/scripts/analyze_song.py \
        V/work/audio/suno_original.mp3 V/dialogue.txt -o V/work/song.json \
        --trim V/work/audio/voice.mp3

dialogue.txt has one line per spoken line, in order:
    A: Bet you can't say this in Spanish.  (A = English producer)
    B: Sueño.                           (B = Tlama, the target language)
    RAP: El pequeño y risueño ...       (the rapped finale, sung by Tlama)
A language with its own script: latin first, then " | original" (same word count in the RAP line):
    B: Dhahab. | ذهب

What it does:
  1. word timestamps with faster-whisper, matched to the expected words (fuzzy, accents ignored,
     missing words interpolated), so captions and mouths use the real timing;
  2. finds the drop (biggest jump of 30-150 Hz energy around the first rap word) and the tempo;
  3. --trim: HARD CUT right after the first rap chorus (Suno sometimes raps it twice), no fade,
     -14 LUFS. The cut snaps to the quietest moment around the last rap word; --cut sets it by hand.
Times in song.json are valid for both the original and the trimmed file (the cut keeps 0.0).
"""
import argparse, json, re, subprocess, unicodedata
from difflib import SequenceMatcher
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("dialogue")
ap.add_argument("-o", "--out", required=True)
ap.add_argument("--trim", help="write the trimmed, normalized track here")
ap.add_argument("--max", type=float, default=35.0)
ap.add_argument("--cut", type=float, help="hard cut at this second (end of the first rap chorus)")
ap.add_argument("--model", default="small")
a = ap.parse_args()

# ---- expected words ---------------------------------------------------------
lines = []
for raw in open(a.dialogue, encoding="utf-8"):
    m = re.match(r"\s*(A|B|RAP)\s*:\s*(.+)", raw)
    if not m: continue
    text, _, orig = m[2].partition("|")
    lines.append({"who": m[1], "text": text.strip(), **({"orig": orig.strip()} if orig.strip() else {})})
assert lines and lines[-1]["who"] == "RAP", "dialogue.txt must end with a RAP: line"

def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^\w']", "", "".join(c for c in w if not unicodedata.combining(c)))

exp = [(li, w) for li, l in enumerate(lines) for w in l["text"].split()]
exp_n = [norm(w) for _, w in exp]

# ---- audio ------------------------------------------------------------------
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", a.audio, "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
dur_in = len(x) / 16000

from faster_whisper import WhisperModel
model = WhisperModel(a.model, compute_type="int8")
segs, _ = model.transcribe(x, language="en", word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False,
                           initial_prompt=" ".join(l["text"] for l in lines))
got = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
got_n = [norm(w) for w, _, _ in got]

# ---- align ------------------------------------------------------------------
times = [None] * len(exp)
for tag, i1, i2, j1, j2 in SequenceMatcher(None, exp_n, got_n, autojunk=False).get_opcodes():
    if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            times[i1 + k] = got[j1 + k][1:]
    elif tag == "replace":  # unequal block: spread the expected words over the heard span
        s, e = got[j1][1], got[j2 - 1][2]
        for k in range(i2 - i1):
            times[i1 + k] = (s + (e - s) * k / (i2 - i1), s + (e - s) * (k + 1) / (i2 - i1))
missing = [exp[k][1] for k, t in enumerate(times) if t is None]
for k, t in enumerate(times):  # interpolate leftovers between known neighbours
    if t is None:
        p = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), 0.0)
        n = next((times[j][0] for j in range(k + 1, len(times)) if times[j]), p + 0.4)
        times[k] = (p + 0.02, min(p + 0.35, n - 0.02))
for l in lines: l["words"] = []
for (li, w), (s, e) in zip(exp, times):
    lines[li]["words"].append([w, round(s, 2), round(e, 2)])

rap = lines[-1]
# The pass above is forced to English, so the foreign rap can come out as garbage that the
# alignment spreads over a wrong span (019: rap heard 1.3 s late, drop search missed the drop).
# Second pass: only the part after the last English line, language auto-detected.
tail = max(w[2] for l in lines[:-1] for w in l["words"]) + 0.3
# A language with its own script comes back in that script, so match against the original words.
orig = rap.get("orig", "").split()
rwords = orig if len(orig) == len(rap["words"]) else [w for w, _, _ in rap["words"]]
segs, _ = model.transcribe(x[int(tail * 16000):], word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False, initial_prompt=" ".join(rwords))
got2 = [(w.word.strip(), w.start + tail, w.end + tail) for s in segs for w in s.words]
rexp = [norm(w) for w in rwords]
got2 = got2[:len(rexp) + 2]              # only the first chorus, even if Suno repeats it
hit = {}
for blk in SequenceMatcher(None, rexp, [norm(w) for w, _, _ in got2], autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        hit[blk.a + k] = got2[blk.b + k][1:]
if len(hit) >= len(rexp) / 2:
    print(f"rap re-heard in its own language: {len(hit)}/{len(rexp)} words matched")
    for k, w in enumerate(rap["words"]):
        if k in hit:
            w[1], w[2] = round(hit[k][0], 2), round(hit[k][1], 2)
        else:  # between matched neighbours
            p = next((hit[j][1] for j in range(k - 1, -1, -1) if j in hit), tail)
            n = next((hit[j][0] for j in range(k + 1, len(rexp)) if j in hit), p + 0.4)
            w[1], w[2] = round(p + 0.02, 2), round(max(p + 0.05, n - 0.02), 2)
rap_start, rap_end = rap["words"][0][1], rap["words"][-1][2]

# ---- drop and tempo -----------------------------------------------------------
hop, n = 80, 1024  # 200 frames per second
win = np.hanning(n); f = np.fft.rfftfreq(n, 1 / 16000)
S = np.array([np.abs(np.fft.rfft(x[i:i + n] * win)) for i in range(0, len(x) - n, hop)])
low = 20 * np.log10(S[:, (f >= 30) & (f <= 150)].mean(1) + 1e-7)
best, drop = -1e9, rap_start
for i in range(int((rap_start - 1.5) * 200), int((rap_start + 1.5) * 200)):
    if i < 60 or i + 60 > len(low): continue
    jump = low[i:i + 60].mean() - low[i - 60:i].mean()
    if jump > best: best, drop = jump, i / 200
flux = np.maximum(np.diff(np.log1p(S), axis=0), 0).sum(1)
seg = flux[int(drop * 200):int(min(drop + 6, rap_end + 2) * 200)]; seg = seg - seg.mean()
ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
lags = np.arange(int(200 * 60 / 180), int(200 * 60 / 60))
k = lags[np.argmax(ac[lags])]                       # parabolic refine: lag steps are 5 ms
y0, y1, y2 = ac[k - 1], ac[k], ac[k + 1]
bpm = 12000 / (k + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12))
if abs(bpm - round(bpm / 5) * 5) < 2.0: bpm = round(bpm / 5) * 5   # Suno uses round tempos
while bpm < 110: bpm *= 2
while bpm > 180: bpm /= 2

# Whisper often glues the first rap word into the quiet pause before it. The pickup starts
# at most ~0.6 s before the drop, so clamp it there (keeps the mouth and the cut honest).
if rap_start < drop - 0.6:
    rap_start = drop - 0.6
    w0 = rap["words"][0]; w0[1] = round(rap_start, 2); w0[2] = round(max(w0[2], rap_start + 0.15), 2)
if a.cut:
    duration = a.cut
else:                      # quietest voice-band moment around the end of the last rap word
    voice = S[:, (f >= 300) & (f <= 3400)].mean(1)
    i0, i1 = int((rap_end - 0.15 - 0.032) * 200), min(int((rap_end + 0.25 - 0.032) * 200), len(voice))
    duration = (i0 + int(np.argmin(voice[i0:i1]))) / 200 + 0.032
duration = round(min(a.max, duration, dur_in), 2)
last = rap["words"][-1]; last[2] = round(min(last[2], duration), 2); rap_end = last[2]
song = {"duration": duration, "finale": round(rap_start - 0.08, 2), "drop": round(drop, 2),
        "bpm": round(bpm, 1), "drop_strength_db": round(best, 1), "lines": lines}
json.dump(song, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"track {dur_in:.2f}s -> cut {duration}s | finale {song['finale']} | drop {song['drop']} "
      f"(+{best:.0f} dB) | {song['bpm']} BPM")
if missing: print("NOT HEARD (interpolated):", " ".join(missing))
for l in lines:
    print(f"  {l['who']:3} {l['words'][0][1]:6.2f}-{l['words'][-1][2]:6.2f}  {l['text']}")
if best < 8: print("WARNING: weak drop, check the finale stills (maybe Suno made no real drop)")

if a.trim:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.audio, "-t", str(duration), "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=11",                      # hard cut, no fade
                    "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "192k", a.trim], check=True)
    print("trimmed ->", a.trim)
