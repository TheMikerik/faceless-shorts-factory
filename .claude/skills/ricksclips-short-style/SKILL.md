---
name: ricksclips-short-style
description: The channel skill for @ricksclips3000-style animated Shorts - flat 2D doodle characters living in a sunlit 3D world, built entirely in code. Use it whenever the user wants to make, plan, render or check a vertical Short in this style, mentions "the channel skill", or asks for any step of it - generate the main character, an emotion sheet, slice a character into layers or rig a puppet, a background, the voiceover, "build the full 3D scene in code", a stop-frame check, a numbers comparison with a reference frame, or pastes a script and asks for the video. Generates every asset through the Higgsfield connector and assembles, checks and renders the video with the bundled three.js stage.
---

# @ricksclips3000 Short style

Make a vertical Short where flat 2D characters stand in a real 3D set: the sun casts their shadows on the ground, the set uses flat colours with an ink outline, the light follows the story and the camera glides from shot to shot. Higgsfield generates what has to be designed (characters, background, voice). **This channel does NOT generate music, textures or 3D models** (see "Channel rules" below). The bundled stage builds, checks and renders the scene in code.

The style rules behind every default were measured frame by frame from 20 Shorts. The short version is at the end; the full numbers are in `references/style-rules.md`.

## Channel rules (override everything below)

- **No music.** Never generate or add music. The Short has the voiceover only; the user adds the background music themselves while editing. Leave `audio.music` out of `short.json`.
- **No textures.** Never generate textures. Use flat colours (`"color"`) for the ground, walls and props; leave `"texture"`, `"wall"` texture and `"roofTexture"` out.
- **No generated 3D models.** Never generate GLB models. Ready-made GLB models supplied by hand in `props/<pack>/` ARE allowed: read `props/catalog.json` (names, sizes) and `props/<pack>/0_preview.jpg`, then use `{"type": "model", "file": "props/<pack>/<name>.glb", "pos": [x, 0, z], "scale": 3, "rotY": 0}` (kit models are ~1 unit, use `scale` 2-3 or `height`). Models and primitives are used together, not instead of each other: models are optional and the primitives (crate, barrel, wall, house, box, tree...) stay fully valid. Models do not have to come from a single pack folder: mix packs freely, even within one scene or shot (e.g. furniture + food + graveyard); the `file` path always includes the pack folder. Combine freely, e.g. primitives for the room, ground, walls and oversized absurd objects, models for details and props. Rebuild the catalog with `.venv/bin/python scripts/props_catalog.py` after a new pack is added.
- **Voice.** Always use the Higgsfield preset voice **Miles** for every voiceover: `voice_id: e18664a7-ee4f-5273-acf8-533eb24cd366`, `voice_type: preset`. Never pick another voice or ask which one.
- **Main character.** `puppets/main_hero_tlama` is the hero of every Short (see `PUPPETS.md`).
- If a step below mentions music, textures or 3D models, skip it.

## What is in the package

| Path | Use it for |
| --- | --- |
| `scripts/stage/puppet.py` | Cut a character cutout into layers and rig it; cut an emotion sheet into faces |
| `scripts/stage/render.mjs` | Stop-frame check (`--stills`) and the full render to MP4 |
| `scripts/stage/stage.js`, `index.html` | The three.js stage that `render.mjs` drives |
| `scripts/stage/shortkit.py` | Word timings for a voiceover, numbers comparison with a reference, style measuring, camera check |
| `references/formats.md` | The `short.json` scene format, `rig.json`, `words.json`, time values, poses and actions |
| `references/prompts.md` | Prompt templates for every generated asset |
| `references/style-rules.md`, `rules.json` | The measured rules, camera math and QA ranges |
| `examples/demo/` | A small finished project to copy from |

## Setup, once

```bash
cd scripts/stage
npm install                       # three + playwright (versions pinned in package.json)
npx playwright install chromium   # or pass --chrome to use an installed Chrome
pip install numpy pillow scipy opencv-python-headless
# ffmpeg and ffprobe must be on PATH
```

