---
name: tlama-thumbnail
description: Writes ready-to-paste image-generation prompts (Nano Banana / Higgsfield) for a video thumbnail with Tlama plus one key thing from the video. Use it at the end of every `--cv` / `--clv`, or whenever the user asks for a thumbnail, cover or "thumbnail prompt" for a Short or a long-form video. It only writes prompts; it never renders anything from the stage and never generates the image itself.
---

# Tlama thumbnail prompts

The user makes the thumbnail by hand: they paste the prompt into Nano Banana / Higgsfield, attach the reference image, download the result and upload it manually in YouTube Studio. **This skill only writes the prompts.** Do not render from the stage (that was tried for long-form and was not good enough), do not call Higgsfield or any generator, do not ask for credits.

## Inputs (read, do not ask)

- `script.txt` of the video (hook, escalation, finale) and `metadata.md` (title).
- `short.json` / `build.py` only if you need to know what the key prop looks like.
- Format by video type:
  - **Short** (`videos/NNN-slug/`): **1080×1920, 9:16 vertical**
  - **Long-form** (`longform/LNNN-slug/`): **1280×720, 16:9 horizontal**

## Song Shorts (`--cvs`): own fixed style, one variant

For a song / language video (it has `dialogue.txt`) **ignore everything below except "Rules"**. The thumbnail is always the same layout, only the flag and the language name change. Write **exactly one** prompt.

**When:** together with the Suno package, before the track exists (only the language is needed, do not wait for `metadata.md`). The user generates the image and puts it into the video folder; `tlama-song` puts it on the first frame of the video, because Instagram and TikTok use that frame as the cover. So ask for exactly 9:16 (it gets fitted to 1080×1920; a 2:3 result still works if the text keeps some side margin).

- Top to bottom, centred: **flag** of the language's country → **language name** in English, ALL CAPS (`ITALIAN`) → **Tlama with a serious face** (head and upper body).
- Flag: Spanish = Spain, French = France, German = Germany, Italian = Italy, Portuguese = Portugal. For another language take its home country. Describe the stripes and colors in the prompt, so the generator does not guess.
- Serious face: mouth closed in one flat straight line, no teeth, no smile, eyes calm and half-lidded, brows low and straight. The reference grins and `emotions.png` has no serious face, so the prompt must say this explicitly. Attach only `puppets/main_hero_tlama/source.png`.
- Plain beige background `#E3CBA8` (same as the video). No key thing, no burst, no other text. Everything in the upper 80 %, away from the right edge.

Skeleton:

```
Vertical 9:16 YouTube Shorts thumbnail, flat 2D cartoon doodle style with thick even plum-black outlines (#271925), flat colors, one soft shadow, no photo-realism, no 3D. Plain solid warm beige background (#E3CBA8). Centered layout, top to bottom. At the top: a large <country> flag, <stripes and colors>, as a simple flat rectangle with a thick plum-black outline. Directly below it: the text "<LANGUAGE>" in huge thick white all-caps letters with a thick plum-black outline and a small drop shadow. Below the text: the character from the attached reference image, same design (round pink head, small black eyes, thick eyebrows, flat yellow goggles on the forehead, white coat), shown from the waist up, facing the camera, large. Important: unlike the reference, the face is completely serious: mouth closed in one flat straight line, no teeth, no smile, calm half-lidded eyes, low straight eyebrows. Keep the bottom 20% and the right edge free of important details. Only the flag, the text and the character, no other objects, no other text, no watermark.
```

Report and save to `thumbnail_prompts.md` as in "Output" below, but with the heading `## Thumbnail prompt (9:16 1080×1920)` and one prompt without a variant number.

## What every thumbnail contains

1. **Tlama**, always, as the clear hero (about 40–60 % of the frame height). Reference to attach: `puppets/main_hero_tlama/source.png` (full body). For a close-up on the face attach `puppets/main_hero_tlama/emotions.png` too and name the expression. Her identity never changes: round **pink** head with a huge grin full of big square white teeth, two small black oval eyes with thick eyebrows, flat **yellow** safety goggles pushed up on the forehead, white lab coat, thin stick arms and legs with round black hands, thick plum-black outline `#271925`.
2. **One key thing from the video**: the one object, creature or moment that makes a stranger ask "what?". It comes from the "What if" question or an early step, not from the finale (do not spoil it). Examples: the giant chicken, the cake taller than a house, the red DO NOT PRESS button, the cave with a shouting echo. Exactly one, drawn big.
3. **Text of 1–3 words**, English, ALL CAPS, huge, thick white or yellow letters with a thick plum-black outline and a slight drop shadow, placed away from the character's face. The text is a hook or a reaction, never the title: "IT ATE IT?!", "DO NOT PRESS", "RUN!", "WHO IS HE?". The generator may misspell it, so always put the exact text in quotes in the prompt and tell the user the fallback (see below).

