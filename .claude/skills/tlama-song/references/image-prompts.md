# Image prompts for `puppets/song_duo/`

Model: Higgsfield `gpt_image_2_6`, `aspect_ratio` 9:16, `quality` medium, `resolution` 1k (1 credit each, 752×1344).
Only needed to rebuild or extend the library; a normal `--cvs` video uses the ready images.
Always ask the user and quote the cost before generating.

## Base images (in this order, each uses the previous as reference)

**B_closed** (reference: `puppets/main_hero_tlama/source.png`)
```
Use the attached character as the exact reference and keep its flat cartoon doodle style: thick even plum-black outlines (#271925), flat colors with one soft shadow tone, no texture, no gradients. Keep the round pink head, thick dark eyebrows, small dot eyes and the yellow goggles pushed up on top of the head, the white coat body and thin stick arms and legs with round hands. Change only the expression and the scene: the huge wide mouth is CLOSED into one long flat bored line across the face, no teeth visible. Heavy half-closed sleepy eyelids, totally bored deadpan look. The character sits in a small simple beige armchair, wearing dark blue over-ear headphones (headband goes over the head behind the goggles). A black podcast microphone on a thin stand stands in front of the chest, below the mouth, not covering the face. Plain flat warm beige background (#E3CBA8), no room, no objects, no floor line, only a soft shadow under the armchair. Vertical 9:16 composition: the character and armchair are centered horizontally and fill only the bottom 45% of the frame; the top 55% is completely empty beige. No text, no watermark, no border.
```

**A_closed** (reference: B_closed). A first friendly version (mint head, green hoodie) was rejected as "too friendly"; the producer must command respect.
```
Same flat cartoon doodle style, same framing, same camera, same plain warm beige background (#E3CBA8) and same character size and position as the attached image (thick even plum-black outlines, flat colors, one soft shadow tone). But draw a DIFFERENT original character: a cool, confident music producer who commands respect. Round dark brown head of the same size, short black beard along the jaw, a black beanie hat, small black rectangular sunglasses pushed down a little so heavy-lidded calm eyes look over them, one eyebrow slightly raised, small confident smirk, mouth closed. Body: oversized black hoodie, a thin gold chain, thin stick arms and legs with round hands like the reference, sitting relaxed and leaning back with arms spread on the armrests. Big black over-ear studio headphones. Sits in a small simple dark charcoal-grey armchair. A black podcast microphone with a round black pop filter on a thin stand in front of the chest, below the mouth, not covering the face. Character and armchair centered, filling only the bottom 45% of the frame, top 55% completely empty beige. Not cute, not childish. No text, no watermark, no border.
```

**F_closed** (references: B_closed, A_closed)
```
Both attached characters together in one image, exactly the same flat cartoon doodle style (thick even plum-black outlines, flat colors, one soft shadow tone) and the same plain warm beige background (#E3CBA8), no room, no floor line. No armchairs now. On the left, slightly behind: the producer character from the second image (black beanie, small black sunglasses, short black beard, black hoodie, gold chain, big black headphones) sits behind a small simple light-brown drum kit (bass drum, two toms, snare, two cymbals), holding two drumsticks, the right drumstick raised up, cool confident smirk. On the right, slightly in front and a bit larger: the pink character with yellow goggles, dark blue headphones and white coat stands at a black microphone with a round black pop filter on a stand, the huge mouth closed into one long flat bored line, heavy half-closed bored eyes, deadpan. The microphone is below the mouth and does not cover the face. Both characters fill only the bottom 42% of the frame and are cut slightly by the bottom edge; the top 58% is completely empty beige. Vertical 9:16. No text, no watermark, no border.
```

## Variants (reference: the matching `_closed` image)

Prefix for A and B:
`Edit the attached image. Change ONLY this, keep everything else exactly identical: same character, same pose, same position and size in the frame, same outlines, colors, headphones, microphone and background. Change: <change>. No text, no watermark.`

For F use `same characters, same poses, same positions and sizes in the frame, same outlines, colors, drums, microphone and background`.

| File | `<change>` |
| --- | --- |
| A_half | the mouth is slightly open while talking, still a confident smirk |
| A_wide | the mouth is wide open mid-word while talking, confident |
| A_o | the mouth is a small round O shape |
| A_blink | the eyes above the sunglasses are closed (eyelids down) |
| A_hand | his right hand is raised up from the armrest in a relaxed explaining gesture, palm open; the rest of the body unchanged |
| B_half | the long flat mouth line opens slightly into a thin, wide, dark opening showing a row of big white teeth, eyes stay bored and half-closed |
| B_wide | the huge mouth opens wide while talking, big white teeth and dark purple inside visible, eyes stay bored and half-closed |
| B_o | the mouth becomes a small round O shape in the middle of the face, eyes stay bored and half-closed |
| B_blink | the eyes are fully closed, two flat curved lines, still bored |
| F_half / F_wide / F_o | `only the pink character's mouth: ` + the B change (F_wide: "while rapping") |
| F_drum | only the drummer's arms: the right drumstick is now down hitting the snare drum and the left drumstick is raised up high |

The edits keep the frame in place (measured shift 0 px). The body outlines still wobble slightly between variants, which is why `build_song.py` pastes only the face area onto the base image.