The Higgsfield connector must be on. If its tools are missing, say so and stop: the assets cannot be generated without it. Rendering alone works without it.

## Project folder

Keep one folder per channel and reuse it for every video. Everything except `short.json` and the audio is a library you build once.

```
my-channel/
  puppets/<character>/   rig.json, layer PNGs, faces/
  bg/                    mountains.png
  audio/                 voice.mp3, script.txt, words.json
  short.json             the scene for this video
```

## The workflow, request by request

Users drive this in short requests. Each one maps to a step below; do the step, show the result, and say what the next step is. When the user pastes a script and nothing else, run steps 7 to 10 with the existing library and ask nothing first.

Download a finished generation with `curl -o <file> <result url>`. If the sandbox cannot reach the URL, ask the user to drop the file into the project folder.

### 1. "Generate our main character"

Generate one image with the character template in `references/prompts.md` (Nano Banana Pro, 2:3, 2k), remove the background, and save the cutout as `puppets/<id>/source.png`. Show it. The proportion to protect is the head: about as wide as the torso. A small head on a realistic body is the usual reason the look fails, so regenerate instead of accepting it.

### 2. "Generate an emotion sheet"

Generate the sheet with the template in `references/prompts.md`, using the character's image job as the reference, then remove the background. Save it as `puppets/<id>/emotions.png`. If the request lists fewer than six expressions, fill the grid with a neutral face.

### 3. "Slice the character into layers and rig a puppet"

```bash
python3 scripts/stage/puppet.py slice puppets/hero/source.png puppets/hero
python3 scripts/stage/puppet.py faces puppets/hero/emotions.png puppets/hero --names happy,nervous,shocked,shouting,confused,neutral
```

`slice` writes head, body, arm and leg layers with their pivots into `rig.json` and a `preview.png` with four panels: original, layers apart, re-assembled, posed. Open the preview and check the posed panel: limbs must swing from the shoulders and hips, and the head must tilt on the neck with no gap. `faces` needs the names in the sheet's order, left to right and top to bottom; check `faces_preview.png` the same way. If a cut is wrong, regenerate the character with the limbs further from the body instead of editing the layers by hand.

From here the character is a puppet driven by code. The stage adds breathing, shoulder bobs, a slight head tilt and blinking on its own, and actions in `short.json` set poses, faces, walking, hops and shaking.

### 4. Textures: not used

This channel does not generate textures. Use flat colours on the ground and on props.

### 5. 3D models: library only

This channel does not generate 3D models. Use the ready-made GLB library in `props/` (see Channel rules) together with primitives (any mix), and write them into `short.json`.

### 6. Background

The sky and the far distance are one flat painting (background template, 21:9), saved into `bg/` and set as `"backdrop"`. The stage wraps it around the world and blurs it. It needs no geometry.

### 7. Script, voice, timing

Write an **absurd, completely made-up story that never happened**. Never use history, real events, real people, real brands or real facts, and do not fact-check; invent everything. Use the formula:
1. a **strong, exaggerated hook** in the first line, with no intro, starting in the middle of the action, with high stakes or a deadline (a number or a time), concrete and impossible, told in first person (Tlama), max 15 words. It must make the viewer ask "what? how does it end?" (see "Silné hooky" in `CLAUDE.md` for 23 examples);
2. two or three escalating details, each more absurd than the last;
3. the pivot, "You see...", where the (absurd but story-logical) explanation starts;
4. a twist in the last line that calls back to the hook, so the Short loops.

The goal is maximum watch time. Open a loop early (promise something that is only explained later), add a new turn or reveal every 2 to 3 sentences, never explain everything at once, and keep the story inside its own rules. Keep it safe for all ages (no violence, hate or sexual content).

**Simple English.** Everyone must understand it, including kids and people who do not speak English as a first language (level A2, B1 at most): short common words, short sentences (about 10 words or fewer, one idea each), simple tenses, no idioms, slang, phrasal verbs, wordplay or technical terms, short easy names (Tom, Mia), numbers kept simple. Test: would a ten-year-old or a beginner understand every sentence? If not, simplify.

