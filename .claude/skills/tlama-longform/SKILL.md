---
name: tlama-longform
description: The channel skill for landscape long-form videos (5-8 min, 1920x1080) with Tlama - the same flat 2D doodle characters in a sunlit 3D world as the Shorts, told as one bigger "What if...?" question. Use it whenever the user writes `--clv`, asks for a long video, a landscape / horizontal video, a long-form story, or any step of making one (ideas, script, scene, stills, render, metadata). Shorts (vertical, ~60 s) use `ricksclips-short-style` instead.
---

# Tlama long-form (landscape) videos

A 5-8 minute landscape video (target ~6 min, ~900 words) that answers **one bigger "What if…?" question** with Tlama as the test subject. It is built with the **same engine, library and style as the Shorts**: read `.claude/skills/ricksclips-short-style/SKILL.md` first. Everything there applies (channel rules, no generated voice / music / textures / 3D models, Higgsfield only after confirmation, puppets, props, `set_dressing.py`, dense sets, light as a storyteller, acting, stills check, camera fixes, the video 004 benchmark generator), **except what this file overrides**. When the two disagree, this file wins for long-form videos.

The `--clv` procedure (steps, output templates, final report) is defined in the project `CLAUDE.md`.

## What is different from a Short

| | Short | Long-form (this skill) |
| --- | --- | --- |
| Format | 1080x1920 | **1920x1080**, `"format": "landscape"` in `short.json` |
| Length | ≤ 35 s, 110–130 words | **5-8 min, target ~900 words (~6 min)** |
| Voice | silences removed + sped up at least 1.25x, strictly ≤ 35 s | **silences removed only, no speed-up** (`voice.sh ... 0`) |
| Story | "What if" hook → 3 ladder steps → "But here is the real problem." → finale | **"What if" hook → ladder of 6 steps in 3 acts, cliffhanger after each act, a midpoint turn → "But here is the real problem." → finale back to the hook** |
| Places / side characters | max 3 / max 2 | **max 5 / max 5** |
| Shot length | 1-3 s (~40 shots) | **4-8 s (~50-90 shots)**, slower camera |
| Captions | 1-2 words, centre | **short phrases (3-5 words) at the bottom** (engine default for landscape) |
| CTA | once, ~27 s | **twice: ~30 s and ~30 s before the end**, top of the frame (engine default) |
| Ideas | `idea-scorecard.md` of the Short skill | **`references/idea-scorecard.md` of this skill**, `idea_check.py --longform`, own registry |
| Metadata | YouTube + Instagram + TikTok | **YouTube only**, with chapters |
| Publishing | Buffer (`publish.mjs`) | **the user uploads by hand**; never use `publish.mjs` for long-form |

## Folders

```
longform/LNNN-slug/          LNNN = L + three digits, own numbering (L001, L002, ...)
  work/
    audio/                   voice_original.mp3, voice.mp3, script.txt, words.json
    build.py, short.json     scene generator and the scene
    out.mp4, out_stills/
    custom/                  one-off assets for this video
  video.mp4, script.txt, metadata.md     final files + thumbnail_prompts.md
```

Paths in `short.json` resolve in the video's `work/` first, then in the shared library, exactly as for Shorts. Commands are run from the project root with `V=longform/LNNN-slug/work` and `S=.claude/skills/ricksclips-short-style/scripts/stage`. The relative paths in the Short commands (`../../../.venv/bin/python`, `../../../scripts/voice.sh`) work unchanged, because `longform/LNNN-slug/work` is as deep as `videos/NNN-slug/work`.

## 1. Ideas

Follow `references/idea-scorecard.md` (this skill) exactly: 8-10 silent candidates → `idea_check.py --longform` → gates + points with reasons → critic pass → fix or drop → show only 10/10 ideas (at least 2, at most 3) in the same output format as `--cv`. After the user chooses, register it with `idea_check.py --longform --add <file> LNNN`. Long-form ideas are checked only against long-form videos (own registry `scripts/ideas_used_longform.json`), so a long-form video may develop a topic that was a Short.

## 2. Facts and script

The same rules as the Shorts (project `CLAUDE.md`: "Script – formula", "Facts", "Topic rules", "Clarity", "Strong hooks", "Simple English", "ElevenLabs tags"). **Check every claim before writing** and save claim → source to `longform/LNNN/facts.md`. Changes for long-form:

- **Limits:** max 5 places, max 5 side characters, who only react. Each is introduced once with a fixed label. Every change of place is said out loud.
- **Length:** about **900 words** (range 750-1200), about one ElevenLabs tag per one or two sentences, never tags that slow the voice down. Tags do not count.
- **Structure (word budget for ~900 words):**

| Part | Words | Time (~6 min) | What happens |
| --- | --- | --- | --- |
| Hook + the change | ~60 | 0:00-0:25 | "What if…?" (max 10 words). What exactly changes is clear **within 30 s**. |
| Act 1 | ~200 | → ~1:45 | Ladder steps 1-2 (small). Ends with an **open question** (cliffhanger). |
| Act 2 | ~250 | → ~3:30 | Ladder steps 3-4 (bigger). The **midpoint turn** (~3:00): a real consequence nobody expects, from the same change. Ends with a cliffhanger. |
| Act 3 | ~250 | → ~5:15 | Ladder steps 5-6 (huge). The biggest visual moment of the video. |
| "But here is the real problem." | ~60 | ~5:30 | The deepest consequence, with one simple real reason. |
| Finale | ~80 | → end | The answer to "how does it end?". **The last line leads back to the hook.** |

