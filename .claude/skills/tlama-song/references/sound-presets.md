# Sound presets: the author's style first, small proven variations second

Videos 018–022 all used one fixed Style prompt, so they had the same voices and almost the same beat. Now each video combines **five parts**, one from each table.

## Rotation rule (mandatory)

**The author's style comes first, variety second.** The base is the **classic sound** of 018–022: `beat=K1 producer=A1 tlama=B1 bed=D1 flow=F1`.

1. **Use only proven ids** (a Suno track made with them reached production):

   | table | proven ids |
   | --- | --- |
   | K beat | K1, K2, K3, K4 |
   | A producer | A1, A2, A3 |
   | B Tlama | B1, B2, B5 |
   | D bed | D1, D2, D3, D4 |
   | F flow | F1, F2, F3 |

   Every other id in the tables below is **blocked**. Never pick it and never invent a new preset or new Style wording on your own. A blocked or new id may be tried only when the user explicitly asks for an experiment; it becomes proven only after a track made with it reaches production.
2. Read the `Sound:` line of the **3 latest** song videos (`videos/*/suno.md`; a file without that line is the classic sound). Do it **right before writing `suno.md`**, because other videos can be in progress at the same time.
3. The whole `Sound:` line must differ from all 3. In every table prefer an id that the **previous** video did not use. If variety and a proven id collide, the proven id wins.
4. Write the line at the top of the new `suno.md`: `Sound: beat=K1 producer=A1 tlama=B1 bed=D1 flow=F1`.
5. **The user says the generations are bad:** switch the whole package to the **classic sound** at once (the exact Style text of `videos/022-polish-pub/suno.md` with the language swapped, plus its lyric tags). Do not tune or remix the failed mix. If the classic sound was already used and is still bad, the problem is probably the words: ask what is wrong and offer another idea.

Failed: video 026, `K4 A6 B4 D2 F4` (many Suno generations, none usable; the exact guilty part is unknown, A6, B4 and F4 had never been used). Tlama's voice is never high-pitched.

All beats stay between **130 and 175 BPM** with a **heavy low-end drop**: `analyze_song.py` reads tempos of 110–180 (a slower one gets doubled and the camera cuts too fast) and finds the drop by the jump in the bass. The producer is always an English speaker, Tlama is always **bored and deadpan** (that is the character). Both stay male voices. A new preset may be added here only on the user's request, and it starts as blocked.

## K: beat of the drop

| id | `{BEAT_NAME}` (goes in "turns into a … drop") | `{BEAT}` | `{DRUMS_TAG}` |
| --- | --- | --- | --- |
| K1 | hard rap | trap rap, 150 BPM half-time, booming 808 bass, punchy kick, snappy snare, fast rolling hi-hats | full 808 trap drums |
| K2 | UK drill | UK drill, 142 BPM, sliding 808 bass, skippy hi-hats, syncopated snare | sliding 808 drill drums |
| K3 | phonk | phonk, 130 BPM, distorted booming bass, dry cowbell hits, crunchy kick and clap | distorted phonk drums |
| K4 | Jersey club | Jersey club rap, 140 BPM, bouncy triplet kick, sharp claps, deep bass hits | bouncing Jersey club drums |
| K5 | grime | grime, 140 BPM, buzzing square sub bass, hard snare, sparse choppy drums | hard grime drums |
| K6 | Miami bass | Miami bass, 135 BPM, huge booming 808 kick, electro snare, fast claps | booming Miami bass drums |
| K7 | breakbeat | drum and bass rap, 170 BPM, chopped breakbeat, heavy rolling sub bass | fast breakbeat drums |
| K8 | crunk | crunk, 150 BPM half-time, stomping kick, loud gang claps, thick 808 bass | stomping crunk drums |

## A: producer voice (English)

| id | `{VOICE_A}` | `{TAG_A}` |
| --- | --- | --- |
| A1 | a cheerful playful American English speaker | cheerful English |
| A2 | a smooth deep late-night radio DJ speaking American English | smooth deep radio DJ, English |
| A3 | a loud high-energy game show host speaking English | excited game show host, English |
| A4 | a fast-talking nerdy American with a high bright voice | fast nerdy English, high voice |
| A5 | a super relaxed West Coast surfer speaking English | laid-back surfer English |
| A6 | a cocky London guy with a British accent | cocky British English |

## B: Tlama's voice (target language)

| id | `{VOICE_B}` ("native <Language> speaker" follows) | `{TAG_B}` |
| --- | --- | --- |
| B1 | a deadpan bored low-voiced | bored, low and cool |
| B2 | a deadpan bored gravelly raspy-voiced | bored, gravelly and raspy |
| B3 | a sleepy bored nasal-voiced, clear diction, | sleepy, bored, nasal |
| B4 | a flat unimpressed high-pitched nasal | flat, high nasal, unimpressed |
| B5 | a very deep slow-voiced, completely unimpressed | very deep, slow, unimpressed |
| B6 | a tired deadpan dry half-whispering, clear diction, | tired dry half-whisper |

## D: bed under the dialogue (never drums, never melody)

| id | `{BED}` | `{BED_TAG_1}` | `{BED_TAG_2}` |
| --- | --- | --- | --- |
| D1 | only a quiet deep sub bass pulse and sparse finger snaps | quiet sub bass pulse | finger snaps, a little more tension |
| D2 | only soft vinyl crackle and sparse rimshot clicks | soft vinyl crackle | rimshot clicks, a little more tension |
| D3 | only a ticking clock and a low heartbeat thump | ticking clock | heartbeat thump, a little more tension |
| D4 | only a low dark drone and sparse single hand claps | low dark drone | single hand claps, a little more tension |
| D5 | only quiet tape hiss and a soft low 808 hum | tape hiss and low hum | 808 hum rising, a little more tension |
| D6 | only water drop sounds and a quiet deep rumble | water drops | deep rumble, a little more tension |

## F: rap flow

| id | `{FLOW}` | `{FLOW_TAG}` |
| --- | --- | --- |
| F1 | a tight staccato flow | fast staccato flow |
| F2 | a rolling triplet flow | rolling triplet flow |
| F3 | a bouncy chanting flow | bouncy chant flow |
| F4 | a hard punchy flow, each word hit on the beat | hard punchy flow |
| F5 | a smooth fast flow that stays calm and low-effort | calm effortless fast flow |
