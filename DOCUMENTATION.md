# TlamaLabs – project documentation

How the project works and why it is built this way. The README gives commands and setup. This file records the idea, the goals and the decisions behind it. `CLAUDE.md` holds the binding rules for Claude, and this file explains them.

> **Keep this file current.** Update it in the same change whenever the workflow, a tool, a folder or a rule changes, then add a line to the changelog at the bottom.

---

## 1. Idea

A faceless YouTube Shorts channel, [@TlamaLabs](https://www.youtube.com/@TlamaLabs). Every video is a ~60 s **invented, absurd story that never happened**, told in first person by the same hero, **Tlama** (a pink head with a huge mouth, yellow goggles and a white coat).

- **Story shape:** strong hook → escalation (rule of three) → the pivot "You see…" → a twist that lands back on the hook, so the Short loops.
- **Look:** flat 2D doodle cutouts standing in a sunlit 3D world. The style is inspired by @RicksClips3000 (but never copies it). Everything is built and rendered in code.
- **Voice:** recorded by the author in ElevenLabs. Claude writes the tagged script and never generates the voice.

Next to the daily Shorts the channel also makes **landscape long-form videos** (5–8 min, target ~6 min, 3× a week): one longer absurd story with Tlama in the same style, built with the same engine and library. See "Long-form videos" below.

The channel used to post Roblox content. That direction has been dropped completely.

## 2. Goals

| Goal | What it means in practice |
| --- | --- |
| **Monetization (YPP)** | Original content only, no real people, facts or brands, no music copyright problems, nothing that could count as reused content, and safe for kids |
| **Retention** | Viewers must stay to the end and ideally replay. This drives the story formula, the 10/10 idea gate, the shot every 1–3 s and the looping last line |
| **Global reach** | English at A2–B1 level, so non-native speakers and kids understand every sentence. English also brings a higher RPM |
| **One video per day** | Production has to be fast and repeatable. The library is built once and each new video only adds its own folder |
| **Long-form 3× a week** | Longer watch time per viewer and a second shelf on the channel, reusing the whole Shorts library and engine |

## 3. Workflow overview

```
--cv ──► videos/NNN/ (empty, reserves the number)
     ──► idea gate: 8–10 hidden candidates → idea_check.py → scorecard → critic → show ≥2 ideas at 10/10
     ──► user picks ──► tagged script (ElevenLabs) ──► WAIT for the user's .mp3
     ──► rename to NNN-slug ──► voice.sh ──► words.json (Whisper) ──► build.py → short.json
     ──► render --stills (auto-fix until clean) ──► full render ──► shortkit check
     ──► video.mp4 + script.txt + metadata.md ──► publish --dry ──► report
     ──► (only on the user's command) publish.mjs NNN → R2 + Buffer
```

The full step-by-step rules are in `CLAUDE.md` (shortcut `--cv`) and in the skill `.claude/skills/ricksclips-short-style/SKILL.md`.

## 4. Story system

### Formula and clarity rules
The **situation** is absurd and the **storytelling** is simple. Each story has one magic rule, Tlama has one goal, escalation repeats one pattern three times, there are at most 3 places and 3 side characters, time only moves forward, and every sentence can be drawn. All of this is in `CLAUDE.md` ("Script – formula", "Clarity", "Strong hooks").

### Idea gate (10/10)
**Why:** a self-rating that is only a feeling inflates. The gate turns "10/10" into "passes a fixed checklist, with written reasons and a critic pass".

- `.claude/skills/ricksclips-short-style/references/idea-scorecard.md`: the procedure, 8 hard gates, 10 points and a calibration table.
- `scripts/idea_check.py`: the mechanical checks (hook length, first person, no intro, puppets exist, hard words, novelty against past videos by mechanic tag and word overlap).
- `scripts/ideas_used.json`: a registry of past videos (hook, rule, mechanic tags). The chosen idea is added with `idea_check.py --add`.
- The user only sees ideas that reach 10/10, at least two of them.
- **Calibration:** 7 days after publishing, the video's views and average % viewed go into the scorecard table. The card changes if 10/10 ideas do not outperform the rest.

### Voice script
ElevenLabs audio tags are used, about 1 per 1–2 sentences. Tags that lengthen the audio (`[pause]`, `[sighs]`…) are not used, because the track gets trimmed and sped up anyway. `script.txt` is kept free of tags so the word alignment works.

## 5. Technical architecture

| Part | Tool | Role |
| --- | --- | --- |
| Stage | three.js (`stage.js`, `index.html`) in headless Chromium via Playwright | draws the 3D world, the 2D puppets, real shadows, the camera and the captions |
| Renderer | `render.mjs` | resolves the timeline (word-indexed shots), pulls frames, pipes them to ffmpeg with the voice and music. `--stills` checks before the full render |
| Scene | `build.py` per video (a copy of `scripts/build_call_from_tomorrow.py`) | generates `short.json`: actors, ~40 shots, locations, light keys |
| Set dressing | `scripts/set_dressing.py` | `scatter` / `line` / `ring` / `clear_zone` fill a location with 120–200 props in a few lines |
| Puppets | `puppet.py` (slice + rig), `scripts/puppet_variants.py`, `scripts/crown_coin_variants.py` | cutout layers with a rig and swappable faces. Variants (phone, nest, coin, crown, king without crown, cat with crown) and prop puppets (crown, coin) are made locally with PIL from existing puppets |
| Props | `props/<pack>/*.glb` + `props/catalog.json` + previews (`scripts/props_catalog.py`) | ready-made CC0 models (Kenney packs) mixed with stage primitives |
| Voice | `scripts/voice.sh` (ffmpeg) | removes silences and speeds up the track to ≤ 60 s without changing the pitch; `scripts/voice.sh raw out 0` = remove silences only, no speed-up (long-form) |
| Timing | `shortkit.py words` with faster-whisper in `.venv` | `words.json` drives the captions and the cuts |
| Picture quality | `stage.js` (`makeFx`, `makePost`, `CURVES`) | on by default in every video: ambient occlusion on the set, depth of field focused on the shot target (character silhouettes go into the depth buffer), fog, bloom, warm/cool grade, vignette, grain, faint colour fringe; poses ease with a small overshoot, hops squash and stretch, faces pop. Tunable or off via `ao`, `fog`, `post`, `shadowSoftness` and an action's `curve` |
| Like & subscribe | `render.mjs` (`_cta`) + `stage.js` (`drawCta`) | ONE automatic on-screen graphic (thumbs-up + bell + "LIKE & SUBSCRIBE", no voice) at ~27 s for 2.5 s, snapped to the nearest sentence start in `words.json` (±3 s) so it never covers a punchline. On by default in every video; change with `"cta": {"at": 30}`, disable with `"cta": false` |
| QA | `render.mjs --stills`, `shortkit.py check` | catches mechanical errors and checks camera speed and zoom against the measured style numbers (`references/rules.json`) |
| Publishing | `scripts/publish/publish.mjs` | uploads `video.mp4` to Cloudflare R2 and queues it through the Buffer API on YouTube, Instagram and TikTok |

### Folder model
- **Shared archive** (root: `puppets/`, `props/`, `bg/`, `music/`, `scripts/`): reusable and **add-only**. Changing an existing asset could break other videos.
- **Per-video folder** `videos/NNN-slug/`: everything specific to that video lives in `work/`, and the final files sit next to it. Any video can be deleted on its own, and several can be produced in parallel.
- Paths in `short.json` are resolved in the video's `work/` first, then in the archive (`--lib .`).

## 6. Key decisions and why

| Decision | Why |
| --- | --- |
| Faceless, one recurring hero | builds recognition and needs no camera. Tlama is in every video |
| Invented stories only | nothing to fact-check, no risk of misinformation or real-person issues, safer for YPP |
| Simple English | a global audience and kids. Retention drops as soon as a viewer gets lost |
| Voice recorded by the author | control over the performance and a human voice. Claude never generates audio |
| Scenes built in code (three.js), not AI video | repeatable, cheap, consistent style, fully automatable for a daily cadence |
| Higgsfield only for new characters or backgrounds, after confirmation | it costs credits and adds style drift. The library covers most stories |
| No generated music, textures or 3D models | copyright safety and consistency. One shared track plus CC0 model packs |
| Generator script per video instead of hand-written JSON | 004's generator is the quality benchmark. Copying it keeps the density and liveliness |
| `--stills` before every render | catches camera or visibility errors in seconds instead of after a full render |
| Silence trim + speed-up to ≤ 60 s | Shorts length limit, and no dead air for retention |
| Like & subscribe as one graphic at ~27 s, not voice | the author records the voice and it is sped up anyway, so a graphic costs no story time. One combined call interrupts the viewer once instead of twice, and the loop shows it again on replays. 27 s is a compromise: late enough that the viewer has seen the first gags, early enough that many are still watching (a 50 s call reaches only those who stay to the end). Tune the time from the YouTube retention graph and the calibration table |
| Publishing never automatic, always `--dry` first | it goes public on three networks. The author reviews every video first |
| R2 as temporary hosting | Buffer can only post video from a public URL |
| Picture effects in the stage, on by default | AO, depth of field, fog and grading make the code-built set read as a real, deep place and separate the hero from the background. They cost nothing per video (no setup in `short.json`), and post runs before the captions so the text stays crisp |
| Idea gate with a checklist and a critic pass | an honest bar for "viral potential" instead of an inflated feeling, calibrated with real data |

## 6b. Long-form videos (landscape)

| Part | What |
| --- | --- |
| Skill | `.claude/skills/tlama-longform/SKILL.md`. It inherits everything from `ricksclips-short-style` and overrides only what differs |
| Shortcut | `--clv` (same steps as `--cv`, no dry run). Defined in `CLAUDE.md` |
| Folder | `longform/LNNN-slug/` (own numbering L001, L002…), same `work/` layout as Shorts, final files `video.mp4`, `script.txt`, `metadata.md` |
| Format | `"format": "landscape"` in `short.json` → 1920×1080, 30 fps |
| Story | ~900 words (~6 min): hook + rule within 30 s → escalation ladder of 6 steps in 3 acts, cliffhanger after each act, midpoint turn at ~3:00 → "You see…" → twist back to the hook. Max 5 places, max 5 side characters, a running gag. Same Simple English and ElevenLabs tags |
| Idea gate | `.claude/skills/tlama-longform/references/idea-scorecard.md` (10 gates, 10 points, the first 30 s worth 2) + `idea_check.py --longform` with its own registry `scripts/ideas_used_longform.json` |
| Voice | `voice.sh … 0`: silences removed, **no speed-up** (length comes from the text) |
| Picture | shots 4–8 s, slower camera (`zoom` 2–4), `headWidth` ≈ 0.56× the Short values, `frameX` to use the width |
| Captions / CTA | engine defaults for landscape: phrases of 3–5 words at the bottom; LIKE & SUBSCRIBE at ~30 s and ~30 s before the end, at the top |
| Music | the same `music/music.mp3`, looped by the renderer |
| Thumbnail | the author generates it by hand from prompts written by `tlama-thumbnail` (1280×720) |
| Render | in one piece with `--cool` (several hours) |
| Publishing | **by hand** in YouTube Studio; `metadata.md` has YouTube Title, Description (with chapters), Tags. `publish.mjs` is not used |

**Why these choices (decided with the author, 2026-11-23):** one shared engine so fixes land once and Shorts never break (portrait is the default, checked pixel-for-pixel); a separate skill because almost every Short number (60 s, ~40 shots, loop, 1–2 word captions) is different for long-form and mixing them in one file would blur the rules; no speed-up so a 6-min voice stays natural; thumbnails by hand (a test thumbnail rendered from the stage was not good enough); Buffer dropped for long-form, the author uploads by hand.

## 7. Quality benchmark

Video **004 "Call From Tomorrow"** is the reference for animation, assets and full scenes. Its generator is `scripts/build_call_from_tomorrow.py`, and what made it work is listed in SKILL.md ("Quality benchmark").

## 8. Videos so far

| # | Title | Magic rule |
| --- | --- | --- |
| 004 | Call From Tomorrow | a phone call from tomorrow's Tlama |
| 005 | Slowest Race | the slowest one wins |
| 006 | A Thousand Cats | Tlama's laugh sounds like a cat-food can |
| 007 | Monster Under Bed | Tlama's snore sounds like a dragon to monsters |
| 008 | Growing Cake | every nice word makes the cake bigger |
| 009 | Wish Coin | a wish coin gives every wish to the one you love the most (Tlama's cat) |
| 010 | Dog Ate My Homework | whatever Max eats, Max knows everything written on it |
| 011 | Opposite Echo | the cave shouts back the opposite of every shout, and the whole town hears it |

(Video 004 has no folder or script in the project, only its generator.)

Long-form videos (`longform/`):

| # | Title | Magic rule |
| --- | --- | --- |
| L001 | One Copy | the school copy machine makes a real, living copy of anything put on it (every copy has Tlama's idea: make a copy) |

## 9. Changelog

- **2026-11-23**: Added the idea gate (`idea-scorecard.md`, `scripts/idea_check.py`, `scripts/ideas_used.json`). `--cv` now shows only ideas at 10/10, at least two. Created this documentation.
- **2026-11-23**: Added the automatic like / subscribe graphic (10 s and 50 s) to the renderer. It applies to every video with no change to `short.json`.
- **2026-11-23**: The like / subscribe graphic changed from two separate ones (10 s and 50 s) to ONE combined "LIKE & SUBSCRIBE" at ~27 s (reaches more viewers, interrupts once).
- **2026-11-23**: Video 009 Wish Coin. New shared script `scripts/crown_coin_variants.py` and puppets `prop_crown`, `prop_coin`, `dwarf_king_nocrown`, `orange_tabby_cat_crown`, `main_hero_tlama_crown`, `main_hero_tlama_coin` (all derived locally, no Higgsfield). Lesson: arm layers draw behind the head, so a prop held high (`armR` ≈ -150) hides behind Tlama's head; hold props at `armR` ≈ -100.
- **2026-11-23**: Video 010 Dog Ate My Homework. New shared puppets `black_hat_noble_nohat`, `dog_floppy_ears_hat`, `prop_hat_black`, `prop_paper`, `prop_book`, `prop_rulebook`, `prop_pill` (local PIL, no Higgsfield; maker script kept in `videos/010-dog-ate-homework/work/custom/make_assets.py`). Lessons: a `house` prop's roof cone has a bounding box far bigger than the house (radius = 0.78 x the longest side), so a big `house` behind a close-up flags `CAMERA_INSIDE_PROP`; build large buildings from `box` parts instead. Swappable signs/boards work as tiny prop puppets in `work/custom/`.
- **2026-11-23**: Added `STORIES.md`, a backlog of 11 ideas that all passed the 10/10 gate and `idea_check.py`. They are not registered in `ideas_used.json` until one is chosen.
- **2026-11-23**: Picture quality upgrade in `stage.js`, on by default for all new renders: easing (poses with a small overshoot `curve: back`, hop squash and stretch, elastic face pop), ambient occlusion on the set (`ao`), sun shadow softness (`shadowSoftness`), closer atmospheric fog (default 30–150, was 40–160, `fog`), and post-processing (`post`: depth of field on the shot target, bloom, warm/cool grade, saturation, contrast, vignette, grain, faint chromatic aberration). Captions are drawn after the post, so they stay sharp. Already rendered videos are unchanged until re-rendered.
- **2026-11-23**: `render.mjs --cool [ms]`: Apple hardware encoder (`h264_videotoolbox`, 16 Mbit/s) instead of libx264, plus a pause between frames (default 100 ms). It halves the average CPU load on the fanless MacBook Air M3 for about 2x the render time, with the same look (SSIM 0.988 vs libx264). It is now the standard full-render command in CLAUDE.md and SKILL.md.
- **2026-11-23**: Video 011 Opposite Echo. New action option `run: true` in `stage.js` (documented in `references/formats.md`): like `walk`, but the legs swing fast and at full strength for the whole move, each character in its own rhythm; a `to` to the same spot = running in place, chained `to` moves with `"curve": "linear"` = a crowd running along a path (a ring). Backward compatible, older videos unchanged. Video-only assets made locally with PIL (`videos/011-opposite-echo/work/custom/make_assets.py`): STOP!/GO! comic shout bursts as prop puppets, a baker (peasant + apron) and a baker holding the cake, wooden signs as `plane` images. Lessons: a running crowd loops seamlessly when the total running time equals a whole number of laps; a shout made visible as a burst (red STOP, green GO, matching red/green light flashes) makes a sound-based rule readable without audio.
- **2026-11-23**: Engine prepared for landscape long-form videos (skill for them comes next). `short.json` accepts `"format": "landscape"` (1920×1080); without it, Shorts render exactly as before (checked pixel-for-pixel on video 011). Landscape defaults: captions as short phrases of up to 5 words at the bottom (`"captions": {"mode": "phrase", "maxWords": 5}`, longer runs split evenly), LIKE & SUBSCRIBE twice (30 s and 30 s before the end, at the top of the frame; `"cta"` also accepts a list and `{"fromEnd": 30}`). Music now loops when it is shorter than the video. `shortkit.py check` handles both orientations. `voice.sh` with max `0` skips the speed-up. Note: `headWidth` is a share of the frame width, so in landscape the same head size needs ~0.56× the Short value.
- **2026-11-23**: Long-form videos added: new skill `.claude/skills/tlama-longform/` (SKILL.md + long-form idea scorecard), shortcut `--clv` in `CLAUDE.md`, folder `longform/LNNN-slug/`, `idea_check.py --longform` with registry `scripts/ideas_used_longform.json`.  Engine keys documented in `references/formats.md` of the Short skill. Shorts are unchanged.
- **2026-11-23**: Long-form thumbnails dropped from the workflow (the stage-rendered test was not good enough; the author makes them by hand). Removed `render.mjs --thumb`, the thumbnail scene and the thumbnail fields of `idea_check.py --longform`; in the long-form scorecard the 2 thumbnail points went to "First 30 s".
- **2026-11-23**: First long-form video L001 "One Copy" made (4:05 voice after silence removal, below the 5-min target; 65 shots, 6 locations, ~290 puppets incl. crowds of Tlamas and moms). Lesson for long-form sets: food-kit models are already life size (scale ~0.5–1, not 2), and "sitting" behind a desk works with a lower desk (top ~0.6) and the puppet at y ≈ -0.18. Its generator is `longform/L001-one-copy/work/build.py`.
- **2026-11-24**: New skill `.claude/skills/tlama-thumbnail/`: writes 3 ready-to-paste thumbnail prompts (Nano Banana / Higgsfield) per video: Tlama (reference `puppets/main_hero_tlama/source.png`) + one key thing from the video + 1–3 words of text, clickbait version of the channel style. Shorts 1080×1920, long-form 1280×720. Runs automatically at the end of `--cv` / `--clv`, saved as `thumbnail_prompts.md` in the video folder. It only writes prompts; nothing is rendered from the stage and the image is generated and uploaded (YouTube Studio) by hand.
- **2026-11-24**: README: added the "Thumbnails" section (prompt workflow with the image generator) with four example thumbnails `docs/images/th1–th4.png`.