- **Escalation ladder:** 6 steps (5-7) on one scale (time or size), each visibly bigger. No filler step and no invented step just to reach the length: if there are not 5 honest steps, the idea is too small for long-form.
- **Running gag:** 1-2 side characters with one clear reaction that comes back after the steps (e.g. Mom only says "Not again.").
- **Something new every 4-6 sentences.** No dead minute.
- **Retell test in 5 sentences:** act 1, act 2, act 3, the real problem, the end.

Output and saving as in `--clv` in `CLAUDE.md`: print the tagged script, save it as `longform/LNNN/script_tagged.txt` and without tags as `longform/LNNN/script.txt`, then wait for the user's voice.

## 3. Voice and timing

```bash
cd $V && ../../../scripts/voice.sh audio/voice_original.mp3 audio/voice.mp3 0    # 0 = remove silences only, no speed-up
cd $V && ../../../.venv/bin/python ../../../.claude/skills/ricksclips-short-style/scripts/stage/shortkit.py words audio/voice.mp3 audio/script.txt -o audio/words.json
```

`audio/script.txt` must be without tags. If the processed voice is shorter than 5 min or longer than 8 min, tell the user in the final report (do not stretch or speed it up).

## 4. Scene (`build.py` → `short.json`)

Start from the benchmark generator as for Shorts: copy `scripts/build_call_from_tomorrow.py` to `$V/build.py` (set `sys.path.insert(0, "<absolute path>/scripts")` for `set_dressing`) and run `cd $V && ../../../.venv/bin/python build.py short.json`. Then change these for landscape:

- **Top level:** `"format": "landscape"`, `"audio": {"voice": "audio/voice.mp3", "music": "music/music.mp3", "musicDb": -18}` (the music loops by itself), `"words": "audio/words.json"`, `"end": "audio"`. Leave `captions` and `cta` out: the landscape defaults are the approved ones (phrases at the bottom, CTA twice at the top).
- **Framing.** `headWidth` is a share of the frame **width**, so landscape values are about 0.56x the Short ones: close-up **0.17-0.24**, medium **0.10-0.13**, wide **0.05-0.08** (wide shots still need `pitch` ≥ 4). Landscape has room at the sides: use `frameX` (fraction of the width from the centre; **+ puts the target right of centre**, - left) of about ±0.12-0.2 to place Tlama on a third and show the other character, the absurd object or the place on the other side. Keep `frameY` ≥ 0.12 so faces stay above the captions.
- **Tempo.** One shot per beat, **4-8 s** each (never over 10 s), ~50-90 shots for ~6 min. Shots still start on spoken words (`"w:<index>"`). Because shots are longer, the camera is slower: **`zoom` 2-4** (%/s; 6 s at 6 %/s would push in 40 %), slow `pan`, and some shots pulling out (`zoom` negative). Still: something new in every shot (Short skill, "Keep every scene alive", rule 1), alternate close / medium / wide and the sign of `yaw`.
- **Places.** Up to 5 locations (one per act or turn), each dressed with **120-200 props** as for Shorts (rule 4), 60-80 units apart, `out: "dissolve"` between locations. Landscape frames show more width: put more midground and background at the sides (`line()` boundaries, `ring()` belts), and check the edges of wide shots in the stills.
- **Light.** A mood per act and a lighting key on every turn (midpoint, the real problem, finale). Short red flash on shocks as in 004.
- **Actors.** Up to 5 side characters; the running-gag character gets a reaction shot after every ladder step. Use real moves (`to`, `run`) at least once per act.

## 5. Stills check, render, camera check

```bash
node $S/render.mjs $V/short.json $V/out.mp4 --stills --lib .              # ~3 stills per shot, contact sheet, flags
node $S/render.mjs $V/short.json $V/preview.mp4 --lib . --scale 0.5 --from 0 --to 30   # optional quick preview
node $S/render.mjs $V/short.json $V/out.mp4 --lib . --cool                # full render, ~10 000 frames
.venv/bin/python $S/shortkit.py check $V/out.mp4
```

- Fix every flag before the full render, exactly as for Shorts. Also look at a few stills at full size (captions at the bottom, CTA at the top must not cover a face or the key action).
- The full render with `--cool` takes **several hours** (the user's decision: one piece, with `--cool`). Run it in the background and do not poll it.
- `shortkit.py check` measures against the Short ranges. With the calmer long-form camera the pan speed and zoom will often read **below** those ranges; report the numbers, and flag only a static picture (`static_frames_pct` high) or jerky moves.

## 6. Final files

Into `longform/LNNN-slug/`: `video.mp4` (copy of `out.mp4`), `script.txt` (copy of `audio/script.txt`) and `metadata.md` in English with exactly this structure:

```
# LNNN – Video title

## YouTube
### Title
one title (with emoji, max ~70 characters), no alternatives

### Description
2-4 short sentences that open a loop (no spoilers of the finale), then an empty line, then the chapters, then an empty line, then 3-5 hashtags (no #shorts)

0:00 Chapter name
0:25 Chapter name
...

### Tags
whatif, science, animation   (comma-separated, for pasting into YouTube Studio)
```

**Chapters:** the first one is `0:00`, at least 3, each at least 10 s long (YouTube rules). Use the start of the hook, each act, and "But here is the real problem" as chapter starts, with times from `audio/words.json` (the first word of that part). Chapter names are short and must not give away the finale. They live inside the description, because that is where YouTube reads them.

At the end write thumbnail prompts with the skill `tlama-thumbnail` (1280×720); the user generates the image from them by hand and uploads everything by hand in YouTube Studio. Never render a thumbnail from the stage. Never run `publish.mjs` for a long-form video.
