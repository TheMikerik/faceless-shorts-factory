# Content creator project – YouTube Shorts

## About the project

My content creator project, focused mainly on **YouTube Shorts**. This repository is a working folder for ideas, scripts, assets and video production.

## Channel

- **Active channel:** [@TlamaLabs](https://www.youtube.com/@TlamaLabs)
- **Goal:** start publishing **faceless Shorts** (animated, without the author's face) using the `ricksclips-short-style` skill

## Vision and goals

- **Main goal:** YouTube monetization (meet the YPP conditions – subscribers + Shorts views – and earn from ads)
- **Focus:** a complete change. Roblox content is in the past, the channel gets a new identity (faceless absurd invented stories). The existing Roblox Shorts are no longer the direction.
- **Topic and language:** **invented absurd stories that never happened** (no history, no real facts, no real people). Always in **English**, format: strong hook → escalating absurdity → pivot "You see…" → twist (global audience, higher RPM)
- **Main character:** `puppets/main_hero_tlama` (Tlama, a pink head with a huge mouth and yellow goggles) is the hero of **every** video. Always use Tlama as the main character. Details in `PUPPETS.md`
- **Voice:** I **generate the voice myself** and upload it into the video folder (see "Shortcut `--cv`"). **Never generate the voice** (no `generate_audio` or any other TTS), and do not suggest generating it. Deliver only the text script.
- **Main goal of a video:** the highest possible retention. The viewer must stay with the Short until the end (and ideally replay it in a loop)
- **English level:** simple, understandable for everyone (see the "Simple English" section)
- **Frequency:** **daily**, 1 Short. Production must therefore be as fast as possible: the library (characters, backgrounds, models) is built once and reused, a new video = only its own folder `videos/NNN-slug/` (script, voice, `short.json`).
- **Consequence:** prefer repeatable, automatable procedures over one-off perfection. Suggest how to shorten the time per video.

## Folder contents

| Path | Description |
| --- | --- |
| `.claude/skills/ricksclips-short-style/` | Main skill for producing faceless Shorts in the @RicksClips3000 style (also holds the shared render engine) |
| `.claude/skills/tlama-longform/` | Skill for landscape long-form videos (5–8 min); inherits everything from the Shorts skill and overrides only what differs |
| `.claude/skills/tlama-thumbnail/` | Skill that writes 3 ready-to-paste thumbnail prompts (Nano Banana / Higgsfield) with Tlama + one thing from the video. Only prompts, I generate the image by hand |
| `longform/` | One folder per long-form video, `LNNN-slug/` |
| `PUPPETS.md` | Overview of the characters in `puppets/` (who is who and when to use them). Update it after adding a new character |
| `DOCUMENTATION.md` | How the project works: idea, goals, workflow, architecture, key decisions and why, videos so far, changelog |

**Keep `DOCUMENTATION.md` up to date (mandatory).** Whenever you change the workflow, a rule in this file, the skill, a script, a tool, the folder structure or a technical decision, update the relevant section of `DOCUMENTATION.md` in the same piece of work and add a dated line to its changelog. After a new video is finished, add it to the "Videos so far" table. Do not let it drift from the actual state of the project.

## Main workflow: faceless Shorts in the RicksClips style

Use the skill **`ricksclips-short-style`** (`.claude/skills/ricksclips-short-style/SKILL.md`). Read it before any work on a video and follow it.

In short: flat 2D doodle characters in a sunlit 3D world, built entirely in code (three.js stage). New characters and backgrounds are **exceptionally** generated through the **Higgsfield connector** (only when truly needed and **only after my explicit confirmation**, see "Higgsfield"). Nobody generates the voice, I record it. The scene is assembled into `short.json` and rendered via `.claude/skills/ricksclips-short-style/scripts/stage/render.mjs`.

Format: 1080x1920, 30 fps, about 60 s, captions of 1–2 words.

### Shortcut `--cv` (create video)

When I write just `--cv`, it means this prompt (I do not have to write it out):

> Using the ricksclips-short-style skill, suggest 3 absurd/funny stories. Give me those ideas and I will choose one of them. Then write a 60-second script with the channel's formula: paradox first line, strong hook, escalation, "You see…", twist. Use puppets available in PUPPETS.md

The procedure is always the same. (The output templates below are intentionally kept in Czech, because they are what I read; the rest of this file is in English.)

1. **Immediately, as the very first step** (before reading anything) create an empty folder `videos/NNN/`, where `NNN` = the highest number in `videos/` + 1 (three digits, e.g. `009`). Only the number for now, no slug and no subfolders. This lets several videos run in parallel.
2. **Three stories.** Read the skill and the scripts of the finished videos so the topic does not repeat. **The topic must always be new, original and different from all previous videos.** Then print exactly this structure and **nothing else** (no intro, no recommendation, no list of characters):

   ```
   # 1 - Název
   - Hook: ...
   - Pravidlo: ...
   - Twist: ...
   - Hodnocení: x/10

   # 2 - Název
   ...
   # 3 - Název
   ...
   ```

   `Hodnocení` (rating) = the score from the idea scorecard. `Pravidlo` (rule) = the one magic rule of the story.

   **10/10 gate (mandatory):** before printing, run the full procedure in `.claude/skills/ricksclips-short-style/references/idea-scorecard.md` silently (8–10 candidates → `scripts/idea_check.py` → scorecard with reasons → critic pass → fix or drop). Print **only ideas that reach 10/10, at least 2** (max 3). If fewer than 2 reach 10/10, keep generating; never show weaker ideas. After I choose, register the idea with `idea_check.py --add`.
3. **Script.** After I choose, print only the text for ElevenLabs (with audio tags, see below) in this form and nothing else. At the same time save it to `videos/NNN/script_tagged.txt` and `videos/NNN/script.txt` (without tags):

   ```
   Příběh:
   [whispering] There is a monster under my bed. ...

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

Next to the daily Shorts, I make **landscape long-form videos**, about **3× a week**: 1920×1080, 30 fps, **5–8 min (target ~6 min, ~900 words)**, one longer invented absurd story with Tlama in the same style. Use the skill **`tlama-longform`** (`.claude/skills/tlama-longform/SKILL.md`); it builds on `ricksclips-short-style` (same engine, library, style and story rules) and lists everything that differs: story structure (escalation ladder of 6 steps in 3 acts, cliffhangers, midpoint turn, "You see…", twist back to the hook), max 5 places and 5 side characters, shots of 4–8 s, captions as short phrases at the bottom, CTA twice, YouTube-only metadata with chapters. Simple English and the ElevenLabs tag rules are the same as for Shorts.

When I write just `--clv` (create long video), run the same procedure as `--cv` with these differences:

1. **Immediately** create an empty folder `longform/LNNN/` (`LNNN` = `L` + the highest number in `longform/` + 1, three digits, e.g. `L001`). Own numbering, separate from `videos/`.
2. **Three stories**: the same output format as `--cv` (`# 1 - Název`, Hook, Pravidlo, Twist, Hodnocení), nothing else. The 10/10 gate uses the long-form scorecard `.claude/skills/tlama-longform/references/idea-scorecard.md` and `scripts/idea_check.py --longform` (own registry `scripts/ideas_used_longform.json`). After I choose, register with `idea_check.py --longform --add`.
3. **Script**: the same output as `--cv` (`Příběh:` … `Nyní čekám na vložení zvukové stopy do složky LNNN.`), saved to `longform/LNNN/script_tagged.txt` and `script.txt`.
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

### Higgsfield (new characters and backgrounds)

Higgsfield is connected, but it is used **only when truly needed** (a character or background that the library lacks). **Always ask me first and wait for my confirmation.** Do not generate anything without confirmation. The main character (`main_hero_tlama`) is always ready, and so are most of the others, so steps 1–4 are usually skipped.

If a new character is generated, it goes through the whole cycle: 1. character image → 2. emotion sheet → 3. slice into layers / rig the puppet → (optionally a background). Then add it to `PUPPETS.md`.

### Workflow steps (details in the skill)

A regular video (the library already exists): 1. script → 2. **waiting for my voice** → 3. timing → 4. scene in `short.json` → 5. stop-frame check (`--stills`) → 6. render → 7. **final files into the video folder** (see "After the video is rendered") → 8. **publication** (see "Publishing via Buffer", never automatic, only after I review the video) → 9. next video

**Not generated:** music, textures or 3D models. **Music:** every video uses my ready-made track `music/music.mp3` (shared archive), in `short.json` `"audio": {"voice": "audio/voice.mp3", "music": "music/music.mp3", "musicDb": -18}`; the render trims it to the video length and fades it out at the end. Do not generate any other music. A video has voice, music, flat colors, props from the stage primitives (crate, barrel, wall, house…) and **ready-made 3D models (GLB) from the `props/` library**, which I supply by hand (downloaded free packs, CC0). Do not generate new 3D models, only use those from the library.

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
  video.mp4        final render
  script.txt       final script without tags
  metadata.md      captions for the platforms
```

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

### Script – formula (invented absurd story)

1. **hook** right in the first sentence, no intro: an absurd, concrete situation that raises the question "what? how?" (e.g. "Every night, my cat pays rent to a tiny king who lives in my wall.")
2. two to three escalating details: each more absurd than the previous one
3. pivot "You see…", where the (absurd but story-logical) explanation begins
4. punchline/twist in the last sentence right before the loop, ideally tied to the hook so the video naturally replays

### Story rules

- **Everything is invented.** No real events, historical figures, dates, real brands or real people. Nothing may look like a true statement about the world. Do not look up or verify facts, just make the story up.
- **Absurd, but internally consistent.** The story has its own rules and they are kept (absurdity works when it makes internal sense).
- **Strong hook.** The first sentence (within ~2 s) must stop the scroll: concrete, bizarre, no intro. No "Hey guys", no "Today I will tell you".
- **Retention.** Every 2–3 sentences a new plot turn, reveal or escalation ("open loop": promise something that is explained later). Never explain everything at once. No dead moment, no filler. The last sentence returns to the beginning so the video loops.
- **One hero, one situation.** A simple story that can be told visually with one character and a few props.
- **Safe content.** No violence, hate or sexual content (monetization, YPP). Suitable for younger viewers too.

### Clarity (the viewer must not get lost)

The **situation** should be absurd, not the storytelling. The story must be followable on first listen, even if the viewer is only half watching.

- **One magic rule.** The whole story stands on a single absurd thing (e.g. "a sneeze changes the mayor"). No second magic and no other unrelated absurdity. Everything else follows from that rule.
- **The viewer always knows what Tlama wants.** The goal or problem is stated right in the hook and never changes (hide a cookie, shrink the chicken, find the machine).
- **Escalation is the same pattern, only bigger.** Rule of three: the same type of event three times, each bigger (small trouble, bigger, huge). The viewer learns the pattern and looks forward to the next step. Do not mix three different kinds of plot.
- **Max. 3 side characters.** Each introduces themselves on first appearance with one clear label ("my mom", "the inventor", "my dog Max") and it never changes afterwards. Nobody new appears after "You see…".
- **No unclear pronouns.** When two characters are in the scene, repeat the name or role instead of "he/she/it". For direct speech always say who is speaking ("Mom said: …").
- **Time only moves forward.** No flashbacks or jumps, except the "You see…" pivot, which is clearly announced.
- **A change of place is said out loud.** Max. 3 places and say every move at the beginning of a sentence ("At school…", "Then I ran outside.").
- **"You see…" is short.** An explanation in 1–2 sentences, one simple cause. No chain of reasons.
- **The twist only uses what the viewer has already seen.** The punchline uses the characters, things and rule from the first half. Nothing new at the last moment.
- **Every sentence is visible.** For every sentence you must be able to show one clear picture (character, thing, reaction). A sentence that cannot be drawn goes.
- **Retelling test.** Before delivering, retell the story in 3 sentences (problem, what happens, how it ends). If you cannot, the story is too complex: cut characters, places and side ideas until you can.

### Strong hooks (they must make people stay)

The first sentence decides whether the viewer scrolls away. Every hook must meet **at least 3 of 5**:
1. **Starts in the middle of the action** (something is happening right now, no "Once upon a time", no introductions).
2. **Exaggerated and concrete** (huge, impossible, with a number or time: "60 seconds", "every adult in the world").
3. **Stakes or a clock:** something threatens that must be solved right now ("before the moon falls", "only I can fix it").
4. **Opens a loop:** raises a question that only the end answers ("Why did every cat look at my house?").
5. **The narrator is in danger or at the center of events** ("I" = Tlama), not a description of the world from the outside.

Max. 15 words, simple English. The story then pays off the hook at the "You see…" pivot and returns to it in the twist.

#### 23 example hooks (+ twist idea)
1. "At 3 AM, my cat looked at me and whispered: 'Run. They are inside the walls.'" / "They" are tiny workers building a pool for the cat. The cat wanted to warn me about the noise.
2. "Today at 8 AM, every adult in the world turned into a potato. Only I can fix it." / The cure is a hug from a kid. At the end, I turn into a potato too, and my little sister has to hug me.
3. "I have 60 seconds before the moon falls on my house." / The moon is only looking for its lost sock. It finds it, and I wake up with a moon-shaped sock in my bed.
4. "A giant chicken has followed me for three days, and today it learned my name." / Each lie I told made it bigger. I tell the truth, and it shrinks. Last line: I lie again.
5. "My shadow packed a bag and said: 'Do not look for me.'" / The shadow got a job with a taller person. At the end, my new shadow is a very small one.
6. "The sun did not come up today, and only I know where it went." / The sun overslept in my bed. I sing it awake, and now it follows me to school.
7. "I woke up and my whole house was on the moon, and my mom did not care at all." / Mom already knew. The moon has the best Wi-Fi. At the end, the house is on Mars.
8. "Do NOT open the fridge. It already knows your name." / The fridge only wants a friend. It lets me in, and inside it is a snowy city for tiny penguins.
9. "My teacher is a dragon, and today he finds out that I know." / He is scared of me, because I am a kid with a pencil. He gives everyone an A to stay quiet.
10. "A tiny king moved into my wall, and today he asked me for one million dollars." / He pays the cat rent with my money. At the end, the cat is the king's boss.
11. "Tonight, everyone in my town has the same dream, and I am the monster in it." / In the dream, I am a kind monster who saves everyone. The town wakes up and they all clap.
12. "My phone just sent me a photo of my room, taken one minute from now." / In the photo, a giant pizza sits on my bed. I run to the kitchen, and now there is a pizza on the table, too.
13. "The mailman gave me a letter. It says: 'You have 10 minutes to hide the last cookie.'" / A cookie thief is a very polite bear. At the end, the bear delivers the next letter.
14. "I sneezed once, and now a pigeon is the mayor of my city." / Every sneeze changes who leads the town. At the end, I sneeze again, and a whale is the mayor.
15. "Yesterday, the ducks took over my town. I am their only hope, and I only have bread." / The ducks only want bread for a giant party. I join them, and I am the guest of honor.
16. "My brother sold me to a pigeon for three coins." / The pigeon planet has a very bad Wi-Fi. At the end, my brother is sold to a squirrel.
17. "There is a red button in my school. It says: DO NOT PRESS. Today, I pressed it." / The school turned upside down. Everyone is on the ceiling, and the lunch is falling like rain.
18. "My grandma's soup makes you invisible, and my sister just drank the whole pot." / She is invisible for a week. At the end, grandma drinks the second pot, and so does the dog.
19. "Every night, all the colors leave my city. Tonight, I follow them." / The colors go to a secret party. At dawn, my city is back, but my hair is now green.
20. "I told one tiny lie, and now a chicken the size of a house is knocking on my door." / The truth makes it small. I say it, and the chicken becomes a chick, and then the chick lies to me.
21. "The goldfish at my school is secretly the principal, and today I caught him without his hat." / He gives me a deal: keep the secret, get free pizza for life. Final scene: the pizza is delivered by the goldfish.
22. "Why did every cat in the world look at my house at exactly 7 PM?" / They are all waiting for my cat, who is the cat king. He walks out, and they all bow, and he asks me for a snack.
23. "I found a door in my school that opens to yesterday, and yesterday's me was waiting with a warning." / The warning: "Do not eat the blue cake." Today, I eat the blue cake anyway, and it is amazing.

### ElevenLabs tags in the script

**Always write** the text script straight away with ElevenLabs audio tags in square brackets, so it can be pasted into ElevenLabs without edits. Write the tags in English, put them before the sentence/phrase they apply to, and do not overdo it (about 1 tag per 1–2 sentences, so the voice does not sound overacted). Dialogue in quotation marks stays normal text.

Mainly use these tags:
- **Emotion:** `[weak]` `[angry]` `[bored]` `[menacing]` `[playful]` `[tired]` `[excited]`
- **Vocalizations:** `[clears throat]` `[coughing]` `[chuckling]` `[sniffling]` `[yawning]` `[laughing]` `[sharp exhale]` `[scoffing]` `[humming]` `[panting]` `[gasping]`
- **Delivery:** `[whispering]` `[singing]` `[voice breaking]`
- **Character:** `[sleepy drowsy voice]` `[witch voice]` `[drunken voice]`
- **Sound effects:** `[keyboard typing]` `[echoing]` `[knocking on door]` `[bell ringing]` `[phone ringing]` `[dog barking]` `[crowd cheering]` `[applause]` `[rain falling]` `[drum roll]` `[heartbeat]` `[engine starting]`

Sample script (style and tag density):

```
[thoughtful] I built the best invention in the world, but nobody can see it. Not even me. This morning, the mayor heard about it. [excited] He ran in and shouted, "I will pay a thousand coins for it!" [chuckles] I said, "Great! Just one problem. I lost it." Then he walked right into it. [sound of impact] Bonk! [surprised] He fell on the floor, and his hat flew out the window. So I ran to the middle of the room. Nothing. [anxious] Oh no. I gave it little wheels. Big mistake. At lunch, the baker hit it on the street. All his bread flew into the sky. [chuckles] Then my friend Bob hit it at the market and landed in a barrel of fish. [annoyed] The whole town was angry. "What is this thing?" [thoughtful] You see, I built a machine that makes things invisible. And the first thing it made invisible was itself. [anxious] The mayor gave me one hour. "Find it, or no coins." I looked everywhere, on my hands and knees. [surprised] Then I touched something warm. It was buzzing. [excited] My machine! [thoughtful] I found two buttons. A small one and a big one. [thoughtful] One makes things come back. But which one? I pressed the big one. [sound of electricity] There was a bright flash. [surprised] And the whole town was gone. The houses. The people. The mayor. Then, from nowhere, I heard his voice. [muffled] "Amazing! I will pay two thousand coins!" So now I have the best town in the world, but nobody can see it. Not even me.
```

**Do not use** tags that slow down or lengthen the audio (`[pause]`, `[short pause]`, `[slowly]`, `[softly]`, `[sighs]`, `[inhales deeply]` etc.). Pauses are trimmed anyway and the goal is the shortest possible track.

The sample may also use other natural tags outside the list (`[thoughtful]`, `[surprised]`, `[anxious]`, `[annoyed]`, `[muffled]`, `[sound of impact]`), but the list above is the baseline.

**Careful with timing and captions:** tags are never shown as captions and do not count toward the pace (~4 words/s). Before `words` / `words.json`, save `audio/script.txt` **without tags** (or filter the tags out), otherwise the word alignment breaks.

### Audio track: raw + local processing

- The uploaded voice is always **raw** and is stored in the video folder as `videos/NNN-slug/work/audio/voice_original.mp3`. Never edit it through Higgsfield or any other online tool.
- Do the processing **locally on this computer** via `ffmpeg`: `scripts/voice.sh` (output `audio/voice.mp3`, the raw file is not overwritten).
  1. removes gaps/silence between sentences (`silenceremove`, only ~0.06 s remains),
  2. speeds up (`atempo`, the pitch does not change) so the result is **at most 60 s** (target ~59.5 s). If it is already shorter, it does not speed up.
- Only then run `words` for `audio/words.json` on the **processed** `voice.mp3` (the timing must match the final track).
- Run: `scripts/voice.sh` (default paths), or `scripts/voice.sh raw.mp3 out.mp3 60`.

### After the video is rendered (mandatory)

**Create the video folder right at the start of the work as an empty `videos/NNN/`** (so parallel videos do not take the same number; `NNN` = next free) and **rename it to `videos/NNN-slug/` after I choose the story**. After the render is finished, save the final files into it without asking:

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
     shorts, story, funny   (the same words as the hashtags without #; Buffer does not send them, only for manual pasting)

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
- Run: `node scripts/publish/publish.mjs NNN` (queues into the next free slot in the Buffer queue, times do not matter). Several videos at once: `... 004 005 006`. Fixed times only on request (`--start`, `--time`).
- The script skips already published videos according to `.published.json`. Do not delete the video from R2 until it has gone out.

### Simple English

Everyone must be able to understand the script, including younger viewers and people for whom English is not the first language (level A2, B1 at most).

- Short words and short sentences (ideally up to ~10 words). One idea per sentence.
- Common everyday words. No complicated or rare words (instead of "consequently" → "so", instead of "purchase" → "buy", instead of "enormous" → "huge").
- Simple tenses (present simple, past simple). No complex sentence constructions, chained subordinate clauses or passive voice unless necessary.
- No idioms, slang, phrasal verbs or wordplay that a foreigner would not understand ("kick the bucket", "spill the beans"…).
- No technical terminology or complicated names. Character names short and easy to pronounce (Tom, Mia, Bob).
- Numbers simple (not "1,347", but "a thousand").
- Before delivering, check the script: if a ten-year-old child or a beginner in English heard it, would they understand every sentence? If not, simplify.

About 4 words per second, no empty space.

## Style rules (short)

- Characters: flat 2D cutouts with big round heads (the head about as wide as the torso), real shadows in 3D
- Lines: thick, even, plum black `#271925`, never pure black
- Colors: warm sun vs. cool shadows, do not lift shadows to pure black
- Lively scenes: a shot every 1–3 s, something changes in every shot (angle, expression, background, light), set dressing in three layers (foreground, middle, background), max. 3 places per video, 1–3 side characters. Details in the skill ("Keep every scene alive")
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
- Respect the monetization goal: original content (no 1:1 copies of other people's videos), no real facts or real people (everything invented, so nothing to verify), no violations of YouTube rules (reused content, music copyright).
- When I send just a script, run the workflow with the existing library and do not ask anything beforehand. **Exception:** I record the voice. As soon as you send the script for ElevenLabs, **wait until I put the `.mp3` into the video folder and write that it is done** (a message that is not a question). Without the voice, timing and render do not start.
- When the style is unclear, rely on the skill and `references/style-rules.md`, not on guesswork.
- **Do not write** new video ideas to `brainstorming.md` or anywhere else. Just write them to me in the chat. Write to `brainstorming.md` only when I say so explicitly.
- When I want an idea or a script, deliver **only the text script** (and optionally the hook/twist). Do not generate the voice, I will record it myself.
