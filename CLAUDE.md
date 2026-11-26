# Content creator project – YouTube Shorts

## About the project

My content creator project, focused mainly on **YouTube Shorts**. This repository is a working folder for ideas, scripts, assets and video production.

## Channel

- **Active channel:** [@TlamaLabs](https://www.youtube.com/@TlamaLabs)
- **Goal:** publish **faceless "What if…?" Shorts** (animated, without the author's face) using the `ricksclips-short-style` skill

## Two Short formats

| | "What if" Short (`--cv`) | Song Short (`--cvs`) |
| --- | --- | --- |
| Skill | `ricksclips-short-style` | `tlama-song` |
| Content | science question | English × another language word game ending in a rapped tongue twister |
| Audio | my ElevenLabs voice + `music/music.mp3` | one Suno track that I make |
| Picture | 3D stage | flat images, hard cuts |
| Folder | `videos/NNN-slug/` | `videos/NNN-language/` |

**Which rules apply:** in this file, the rules about the "What if" topic, script formula, 110–130 words, voice speed-up, `music/music.mp3`, the 3D scene, hooks, clarity and retention fixes are for "What if" videos. Song Shorts follow "Song Shorts and shortcut `--cvs`" and the `tlama-song` skill, which override them. Everything else (channel, 35 s hard limit, never generate audio, safe and original content, Higgsfield only after confirmation, own folder per video, publishing only on command) applies to both.

## Vision and goals

- **Main goal:** YouTube monetization (meet the YPP conditions – subscribers + Shorts views – and earn from ads)
- **Focus:** since 2026-11-25 the niche is **"What if…?" videos**. The invented absurd stories (videos 005–016, L001) and the older Roblox Shorts are finished and no longer the direction. Song Shorts (since 2026-11-26) are the second format, see "Two Short formats".
- **Topic and language:** **hypothetical "What if…?" questions** answered with real, checked science, exaggerated and funny to watch. Always in **English**, format: "What if…?" hook → escalation ladder (time or size) → pivot "But here is the real problem." → finale that loops back (global audience, higher RPM)
- **Main character:** `puppets/main_hero_tlama` (Tlama, a pink head with a huge mouth and yellow goggles) is in **every** video as the **test subject**: the voice says "you", and on screen it happens to Tlama. Details in `PUPPETS.md`
- **Voice:** I **generate the voice myself** and upload it into the video folder (see "Shortcut `--cv`"). **Never generate the voice** (no `generate_audio` or any other TTS), and do not suggest generating it. Deliver only the text script.
- **Length (since 2026-11-25):** Shorts are **strictly 35 s at most (hard limit), 110–130 words**, and the voice is **always sped up at least 1.25x**. Reason: analytics of 005/006/012 showed 38–45 % swiped away and only ~22 s average watch time of 60 s.
- **Main goal of a video:** the highest possible retention. The viewer must stay with the Short until the end (and ideally replay it in a loop)
- **English level:** simple, understandable for everyone (see the "Simple English" section)
- **Frequency:** **daily**, 1 Short. Production must therefore be as fast as possible: the library (characters, backgrounds, models) is built once and reused, a new video = only its own folder `videos/NNN-slug/` (script, voice, `short.json`).
- **Consequence:** prefer repeatable, automatable procedures over one-off perfection. Suggest how to shorten the time per video.

## Folder contents

| Path | Description |
| --- | --- |
| `.claude/skills/ricksclips-short-style/` | Main skill for producing faceless Shorts in the @RicksClips3000 style (also holds the shared render engine) |
| `.claude/skills/tlama-longform/` | Skill for landscape long-form videos (5–8 min); inherits everything from the Shorts skill and overrides only what differs |
| `.claude/skills/tlama-song/` | Skill for "song" Shorts (`--cvs`): English × another language word game that ends in a rapped tongue twister; Suno track, flat images, own generator |
| `.claude/skills/tlama-thumbnail/` | Skill that writes 3 ready-to-paste thumbnail prompts (Nano Banana / Higgsfield) with Tlama + one thing from the video. Only prompts, I generate the image by hand. Song Shorts (`--cvs`) have their own fixed style: 1 prompt, serious Tlama under the country flag and the language name |
| `longform/` | One folder per long-form video, `LNNN-slug/` |
| `PUPPETS.md` | Overview of the characters in `puppets/` (who is who and when to use them). Update it after adding a new character |
| `DOCUMENTATION.md` | How the project works: idea, goals, workflow, architecture, key decisions and why, videos so far, changelog |

**Keep `DOCUMENTATION.md` up to date (mandatory).** Whenever you change the workflow, a rule in this file, the skill, a script, a tool, the folder structure or a technical decision, update the relevant section of `DOCUMENTATION.md` in the same piece of work and add a dated line to its changelog. After a new video is finished, add it to the "Videos so far" table. Do not let it drift from the actual state of the project.

## Main workflow: faceless Shorts in the RicksClips style

Use the skill **`ricksclips-short-style`** (`.claude/skills/ricksclips-short-style/SKILL.md`). Read it before any work on a video and follow it.

In short: flat 2D doodle characters in a sunlit 3D world, built entirely in code (three.js stage). New characters and backgrounds are **exceptionally** generated through the **Higgsfield connector** (only when truly needed and **only after my explicit confirmation**, see "Higgsfield"). Nobody generates the voice, I record it. The scene is assembled into `short.json` and rendered via `.claude/skills/ricksclips-short-style/scripts/stage/render.mjs`.

Format: 1080x1920, 30 fps, **strictly 35 s at most (110–130 words)**, captions of 1–2 words.

### Shortcut `--cv` (create video)

When I write just `--cv`, it means this prompt (I do not have to write it out):

> Using the ricksclips-short-style skill, suggest 3 "What if…?" ideas. Give me those ideas and I will choose one of them. Then write a script for at most 35 seconds (110–130 words, hook max 10 words) with the channel's formula: "What if…?" hook, escalation ladder, "But here is the real problem.", finale that loops. Use puppets available in PUPPETS.md

The procedure is always the same. (The output templates below are intentionally kept in Czech, because they are what I read; the rest of this file is in English.)

1. **Immediately, as the very first step** (before reading anything) create an empty folder `videos/NNN/`, where `NNN` = the highest number in `videos/` + 1 (three digits, e.g. `009`). Only the number for now, no slug and no subfolders. This lets several videos run in parallel.
2. **Three ideas.** Read the skill and the scripts of the finished videos so the topic does not repeat. **The topic must always be new, original and different from all previous videos.** Then print exactly this structure and **nothing else** (no intro, no recommendation, no list of characters):

   ```
   # 1 - Název
   - Hook: What if ...?
   - Eskalace: krok → krok → krok
   - Finále: ...
   - Hodnocení: x/10

   # 2 - Název
   ...
   # 3 - Název
   ...
   ```

   `Hook` is in English (it goes into the video), the rest in Czech. `Eskalace` = the steps of the ladder, `Finále` = the final payoff. `Hodnocení` (rating) = the score from the idea scorecard.

   **10/10 gate (mandatory):** before printing, run the full procedure in `.claude/skills/ricksclips-short-style/references/idea-scorecard.md` silently (8–10 candidates → basic plausibility check → `scripts/idea_check.py` → scorecard with reasons → critic pass → fix or drop). Print **only ideas that reach 10/10, at least 2** (max 3). If fewer than 2 reach 10/10, keep generating; never show weaker ideas. After I choose, register the idea with `idea_check.py --add`.
3. **Fact check, then script.** After I choose, **first check every factual claim** (see "Facts") and save the claims with sources to `videos/NNN/facts.md`. Only then write the script, so I never record a wrong sentence. Print only the text for ElevenLabs (with audio tags, see below) in this form and nothing else. At the same time save it to `videos/NNN/script_tagged.txt` and `videos/NNN/script.txt` (without tags):

   ```
   Příběh:
   [excited] What if you never stopped growing? ...

   Nyní čekám na vložení zvukové stopy do složky NNN.
   ```
4. **Waiting for the voice.** I record the voice myself and put it into `videos/NNN/` (it will be the only `.mp3` there, any name). No continue word is needed. Once I write that it is done (anything that is not a question), continue. If I ask something, answer clearly and keep waiting. If the folder does not contain exactly one `.mp3`, tell me and stop.
5. **Production.** Rename the folder to `NNN-slug` (slug = short English title of the video), move the mp3 to `work/audio/voice_original.mp3` and run the whole workflow: voice processing (`voice.sh`), word timing, scene generator, stills check, render, final files (`video.mp4`, `script.txt`, `metadata.md`). Do not ask questions. Fix errors (stills flags, render failures) yourself. Ask or notify me only when something cannot be solved without me.
6. **Dry run.** When finished, run `node scripts/publish/publish.mjs --dry NNN` (nothing is published). Never run the real publication yourself.
7. **Final report** always in this structure:

   ```
   - Plný render doběhl: <snímky>, <délka>, 1080×1920, 30 fps, hlas + hudba.
   - `shortkit.py check`: <výsledek kamery a zoomu>
   - Vytvořeno: `video.mp4`, `script.txt`, `metadata.md`
   - Dry run: <OK nebo problém>, výpis:
     <celý výstup `publish.mjs --dry NNN`>
   - [případné upozornění na chyby nebo věci, které musím vědět]
   - Thumbnail prompty (skill `tlama-thumbnail`, 1080×1920): <celý výstup skillu, 3 varianty, uloženo v `thumbnail_prompts.md`>
   - command pro nahrání:
     - node scripts/publish/publish.mjs NNN
   ```

### Long-form videos (landscape) and shortcut `--clv`

Next to the daily Shorts, I make **landscape long-form videos**, about **3× a week**: 1920×1080, 30 fps, **5–8 min (target ~6 min, ~900 words)**, one bigger "What if…?" question with Tlama in the same style. Use the skill **`tlama-longform`** (`.claude/skills/tlama-longform/SKILL.md`); it builds on `ricksclips-short-style` (same engine, library, style, script and fact rules) and lists everything that differs: structure (escalation ladder of 6 steps in 3 acts, cliffhangers, midpoint turn, "But here is the real problem.", finale back to the hook), max 5 places and 5 side characters, shots of 4–8 s, captions as short phrases at the bottom, CTA twice, YouTube-only metadata with chapters. Simple English and the ElevenLabs tag rules are the same as for Shorts.

When I write just `--clv` (create long video), run the same procedure as `--cv` with these differences:

1. **Immediately** create an empty folder `longform/LNNN/` (`LNNN` = `L` + the highest number in `longform/` + 1, three digits, e.g. `L001`). Own numbering, separate from `videos/`.
2. **Three ideas**: the same output format as `--cv` (`# 1 - Název`, Hook, Eskalace, Finále, Hodnocení), nothing else. The 10/10 gate uses the long-form scorecard `.claude/skills/tlama-longform/references/idea-scorecard.md` and `scripts/idea_check.py --longform` (own registry `scripts/ideas_used_longform.json`). After I choose, register with `idea_check.py --longform --add`.
3. **Fact check and script**: as in `--cv` (facts first, saved to `longform/LNNN/facts.md`); the same output (`Příběh:` … `Nyní čekám na vložení zvukové stopy do složky LNNN.`), saved to `longform/LNNN/script_tagged.txt` and `script.txt`.
4. **Waiting for the voice**: the same as `--cv` (exactly one `.mp3` in `longform/LNNN/`).
5. **Production**: rename to `longform/LNNN-slug`, move the mp3 to `work/audio/voice_original.mp3`, then the whole workflow from the long-form skill without asking: `voice.sh … 0` (silences removed, **no speed-up**), word timing, scene generator (`short.json`), stills check, full render **in one piece with `--cool`**, final files `video.mp4`, `script.txt`, `metadata.md`. **Thumbnail prompts** (skill `tlama-thumbnail`, 1280×720) are written at the end, the image itself I generate by hand.
6. **No dry run and no Buffer.** I upload long-form videos **by hand** in YouTube Studio. Never run `publish.mjs` for a long-form video.
7. **Final report** in this structure:

   ```
   - Plný render doběhl: <snímky>, <délka>, 1920×1080, 30 fps, hlas + hudba.
   - `shortkit.py check`: <výsledek kamery a zoomu>
   - Vytvořeno: `video.mp4`, `script.txt`, `metadata.md`
   - [případné upozornění na chyby nebo věci, které musím vědět]
   - Thumbnail prompty (skill `tlama-thumbnail`, 1280×720): <celý výstup skillu, 3 varianty, uloženo v `thumbnail_prompts.md`>
   - Nahrání: ručně v YouTube Studiu (video + thumbnail, title, description s kapitolami a tags z `metadata.md`)
   ```

`metadata.md` for long-form has only the YouTube part: `### Title`, `### Description` (with chapters `0:00 …` inside, then 3–5 hashtags without #shorts) and `### Tags`. The exact template is in the long-form skill. After a long-form video is finished, add it to the long-form table in `DOCUMENTATION.md`.

### Song Shorts and shortcut `--cvs` (create video song)

A second Short format, first made as video 018 (Spanish): the English producer asks a bored Tlama how to say simple words, every answer shares one funny sound, and the words end up in one tongue twister that Tlama raps on a beat drop. Use the skill **`tlama-song`** (`.claude/skills/tlama-song/SKILL.md`); it holds the whole procedure, the idea rules and gate, the Suno prompt template, the scripts and the final report.

When I write just `--cvs`:

1. **Immediately** create an empty folder `videos/NNN/` (shared numbering with the other Shorts). **Song folders are named by the language, never by the story**: right after I answer the language question, rename it to `videos/NNN-language/` (English, lowercase, e.g. `022-polish`). This overrides the `NNN-slug` naming used elsewhere in this file.
2. **Always ask me which language** it is (English × ?), every time, before anything else. Never guess it.
3. Three ideas (only 10/10, at least 2 shown; every idea needs one shared sound family, a trap pair and a tongue twister), then after I choose: check every translation and the twister's grammar in a dictionary (`facts.md`), save `dialogue.txt`, `script.txt`, `suno.md` and `thumbnail_prompts.md`, and print only the **Suno package** (Style, Exclude styles, Lyrics) + the **thumbnail prompt** + `Nyní čekám na vložení písně ze Suno a obrázku náhledovky do složky NNN-language.` The sound is my classic style or a small variation made **only from proven presets** (never untested ones); the whole mix differs from the 3 latest song videos, and when I say the generations are bad, go straight back to the classic sound (`references/sound-presets.md`).
4. I make the whole track in Suno and the thumbnail image, and put both into `videos/NNN-language/` (the only `.mp3` and the only image). Without both, production does not start.
5. Production without questions (mp3 moved to `work/audio/suno_original.mp3`; `analyze_song.py` → `dress.py` (costume) → `build_song.py --stills` → `build_song.py`; no `--cool` needed, the render takes about 20 s; render with the thumbnail as **the first frame only** (Instagram and TikTok take their cover from it), final files, metadata), dry run, final report from the skill.

The video opens with the line **"Bet you can't say this in <Language>."**

Song metadata: the title **never starts with an emoji**; no "Can you say this?" / "Say it 3 times" lines in descriptions or captions; instead every platform asks in the comments **which language should be next**.

Song folder:

```
videos/NNN-language/
  dialogue.txt          spoken lines (A: producer, B: Tlama, RAP:)
  script.txt            the same text for publishing, transliterated if non-Latin
  facts.md              checked translations with sources
  suno.md               sound mix line + Suno package
  thumbnail_prompts.md  one thumbnail prompt
  <image>               my thumbnail (the only image in the folder)
  video.mp4, metadata.md
  work/                 audio/, song.json, custom/ (dressed images), out_stills/, out.mp4
```

What differs from `--cv`: the audio is one Suno track (no ElevenLabs voice, no `music/music.mp3`, no `voice.sh` speed-up; the 35 s limit stays, the track is cut after the rap; the usual length is 30–35 s, shorter is fine when the cut requires it), the picture is flat images of the duo in `puppets/song_duo/` with hard cuts (no 3D stage), and the fact check is a translation check.

**Four fixed rules for song videos:**

1. **Costume:** Tlama in the video **always** wears the typical clothing / national costume of the language's country (the same country as the thumbnail flag). A saved costume (`puppets/song_duo/costumes/<country>/`) is reused for free. A missing one is one Higgsfield generation (1 credit): ask me for confirmation as always (best together with the Suno package). **The thumbnail always keeps the original Tlama** (white coat).
2. **Cut:** the track is **always cut right after the first rap chorus** in the target language (Suno sometimes raps it twice, I do not want that). It is a **plain hard cut, no fade**. Check by listening/transcription that nothing from a second round is left.
3. **Non-Latin script** (Arabic, Greek, Japanese…): captions show the **original script on top and the Latin transliteration under it in brackets**.
4. **Published folders** get the `-pub` suffix (see "Publishing via Buffer").

### Higgsfield (new characters and backgrounds)

Higgsfield is connected, but it is used **only when truly needed** (a character or background that the library lacks). **Always ask me first and wait for my confirmation.** Do not generate anything without confirmation. The main character (`main_hero_tlama`) is always ready, and so are most of the others, so steps 1–4 are usually skipped.

If a new character is generated, it goes through the whole cycle: 1. character image → 2. emotion sheet → 3. slice into layers / rig the puppet → (optionally a background). Then add it to `PUPPETS.md`.

### Workflow steps (details in the skill)

A regular video (the library already exists): 1. fact check and script → 2. **waiting for my voice** → 3. timing → 4. scene in `short.json` → 5. stop-frame check (`--stills`) → 6. render → 7. **final files into the video folder** (see "After the video is rendered") → 8. **publication** (see "Publishing via Buffer", never automatic, only after I review the video) → 9. next video

**Not generated:** music, textures or 3D models. **Music:** every video except song Shorts uses my ready-made track `music/music.mp3` (shared archive), in `short.json` `"audio": {"voice": "audio/voice.mp3", "music": "music/music.mp3", "musicDb": -18}`; the render trims it to the video length and fades it out at the end. Do not generate any other music. A video has voice, music, flat colors, props from the stage primitives (crate, barrel, wall, house…) and **ready-made 3D models (GLB) from the `props/` library**, which I supply by hand (downloaded free packs, CC0). Do not generate new 3D models, only use those from the library.

### 3D model library (`props/`)

- One folder per pack (e.g. `props/basic_scene/` = Kenney castle kit), containing `*.glb` and `Textures/` (the GLB refers to `Textures/colormap.png`, do not delete).
- **`props/catalog.json`** = list of all models with dimensions (stage unit, the hero is 1.8). **`props/<pack>/0_preview.jpg`** = preview sheet of all models. Read them before building a scene and choose from them.
- After adding a new pack run `.venv/bin/python scripts/props_catalog.py` (refreshes the catalog and the preview).
- **Combine:** models from `props/` and stage primitives (crate, barrel, wall, house, tree…) are used together, not instead of each other. Models are not mandatory, primitives still apply (walls, floors, large shapes, absurd objects). Pick what suits the scene; typically primitives to build the place + models for details and props.
- **Packs combine:** you do not have to take models from one folder only. In a scene (even in one shot) mix packs as needed, e.g. furniture + food + graveyard. The path in `file` always contains the pack folder.
- **Scene density:** a location must feel like a real place, not a bare stage. Target **120–200 objects per location** (center, small clutter on the ground, fences/walls, foreground, a belt of trees and large backdrops in the background, a mix of packs). Build it with `scripts/set_dressing.py` (`scatter`, `line`, `ring`, `clear_zone`), a few lines per layer. Detailed rules are in SKILL.md, rule 4.
- Usage in `short.json`: `{"type": "model", "file": "props/basic_scene/wall.glb", "pos": [x, 0, z], "scale": 3, "rotY": 30}`. Kenney models are small (1×1 tiles), usually `scale` 2–3, or `height` in stage units.

### Structure: shared archive + a folder per video

**Every video has its own folder `videos/NNN-slug/`**, which I can delete as a whole at any time without breaking anything. Videos do not affect one another, so several can be produced at once (in parallel, e.g. in separate agents). No video may write to the project root (`short.json`, `audio/`, `out.mp4` in the root are no longer used) or to another video's folder.

```
videos/NNN-slug/
  work/            working files for this video only (deletable)
    audio/         voice_original.mp3 (raw), voice.mp3, script.txt, words.json
    build.py       scene generator (copy of the template, see below)
    short.json     scene
    out.mp4, out_stills/
    custom/        anything one-off: background, puppet for this video only, images
  facts.md         checked claims with sources
  video.mp4        final render
  script.txt       final script without tags
  metadata.md      captions for the platforms
```

Song Shorts are named `videos/NNN-language/` and have their own layout (see "Song Shorts and shortcut `--cvs`"). Their shared images and country costumes are in `puppets/song_duo/`.

**Shared archive** (in the root, reusable across videos): `puppets/`, `props/`, `bg/`, `music/`, `scripts/` (generator templates, `set_dressing.py`, `puppet_variants.py`, `voice.sh`, `publish/`). Deciding what goes where:
- **Has a real chance of being reused** (new character, generic background, new GLB pack, new helper script, generic template) → straight into the shared archive (`puppets/`, `bg/`, `props/`, `scripts/`…), and update `PUPPETS.md` if needed.
- **Specific to this video only** (voice, script, words, `short.json`, scene generator, one-off prop, custom background or puppet variant, stills) → into `videos/NNN-slug/work/`. When in doubt, treat it as video-specific and do not clutter the archive.
- Only **add** to the shared archive; do not change existing files in it for one video (you would break the other videos). Need to alter a character? Make a variant in `work/custom/`.

**Paths in `short.json`** are looked up first in the video's `work/`, then in the shared archive. So `audio/voice.mp3` = from the video, `puppets/main_hero_tlama` and `props/...glb` = from the archive, `custom/bg.png` = from the video. Therefore always render with `--lib` pointing at the project root:

```
V=videos/NNN-slug/work
node .claude/skills/ricksclips-short-style/scripts/stage/render.mjs $V/short.json $V/out.mp4 --stills --lib .
node .claude/skills/ricksclips-short-style/scripts/stage/render.mjs $V/short.json $V/out.mp4 --lib . --cool
```

**Always add `--cool` to the full render.** The machine is a fanless MacBook Air M3 (16 GB), and I do not want it to overheat. `--cool` uses Apple's hardware encoder and pauses between frames: about 2x slower, same look.

Scene generator: copy `scripts/build_call_from_tomorrow.py` to `$V/build.py` and run `cd $V && ../../../.venv/bin/python build.py short.json` (in the copy set `sys.path.insert(0, "<absolute path>/scripts")` for `set_dressing`). Voice: `cd $V && ../../../scripts/voice.sh`. Word timing: `cd $V && ../../../.venv/bin/python ../../../.claude/skills/ricksclips-short-style/scripts/stage/shortkit.py words audio/voice.mp3 audio/script.txt -o audio/words.json`. Check that you can see the `.venv/bin/python` path (otherwise use an absolute one).

### Script – formula ("What if…?")

1. **hook** = one "What if…?" question, max 10 words, no intro (e.g. "What if you never stopped growing?").
2. **escalation ladder**: 3–4 steps on **one scale** (time: day 1 → week 1 → year 1; or size, speed, number). Say the step out loud at the start ("After one week…"). Each step is one clear consequence, bigger than the one before. The first step comes within 5 s.
3. pivot **"But here is the real problem."**: the one consequence nobody expects, with one simple real reason (1–2 sentences).
4. **finale**: the biggest picture of the video and the answer to "how does it end?". The last line leads back into the hook so the video loops.

### Facts (mandatory)

The question is imaginary, **the answer must be honest**. This replaces the old "everything is invented" rule.

- **Check before the script.** Every factual claim (numbers, cause and effect) is verified with web search **before** I get the script. Prefer encyclopedias, universities, space and science agencies, museums. One good source per claim; two for a surprising number. Content farms and other YouTube videos are not sources.
- **Save it** to `facts.md` in the video folder: claim in the script → source link → note (fact / estimate).
- **No made-up numbers.** If a number cannot be verified, cut it or say it without a number. If scientists do not know, say "would probably" / "might". Consequences of the impossible premise use "would".
- **Simplify, do not distort.** A simple sentence must still be true. If it cannot be simple and true, choose another step.
- **If the science makes the idea boring or wrong**, tell me and offer another idea. Never bend the facts.

### Topic rules

- **One change to the world.** One "what if", and everything follows from it. No second what-if.
- **A question a ten-year-old would ask.** Body, animals, food, Earth, space, sea, weather, home, school. No lessons in physics terms.
- **Every step is visible.** For every sentence you must be able to show one clear picture with Tlama and library props or primitives. A sentence that cannot be drawn goes.
- **Variety.** The 3 shown ideas come from 3 different areas (e.g. body, space, animals); do not repeat the area or the setting of the last 3 videos in `scripts/ideas_used.json`. Choose a setting that uses the `props/` library (factory, pirate ship, forest, graveyard, furniture, food, castle) or primitives (space, sea, desert, snow). Mixing packs is encouraged.
- **Safe content.** No violence, gore, death shown or described in detail, real fear, hate or sexual content. **No health or medical advice, nothing a child could try at home and get hurt**, no politics, religion, real tragedies, real people or brands. Consequences for the body stay cartoon-style and funny (YPP, suitable for younger viewers too).
- **Not a template.** YouTube does not monetize generic or repetitive content, so every video has its own steps, pictures, jokes and finale, not the same script with one word swapped.

### Clarity (the viewer must not get lost)

- **The question is clear from the hook and never changes.** Every sentence answers it.
- **One ladder.** The same scale all the way up; the viewer learns the pattern and waits for the next step.
- **"You" is Tlama.** The voice says "you", the screen shows Tlama. Max. 2 side characters, who only react ("your mom", "your dog").
- **Time and size only go up.** No jumps back.
- **A change of place is said out loud.** Max. 3 places.
- **The pivot is short.** 1–2 sentences, one simple cause. No chain of reasons.
- **The finale follows from what was shown.** Nothing new from nowhere.
- **Retelling test.** Retell it in 3 sentences (question, what happens, how it ends). If you cannot, cut steps and side ideas.

### Retention fixes (from the analytics of the old story videos 005, 006, 012)

Data: 38–45 % swiped away in the first seconds (healthy: under 33 %), those who stayed watched ~74 %, likes ~1.3 %, almost no subs. The **start** and the **length** lost people. These rules stay for the new format.

- **Length:** 110–130 words, strictly 35 s at most. No scene is needed after the finale.
- **First frame = the question as a picture.** At 0:00 the viewer must already see Tlama in the most extreme moment of the what-if (giant Tlama over houses, Tlama floating off the Earth), not an empty room or a slow zoom into a place. The hook words are on screen as the first caption. A close or medium shot with movement from frame 1.
- **Hook max 10 words**, and the voice starts at 0.0 s (`voice.sh` already trims leading silence).
- **No setup**: the first step of the ladder comes within 5 s.
- **Testing:** the first 10 "What if" videos are the baseline with an unchanged format. Targets, how to read the numbers and the video log are in `z_info/hook_tests.md`; after I report the numbers, update the log.

### Strong hooks (they must make people stay)

Every hook starts with **"What if"**, has **max. 10 words** in simple English and must meet **at least 3 of 4**:
1. **About the viewer** ("you", "your house") or about something everybody knows (the Sun, the sea, a dog).
2. **A picture:** a muted viewer understands it from the first frame.
3. **Huge or extreme** (never, forever, all, 100, one million).
4. **Opens a loop:** the viewer cannot guess the end.

Examples (patterns, not facts; every topic still goes through the fact check):
1. "What if you never stopped growing?"
2. "What if the Sun turned off today?"
3. "What if you fell into a hole through Earth?"
4. "What if it never stopped raining?"
5. "What if you were as small as an ant?"
6. "What if all the oceans disappeared?"
7. "What if your dog was bigger than your house?"
8. "What if you could not stop jumping higher?"
9. "What if the Moon came much closer?"
10. "What if you only ate bananas?" (careful: no health advice)

### ElevenLabs tags in the script

**Always write** the text script straight away with ElevenLabs audio tags in square brackets, so it can be pasted into ElevenLabs without edits. Write the tags in English, put them before the sentence/phrase they apply to, and do not overdo it (about 1 tag per 1–2 sentences, so the voice does not sound overacted). Dialogue in quotation marks stays normal text.

Mainly use these tags:
- **Emotion:** `[weak]` `[angry]` `[bored]` `[menacing]` `[playful]` `[tired]` `[excited]`
- **Vocalizations:** `[clears throat]` `[coughing]` `[chuckling]` `[sniffling]` `[yawning]` `[laughing]` `[sharp exhale]` `[scoffing]` `[humming]` `[panting]` `[gasping]`
- **Delivery:** `[whispering]` `[singing]` `[voice breaking]`
- **Character:** `[sleepy drowsy voice]` `[witch voice]` `[drunken voice]`
- **Sound effects:** `[keyboard typing]` `[echoing]` `[knocking on door]` `[bell ringing]` `[phone ringing]` `[dog barking]` `[crowd cheering]` `[applause]` `[rain falling]` `[drum roll]` `[heartbeat]` `[engine starting]`

Sample (style and tag density only; claims in a real script must pass the fact check):

```
[excited] What if you never stopped growing? [playful] On day one, you only grow a little. Your pants are short. [chuckling] After one month, your bed is too small.
```

**Do not use** tags that slow down or lengthen the audio (`[pause]`, `[short pause]`, `[slowly]`, `[softly]`, `[sighs]`, `[inhales deeply]` etc.). Pauses are trimmed anyway and the goal is the shortest possible track.

The sample may also use other natural tags outside the list (`[thoughtful]`, `[surprised]`, `[anxious]`, `[annoyed]`, `[muffled]`, `[sound of impact]`), but the list above is the baseline.

**Careful with timing and captions:** tags are never shown as captions and do not count toward the pace (~3.5 words/s). Before `words` / `words.json`, save `audio/script.txt` **without tags** (or filter the tags out), otherwise the word alignment breaks.

### Audio track: raw + local processing

- The uploaded voice is always **raw** and is stored in the video folder as `videos/NNN-slug/work/audio/voice_original.mp3`. Never edit it through Higgsfield or any other online tool.
- Do the processing **locally on this computer** via `ffmpeg`: `scripts/voice.sh` (output `audio/voice.mp3`, the raw file is not overwritten).
  1. removes gaps/silence between sentences (`silenceremove`, only ~0.06 s remains),
  2. speeds up (`atempo`, the pitch does not change) **always at least 1.25x**, and more if needed so the result is **strictly at most 35 s** (target 34.5 s). Both rules are mandatory for every Short; before the render check that `voice.mp3` is ≤ 35 s. (Long-form uses max `0` = no speed-up.)
- Only then run `words` for `audio/words.json` on the **processed** `voice.mp3` (the timing must match the final track).
- Run: `scripts/voice.sh` (default paths), or `scripts/voice.sh raw.mp3 out.mp3 30` (last number = max seconds).

### After the video is rendered (mandatory)

**Create the video folder right at the start of the work as an empty `videos/NNN/`** (so parallel videos do not take the same number; `NNN` = next free) and **rename it to `videos/NNN-slug/` after I choose the idea**. After the render is finished, save the final files into it without asking:

- Name: `videos/NNN-video-name/`, where `NNN` is the next sequence number (based on the highest number in `videos/`) and the name is a short English slug (e.g. `003-invisible-invention`).
- Folder contents: `work/` (working files, see "Structure") and **three final files** read by the publication:
  1. `video.mp4`: copy of the final `out.mp4`,
  2. `script.txt`: copy of `audio/script.txt` (final script without tags),
  3. `metadata.md`: in English, **separately for each platform** (each has different conventions). Exact structure (keep the headings unchanged, the publishing script parses them):

     ```
     # NNN – Video title

     ## YouTube
     ### Title
     a single title (with emoji, max ~70 characters), no alternatives

     ### Description
     a short description that opens a loop ("Watch till the end…"), 3–5 hashtags at the end (the first always #shorts)

     ### Tags
     shorts, whatif, science   (the same words as the hashtags without #; Buffer does not send them, only for manual pasting)

     ## Instagram
     ### Caption
     the first line is the hook, then a short description, 3–5 hashtags at the end (without #shorts)

     ## TikTok
     ### Caption
     a very short description (1–2 sentences), 3–5 hashtags at the end
     ```
- Hashtags are single words (no spaces). Each platform has its own text, do not mechanically copy the same description three times.

### Publishing via Buffer (only on explicit command)

Videos are published by the script `scripts/publish/publish.mjs` (it uploads `video.mp4` to Cloudflare R2 and queues it through the Buffer API for YouTube, Instagram and TikTok). The keys are in `.env` (never read or print them).

- **Never publish automatically.** I review the video first. Run the publication only on my explicit command (e.g. "publish 004"), because it goes to public networks.
- Before the real run always do `--dry NNN` first and show me the output.
- Run: `node scripts/publish/publish.mjs NNN` (queues into the next free slot in the Buffer queue, times do not matter). **`--now`** publishes immediately on all platforms (Buffer `shareNow`, no queue), only when I explicitly say "publish now"; still run `--dry --now NNN` first. Several videos at once: `... 004 005 006`. Fixed times only on request (`--start`, `--time`).
- The script skips already published videos according to `.published.json`. Do not delete the video from R2 until it has gone out.
- **Every published video folder gets the `-pub` suffix** (e.g. `018-spanish-pub`). `publish.mjs` renames it itself right after it writes `.published.json` (only when all channels succeeded). If `.published.json` ever appears another way, add the suffix by hand.

### Simple English

Everyone must be able to understand the script, including younger viewers and people for whom English is not the first language (level A2, B1 at most).

- Short words and short sentences (ideally up to ~10 words). One idea per sentence.
- Common everyday words. No complicated or rare words (instead of "consequently" → "so", instead of "purchase" → "buy", instead of "enormous" → "huge").
- Simple tenses (present simple, past simple). No complex sentence constructions, chained subordinate clauses or passive voice unless necessary.
- No idioms, slang, phrasal verbs or wordplay that a foreigner would not understand ("kick the bucket", "spill the beans"…).
- No technical terminology or complicated names. Character names short and easy to pronounce (Tom, Mia, Bob).
- Numbers simple (not "1,347", but "a thousand").
- Before delivering, check the script: if a ten-year-old child or a beginner in English heard it, would they understand every sentence? If not, simplify.

About 3.5 words per second, no empty space.

## Style rules (short)

- Characters: flat 2D cutouts with big round heads (the head about as wide as the torso), real shadows in 3D
- Lines: thick, even, plum black `#271925`, never pure black
- Colors: warm sun vs. cool shadows, do not lift shadows to pure black
- Lively scenes: a shot every 1–3 s, something changes in every shot (angle, expression, background, light), set dressing in three layers (foreground, middle, background), max. 3 places per video, max. 2 side characters. Details in the skill ("Keep every scene alive")
- Camera: movement in every shot, mostly zooming in, no hard cuts

## Technical requirements

- The Higgsfield connector is connected, but it is optional: it is used only for new characters and backgrounds after my confirmation (see "Higgsfield"). A regular video and the render do not need it
- Setup (once): `cd .claude/skills/ricksclips-short-style/scripts/stage && npm install && npx playwright install chromium`, `pip install numpy pillow scipy opencv-python-headless`, `ffmpeg` and `ffprobe` in PATH
- Run the skill's Python scripts via `.venv/bin/python` (it contains `faster-whisper` for accurate word timing in `words.json`; the system `python3` does not have it and falls back to an estimate based on loudness)
- Always do the `--stills` check before every full render

## Inspiration

- **RicksClips3000** – https://www.youtube.com/@RicksClips3000/shorts – the visual style I copy

## How to work with me

- Communicate in Czech unless I write otherwise. Write scripts, voice, captions, titles and video descriptions in **English**.
- Respect the monetization goal: original content (no 1:1 copies of other people's videos), only checked facts (see "Facts"), no real people or brands, no violations of YouTube rules (reused or repetitive content, music copyright).
- For song Shorts, production waits for both the Suno `.mp3` and the thumbnail image. The "I record the voice" exception below is for "What if" and long-form videos.
- When I send just a script, run the workflow with the existing library and do not ask anything beforehand. **Exception:** I record the voice. As soon as you send the script for ElevenLabs, **wait until I put the `.mp3` into the video folder and write that it is done** (a message that is not a question). Without the voice, timing and render do not start.
- When the style is unclear, rely on the skill and `references/style-rules.md`, not on guesswork.
- **Do not write** new video ideas to `brainstorming.md` or anywhere else. Just write them to me in the chat. Write to `brainstorming.md` only when I say so explicitly.
- When I want an idea or a script, deliver **only the text script** (and optionally the hook/finale). Do not generate the voice, I will record it myself.