Before writing, read the three real reference scripts in `references/transcripts/` (`transcript1.txt` to `transcript3.txt`, timestamped, about 230 to 260 words each). Study their rhythm only: how the opening line hits, sentence length, how details escalate, where "You see..." lands, how the twist closes. Never copy their topics, sentences or facts, and do not imitate their vocabulary level; every script must be original, and simpler in language.

About four words a second, no dead air. Write the voice script with ElevenLabs audio tags in square brackets (e.g. `[excited]`, `[whispering]`, `[short pause]`, `[sighs]`; full list and a sample in the project `CLAUDE.md`), roughly one tag per one or two sentences. Tags are never subtitles and do not count toward pacing: keep `audio/script.txt` tag-free (strip `[...]`) before running `words`, or word alignment breaks. Then generate the voice with Miles (`voice_id e18664a7-ee4f-5273-acf8-533eb24cd366`, `voice_type: preset`; see `references/prompts.md`; no music), save the raw take as `audio/voice_original.mp3` (never edit audio through Higgsfield). Process it locally with ffmpeg via the project's `scripts/voice.sh`: it removes the gaps between sentences and speeds the track up so it is 60 s at most, writing `audio/voice.mp3`. Save the script as `audio/script.txt`, then get the word timings from the processed `voice.mp3`:

```bash
python3 scripts/stage/shortkit.py words audio/voice.mp3 audio/script.txt -o audio/words.json
```

Check that the voice is in the language you asked for before building on it.

### 8. "Build the full 3D scene in code"

Write `short.json`. Read `references/formats.md` first; `examples/demo/short.json` is a working example to copy. Decisions to make:

- **Shots.** One per beat of the script, each starting on a spoken phrase (`"start": "say:..."`), so the picture stays locked to the voice. Most shots last one to three seconds; none longer than four. Every shot moves; most push in (`zoom` 3 to 8).
- **Framing.** `headWidth` 0.2 is the house close-up; 0.08 to 0.12 is a wide shot. Vary `yaw` between shots so the glide between them reads as a camera move.
- **Light.** Define a warm `day` mood and a cool `night` mood, and switch on the pivot: `{"t": "say:You see", "mood": "night"}`.
- **Acting.** Give each shot one clear action: a face, a pose, a walk. The idle motion covers the rest.
- **Layout.** The camera looks from +z toward -z by default. Put the set behind the characters (negative z) and leave open ground in front. Separate locations go 60 or more units apart in the same world.

### Keep every scene alive (anti-boring rules)

A scene feels empty when the picture barely changes between shots. Without music, textures or 3D models, the variety has to come from the shots, the set layout, the light and the acting. Apply all of this when writing `short.json`:

1. **Something new in every shot.** Compared with the previous shot, at least two of these must differ: framing (`headWidth`), angle (`yaw`/`pitch`), the face or pose of Tlama, who is on screen, what is behind the character, or the light mood. If two neighbouring shots look alike, merge them or change one.
2. **Short beats.** One shot per sentence or per new idea, 1 to 3 seconds. A 60 s Short has 20 to 30 shots, not 8.
3. **Alternate the framing.** Close-up, medium, wide, then close again. Alternate the sign of `yaw` (left, right). Use low and high `pitch`, a wide `fov` for drama, push-ins (`zoom` positive) and sometimes pull-outs (`zoom` negative). Keep `glide` for the move between shots.
4. **Fill the set in three layers.** Every location gets at least 8 to 12 props: foreground (near the camera, partly cropping the frame: posts, crates, tree trunks), midground (around the character) and background (houses, walls, tree groups, far shapes). Vary height, size and colour; use a palette of 4 to 6 saturated flat colours, not one grey. Use `box` stacks, `wall` segments and `tree` clusters instead of leaving open ground.
5. **Change place.** 3 to 5 locations per video, one per story act (different ground colour, different `backdrop`, different props), 60+ units apart. Move between them on the pivot or on a new reveal, not mid-sentence.
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
- **3 locations, 15–25 props each**, 60–80 units apart. An interior is built from a floor box + 3 walls + window + door + furniture + shelf with coloured books + rug + foreground plant/toy box. Make the floor box big enough that the global ground never shows inside a room.
- **8 moods** (day, red, tense, night, flashback, dusk, gold, morning) with a lighting key on every story turn; short red flash (`fade` 0.15) on each shock.

