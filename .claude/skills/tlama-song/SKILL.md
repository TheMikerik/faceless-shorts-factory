---
name: tlama-song
description: The channel skill for "song" Shorts (shortcut `--cvs`, create video song) - an English x <other language> language joke: a cool English producer asks a bored Tlama how to say simple words, every answer has the same funny sound, then the words snap together into one tongue twister that Tlama raps on a trap beat drop. Covers the language question, ideas, translation check, the Suno prompt (style, exclude, lyrics), the analysis of the Suno track and the render (flat images, hard cuts, mouth swaps). Use it whenever the user writes `--cvs`, asks for a song / rap / tongue-twister / language Short, or any step of one.
---

# Tlama song Shorts (`--cvs`)

A vertical Short, 30–35 s, 1080×1920, 30 fps. Two characters on a plain beige background:

- **A, the producer** (black beanie, small sunglasses, beard, black hoodie, gold chain): speaks **English**, cool and a bit cocky, leads the game.
- **B, Tlama** (the channel's main character, pink head, yellow goggles, blue headphones): speaks the **other language**, totally bored and deadpan, until she raps.

The whole soundtrack (both voices, the beat, the rap) is **one track the user makes in Suno** from the prompt this skill writes. The user always makes the track; never generate audio yourself.

First test: video `videos/018-spanish-pub/` (Spanish, "-eño" sound). It went well; use it as the reference for everything below.

## Why it works

1. **Challenge start:** "Bet you can't say this in Spanish." It speaks straight to the viewer and opens a loop: what is "this"? (018 and 019 used the older line "<Language> is easy, right?"; from the next song video on, use only the challenge line.)
2. **The trap:** the first question's answer is a word that means two things ("sueño" = *dream* and *sleepy*). The next English word gets **the same answer again**, which is the first laugh.
3. **One sound everywhere:** every answer shares one audible ending (ñ: sue**ño**, peque**ño**, due**ño**…). After three answers the viewer waits for the sound, which is retention.
4. **The puzzle:** the 7–8 words the viewer just learned click together into one sentence: "Try this." English line → Spanish tongue twister.
5. **The payoff:** silence, then a beat drop, and the bored Tlama raps the whole tongue twister. People replay it to catch it or to try it themselves.

## Differences from the "What if" Shorts (CLAUDE.md rules this skill overrides)

| | "What if" Short (`--cv`) | Song Short (`--cvs`, this skill) |
| --- | --- | --- |
| Audio | the user's ElevenLabs voice + `music/music.mp3` | **one Suno track** with both voices, beat and rap; no extra music |
| Voice processing | `voice.sh`, silences removed, ≥1.25× speed-up | **none**: pauses are part of the joke. `analyze_song.py --trim` hard-cuts right after the first rap chorus (≤35 s, **no fade**) and normalizes to −14 LUFS |
| Picture | 3D stage, moving camera, dense sets | **flat images, static frames, hard cuts** to whoever speaks; camera jumps only in the finale on the beat |
| Characters | Tlama + library puppets | **always the same duo** from `puppets/song_duo/` (no Higgsfield needed) |
| Script formula | hook → ladder → "But here is the real problem." → finale | hook → trap → sound pairs → "Try this." → English line → rap drop (below) |
| Facts | science checked | **every translation and the tongue twister checked** in a dictionary |
| Captions | 1–2 words | full phrase above the characters (dialogue); the whole twister in 3–4 rows during the rap |

Everything else from CLAUDE.md stays: channel, simple English (A1–A2 for the English words), safe content, original content (never copy a known tongue twister word for word), daily speed, folder model (own folder per video, shared numbering with the other Shorts, but **named by the language**: `videos/NNN-language/`), metadata format, Buffer only on command.

## Fixed rules (author's, mandatory)

1. **Tlama always wears the country's typical clothing / costume** in the video (same country as the thumbnail flag; see "Country costumes"). The thumbnail **always** keeps the original Tlama.
2. **The song is always cut right after the first rap chorus**, a plain hard cut, **no fade**. Suno sometimes raps the chorus twice; none of the second round may be left.
3. **Non-Latin script:** the original script on top, the Latin transliteration under it in brackets.
4. **After publishing** (`.published.json` in the folder) the folder gets the `-pub` suffix (`018-spanish-pub`); `publish.mjs` does it itself.

## The `--cvs` procedure

1. **Immediately** create an empty folder `videos/NNN/` (`NNN` = highest number in `videos/` + 1, three digits).
2. **Ask the language. Always, every time, before anything else.** Use AskUserQuestion: "Angličtina × jaký jazyk?" with options like Španělština, Francouzština, Italština, Němčina (the user can type another one). The pair is always **English × that language**. Do not guess it from earlier videos. **Right after the answer, rename the folder to `NNN-language`**: the language in English, lowercase (`022-polish`, `023-french`). Never name a song folder after the story or the idea; the name does not change later.
3. **Three ideas.** Read `videos/*/dialogue.txt` of earlier song videos so a sound family is never reused for the same language. Run the idea gate silently (below), then print exactly this and nothing else (labels in Czech, words in the languages they belong to):

   ```
   # 1 - Název
   - Zvuk: -eño / -eña
   - Past: dream → sueño, sleepy → sueño
   - Slova: little → pequeño, owner → dueño, smiling → risueño, southern → sureño, log → leño, dreams → sueña
   - Jazykolam: El pequeño y risueño dueño sureño sueña que su leño tiene sueño.
   - Překlad: The little, smiling, southern owner dreams that their log is sleepy.
   - Hodnocení: 10/10

   # 2 - Název
   ...
   ```

   Show **only ideas that score 10/10, at least 2** (max 3). Each idea uses a different sound family.
4. **Check, then the Suno package.** After the user picks one, check every word and the tongue twister (see "Translation check") and save `videos/NNN-language/facts.md`. Then save `dialogue.txt`, `script.txt`, `suno.md` (template below, with a **proven sound mix** from `references/sound-presets.md`) and `thumbnail_prompts.md` (skill `tlama-thumbnail`, song style) into `videos/NNN-language/` and print only this:

   ```
   Style:
   <style>

   Exclude styles:
   <exclude>

   Lyrics:
   <lyrics>

   Thumbnail prompt (9:16 1080×1920, přilož puppets/main_hero_tlama/source.png):
   <prompt>

   Nyní čekám na vložení písně ze Suno a obrázku náhledovky do složky NNN-language.
   ```
5. **Wait for the track and the thumbnail.** The user makes the track in Suno (Custom mode, Instrumental off) and the thumbnail image from the prompt, and puts both into `videos/NNN-language/`: the only `.mp3` and the only image (`.png` / `.jpg` / `.jpeg` / `.webp`), any names. Continue when they say it is done (anything that is not a question). Not exactly one `.mp3` or not exactly one image: say what is missing and stop. Never produce the final video without the thumbnail. (A video started before this rule has no prompt yet: write it, then wait.)
6. **Production, no questions.** Move the mp3 to `work/audio/suno_original.mp3` (the image stays in the video folder), then follow "Production" below: analyze + trim, stills check, render, final files, metadata. `build_song.py` puts the image on **frame 0 only**. Fix problems yourself. If a key word was not heard or the English line is wrong in the track (see `NOT HEARD`), tell the user which second to listen to and ask whether to continue or regenerate the track in Suno.
7. **Dry run:** `node scripts/publish/publish.mjs --dry NNN` (never the real run without an explicit command).
8. **Final report** (Czech):

   ```
   - Plný render doběhl: <snímky>, <délka>, 1080×1920, 30 fps, zvuk ze Suno.
   - Analýza: drop <s>, <BPM> BPM, finále od <s>, střih na <s>; neslyšená slova: <žádná / seznam>
   - Vytvořeno: `video.mp4`, `script.txt`, `metadata.md`
   - Dry run: <OK nebo problém>, výpis:
     <celý výstup `publish.mjs --dry NNN`>
   - [případné upozornění]
   - Kostým: <země>; střih <s> po prvním refrénu (ověřeno, bez fade)
   - Náhledovka: vložena jako první snímek (IG a TikTok ji berou jako cover; na YouTube ji případně nahraj ručně ve Studiu)
   - command pro nahrání:
     - node scripts/publish/publish.mjs NNN
   ```

## Writing the idea

### Structure of `dialogue.txt` (fixed, only the words change)

```
A: Bet you can't say this in <Language>.
A: How do you say <trap word> in <Language>?
B: <answer 1>.
A: <trap word 2>.            ← different English word, SAME answer as above
B: <answer 1>.
A: <word>.                   ← then 6 more pairs, one word each
B: <word>.
...
A: Try this.
A: <the English sentence>.
RAP: <the tongue twister>.
```

8 pairs in total (the trap + 7). This lands at ~23 s of dialogue, ~2 s pause, ~3–5 s rap = 30–33 s. The video ends hard right after the first rap chorus.

### Rules

- **One sound family:** a clearly audible ending or sound that most target words share (Spanish `-eño/-eña` with ñ, `-aña`, `rr`; French `-ouille`, `-eau`, `-eur`; Italian `-ello/-ella`, `gli`; German `-tz`, `sch`, `-chen`; Portuguese `-ão`, `-inho`). These are starting points only; the words must still pass the check. A viewer who does not speak the language must **hear** the pattern.
- **The trap pair** is mandatory: one target word with two common English meanings (or two English words with one answer). Without it the idea fails the gate.
- **English words:** one word each, A1–A2, easy to picture (sleepy, little, owner, mud, cat). No proper names.
- **Target words:** real, common, correctly spelled with accents; at least 6 of the 8 answers carry the sound. Prefer words of 2+ syllables: a long row of one-syllable, near-identical answers (026: négy, nagy, légy, hegy, megy) is a risk for Suno, so such an idea loses the "Raps well" point.
- **Tongue twister:** grammatical, max 14 words, uses at least 6 of the taught words, makes one silly picture (a sleepy log, a spider on a mountain). Natural stress rhythm, so it raps well. Own sentence, not a famous existing tongue twister.
- **English sentence:** the honest translation of the twister, simple words, max 14 words. Avoid words Suno may slur into another word (018: "log" was at risk of sounding like "love").
- **Safe:** no swear words or rude double meanings in either language (check the slang meaning too), nothing about real people, brands, politics or religion.

### Idea gate (10 points, show only 10/10)

| Points | Test |
| --- | --- |
| 2 | The sound family is clear and repeats in ≥6 answers |
| 2 | The trap pair is real (a dictionary confirms both meanings) and funny |
| 2 | All words are common, correctly spelled and easy to picture |
| 2 | The tongue twister is grammatical, ≤14 words, uses ≥6 taught words and is a funny picture |
| 1 | Never used before for this language (`videos/*/dialogue.txt`) |
| 1 | Raps well: even stress, the sound lands on the beat |

Silently: write 6–8 candidates, score them with reasons, run a critic pass ("would a viewer who does not speak the language hear the pattern?"), fix or drop. Never show weaker ideas.

### Translation check (mandatory, before the Suno package)

Check every word pair, the trap's both meanings and the tongue twister's grammar in a real dictionary: for Spanish RAE (dle.rae.es) or Wiktionary; for French Larousse or Wiktionary; for German Duden; for Italian Treccani; otherwise Wiktionary or a university dictionary. Save `facts.md` as `word → meaning → source link → note`. If a word fails, swap it; if the trap fails, drop the idea.

### Non-Latin languages (`dialogue.txt`)

Latin transliteration first, then ` | original script` on every `B:` line and the `RAP:` line:

```
B: Dhahab. | ذهب
RAP: Dhahab arnab li-yal'ab … | ذهب أرنب ليلعب …
```

- The `RAP:` original must have the **same number of words** as the transliteration (it is also used to hear the rap in its own language).
- Transliteration: plain Latin letters, no special diacritics. Original: normal everyday spelling (Arabic without vowel marks). Suno lyrics use the original script (vowel marks help pronunciation).
- Captions (done by `build_song.py`): original on top, `(transliteration)` below, both for the dialogue words and the rap.
- `script.txt` stays transliterated.

## Suno package (`suno.md`)

**First pick the sound** with `references/sound-presets.md`: five parts (beat K, producer voice A, Tlama voice B, dialogue bed D, rap flow F), **only proven ids** (never an untested one), the whole line different from the 3 latest song videos. The base is the author's classic sound (`K1 A1 B1 D1 F1`); when the user says the generations are bad, go straight back to it. First line under the title in `suno.md`: `Sound: beat=K? producer=A? tlama=B? bed=D? flow=F?`.

Then fill every `{…}` slot and `<Language>`. The frame (dialogue first without drums, silence, drop) is what made 018 work, after two failed tries: rapping from the first second was wrong, and an audible piano was unwanted. Keep the filled Style under 1000 characters.

**Style:**
```
comedy podcast skit that turns into a {BEAT_NAME} drop, two male voices, first part is spoken dialogue only, not rapped: {VOICE_A} and {VOICE_B} native <Language> speaker, both talking with confident street swagger, short punchy lines, natural pauses, over almost nothing, {BED}, no drums and no melody during dialogue, tension slowly rises with a subtle riser, short silence, then a sudden beat drop into hard <Language> {BEAT}, the same <Language> voice stays deadpan and raps with {FLOW}, dry upfront vocals, crisp diction, short, no intro
```

**Exclude styles:**
```
piano, keys, guitar, strings, melodic lead, rapping in the dialogue, drums in the dialogue, singing, autotune, choir, pop, EDM, heavy reverb, female vocals, long intro, instrumental solo
```

**Lyrics** (the dialogue.txt lines in this frame):
```
[Spoken Word - talking with rapper swagger, not rapping, no drums, starts immediately]
[Speaker 1: {TAG_A}]
Bet you can't say this in <Language>.
How do you say <trap word> in <Language>?

[Short Pause]

[Speaker 2: <Language>, {TAG_B}]
<answer 1>.

[Spoken - {BED_TAG_1}]
[Speaker 1]
<trap word 2>.
[Speaker 2]
<answer 1>.

[Speaker 1]
<word>.
[Speaker 2]
<word>.

  ... (pairs 3–4 here, then:)

[Spoken - {BED_TAG_2}]
  ... (pairs 5–8)

[Spoken - riser slowly builds, still no drums]
[Speaker 1]
Try this.
<English sentence>.

[Silence]

[Beat Drop - {DRUMS_TAG}]
[Rap Verse - Speaker 2: deadpan, {FLOW_TAG}, no singing]
<twister, first half, ending on the sound>
<twister, second half>!

[End]
```

For the rap, break the twister into two lines and put commas between the rhyming words (`El pequeño, y risueño, dueño sureño`); Suno raps shorter, punchier pieces. The commas are only for Suno, the caption uses the clean sentence.

**Tips for the user** (put them under the package in `suno.md`):
- Generate several versions. Pick one where the first question follows the opening line right away (no gap), the dialogue is spoken (not rapped), the two voices never swap, every word is there, the drums start only at the drop, and it is ≤ ~36 s (the tail after the rap gets cut).
- The dialogue still raps: in Style replace `both talking with confident street swagger` with `both talking in a cool, relaxed, confident tone`.
- A melody / piano is audible: raise Style Influence (Advanced Options) and generate again.
- Do not use a Suno Persona, Cover or "Reuse prompt" from an earlier song: it brings the old voices back.
- Use a paid Suno plan for anything that is published (the free plan gives no commercial rights).

## Production

```
V=videos/NNN-language
mkdir -p $V/work/audio && mv $V/*.mp3 $V/work/audio/suno_original.mp3
.venv/bin/python .claude/skills/tlama-song/scripts/analyze_song.py \
    $V/work/audio/suno_original.mp3 $V/dialogue.txt -o $V/work/song.json --trim $V/work/audio/voice.mp3
.venv/bin/python .claude/skills/tlama-song/scripts/dress.py <country> $V/work/custom      # costume, always
cd $V/work && ../../../.venv/bin/python ../../../.claude/skills/tlama-song/scripts/build_song.py --stills
cd $V/work && ../../../.venv/bin/python ../../../.claude/skills/tlama-song/scripts/build_song.py
# the thumbnail is the only image in $V/ ; the full render stops without it
cp $V/work/out.mp4 $V/video.mp4 && cp $V/script.txt $V/work/audio/script.txt
```

- **The cut:** `analyze_song.py` cuts at the quietest moment around the end of the last rap word, with no fade. **Always verify it:** Suno may repeat the chorus with almost no gap (023: 0.1 s) and whisper times can reach into the repeat. Transcribe or look at the audio around the cut; if the last word is clipped or the second round is audible, re-run with `--cut <seconds>`.
- **`analyze_song.py`** prints the cut, the finale start, the drop (with its strength in dB) and the tempo, every line with its times, and `NOT HEARD` words (they get interpolated times). It writes `work/song.json`; the numbers there can be edited by hand if a still shows a wrong cut, then just re-run the build. The dialogue is transcribed in English; the rap gets a second pass in its own language (auto-detected) from the end of the English line, and the drop is searched around that rap start (it prints `rap re-heard in its own language: n/m`). If that line is missing or the finale stills show Tlama still sitting with closed eyes while the rap is already heard (019), the rap start is wrong: fix `finale`, `drop` and the RAP word times in `song.json` by hand.
- **Check the stills** (`work/out_stills/`, one per caption + the pause + the finale beats) before the full render: the right character on screen for each caption, the caption matches the word, an open mouth on spoken words, Tlama's closed eyes in the pause, drums + rap from the finale on. A weak drop (`WARNING`) means Suno made no real drop; look at the finale stills and the drop value.
- **`build_song.py`** renders in ~20 s with the hardware encoder (light on the fanless Mac, no `--cool` needed). Images come from `work/custom/<name>.png` when present (per-video override), otherwise from `puppets/song_duo/`.

### What the generator does (so you can change it with intent)

- **Thumbnail = frame 0.** The only image in the video folder is fitted to 1080×1920 (a wider image such as 2:3 loses only 5 % of its width, keeps its bottom edge, and the missing height is filled at the top with its own background, so the text is not cut) and replaces the first frame (one frame, 33 ms; length and audio timing do not change). `publish.mjs` tells Buffer to use offset 0 as the Instagram and TikTok cover. YouTube does not get it through Buffer.
- Hard cut to the speaker ~0.25 s before each line. A silent bored reaction shot of the other character after the first line (when the gap is >1 s). A pause shot (Tlama, eyes closed) between the English line and the drop.
- Mouths: only inside the whisper word times; **one opening per syllable**, shape from its vowel (a = wide, o/u = o, e/i = half), closed between syllables; syllable borders snap to dips of the harmonic voice band (drums filtered out). English spellings that break the vowel count go into `ENGLISH` in the script. If the mouth is off, the word times are wrong: **check the first RAP word** (whisper tends to glue it into the pause before the drop; 020 was 0.8 s early) and fix it in `song.json`. Only the face area of a variant is pasted onto the base image, through a feathered mask, so outlines never jitter between frames. Random blinks when the mouth is closed.
- The producer gestures (`A_hand`) on lines with ≥6 words, plus a short A line right before one ("Try this.").
- Captions: Avenir Next Demi Bold 60 px, plum black `#271925`, centred at 33 % of the height (above the characters and their hats). Dialogue lines whole, the last English line in 3-word phrases (stays on screen through the pause), the twister in rows of ≤4 words from the finale on, its bottom edge at y = 430 so hats stay free.
- Finale: the drum pose swaps on every beat from the drop; the camera jumps every 2 beats between wide, Tlama close-up, wide, drummer close-up and medium.

## Characters (`puppets/song_duo/`)

16 flat images, 752×1344, generated once with Higgsfield (GPT Image 2.6, medium, 1k), in the channel line style on the plain beige `#E3CBA8`:

| Files | What |
| --- | --- |
| `A_closed`, `A_half`, `A_wide`, `A_o`, `A_blink`, `A_hand` | producer in a charcoal armchair with a pop-filter mic |
| `B_closed`, `B_half`, `B_wide`, `B_o`, `B_blink` | Tlama in a beige armchair, blue headphones, flat bored mouth line |
| `F_closed`, `F_half`, `F_wide`, `F_o`, `F_drum` | finale: producer on drums (left), Tlama standing at the mic (right); `F_drum` = the other stick up |

The prompts are in `references/image-prompts.md`. A new look (a costume for a special episode, another drummer pose) goes into `work/custom/` of that video under the same file name, and **only after the user confirms the Higgsfield cost** (CLAUDE.md rule). Higgsfield runs at most 4 jobs at once; a batch submit can time out, so check `transactions` before resubmitting anything.

## Country costumes (mandatory for every song video)

Tlama in the video always wears the typical clothing of the language's country; the **thumbnail stays with the original Tlama**. Check `puppets/song_duo/costumes/` first: a saved costume is free. If it is missing, ask for the 1 credit together with the Suno package (name the garments you will generate; real typical clothing, not just accessories in flag colours; no religious head coverings or caricature).

One costume = **one** Higgsfield generation (`gpt_image_2_6`, 16:9, medium, 1k, 1 credit; confirm the cost first): a sheet with three separate items on a transparent / solid background, left to right **seated robe, standing robe, hat**, with `B_closed` and `F_closed` as references. Save it as `puppets/song_duo/costumes/<country>/sheet.png`. `scripts/dress.py <country> videos/NNN-language/work/custom` then dresses all 10 Tlama images for free (head, mic, arms and hands stay in front); run it before the stills. Positions are per country in `costumes/<country>/place.json` (copy one, adjust, check the preview). Saved so far: `egypt`, `france`, `poland`, `russia`, `india`, `hungary`, `japan`, `germany`, `srilanka`. A saved costume is reused without a new generation.

## Metadata template (`metadata.md`)

Same headings as the other Shorts (the publish script parses them).

**Rules for song videos (mandatory, they override the CLAUDE.md title template):**
- The **title never starts with an emoji**. It starts with a word; one emoji at the end is fine.
- **No challenge lines** in any description or caption: no "Can you say this?", "Can you rap it?", "Say it 3 times", "Say it fast", "Tell me how it went", "Send this to a friend who can…". (The spoken opening line in the video and the title "Bet you can't say this…" are not affected.)
- **Every platform** (YouTube, Instagram, TikTok) has a CTA that asks **which language comes next**, in the style of "Comment which language I should do next" or "Type in the comments which language should be next". Word it differently on each platform and in each video.

Example:

```
# NNN – <Language>

## YouTube
### Title
Bet You Can't Say This In Spanish 😴

### Description
One sound: ñ. Eight easy Spanish words, then all of them in one sentence on the beat. Watch till the drop… 🔁
Comment which language I should do next 👇

#shorts #spanish #tonguetwister #learnspanish #rap

### Tags
shorts, spanish, tonguetwister, learnspanish, rap, languages, funny, cartoon, tlamalabs

## Instagram
### Caption
Spanish gets hard when the beat drops. 😴

Sueño, pequeño, dueño, risueño… then all of them in one line. 🥁
Type in the comments which language should be next 👇

#spanish #tonguetwister #learnspanish #rap #tlamalabs

## TikTok
### Caption
One bored pink head, one Spanish tongue twister. 🥁 Which language next? Drop it in the comments.

#spanish #tonguetwister #learnspanish #rap #tlamalabs
```

Vary the emoji, the hook line and the CTA wording per video; do not paste the same text with one word swapped.
