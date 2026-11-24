#!/usr/bin/env python3
"""Mechanical checks for story ideas (the judgment part is in
.claude/skills/ricksclips-short-style/references/idea-scorecard.md).

  idea_check.py candidates.json          check candidates, exit 1 if any FAIL
  idea_check.py --add candidate.json NNN register the chosen idea as used

candidates.json = list of {title, hook, rule, twist, mechanics:[tags],
                           puppets:[folder names], places:[...], side_characters:[...]}

Long-form (landscape) videos: add --longform to either form. It uses its own registry
(scripts/ideas_used_longform.json + longform/*/script.txt), allows 5 places and 5 side
characters, and each candidate also needs ladder:[5-7 escalation steps] and midpoint. The judgment part is in
.claude/skills/tlama-longform/references/idea-scorecard.md.
  idea_check.py --longform candidates.json
  idea_check.py --longform --add candidate.json L001
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USED = ROOT / "scripts" / "ideas_used.json"
LONG = False                     # set by --longform: own registry, own folder, own limits

STOP = set("""a an the i me my mine we our you your he she it its they them their is am are was
were be been to of in on at by for with and or but so if then than that this these those
there here now today one two three every all no not do does did have has had can will just
from up down out into over very what who how why when where only""".split())
INTROS = ("once upon", "hey", "today i will", "this is the story", "let me tell", "did you know")
HARD = set("""consequently purchase enormous gigantic suddenly immediately approximately however
therefore although nevertheless mysterious mysteriously extraordinary terrified""".split())


def words(text):
    return re.findall(r"[a-z']+", text.lower())


def content(text):
    return {w for w in words(text) if w not in STOP and len(w) > 2}


def jaccard(a, b):
    return len(a & b) / max(1, len(a | b))


def past_items():
    items = json.loads(USED.read_text()) if USED.exists() else []
    seen = {i["video"] for i in items}
    for f in sorted(ROOT.glob(("longform" if LONG else "videos") + "/*/script.txt")):
        num = f.parent.name.split("-")[0]
        if num in seen:
            continue
        first = " ".join(re.split(r"(?<=[.!?])\s+", f.read_text().strip())[:2])
        items.append({"video": num, "title": f.parent.name, "hook": first, "rule": "", "mechanics": []})
    return items


def check(c, past):
    fails, warns = [], []
    hook = c.get("hook", "")
    n = len(words(hook))
    if n > 15:
        fails.append(f"hook has {n} words (max 15)")
    if hook.lower().startswith(INTROS):
        fails.append("hook starts with an intro")
    if not re.search(r"\b(i|me|my)\b", hook.lower()):
        fails.append("hook is not first person (Tlama)")
    if not re.search(r"\d|\b(one|two|three|ten|hundred|thousand|million|every|all|first|last|minutes?|hours?|days?|seconds?|night|morning|today|tonight|breakfast|lunch|dinner|yesterday|tomorrow)\b", hook.lower()):
        warns.append("hook has no number/time/scale word (concrete + clock)")
    for field in ("hook", "rule", "twist"):
        hard = [w for w in words(c.get(field, "")) if w in HARD or len(w) > 11]
        if hard:
            warns.append(f"{field}: hard words {sorted(set(hard))}")
    limit = 5 if LONG else 3
    if len(c.get("places", [])) > limit:
        fails.append(f"more than {limit} places")
    if len(c.get("side_characters", [])) > limit:
        fails.append(f"more than {limit} side characters")
    if LONG:
        n = len(c.get("ladder", []))
        if not 5 <= n <= 7:
            fails.append(f"ladder has {n} steps (need 5 to 7)")
        if not str(c.get("midpoint", "")).strip():
            fails.append("no midpoint turn")
    for p in c.get("puppets", []):
        if not (ROOT / "puppets" / p).is_dir():
            fails.append(f"puppet '{p}' not in puppets/ (would need Higgsfield)")
    mine = set(c.get("mechanics", []))
    if not mine:
        fails.append("no mechanics tags given (needed for the novelty check)")
    text = content(hook + " " + c.get("rule", ""))
    for p in past:
        same = mine & set(p.get("mechanics", []))
        if same:
            fails.append(f"same mechanic as {p['video']} {p['title']}: {sorted(same)}")
        sim = jaccard(text, content(p["hook"] + " " + p.get("rule", "")))
        if sim >= 0.2:
            fails.append(f"too close to {p['video']} {p['title']} (word overlap {sim:.2f})")
    return fails, warns


def main(argv):
    global LONG, USED
    if "--longform" in argv:
        argv = [a for a in argv if a != "--longform"]
        LONG, USED = True, ROOT / "scripts" / "ideas_used_longform.json"
    if len(argv) == 3 and argv[0] == "--add":
        c = json.loads(Path(argv[1]).read_text())
        c = c[0] if isinstance(c, list) else c
        items = json.loads(USED.read_text()) if USED.exists() else []
        item = {"video": argv[2], "title": c["title"], "hook": c["hook"],
                "rule": c["rule"], "mechanics": c.get("mechanics", [])}
        if LONG:
            item.update(ladder=c.get("ladder", []), midpoint=c.get("midpoint", ""))
        items.append(item)
        USED.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
        print(f"registered {argv[2]} {c['title']}")
        return 0
    if len(argv) != 1:
        print(__doc__)
        return 2
    cands = json.loads(Path(argv[0]).read_text())
    past = past_items()
    bad = 0
    for c in cands:
        fails, warns = check(c, past)
        bad += bool(fails)
        print(f"{'FAIL' if fails else 'PASS'}  {c.get('title', '?')}")
        for f in fails:
            print(f"   x {f}")
        for w in warns:
            print(f"   ! {w}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