**Animation tricks that sell it**
- **Growing/shrinking things:** several copies of a character at different `height`, parked underground (`pos` y = -60), swapped with `to` + `over: 0.01` at a word (`show()` helper). Same for appearing/vanishing characters.
- **Real motion with `to`:** the dog falls from the roof into Tlama's arms; Tlama walks between spots in the room; the dog runs across the park. Put at least 3–4 moves like this in every video.
- **Props that belong to a character are painted into its puppet** (`scripts/puppet_variants.py`: phone in hand, nest on head). Static props near a character float when it moves or disappears.
- 2–4 side characters with reaction shots (neighbour shocked, tomorrow-me shouting, dog barking via `hop`).

**Camera fixes learned the hard way**
- Between locations always `out: "dissolve"` (the generator sets it automatically); a glide flies through floors and walls.
- Wide shots (`headWidth` < 0.2) need `pitch` ≥ 4, otherwise the camera goes under ground.
- When the target is swapped/hidden at the shot start, frame it with `anchor` + `distance` instead of `target` (the camera would follow the hidden copy underground).
- Keep foreground props out of the line between the camera and a close-up (the `TARGET_HIDDEN_BEHIND_SET` flag).
- After `--stills` passes, look at a few stills at full size (paste 4–8 into one image), not only the contact sheet.

### 9. Stop-frame check, before every full render

```bash
node scripts/stage/render.mjs short.json out.mp4 --stills
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

### 10. Render

```bash
node scripts/stage/render.mjs short.json out.mp4            # 1080x1920, 30 fps, captions + voice
node scripts/stage/render.mjs short.json preview.mp4 --scale 0.5 --from 0 --to 8   # fast partial preview
```

Software rendering in a sandbox takes roughly half a second per frame; a machine with a GPU is many times faster. Use `--scale` and `--from/--to` while iterating.

### 11. "Compare it with the original"

Compare with numbers, not by eye:

```bash
python3 scripts/stage/shortkit.py compare out_stills/shot02_b.jpg reference_frame.png
python3 scripts/stage/shortkit.py check out.mp4
```

`compare` prints contrast, shadow depth and colour, saturation, warm and cool shares and ink density for both pictures, and names the fields in `short.json` to change for the largest gaps. `check` measures camera speed and zoom against the style's ranges. Two fixes come up most:

- **Floating characters.** The soft contact shadow under the feet pins a character to the ground. It is on by default (`contactShadow`); raise it if feet still look detached, and make sure the character's `pos` y is on the ground.
- **Flat, pale picture.** Raise `sun.intensity`, deepen `fill.ground`, and use richer flat colours (no textures).

### 12. The next video

Reuse the project folder: the puppets and background stay. A new video is a new `audio/` set and a new `short.json`.

### Measuring another style

To study reference videos the way these rules were made:

```bash
python3 scripts/stage/shortkit.py measure path/to/videos out_dir
```

It writes one reference sheet per two seconds of video and `measured.json` with cut timing, camera speed and zoom, brightness, shadow colour and saturation. Measure every frame, then decide; an opinion about a video cannot be reproduced, a number can.

## Working with sub-agents

If you split the work across agents, give each one its own files: one owns `short.json` lighting and moods, one owns shots and camera, one owns asset generation and the library folders. Two agents writing the same file at the same time overwrite each other, and parts of the scene vanish.

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
- The rules describe 20 videos of one channel, not what performs best.
