---
name: ricksclips-short-style
description: The channel skill for @ricksclips3000-style animated Shorts - flat 2D doodle characters living in a sunlit 3D world, built entirely in code. Use it whenever the user wants to make, plan, render or check a vertical Short in this style, mentions "the channel skill", or asks for any step of it - generate the main character, an emotion sheet, slice a character into layers or rig a puppet, a background, "build the full 3D scene in code", a stop-frame check, or pastes a script and asks for the video. New characters and backgrounds can be generated through the Higgsfield connector (only after the user confirms); the video is assembled, checked and rendered with the bundled three.js stage.
---

# @ricksclips3000 Short style

Make a vertical Short where flat 2D characters stand in a real 3D set: the sun casts their shadows on the ground, the set uses flat colours with an ink outline, the light follows the story and the camera glides from shot to shot. Higgsfield can generate what has to be designed (new characters, backgrounds), but only on the user's explicit confirmation; the voice is never generated. **This channel does NOT generate music, textures or 3D models** (see "Channel rules" below). The bundled stage builds, checks and renders the scene in code.

The style rules behind every default were measured frame by frame from 20 Shorts. The short version is at the end; the full numbers are in `references/style-rules.md`.

## Channel rules (override everything below)

- **Music: use the shared track, never generate one.** Every Short gets the user's ready-made track `music/music.mp3` (shared library, lives in the project root). Put `"music": "music/music.mp3", "musicDb": -18` in `short.json` `audio`. The render trims it to the video length and fades it out; never generate other music.
- **No textures.** Never generate textures. Use flat colours (`"color"`) for the ground, walls and props; leave `"texture"`, `"wall"` texture and `"roofTexture"` out.
- **No generated 3D models.** Never generate GLB models. Ready-made GLB models supplied by hand in `props/<pack>/` ARE allowed: read `props/catalog.json` (names, sizes) and `props/<pack>/0_preview.jpg`, then use `{"type": "model", "file": "props/<pack>/<name>.glb", "pos": [x, 0, z], "scale": 3, "rotY": 0}` (kit models are ~1 unit, use `scale` 2-3 or `height`). Models and primitives are used together, not instead of each other: models are optional and the primitives (crate, barrel, wall, house, box, tree...) stay fully valid. Models do not have to come from a single pack folder: mix packs freely, even within one scene or shot (e.g. furniture + food + graveyard); the `file` path always includes the pack folder. Combine freely, e.g. primitives for the room, ground, walls and oversized absurd objects, models for details and props. Rebuild the catalog with `.venv/bin/python scripts/props_catalog.py` after a new pack is added.
- **Voice: never generate it.** The user records the voiceover themselves and drops it into the video folder (see "Shortcut `--cv`" in the project `CLAUDE.md`). No `generate_audio`, no other TTS, and do not offer to generate it. Only write the text script.
- **Main character.** `puppets/main_hero_tlama` is the hero of every Short (see `PUPPETS.md`).
- If a step below mentions generating music, textures or 3D models, skip it.

## What is in the package

| Path | Use it for |
| --- | --- |
| `scripts/stage/puppet.py` | Cut a character cutout into layers and rig it; cut an emotion sheet into faces |
| `scripts/stage/render.mjs` | Stop-frame check (`--stills`) and the full render to MP4 |
| `scripts/stage/stage.js`, `index.html` | The three.js stage that `render.mjs` drives |
| `scripts/stage/shortkit.py` | Word timings for a voiceover and the camera check |
| `references/formats.md` | The `short.json` scene format, `rig.json`, `words.json`, time values, poses and actions |
| `references/prompts.md` | Prompt templates for every generated asset |
| `references/style-rules.md`, `rules.json` | The measured rules, camera math and QA ranges |
| `examples/demo/` | A small finished project to copy from |

## Setup, once

```bash
cd .claude/skills/ricksclips-short-style/scripts/stage
npm install                       # three + playwright (versions pinned in package.json)
npx playwright install chromium   # or pass --chrome to use an installed Chrome
pip install numpy pillow scipy opencv-python-headless
# ffmpeg and ffprobe must be on PATH
```