## Style: the "clickbait" version of the channel look

Same character and outline as the video, but pushed harder so it works as a tiny thumbnail:
- flat 2D doodle cutout style, thick even plum-black outlines `#271925` (never pure black), flat colors with one soft shadow, no photo-realism, no 3D render, no gradients on the character
- **high contrast and saturation**, a bright simple background in one or two colors (sunny yellow, sky blue, hot orange, deep purple; pick the one that contrasts with pink and with the key thing)
- **dramatic expression**: shocked (huge round white eyes, open mouth), screaming, or nervous with a sweat drop. Not the default smile unless the joke is the smile
- **the key thing exaggerated** (2–3× bigger than logical) and clearly readable in one second
- a simple dynamic composition: a diagonal, the character in a corner pointing or looking at the key thing, a clean glow or burst behind it, optional motion lines. Maximum 3 elements plus text. No clutter
- readable at the size of a fingernail: big shapes, no tiny details

## Safe zones

- **Short (9:16):** YouTube and the app cover the bottom ~20 % and the right edge with buttons and the title. Keep the face, key thing and text in the **upper 70 %**, centered or slightly left. Text in the upper-middle, not at the very bottom.
- **Long-form (16:9):** the duration badge covers the bottom-right corner. Keep it empty. Text on the left or right third, Tlama's face on the other side, key thing between or behind.

## Output: 3 variants

(Song Shorts: one prompt, see above.) Always exactly **3 variants**, each a different idea (different key moment or key thing, different expression, different text). Do not pad with near-duplicates. For each variant write one prompt in English, as one paragraph, ready to paste, in this order: format and style → background → Tlama (identity, expression, pose, where) → key thing (what, size, where) → text (exact, in quotes, style, where) → composition and what to avoid.

Prompt skeleton (fill in, keep it concrete, no generic filler):

```
Vertical 9:16 YouTube Shorts thumbnail, flat 2D cartoon doodle style with thick even plum-black outlines (#271925), flat saturated colors, one soft shadow, no photo-realism, no 3D. Background: <simple bright background, colors>, <glow/burst/lines>. The character from the attached reference image, exactly as in the reference (round pink head, huge grin of big white square teeth, small black eyes, flat yellow goggles on the forehead, white coat, stick limbs), <expression, e.g. screaming with huge round white eyes and open mouth>, <pose and position, e.g. in the lower left, pointing at the thing, about half the frame height>. Next to it: <the key thing, exaggerated, where, how big, its color>. Big bold text "<TEXT>" in thick white all-caps letters with a thick plum-black outline and a small drop shadow, placed <where>. Keep the bottom 20% and the right edge free of important details. Maximum three elements plus the text, readable at a tiny size. Do not change the character's design, do not add extra characters, no watermark, no other text.
```

For long-form replace the first words with "Horizontal 16:9 YouTube thumbnail" and the safe-zone sentence with "Keep the bottom-right corner empty."

## Report format (this is what you print, in Czech, around the English prompts)

```
## Thumbnail prompty (<9:16 1080×1920 | 16:9 1280×720>)
Přilož referenci: puppets/main_hero_tlama/source.png  (+ emotions.png u variant s detailem obličeje)

### 1 – <krátký popis nápadu česky>
<EN prompt>

### 2 – ...
### 3 – ...

Tip: pokud generátor zkomolí text, vygeneruj obrázek bez textu (přidej "no text") a napiš nápis ručně.
```

Save exactly the same content to `thumbnail_prompts.md` in the final video folder (`videos/NNN-slug/`, for song videos `videos/NNN-language/`, or `longform/LNNN-slug/`), next to `video.mp4`. If the file already exists, overwrite it only when the user asked for a redo.

## Rules

- Use only Tlama as the character (plus at most one other character from `PUPPETS.md` if it is the key thing of the video). No real people, brands or logos.
- No spoilers of the finale. The thumbnail asks the question, the video answers it.
- Safe for all ages (YPP): no violence, blood, weapons, scary gore. "Scary" is fine only in the funny, cartoon way.
- Simple English text (see "Simple English" in the project `CLAUDE.md`).
- Do not claim the result will look exactly like the prompt; it is a prompt for a generator the user runs.
