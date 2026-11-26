# TlamaLabs – project documentation

How the project works and why it is built this way. The README gives commands and setup. This file records the idea, the goals and the decisions behind it. `CLAUDE.md` holds the binding rules for Claude, and this file explains them.

> **Keep this file current.** Update it in the same change whenever the workflow, a tool, a folder or a rule changes, then add a line to the changelog at the bottom.

---

## 1. Idea

A faceless YouTube Shorts channel, [@TlamaLabs](https://www.youtube.com/@TlamaLabs). Since 2026-11-25 every video is a max 35 s **"What if…?" question** answered with checked science. The voice says "you" and on screen it happens to the same hero, **Tlama** (a pink head with a huge mouth, yellow goggles and a white coat), the test subject.

- **Shape:** "What if…?" hook → escalation ladder on one scale (time or size) → "But here is the real problem." → a finale that leads back into the hook, so the Short loops.
- **Look:** flat 2D doodle cutouts standing in a sunlit 3D world. The style is inspired by @RicksClips3000 (but never copies it). Everything is built and rendered in code.
- **Voice:** recorded by the author in ElevenLabs. Claude writes the tagged script and never generates the voice.

Since 2026-11-26 there is a second Short format, the **song Short** (`--cvs`): a language word game that ends in a rapped tongue twister. The Idea bullets above and the Story system below describe "What if" videos; song Shorts are described in section 6c.

Next to the daily Shorts the channel also makes **landscape long-form videos** (5–8 min, target ~6 min, 3× a week): one bigger "What if…?" question, built with the same engine and library. See "Long-form videos" below.

Earlier directions are dropped: Roblox content, and invented absurd stories (videos 005–016, L001). **Why the last change (author's decision, 2026-11-25):** the stories got few views. Note for later reading of the data: they had been published for only a few days. The expectation for "What if" (an instantly clear question, wider audience) is a hypothesis, tested by the 10-video baseline in `z_info/hook_tests.md`.

## 2. Goals

| Goal | What it means in practice |
| --- | --- |
| **Monetization (YPP)** | Original content only, no real people or brands, only checked facts, no music copyright problems, nothing that could count as reused or repetitive content, and safe for kids |
| **Retention** | Viewers must stay to the end and ideally replay. This drives the story formula, the 10/10 idea gate, the shot every 1–3 s and the looping last line |
| **Global reach** | English at A2–B1 level, so non-native speakers and kids understand every sentence. English also brings a higher RPM |
| **One video per day** | Production has to be fast and repeatable. The library is built once and each new video only adds its own folder |
| **Long-form 3× a week** | Longer watch time per viewer and a second shelf on the channel, reusing the whole Shorts library and engine |

## 3. Workflow overview

```
--cv ──► videos/NNN/ (empty, reserves the number)
     ──► idea gate: 8–10 hidden candidates → idea_check.py → scorecard → critic → show ≥2 ideas at 10/10
     ──► user picks ──► fact check (facts.md) ──► tagged script (ElevenLabs) ──► WAIT for the user's .mp3
     ──► rename to NNN-slug ──► voice.sh ──► words.json (Whisper) ──► build.py → short.json
     ──► render --stills (auto-fix until clean) ──► full render ──► shortkit check
     ──► video.mp4 + script.txt + metadata.md ──► publish --dry ──► report
     ──► (only on the user's command) publish.mjs NNN → R2 + Buffer
```

The full step-by-step rules are in `CLAUDE.md` (shortcut `--cv`) and in the skill `.claude/skills/ricksclips-short-style/SKILL.md`.

Song Shorts (second format, skill `.claude/skills/tlama-song/`):

```
--cvs ──► videos/NNN/ ──► ASK the language (English × ?) every time ──► rename to NNN-language
      ──► idea gate (sound family + trap pair + tongue twister) ──► show ≥2 ideas at 10/10
      ──► user picks ──► translation check (facts.md) ──► Suno package (proven sound mix) + thumbnail prompt ──► WAIT for the Suno .mp3 + thumbnail image
      ──► analyze_song.py (whisper words, drop, BPM, hard cut after the first rap chorus, ≤35 s) → song.json
      ──► dress.py (country costume) ──► build_song.py --stills ──► full render (~20 s, thumbnail on frame 0) ──► video.mp4 + script.txt + metadata.md ──► publish --dry ──► report
      ──► (only on the user's command) publish.mjs NNN → folder renamed to NNN-language-pub
```

## 4. Story system

### Formula and clarity rules
One change to the world per video, one escalation ladder, at most 3 places and 2 side characters (they only react), every sentence can be drawn. All of this is in `CLAUDE.md` ("Script – formula", "Topic rules", "Clarity", "Strong hooks").

### Facts
The question is imaginary, the answer must be honest. Claude verifies every claim with web search **before** handing over the script (so the author never records a wrong sentence) and saves claim → source in the video's `facts.md`. Unverifiable numbers are cut; consequences use "would" / "might". No health advice, nothing dangerous to copy.

### Idea gate (10/10)
**Why:** a self-rating that is only a feeling inflates. The gate turns "10/10" into "passes a fixed checklist, with written reasons and a critic pass".

- `.claude/skills/ricksclips-short-style/references/idea-scorecard.md`: the procedure, 8 hard gates, 10 points and a calibration table.
- `scripts/idea_check.py`: the mechanical checks (hook starts with "What if" and has max 10 words, ladder length, places and side characters, puppets exist, hard words, novelty against past videos by mechanic tag and word overlap).
- `scripts/ideas_used.json`: a registry of past "What if" videos (hook, change, ladder, mechanic tags). The chosen idea is added with `idea_check.py --add`. The old story registries are kept as `scripts/ideas_used*_stories_archive.json`.
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
| Puppets | `puppet.py` (slice + rig), `scripts/puppet_variants.py`, `scripts/crown_coin_variants.py`, `scripts/pirate_variants.py`, `scripts/skeleton_puppets.py` | cutout layers with a rig and swappable faces. Variants (phone, nest, coin, crown, king without crown, cat with crown) and prop puppets (crown, coin) are made locally with PIL from existing puppets |
| Props | `props/<pack>/*.glb` + `props/catalog.json` + previews (`scripts/props_catalog.py`) | ready-made CC0 models (Kenney packs) mixed with stage primitives |
| Moving 3D models | `scripts/glb_card.mjs` | renders GLB models from `props/` into a transparent PNG with the ink outline, so a ship or a whole castle becomes a prop puppet that can move with `to` (static props cannot) |
| Voice | `scripts/voice.sh` (ffmpeg) | removes silences and speeds up the track always at least 1.25x, and more if needed to stay strictly ≤ 35 s, without changing the pitch; `scripts/voice.sh raw out 0` = remove silences only, no speed-up (long-form) |
| Timing | `shortkit.py words` with faster-whisper in `.venv` | `words.json` drives the captions and the cuts |
| Picture quality | `stage.js` (`makeFx`, `makePost`, `CURVES`) | on by default in every video: ambient occlusion on the set, depth of field focused on the shot target (character silhouettes go into the depth buffer), fog, bloom, warm/cool grade, vignette, grain, faint colour fringe; poses ease with a small overshoot, hops squash and stretch, faces pop. Tunable or off via `ao`, `fog`, `post`, `shadowSoftness` and an action's `curve` |
| Like & subscribe | `render.mjs` (`_cta`) + `stage.js` (`drawCta`) | ONE automatic on-screen graphic (thumbs-up + bell + "LIKE & SUBSCRIBE", no voice) at ~27 s for 2.5 s, snapped to the nearest sentence start in `words.json` (±3 s) so it never covers a punchline. On by default in every video; change with `"cta": {"at": 30}`, disable with `"cta": false` |
| QA | `render.mjs --stills`, `shortkit.py check` | catches mechanical errors and checks camera speed and zoom against the measured style numbers (`references/rules.json`) |
| Song Shorts | `.claude/skills/tlama-song/scripts/analyze_song.py`, `build_song.py`, images `puppets/song_duo/` | no 3D stage: the Suno track is aligned to `dialogue.txt` with faster-whisper (fuzzy, accents ignored; a second pass hears the rap in its own language), the track is hard-cut after the first rap chorus at −14 LUFS, the drop is the biggest 30–150 Hz jump near the first rap word, the tempo comes from onset autocorrelation; the build pastes only the face area of mouth / blink variants onto the base images (feathered diff mask), one mouth opening per syllable, `dress.py` puts the country costume on Tlama, the user's thumbnail is frame 0, hard cuts to the speaker, beat-synced drum pose and camera jumps in the finale, PIL frames piped to `h264_videotoolbox` |
| Publishing | `scripts/publish/publish.mjs` | uploads `video.mp4` to Cloudflare R2 and queues it through the Buffer API on YouTube, Instagram and TikTok; sends `thumbnailOffset: 0` (cover = first frame) for Instagram and TikTok; renames a fully published folder to `…-pub` |

### Folder model
- **Shared archive** (root: `puppets/`, `props/`, `bg/`, `music/`, `scripts/`): reusable and **add-only**. Changing an existing asset could break other videos.
- **Per-video folder** `videos/NNN-slug/`: everything specific to that video lives in `work/`, and the final files sit next to it. Song folders are `videos/NNN-language/` (shared numbering). Published folders get the `-pub` suffix. Any video can be deleted on its own, and several can be produced in parallel.
- Paths in `short.json` are resolved in the video's `work/` first, then in the archive (`--lib .`).

## 6. Key decisions and why

| Decision | Why |
| --- | --- |
| Faceless, one recurring hero | builds recognition and needs no camera. Tlama is in every video |
| "What if" with checked facts | the question is clear from the first second and needs no knowledge of the character. Price: every video needs a fact check, and the niche has strong competition |
| Simple English | a global audience and kids. Retention drops as soon as a viewer gets lost |
| Voice recorded by the author | control over the performance and a human voice. Claude never generates audio |
| Scenes built in code (three.js), not AI video | repeatable, cheap, consistent style, fully automatable for a daily cadence |
| Higgsfield only for new characters or backgrounds, after confirmation | it costs credits and adds style drift. The library covers most stories |
| No generated music, textures or 3D models (Claude never generates audio) | copyright safety and consistency. One shared track plus CC0 model packs. Song Shorts use a track the author makes in Suno (paid plan for published videos, because the free plan gives no commercial rights) |
| Generator script per video instead of hand-written JSON | 004's generator is the quality benchmark. Copying it keeps the density and liveliness |
| `--stills` before every render | catches camera or visibility errors in seconds instead of after a full render |
| Silence trim + speed-up (min 1.25x, hard limit 35 s) | Shorts are strictly ≤ 35 s since 2026-11-25 (author's decision, see changelog); no dead air for retention |
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
| Story | ~900 words (~6 min): "What if" hook + the change within 30 s → ladder of 6 steps in 3 acts, cliffhanger after each act, midpoint turn at ~3:00 → "But here is the real problem." → finale back to the hook. Max 5 places, max 5 side characters, a running gag. Facts in `facts.md`. Same Simple English and ElevenLabs tags |
| Idea gate | `.claude/skills/tlama-longform/references/idea-scorecard.md` (10 gates, 10 points, the first 30 s worth 2) + `idea_check.py --longform` with its own registry `scripts/ideas_used_longform.json` |
| Voice | `voice.sh … 0`: silences removed, **no speed-up** (length comes from the text) |
| Picture | shots 4–8 s, slower camera (`zoom` 2–4), `headWidth` ≈ 0.56× the Short values, `frameX` to use the width |
| Captions / CTA | engine defaults for landscape: phrases of 3–5 words at the bottom; LIKE & SUBSCRIBE at ~30 s and ~30 s before the end, at the top |
| Music | the same `music/music.mp3`, looped by the renderer |
| Thumbnail | the author generates it by hand from prompts written by `tlama-thumbnail` (1280×720) |
| Render | in one piece with `--cool` (several hours) |
| Publishing | **by hand** in YouTube Studio; `metadata.md` has YouTube Title, Description (with chapters), Tags. `publish.mjs` is not used |

**Why these choices (decided with the author, 2026-11-23):** one shared engine so fixes land once and Shorts never break (portrait is the default, checked pixel-for-pixel); a separate skill because almost every Short number (60 s, ~40 shots, loop, 1–2 word captions) is different for long-form and mixing them in one file would blur the rules; no speed-up so a 6-min voice stays natural; thumbnails by hand (a test thumbnail rendered from the stage was not good enough); Buffer dropped for long-form, the author uploads by hand.

## 6c. Song Shorts (`--cvs`)

| Part | What |
| --- | --- |
| Skill | `.claude/skills/tlama-song/SKILL.md`: procedure, idea rules and 10-point gate, translation check, Suno template, metadata, final report. `references/sound-presets.md`, `references/image-prompts.md` |
| Story | "Bet you can't say this in <Language>." → trap pair (two English words, one answer) → 7 more word pairs, all sharing one sound → "Try this." → English sentence → beat drop and Tlama raps the tongue twister |
| Characters | the producer (English) and bored Tlama (target language), 16 flat images in `puppets/song_duo/` |
| Costumes | `puppets/song_duo/costumes/<country>/` (`sheet.png` + `place.json`), applied by `dress.py`. A new one costs 1 Higgsfield credit, after confirmation; a saved one is free |
| Inputs from the author | one Suno `.mp3` and one thumbnail image |
| Scripts | `analyze_song.py` (word times, cut, drop, BPM → `work/song.json`, hand-editable), `dress.py`, `build_song.py` (`--stills`; `--no-cover` only for old videos without a thumbnail) |
| Metadata | same headings as other Shorts; no leading emoji in the title, no "can you say it" lines in descriptions or captions, every platform asks which language comes next |
| Results | "Song Shorts" table in `z_info/hook_tests.md` |

| Decision | Why |
| --- | --- |
| A second format next to "What if" | the first test, 018, had the channel's best early numbers (see the changelog). That is one video read after ~8–9 h |
| Opening line "Bet you can't say this in <Language>." | a direct challenge, meant to lower swipe-away |
| One Suno track, no `voice.sh` | voices, beat and rap come together, and the pauses are part of the joke |
| Flat images, no 3D stage | copies the structure of the tested format and renders in ~20 s |
| Hard cut after the first rap chorus, no fade | Suno sometimes repeats the chorus, which the author does not want |
| Only proven sound presets, classic sound as fallback | a new mix for 026 gave no usable track |
| Country costume in the video, original Tlama on the thumbnail | author's rule |
| Thumbnail on frame 0 | Instagram and TikTok take the cover from it; YouTube cannot get a cover through Buffer |
| Folder named by language | author's request |

## 7. Quality benchmark

Video **004 "Call From Tomorrow"** is the reference for animation, assets and full scenes. Its generator is `scripts/build_call_from_tomorrow.py`, and what made it work is listed in SKILL.md ("Quality benchmark").

## 8. Videos so far

Videos 005–016 and L001 use the old story format; "What if" videos start after 016.

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
| 012 | The X Is Me | the X on the map is always where the gold coin is, and the coin is in Tlama's pocket |
| 013 | The Floor Is Lava | the floor becomes whatever Tlama calls it |
| 014 | One Old Sock | it is Trade Day: nobody can say no to a trade |
| 015 | It Rains Me | the rain machine rains the last thing that fell in |
| 016 | Nine More Minutes | anyone who wakes up from the alarm clock is super hungry |
| 017 | Paper Fold (first "What if") | what if you folded one paper a hundred times (10 → 24 → 42 → 100 folds; real problem: it gets thinner than an atom) |
| 018 | Spanish (test: dialogue + rap format, not monetized) | "Spanish is easy, right?": English word → Spanish "-eño" word, then the whole tongue twister rapped on a beat drop |
| 019 | French (song Short, French) | "French is easy, right?": owl = "cool" = chouette trap, English word → French "-ette" word, tongue twister rapped on the drop |
| 020 | Italian (song Short, Italian) | hedgehog = "curly" = riccio trap, English word → Italian "-ccio/-ccia" word, tongue twister rapped on the drop; cut right after the first rap pass (28.15 s) |
| 022 | Polish (song Short, Polish) | little fly = bow tie = muszka trap, English word → Polish "-uszka" word, tongue twister rapped on the drop; cut right after the rap (30.57 s) |
| 023 | Arabic (song Short, Arabic) | gold = went = dhahab trap, English word → Arabic "-ab" word, tongue twister rapped on a UK drill drop; first song with the new sound presets (K2 A2 B2 D3 F2) and Latin-transliterated captions |
| 024 | Russian (song Short, Russian) | onion = bow = luk trap, English word → Russian "-uk" word, tongue twister rapped on a phonk drop; Cyrillic captions with transliteration, new `russia` costume |
| 025 | Hindi (song Short, Hindi) | mango = common = aam trap, English word → Hindi "-aam" word, line rapped on a Jersey club drop (30.75 s); Devanagari captions with transliteration, new `india` costume; the track did not clearly say the final "karta hai", so it is cut after "aaraam" |
| 026 | Hungarian (song Short, Hungarian) | ticket = grade = jegy trap, English word → Hungarian "-gy" word, tongue twister rapped on a trap drop (29.2 s, classic sound); new `hungary` costume |
| 027 | Japanese (song Short, Japanese) | bridge = chopsticks = hashi trap, English word → Japanese "-shi" word, tongue twister rapped on a UK drill drop (28.7 s, sound `K2 A2 B2 D3 F2`); new `japan` costume |
| 028 | German (song Short, German) | treasure = sweetheart = Schatz trap, English word → German "-atz(e)" word, tongue twister rapped on a phonk drop (31.5 s, sound `K3 A1 B5 D2 F3`); new `germany` costume |
| 029 | Sinhala (song Short, Sinhala) | sand = beach = waella trap, English word → Sinhala "-lla" word, tongue twister rapped on a Jersey club drop (25.07 s, sound `K4 A3 B1 D4 F1`); Sinhala captions with transliteration, new `srilanka` costume |

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
- **2026-11-24**: `publish.mjs --now NNN`: publishes immediately on all platforms (Buffer `mode:shareNow`) instead of the queue. Cannot be combined with `--start`. Still only on explicit command.
- **2026-11-25**: Video 013 The Floor Is Lava. New shared puppets `hoodie_kid_blue`, `hoodie_kid_green`, `hoodie_kid_red` (local recolour, no Higgsfield). Lessons: a place that changes on one word (floor → lava) is built twice with the same layout (`x` offset) and the shot hands over with `"out": "cut"` to the same framing in the other copy, characters teleported by the same offset just before that frame (`snap()` / `cutshift()` in `videos/013-floor-is-lava/work/build.py`). The ink pass draws set outlines over `plane` cards, so keep only a plain wall/hedge behind crowd cards. Prop puppets can only rotate a little (`pose.body`), a big turn leaves their canvas. Kenney chairs face away from the camera at `rotY` 0, use 180.
- **2026-11-25**: Video 014 One Old Sock. New shared puppets `main_hero_tlama_hat`, `prop_sock`, `prop_bike`, `prop_key` (local PIL, no Higgsfield; maker script in `videos/014-one-old-sock/work/custom/make_assets.py`, which also has the "both hands on the mouth" and "item in the hand" helpers). Lessons: the stage canvas has only 12 % headroom above a rig, so a tall hat gets cut unless the rig is moved down (bigger `size`/`feetY`) and `height` is scaled by the same ratio; `hide` of a flying prop must come after its last `to` ends, otherwise it comes back; riding = rider and bike moved with the same `to` and `over`. The parallel videos 013 and 014 both made `hoodie_kid_blue/red/green`; 014 overwrote the 013 files (same rig, slightly different shades, current files are from 014). Lesson: a maker script must skip a shared puppet that already exists.
- **2026-11-25**: Video 012 The X Is Me (pirates, first video outside a town). New shared scripts `scripts/glb_card.mjs` (GLB models → movable card puppet: ship sails in and sinks, castle sinks into the ground) and `scripts/pirate_variants.py` (6 pirates + `*_shovel` variants). Lessons: a crowd of 100 = about 12 cards with 9 characters each; cutouts are sorted by distance, so something that must lie ON a card (the X on the map) needs about +0.2 z, and something BEHIND a tall card (Tlama on the roof) needs about -1.6 z; `frameY` 0.06-0.09 keeps less empty ground under the captions.
- **2026-11-25**: Setting variety rule. Ideas kept defaulting to "town / mayor / city". Added "Setting variety" to `CLAUDE.md` (story rules), `ricksclips-short-style/SKILL.md` (step 5), both idea scorecards (candidate step; Shorts also gate G5b): choose the setting first from all `props/` packs, max 1 of 3 ideas in a town, never repeat the setting of the last 3 videos.
- **2026-11-25**: Retention reset after analytics of 005/006/012 (1.2–1.4k views each, 38–45 % swiped away, ~22 s average watch of 60 s, likes ~1.3 %, 0–4 subs; viewers who stayed watched ~74 %). Shorts are now **~35 s (120–150 words)**, hook **max 10 words**, and the **first frame must show the absurd thing** (new gate G1b in the Shorts scorecard, "Retention fixes" in `CLAUDE.md`). Changed: `voice.sh` default cap 45 s, `idea_check.py` hook max 10 words, render CTA default at 45 % of the video (was fixed 27 s), skill shot counts (~24 shots). Target: swipe-away under 33 % after 3 videos; change only these things meanwhile.
- **2026-11-25**: Video 015 It Rains Me (cloud factory, first Short of the new ~150-word length). New shared puppets `prop_sandwich`, `prop_glass`, `prop_drop`, `prop_splash`, `prop_cloud`, `prop_wind`, `pith_helmet_official_wet` (local PIL, no Higgsfield; maker script in `videos/015-it-rains-me/work/custom/make_assets.py`). Lessons: rain of anything = one card with 9-60 figures that falls through the ground in a loop (`rain()` in `videos/015-it-rains-me/work/build.py`, starts mid-fall; keep the cards behind the landed crowd, so the line where they enter the ground is hidden); a falling hero = hero stays still, clouds and speed lines move up, camera `pitch` -17 (looking up hides the contact shadow); puppets turn to face the camera, so a card in front of a `plane` (screen icon) needs about 0.6 z of space; `pose.body` over ~17° clips the head, use pre-rotated cards. ElevenLabs read 144 words in 60 s raw (52 s without gaps), so the first render was 44.5 s and was redone at 1.52x (34.5 s) after the hard limit below.
- **2026-11-25**: Hard limits for Shorts (author's decision after 015 came out 44.5 s): length **strictly ≤ 35 s** and the voice **always sped up at least 1.25x**. `voice.sh` default cap 45 → 35 s and minimum tempo 1.25x (long-form with max `0` unchanged, no speed-up). Updated `CLAUDE.md`, the Shorts `SKILL.md`, the idea scorecard, the comparison table in the long-form `SKILL.md` and `README.md`. Pace to expect: the ElevenLabs voice of 015 read ~2.7 words/s after silence removal, so at 1.25x about 115-120 words fit in 35 s; longer scripts get sped up more.
- **2026-11-25**: Script length for Shorts lowered from 120–150 to **110–130 words** (pace ~3.5 words/s), so the voice fits 35 s with less speed-up (at 015's reading pace about 1.2–1.4x instead of 1.5x; the 1.25x minimum still applies). Changed in `CLAUDE.md`, the Shorts `SKILL.md`, the idea scorecard (G1b) and the comparison table in the long-form `SKILL.md`.
- **2026-11-25**: Hook tests. Video 015 had 64 % swiped away (36 % stayed) at 539 views, worse than 005/006/012. New `z_info/hook_tests.md`: one rule under test at a time, **each rule tested on 3 videos** (read at 500+ views and ~2 h, YouTube only, decision by block average: keep at 5+ points better, drop at 5+ points worse), queue T0-T3 and a video log. `CLAUDE.md` ("Retention fixes") and the Shorts idea scorecard ("Active hook test") now send `--cv` to that file.
- **2026-11-25**: Video 016 Nine More Minutes (graveyard, kitchen, garden; hook test block T0). New shared script `scripts/skeleton_puppets.py` and puppets `skeleton`, `skeleton_old`, `main_hero_tlama_sleep` (drawn locally with PIL, no Higgsfield). Lessons: a whole new character can be drawn in code in the channel style (one function per layer, 8 faces) when it is made of simple shapes; things that get eaten = one card in 3-4 stages made by `bite()` (`videos/016-nine-more-minutes/work/custom/make_assets.py`), swapped with a small hop; a sleeping crowd = crowd cards sunk to the waist (`y` -0.75) with dirt discs; a puppet sunk into the ground needs a disc around it, otherwise the cut looks flat; keep crowd cards away from the line behind Tlama's head (a skull behind the head looks like a hat).
- **2026-11-25**: **Niche change to "What if…?" videos** (author's decision). `CLAUDE.md`: new formula, new "Facts" and "Topic rules" (replacing invented-only story rules), new hooks, `--cv` / `--clv` output is now Hook / Eskalace / Finále, facts are checked before the script and saved to `facts.md`, max 2 side characters in Shorts. Updated both skills, both idea scorecards, the thumbnail skill, `idea_check.py` (hook must start with "What if", ladder of 3–4 steps). Story registries archived as `scripts/ideas_used*_stories_archive.json`, new registries start empty. `z_info/hook_tests.md`: new 10-video baseline read at 48 h (replaces the T0–T3 story hook tests). `STORIES.md` marked as archive. Engine, library, voice, render and publishing are unchanged.
- **2026-11-25**: Video 017 Paper Fold, the first "What if" Short (32.5 s, 33 shots). No new shared assets; one-off cards in `videos/017-paper-fold/work/custom/` (paper tower segments, Moon, Earth, light, atom, fold badges). Lessons: space = a location 250+ units above the ground (the ground is lost in the fog, so the mood's horizon colour becomes the sky) with `plane` stars and galaxies; a tall object that grows = several 4-unit cards stacked and moved together (one tall card gets too blurry, its canvas is limited to 900 px); to follow a moving thing that gets swapped, target an invisible carrier card that makes the same move.
- **2026-11-26**: Test of a second format, video 018 "Dream Log" (copied structure of a viral Spanish tongue-twister Short, own text and characters). Differs from the "What if" Shorts: the whole soundtrack (two voices + rap finale) is one Suno track instead of the author's voice + `music/music.mp3`; no `voice.sh` speed-up or silence removal (pauses are part of the joke), only cut to 33 s with a fade and loudness −14 LUFS; no 3D stage. 16 flat images from Higgsfield (GPT Image 2.6, medium, 1k, ~18 credits) on a plain beige background: base images `A_closed` (new producer character), `B_closed` (Tlama in the channel style), `F_closed` (finale with drums) and mouth / blink / gesture variants. Generator `videos/018-spanish/work/build_dialogue.py` (PIL + ffmpeg): hard cuts to the speaker, mouth patches pasted from the variants onto the base image (feathered diff mask, so outlines never jitter), mouth shape from the voice-band loudness inside whisper word times, finale drum pose and camera jumps on a 150 BPM beat grid. Higgsfield runs max 4 jobs at once. Not part of the daily workflow; decide after the test whether it becomes a series.
- **2026-11-26**: The song format became a skill: `.claude/skills/tlama-song/` (SKILL.md with the procedure, idea rules + 10-point gate, translation check, the Suno style / exclude / lyrics template that worked for 018, metadata template; `references/image-prompts.md`; scripts `analyze_song.py` and `build_song.py`, the generic, data-driven version of 018's `build_dialogue.py`). Shortcut `--cvs` in `CLAUDE.md`: always asks the language first (English × ?). The 16 duo images moved to the shared archive as `puppets/song_duo/` (listed in `PUPPETS.md`), so a new song video needs no Higgsfield. Video 018 now also has `dialogue.txt`. Lessons: whisper may glue the first rap word into the pause, so the rap start is clamped to ≤0.6 s before the detected drop; the tempo is refined and snapped to a round value (Suno makes 150 BPM, not 148).
- **2026-11-26**: Video 019 (French song Short) had the finale cut 1.3 s late: Tlama sat in the pause shot with closed eyes while the rap was already playing. Cause: `analyze_song.py` transcribed the whole track in English, so the French rap was misheard and the drop was searched in the wrong place. Fix: a second whisper pass for the rap only, in its own language (auto-detected), from the end of the English line; the BPM snap to a round tempo now accepts ±2 BPM (Suno's 150 was read as 148). Checked on 018 and 019.
- **2026-11-26**: First numbers of song Short 018 (~8–9 h): 3893 views, 62.8 % stayed, 84.6 % average viewed, 127 likes, 14 shares, 13 subs, so far the channel's best video. New "Song Shorts" table in `z_info/hook_tests.md`.
- **2026-11-26**: Trial opening for song Short 019: ~1.5 s of the rap drop cut mid-sentence ("La chouette à lunettes et…") + 0.12 s gap before "French is easy, right?", to lower swipe-away. One-off script `videos/019-french/work/custom/teaser.py`, output `video_teaser.mp4` (34.9 s) next to the unchanged `video.mp4`. Not part of the `--cvs` workflow; waiting for the author to review and test it.
- **2026-11-26**: Song Shorts: the opening line changed from "<Language> is easy, right?" to **"Bet you can't say this in <Language>."** to lower swipe-away (a direct challenge to the viewer). Applies from the next song video; 018 and 019 are unchanged. Updated `tlama-song/SKILL.md` (why it works, `dialogue.txt` structure, Suno lyrics, metadata example) and the example in `analyze_song.py`. The drop teaser trial on 019 was rejected by the author and is not part of the workflow.
- **2026-11-26**: Song Shorts: removed the `[Short Pause]` between the opening line and the first question in the Suno lyrics template (019 had over 1.5 s without speech there). New tip in `tlama-song/SKILL.md`: pick a Suno version where the question follows right away.
- **2026-11-26**: Video 020 (Italian song Short) finished. Suno repeated the rap, so the author asked to cut right after the first pass: `work/audio/voice.mp3` was re-cut by hand with ffmpeg at 28.15 s (60 ms fade instead of the default 2.6 s tail) and `duration` in `song.json` set to match. Re-running `analyze_song.py --trim` would bring the tail back.
- **2026-11-26**: Song Shorts lip sync fixed after the author saw mismatches in 020. (1) `build_song.py` no longer shapes the mouth from the loudness of the whole mix (it stayed open through whole words and followed the drums): now one opening per syllable, shape from the vowel, closed between syllables; no blinks inside words. (2) In 020 the first rap word started 0.8 s before the voice (whisper glued it into the pause); RAP word times fixed by hand in `song.json` from the spectrogram.
- **2026-11-26**: New thumbnail style for song Shorts only (author's request): one prompt instead of three; Tlama with a serious face, above them the country flag and the language name, plain beige background. Updated `tlama-thumbnail/SKILL.md` and `tlama-song/SKILL.md`; redone for 020. "What if" and long-form thumbnails are unchanged.
- **2026-11-26**: Video 022 (Polish song Short) finished. On the author's request cut right after the last rap word (30.57 s, 0.1 s fade). Fixed by hand in `work/song.json`: finale set to the drop (the drums play ~1.3 s before the rap, so there is no pause shot) and RAP word times taken from a `medium` whisper pass. `myszka` (mouse) was dropped in the translation check because it also has a vulgar slang meaning.
- **2026-11-26**: Song Shorts, four changes (author's request). (1) Titles never start with an emoji. (2) No "can you say it" lines in descriptions/captions; every platform asks which language comes next. (3) The thumbnail prompt now comes with the Suno package; the user adds the image next to the `.mp3`, `build_song.py` puts it on frame 0 only, and `publish.mjs` sends `thumbnailOffset: 0` for Instagram and TikTok (checked in the Buffer API schema; YouTube cannot get a cover through Buffer). (4) The fixed Suno Style became a template with five rotating parts (beat, producer voice, Tlama voice, dialogue bed, rap flow) in `tlama-song/references/sound-presets.md`; each must differ from the 3 latest song videos.
- **2026-11-26**: Song video folders are named by the language only (`videos/NNN-language/`), set right after the language question (author's request). Renamed 018–022 to `018-spanish`, `019-french`, `020-italian`, `021-czech`, `022-polish` and changed their `metadata.md` headings. Older changelog entries use the new paths.

- **2026-11-26**: Video 023 (Arabic song Short) finished (33.5 s). For a non-Latin language, `dialogue.txt` and the captions use a plain Latin transliteration (`analyze_song.py` and the caption font do not handle Arabic script); the Suno lyrics use Arabic script with vowel marks. Fixed by hand in `work/song.json`: RAP word times from a second Arabic whisper pass, several dialogue word times from a spectrogram, tempo 142 BPM (detected 95, a drill syncopation; the script's tempo range loops can leave a value below 110).
- **2026-11-26**: Optional country costumes for song Shorts (author's request): one Higgsfield sheet (1 credit) in `puppets/song_duo/costumes/<country>/`, applied to Tlama in code by `.claude/skills/tlama-song/scripts/dress.py` into the video's `work/custom/`. First costume: `egypt` (galabeya + tarboosh) for video 023.
- **2026-11-26**: Four new rules (author's request), in `CLAUDE.md` and the `tlama-song` skill. (1) Song videos: Tlama always wears the country's typical costume (`dress.py`); the thumbnail keeps the original Tlama. (2) The song is hard-cut right after the first rap chorus, no fade (`analyze_song.py`, manual `--cut`). (3) Non-Latin languages: original script on top, transliteration in brackets below (`dialogue.txt`: `latin | original`; `build_song.py`, Arial Unicode). (4) `publish.mjs` renames a fully published folder to `NNN-slug-pub`; existing published folders 018 and 020 were renamed by hand. Video 023 was re-rendered with all of these (the earlier render still contained most of a repeated chorus).
- **2026-11-26**: Videos 019 and 022 re-rendered under the new song rules (author's request): new costumes `france` (beret, Breton shirt, red neckerchief) and `poland` (Krakow folk costume), 1 credit each; hard cut with no fade (019 at 30.87 s, 022 at 30.57 s). Neither has a thumbnail, so they were rendered with the new `build_song.py --no-cover` (only for old videos). Costume placement moved to `costumes/<country>/place.json`. `019-french/video_teaser.mp4` was not updated.
- **2026-11-26**: Videos 019 and 022 re-rendered with the author's thumbnails on frame 0. The generator returned 2:3 instead of 9:16 and the old cover-crop cut the edges of "FRENCH", so `build_song.py` now fits wider images by cropping the sides only slightly, anchoring the bottom and extending the background at the top. `019-french/video_teaser.mp4` (rejected trial) was not updated. 019 metadata updated to the current song rules (no leading emoji in the title, no challenge lines, a "which language next" CTA on every platform).
- **2026-11-26**: Song Shorts: the Suno prompt for 026 (Hungarian) gave no usable track with a new mix (`K4 A6 B4 D2 F4`). New rule in `references/sound-presets.md`, `tlama-song/SKILL.md` and `CLAUDE.md`: only proven preset ids, the author's classic sound (018–022) is the base and the immediate fallback, untested presets only on request; replaces the old "every part differs from the 3 latest" rule. 026 `suno.md` switched to the classic sound. Idea rule: avoid rows of one-syllable look-alike answers (precaution, not a confirmed cause).
- **2026-11-26**: Video 024 (Russian song Short) finished (27.8 s, sound `K3 A3 B5 D4 F3`). New costume `puppets/song_duo/costumes/russia` (red kosovorotka, ushanka, 1 credit). The library `B_o` image has lighter skin than `B_closed`, which showed a pale patch around the mouth; fixed for this video only with `work/custom/skin_match.py` (run after `dress.py`).
- **2026-11-26**: Video 025 (Hindi song Short): new costume `puppets/song_duo/costumes/india` (mustard kurta, navy Nehru jacket, festive Rajasthani safa, 1 credit, confirmed).
- **2026-11-26**: Video 025 finished. By the author's decision the rap is cut at 30.75 s and "करता है" is dropped from captions and script. `work/build.py` is a per-video copy of `build_song.py` that sets the Devanagari rap caption in 2+2 rows (the 3+3 default overlapped the turban in the close-up).
- **2026-11-26**: Video 026 (Hungarian song Short) finished (29.2 s). New costume `puppets/song_duo/costumes/hungary` (white shirt, embroidered black vest, wide gatya, black hat with a feather-grass plume, 1 credit, confirmed). Same light-skin `B_o` problem as in 024, fixed with a copy of `skin_match.py` in the video's `work/custom/`.
- **2026-11-26**: Video 027 (Japanese song Short) finished (28.7 s). Captions show kana/kanji over the transliteration with no code change. New costume `puppets/song_duo/costumes/japan` (indigo kimono, black haori, grey hakama, sugegasa, 1 credit, confirmed); its wide hat is set lower and flatter in the finale pose (`place.json`) so it clears the rap caption. The idea's "paper → washi" pair was replaced by "bug → mushi" in the translation check (washi is only traditional Japanese paper). Cut set by hand to 28.69 s (`--cut`), the automatic 28.59 s clipped the last "tsu"; rap word times in `song.json` fixed by hand (first word was 0.5 s early).
- **2026-11-26**: Video 028 (German song Short) finished (31.5 s, cut right after the first rap chorus). The first Suno package failed on the word "Scratches" (author's report; the cause is a guess: Suno may read it as a DJ cue), so it was replaced by "Sentence → Satz" and the twister verb "kratzt" by "holt" (5 taught words in the twister). New costume `puppets/song_duo/costumes/germany` (white shirt, Lederhosen with edelweiss chest panel, green Alpine hat, 1 credit, confirmed). `skin_match.py` copied into the video's `work/custom/`.
- **2026-11-26**: Video 029 (Sinhala song Short) finished (25.07 s, shorter than the usual 30–35 s because the cut right after the first rap chorus has priority). New costume `puppets/song_duo/costumes/srilanka` (Kandyan formal dress, 1 credit, confirmed). `build_song.py` now uses Sinhala Sangam MN for Sinhala script (the rap caption sits a bit higher, clear of the tall hat). The sentence grammar was not confirmed by a native speaker (see `facts.md`). Light-skin `B_o` fixed again with `work/custom/skin_match.py`.
- **2026-11-26**: Documentation pass for `--cvs`: `CLAUDE.md` got a "Two Short formats" table that says which general rules apply to song Shorts, the song folder layout and the missing production steps. This file got section 6c (song Shorts and their decisions) and up-to-date workflow, architecture, publishing and folder notes. No workflow rule changed.