The Higgsfield connector is connected, but use it **only when truly needed** (a character or background the library lacks) and **always ask the user first and wait for their confirmation** before any generation. Rendering and the normal `--cv` workflow do not need it. If it is needed but its tools are missing, say so.

## Project folder

One shared library in the project root, plus one folder per video. The library is built once; each video only adds its own folder.

```
puppets/<character>/     rig.json, layer PNGs, faces/   (shared)
props/, bg/, music/      shared library
videos/NNN-slug/
  work/
    audio/               voice_original.mp3, voice.mp3, script.txt, words.json
    build.py, short.json the scene for this video
    out.mp4, out_stills/
    custom/              one-off assets for this video
  video.mp4, script.txt, metadata.md   final files
```

## The workflow, request by request

Users drive this in short requests. Each one maps to a step below; do the step, show the result, and say what the next step is. When the user pastes a script and nothing else, run steps 5 to 8 with the existing library and ask nothing first (the voice file comes from the user). The `--cv` shortcut (idea → script → wait for the user's voice → full production → report) is defined in the project `CLAUDE.md`.

Steps 1 to 4 below are only for a **new** character or background that the library lacks: the main character and most others already exist, so normally skip them. Before any Higgsfield generation, ask the user and wait for their confirmation. A new character goes through the whole chain (image → emotion sheet → slice/rig) and is then added to `PUPPETS.md`.

All commands below are run from the project root with `.venv/bin/python` (the system `python3` has no Whisper), using `V=videos/NNN-slug/work` and `S=.claude/skills/ricksclips-short-style/scripts/stage`.

Download a finished generation with `curl -o <file> <result url>`. If the sandbox cannot reach the URL, ask the user to drop the file into the project folder.

### 1. "Generate our main character"

Generate one image with the character template in `references/prompts.md` (Nano Banana Pro, 2:3, 2k), remove the background, and save the cutout as `puppets/<id>/source.png`. Show it. The proportion to protect is the head: about as wide as the torso. A small head on a realistic body is the usual reason the look fails, so regenerate instead of accepting it.

### 2. "Generate an emotion sheet"

Generate the sheet with the template in `references/prompts.md`, using the character's image job as the reference, then remove the background. Save it as `puppets/<id>/emotions.png`. If the request lists fewer than six expressions, fill the grid with a neutral face.

### 3. "Slice the character into layers and rig a puppet"

```bash
.venv/bin/python $S/puppet.py slice puppets/hero/source.png puppets/hero
.venv/bin/python $S/puppet.py faces puppets/hero/emotions.png puppets/hero --names happy,nervous,shocked,shouting,confused,neutral
```

`slice` writes head, body, arm and leg layers with their pivots into `rig.json` and a `preview.png` with four panels: original, layers apart, re-assembled, posed. Open the preview and check the posed panel: limbs must swing from the shoulders and hips, and the head must tilt on the neck with no gap. `faces` needs the names in the sheet's order, left to right and top to bottom; check `faces_preview.png` the same way. If a cut is wrong, regenerate the character with the limbs further from the body instead of editing the layers by hand.

From here the character is a puppet driven by code. The stage adds breathing, shoulder bobs, a slight head tilt and blinking on its own, and actions in `short.json` set poses, faces, walking, hops and shaking. Poses overshoot slightly and settle, hops squash and stretch, face changes pop (see `curve` in `references/formats.md`).

The finished picture gets ambient occlusion on the set, depth of field focused on the shot's target, atmospheric fog, bloom, a warm/cool grade, vignette and light grain automatically (`ao`, `fog`, `post` in `references/formats.md`). Leave the defaults on; turn something down only when the stills show a problem (e.g. `"post": {"dof": 0}` if a wide shot needs the whole set sharp).

### 4. Background

The sky and the far distance are one flat painting (background template, 21:9), saved into `bg/` and set as `"backdrop"`. The stage wraps it around the world and blurs it. It needs no geometry.

### 5. Script, voice, timing

Write an **absurd, completely made-up story that never happened**. Never use history, real events, real people, real brands or real facts, and do not fact-check; invent everything. Use the formula:
1. a **strong, exaggerated hook** in the first line, with no intro, starting in the middle of the action, with high stakes or a deadline (a number or a time), concrete and impossible, told in first person (Tlama), max 15 words. It must make the viewer ask "what? how does it end?" (see "Strong hooks" in `CLAUDE.md` for 23 examples);
2. two or three escalating details, each more absurd than the last;
3. the pivot, "You see...", where the (absurd but story-logical) explanation starts;
4. a twist in the last line that calls back to the hook, so the Short loops.

The goal is maximum watch time. Open a loop early (promise something that is only explained later), add a new turn or reveal every 2 to 3 sentences, never explain everything at once, and keep the story inside its own rules. Keep it safe for all ages (no violence, hate or sexual content).

**Simple English.** Everyone must understand it, including kids and people who do not speak English as a first language (level A2, B1 at most): short common words, short sentences (about 10 words or fewer, one idea each), simple tenses, no idioms, slang, phrasal verbs, wordplay or technical terms, short easy names (Tom, Mia), numbers kept simple. Test: would a ten-year-old or a beginner understand every sentence? If not, simplify.

**Easy to follow.** The situation is absurd, the storytelling is not: a viewer who only half watches must never get lost (full rules in "Clarity" in `CLAUDE.md`).
- One magic rule carries the whole story; no second magic, no unrelated absurd extras.
- Tlama's goal or problem is clear from the hook and never changes.
- Escalation is one pattern repeated three times, each time bigger (rule of three), not three different kinds of trouble.
- At most 3 side characters, each introduced once with a fixed label ("my mom", "the inventor"); nobody new after "You see...".
- No unclear pronouns when two characters are on screen: repeat the name or role. Always say who speaks ("Mom said: ...").
- Time only moves forward (the "You see..." explanation is the only, clearly signalled, step back). At most 3 places, and every change of place is said out loud ("At school...").
- "You see..." is 1 or 2 sentences with one simple cause.
- The twist uses only characters, things and the rule already shown.
- Every sentence has one clear picture to show; cut sentences that cannot be drawn.
- Retell test: the story fits into 3 sentences (problem, what happens, how it ends). If not, cut characters, places and side ideas.

**Choosing the story:** every idea shown to the user must pass the 10/10 gate in `references/idea-scorecard.md` (candidates → `scripts/idea_check.py` → scorecard → critic pass). Show at least two 10/10 ideas, never weaker ones.

Before writing, read the three real reference scripts in `references/transcripts/` (`transcript1.txt` to `transcript3.txt`, timestamped, about 230 to 260 words each). Study their rhythm only: how the opening line hits, sentence length, how details escalate, where "You see..." lands, how the twist closes. Never copy their topics, sentences or facts, and do not imitate their vocabulary level; every script must be original, and simpler in language.

About four words a second, no dead air. Write the voice script with ElevenLabs audio tags in square brackets (e.g. `[excited]`, `[whispering]`, `[gasping]`; full list and a sample in the project `CLAUDE.md`), roughly one tag per one or two sentences. Never use tags that slow down or lengthen the audio (`[pause]`, `[short pause]`, `[slowly]`, `[softly]`, `[sighs]`, `[inhales deeply]`): pauses are trimmed anyway and the track must be as short as possible. Tags are never subtitles and do not count toward pacing: keep `audio/script.txt` tag-free (strip `[...]`) before running `words`, or word alignment breaks. Then **stop and wait until the user has put the `.mp3` into the video folder and confirmed**; do not continue without both. The user records it and supplies it as the raw take `work/audio/voice_original.mp3` (never generate it, never edit audio through Higgsfield). Process it locally with ffmpeg via the project's `scripts/voice.sh`: it removes the gaps between sentences and speeds the track up so it is 60 s at most, writing `audio/voice.mp3`. Save the script as `audio/script.txt`, then get the word timings from the processed `voice.mp3`:

```bash
.venv/bin/python $S/shortkit.py words $V/audio/voice.mp3 $V/audio/script.txt -o $V/audio/words.json
```

Check that the voice is in the language you asked for before building on it.

### 6. "Build the full 3D scene in code"

Write `short.json`. Read `references/formats.md` first; `examples/demo/short.json` is a working example to copy. Decisions to make:

- **Shots.** One per beat of the script, each starting on a spoken phrase (`"start": "say:..."`), so the picture stays locked to the voice. Most shots last one to three seconds; none longer than four. Every shot moves; most push in (`zoom` 3 to 8).
- **Framing.** `headWidth` 0.2 is the house close-up; 0.08 to 0.12 is a wide shot. Vary `yaw` between shots so the glide between them reads as a camera move.
- **Light.** Define a warm `day` mood and a cool `night` mood, and switch on the pivot: `{"t": "say:You see", "mood": "night"}`.
- **Acting.** Give each shot one clear action: a face, a pose, a walk. The idle motion covers the rest.
- **Layout.** The camera looks from +z toward -z by default. Put the set behind the characters (negative z) and leave open ground in front. Separate locations go 60 or more units apart in the same world.

### Keep every scene alive (anti-boring rules)

A scene feels empty when the picture barely changes between shots. With flat colours and a fixed model library, the variety has to come from the shots, the set layout, the light and the acting. Apply all of this when writing `short.json`:

1. **Something new in every shot.** Compared with the previous shot, at least two of these must differ: framing (`headWidth`), angle (`yaw`/`pitch`), the face or pose of Tlama, who is on screen, what is behind the character, or the light mood. If two neighbouring shots look alike, merge them or change one.
2. **Short beats.** One shot per sentence or per new idea, 1 to 3 seconds. A 60 s Short has about 40 shots (average ~1.5 s), not 8.
3. **Alternate the framing.** Close-up, medium, wide, then close again. Alternate the sign of `yaw` (left, right). Use low and high `pitch`, a wide `fov` for drama, push-ins (`zoom` positive) and sometimes pull-outs (`zoom` negative). Keep `glide` for the move between shots.
4. **Dress every location densely (the set must look like a real place, not a stage).** Target **120-200 props per location**, not 10-25. A sparse set looks cheap even when the hero is perfect. Build it in layers, with `scripts/set_dressing.py` (`scatter`, `line`, `ring`, `clear_zone`; see its docstring), a few lines per layer:
   - **Hero zone (5-10 props):** only what the story needs, clean and readable.
   - **Midground (30-50):** gravestones, furniture, crates, stalls: different models, sizes and rotations (random `rotY`, scale jitter), grouped in clusters, not an even grid.
   - **Ground clutter (25-40 small items):** pumpkins, rocks, plants, debris, plates, books. Small items right up to the hero make the ground feel lived-in.
   - **Boundaries:** fences, walls, hedges, house rows with `line()`, so the place has edges and space is enclosed.
   - **Foreground (5-8, cropping the frame):** big out-of-focus shapes at the edges (rocks, trunks, crates), never in the camera line.
   - **Background (50+):** a belt of trees/rocks/buildings with `ring()` at 16-40 units from the hero, plus a few big far landmarks (crypt, tower, house) at 25+ units, so every shot has depth behind the character.
   - **Mix packs** (e.g. graveyard + forest + food), and mix with primitives. Vary heights: tall (trees, lamp posts) next to low (rocks, stones).
   - **Keep the camera path free:** pass `keep_out=clear_zone((hero_x, hero_z))` to every scatter of BIG props (trees, rocks, crypts), otherwise the stage flags `CAMERA_INSIDE_PROP`. Small clutter can use `keep_out=[(hx, hz, 2.5)]`.
   - Interiors: floor box big enough, 3-4 walls, window + door, furniture in 2-3 depth rows, and clutter on every surface (books, plates, plants, lamps), plus something in front of the camera at the edges.
   - Palette: 4 to 6 saturated colours across the set; use `seed` in every scatter so the set is reproducible when you re-render.
5. **Change place.** 3 locations per video (the script has at most 3 places), one per story act (different ground colour, different `backdrop`, different props), 60+ units apart. Move between them on the pivot or on a new reveal, not mid-sentence.
6. **Use the light as a storyteller.** Define more than `day` and `night`: for example `dusk`, an alarm `red`, a weird `green`, a bright `flash`. Switch the mood on every story turn (`lighting` keyframes at `say:` phrases), with a short `fade`.
7. **More actors.** Put 1 to 3 extra puppets from the library (`PUPPETS.md`) into most scenes as a crowd, a rival or a reaction. Cut to their reaction shots (shocked, nervous, confused). Never leave Tlama alone for the whole video.
8. **Always acting.** Tlama gets a new face or pose in every shot. Use `walk` + `to`, `hop` on surprises, `shake` for fear or anger, arms up for excitement. Reactions should be big and quick.
9. **Show the absurd thing.** The key absurd object or creature must be visible, large and in the frame early. Build it from primitives (stacked boxes, a huge barrel, a tall tree) at an exaggerated size. Props do not move or change on their own, so show change by cutting between two locations or two groups of props.
10. **Captions keep the pace.** Keep word-timed captions (1 to 2 words); they carry attention when the picture is simple.

Variety check: after `--stills`, look at the contact sheet. If any three neighbouring stills look similar (same angle, same background, same pose), fix them before rendering.

### Quality benchmark: video 004 "Call From Tomorrow" (match this every time)

The user called 004 the best video so far (good animation, assets, full scenes). Its generator is `scripts/build_call_from_tomorrow.py`: **start every new `short.json` by copying it**, not by writing JSON by hand. What made it work:

**Script → pictures**
- Every sentence names something **showable** (dog bed is empty, bird on the roof, nest on the head, dog falls into arms). Avoid sentences with nothing to show.
- The last shot repeats the **first shot's framing** (same target, `headWidth`, `yaw`, `pitch`, `pan`) so the loop is seamless.

**Scene built by a Python generator**
- Helpers `prop()`, `shot()`, `a()`, `show()`; shots start on `"w:<index>"` from `words.json` (print the indexed word list first).
- **~40 shots for 60 s** (avg ~1.5 s), one per phrase. Alternate close (`headWidth` 0.3–0.42) / medium / wide (0.09–0.14), flip the sign of `yaw` every shot.
- **3 locations, 120–200 props each** (see rule 4 and `scripts/set_dressing.py`), 60–80 units apart. An interior is built from a floor box + 3 walls + window + door + furniture + shelf with coloured books + rug + foreground plant/toy box. Make the floor box big enough that the global ground never shows inside a room.
- **8 moods** (day, red, tense, night, flashback, dusk, gold, morning) with a lighting key on every story turn; short red flash (`fade` 0.15) on each shock.

**Animation tricks that sell it**
- **Growing/shrinking things:** several copies of a character at different `height`, parked underground (`pos` y = -60), swapped with `to` + `over: 0.01` at a word (`show()` helper). Same for appearing/vanishing characters.
- **Real motion with `to`:** the dog falls from the roof into Tlama's arms; Tlama walks between spots in the room; the dog runs across the park. Put at least 3–4 moves like this in every video. For running use `run: true` (fast legs for the whole move; a `to` to the same spot = running in place; chained `"curve": "linear"` moves = a crowd running in a ring, see video 011).
- **Props that belong to a character are painted into its puppet** (`scripts/puppet_variants.py`: phone in hand, nest on head). Static props near a character float when it moves or disappears.
- 2–3 side characters with reaction shots (neighbour shocked, tomorrow-me shouting, dog barking via `hop`).

**Camera fixes learned the hard way**
- Between locations always `out: "dissolve"` (the generator sets it automatically); a glide flies through floors and walls.
- Wide shots (`headWidth` < 0.2) need `pitch` ≥ 4, otherwise the camera goes under ground.
- When the target is swapped/hidden at the shot start, frame it with `anchor` + `distance` instead of `target` (the camera would follow the hidden copy underground).
- Keep foreground props out of the line between the camera and a close-up (the `TARGET_HIDDEN_BEHIND_SET` flag).
- After `--stills` passes, look at a few stills at full size (paste 4–8 into one image), not only the contact sheet.

**Like & subscribe call-to-action.** The renderer adds it automatically to every video (no voice, no setup): ONE pill with a thumbs-up, a bell and the text "LIKE & SUBSCRIBE", near 27 s for 2.5 s, snapped to the nearest sentence start in `words.json`. Do not add your own. Change the time with `"cta": {"at": 30}` in `short.json`, or turn it off with `"cta": false`. It sits at y = 1180, above the captions: in the stills check make sure it does not hide a face or the key action.

### 7. Stop-frame check, before every full render

```bash
node $S/render.mjs $V/short.json $V/out.mp4 --stills --lib .
```

This renders three stills per shot into `out_stills/` with a contact sheet `sheet.jpg` and checks each one. Look at the sheet yourself as well: the flags catch the mechanical failures, not a dull composition.

| Flag | Meaning | Usual fix |
| --- | --- | --- |
| `CAMERA_INSIDE_PROP` | The camera sits inside a house, wall or model | Change the shot's `yaw` or `headWidth`, or move the prop |
| `TARGET_HIDDEN_BEHIND_SET` | Something stands between the camera and the character's head | Change `yaw`, or move the prop or the character |
| `TARGET_OFF_SCREEN` | The character left the frame | Lower `pan`, check `frameX` / `frameY` |
| `FLAT_FRAME` | The frame is nearly one colour, usually a wall filling the lens | As for `CAMERA_INSIDE_PROP` |
| `TOO_DARK`, `TOO_BRIGHT` | Mean brightness outside the style's range | Mood `sun.intensity`, `fill.intensity`, `exposure` |
| `PURE_BLACK` | Pure black areas | Lighten `fill.ground`; never use `#000000` |

Fix `short.json` and run the check again until it reports no problems. Only then render.

### 8. Render

```bash
node $S/render.mjs $V/short.json $V/out.mp4 --lib . --cool     # 1080x1920, 30 fps, captions + voice; --cool = hardware encoder + pauses so the fanless Mac stays cool (about 2x slower, same look)
node $S/render.mjs $V/short.json $V/preview.mp4 --lib . --scale 0.5 --from 0 --to 8   # fast partial preview
```

Software rendering in a sandbox takes roughly half a second per frame; a machine with a GPU is many times faster. Use `--scale` and `--from/--to` while iterating.

### 9. Camera check

```bash
.venv/bin/python $S/shortkit.py check $V/out.mp4
```

`check` measures camera speed and zoom against the style's ranges. Two fixes come up most:

- **Floating characters.** The soft contact shadow under the feet pins a character to the ground. It is on by default (`contactShadow`); raise it if feet still look detached, and make sure the character's `pos` y is on the ground.
- **Flat, pale picture.** Raise `sun.intensity`, deepen `fill.ground`, and use richer flat colours (no textures).

### 10. The next video

Reuse the shared library (`puppets/`, `props/`, `bg/`, `scripts/`): it stays. Each video lives in its own folder `videos/NNN-slug/work/` (audio, `short.json`, generator, stills, one-off assets) that can be deleted without touching anything else, so several videos can be made at the same time. Render with `--lib <project root>`: paths in `short.json` are looked up in the video's `work/` folder first, then in the shared library. Anything with a real chance of reuse (new puppet, background, GLB pack, helper script) goes to the shared library; video-specific things stay in `work/`. See the project `CLAUDE.md`, section "Structure".

## Working with sub-agents

If you split the work across agents, give each one its own files: one owns `short.json` lighting and moods (or better: one agent per video, each in its own `videos/NNN-slug/work/`), one owns shots and camera, one owns asset generation and the library folders. Two agents writing the same file at the same time overwrite each other, and parts of the scene vanish.

## The four rules

1. **Characters** are flat 2D cutouts with big round heads, about a fifth of the frame wide in a close-up, standing in real 3D space: light tints them and they cast real shadows.
2. **Lines** are thick, even and plum-black (`#271925`), never pure black.
3. **Colour** sets warm sunlight against cool shadow; shadows are tinted red-brown, blue or violet and lifted off black.
4. **The camera** moves in every shot, mostly pushing in, and travels to the next shot instead of cutting. Hard cuts are under 1%.

Format: 1080x1920, 30 fps, about 60 seconds, captions of one or two words centred at 70% of the height.

## Limits

- The puppet is a cutout rig: limbs rotate at the shoulder and hip, with no elbows or knees and no lip sync. For acting beyond that, add faces to the emotion sheet or generate extra poses as separate characters.
- `shortkit.py words` uses Whisper when it is installed; otherwise it estimates timings from the loudness of the track, good to about 0.15 s.
- The far background is blurred, but the stage has no lens depth of field.
